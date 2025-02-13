import asyncio
import subprocess
import sys
import websockets
import json
import logging

from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel

# setup logging
logging.basicConfig(level=logging.INFO)


async def clean_exit(pc, websocket):
    logging.INFO("Closing WebRTC connection...")
    await pc.close()

    logging.INFO("Closing websocket connection...")
    await websocket.close()

    logging.INFO("Client shutdown complete. Exiting...")


async def send_worker_messages(channel, pc, websocket):

    message = input("Enter message to send (or type 'quit' to exit): ")

    if message.lower() == "quit":
        logging.INFO("Quitting...")
        await pc.close()
        return

    if channel.readyState != "open":
        logging.INFO(f"Data channel not open. Ready state is: {channel.readyState}")
        return
   
    channel.send(message)
    logging.INFO(f"Message sent to client.")


async def handle_connection(pc, websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            
            # 1. receieve offer SDP from client (forwarded by signaling server)
            if data['type'] == "offer":
                # 1a. set worker peer's remote description to the client's offer based on sdp data
                logging.INFO('Received offer SDP')

                await pc.setRemoteDescription(RTCSessionDescription(sdp=data['sdp'], type='offer')) 
                
                # 1b. generate worker's answer SDP and set it as the local description
                await pc.setLocalDescription(await pc.createAnswer())
                
                # 1c. send worker's answer SDP to client so they can set it as their remote description
                await websocket.send(json.dumps({'type': pc.localDescription.type, 'target': data['target'], 'sdp': pc.localDescription.sdp}))
            
            # 2. to handle "trickle ICE" for non-local ICE candidates (might be unnecessary)
            elif data['type'] == 'candidate':
                logging.INFO("Received ICE candidate")
                candidate = data['candidate']
                await pc.addIceCandidate(candidate)

            elif data['type'] == 'quit': # NOT initiator, received quit request from worker
                logging.INFO("Received quit request from Client. Closing connection...")
                await clean_exit(pc, websocket)
                return

            # 3. error handling
            else:
                logging.DEBUG(f"Unhandled message: {data}")
                
    
    except json.JSONDecodeError:
        logging.DEBUG("Invalid JSON received")

    except Exception as e:
        logging.DEBUG(f"Error handling message: {e}")

        
async def run_worker(pc, peer_id, port_number):
    # websockets are only necessary here for setting up exchange of SDP & ICE candidates to each other
    
    # 2. listen for incoming data channel messages on channel established by the client
    @pc.on("datachannel")
    def on_datachannel(channel):
        # listen for incoming messages on the channel
        logging.INFO("channel(%s) %s" % (channel.label, "created by remote party & received."))

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            logging.INFO(f"ICE connection state is now {pc.iceConnectionState}")
            if pc.iceConnectionState == "failed":
                logging.DEBUG('ICE connection failed')
                await clean_exit(pc, websocket)
                return
            elif pc.iceConnectionState in ["failed", "disconnected"]:
                logging.INFO("ICE connection failed/disconnected. Closing connection.")
                await clean_exit(pc, websocket)
                return
            elif pc.iceConnectionState == "closed":
                logging.INFO("ICE connection closed.")
                await clean_exit(pc, websocket)
                return
            
        @channel.on("open")
        def on_channel_open():
            logging.INFO(f'{channel.label} channel is open')
        
        @channel.on("message")
        async def on_message(message):
            # receive client message
            logging.INFO(f"Worker received: {message}")

            if message.lower() == "sleap-label": # TEST RECEIVING COMMMAND AND EXECUTING INSIDE DOCKER CONTAINER
                logging.INFO(f"Running {message} command...")
                try:
                    result = subprocess.run(
                        message, 
                        capture_output=True,
                        text=True,
                        check=True,                        
                    )
                    logging.INFO(result.stdout) # simple print for now
                except:
                    logging.DEBUG("Error running SLEAP label command.")
            
            # send message to client
            await send_worker_messages(channel, pc, websocket)


    # 1. worker registers with the signaling server (temp: localhost:8080) via websocket connection
    # this is how the worker will know the client peer exists
    async with websockets.connect(f"ws://host.docker.internal:{port_number}") as websocket:
        # 1a. register the worker with the server
        await websocket.send(json.dumps({'type': 'register', 'peer_id': peer_id}))
        logging.INFO(f"{peer_id} sent to signaling server for registration!")

        # 1b. handle incoming messages from server (e.g. answers)
        await handle_connection(pc, websocket)
        logging.INFO(f"{peer_id} connected with client!" )


    # ICE, or Interactive Connectivity Establishment, is a protocol used in WebRTC to establish a connection
    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        logging.INFO(f"ICE connection state is now {pc.iceConnectionState}")
        if pc.iceConnectionState == "failed":
            logging.DEBUG('ICE connection failed')
            await clean_exit(pc, websocket)
            return
        elif pc.iceConnectionState in ["failed", "disconnected"]:
            logging.INFO("ICE connection failed/disconnected. Closing connection.")
            await clean_exit(pc, websocket)
            return
        elif pc.iceConnectionState == "closed":
            logging.INFO("ICE connection closed.")
            await clean_exit(pc, websocket)
            return
    
        
if __name__ == "__main__":
    pc = RTCPeerConnection()
    port_number = sys.argv[1] if len(sys.argv) > 1 else 8080
    try:
        asyncio.run(run_worker(pc, "worker1", port_number))
    except KeyboardInterrupt:
        logging.INFO("KeyboardInterrupt: Exiting...")
    finally:
        logging.INFO("exited")
        

    
