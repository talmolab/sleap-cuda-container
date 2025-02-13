import asyncio
import subprocess
import websockets
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel

async def clean_exit(pc, websocket):
    print("Closing WebRTC connection...")
    await pc.close()

    print("Closing websocket connection...")
    await websocket.close()

    print("Client shutdown complete. Exiting...")


async def send_worker_messages(channel, pc, websocket):

    message = input("Enter message to send (or type 'quit' to exit): ")

    if message.lower() == "quit":
        print("Quitting...")
        await pc.close()
        return

    if channel.readyState != "open":
        print(f"Data channel not open. Ready state is: {channel.readyState}")
        return
   
    channel.send(message)
    print(f"Message sent to client.")


async def handle_connection(pc, websocket):
    try:
        async for message in websocket:
            data = json.loads(message)
            
            # 1. receieve offer SDP from client (forwarded by signaling server)
            if data['type'] == "offer":
                # 1a. set worker peer's remote description to the client's offer based on sdp data
                print('Received offer SDP')

                await pc.setRemoteDescription(RTCSessionDescription(sdp=data['sdp'], type='offer')) 
                
                # 1b. generate worker's answer SDP and set it as the local description
                await pc.setLocalDescription(await pc.createAnswer())
                
                # 1c. send worker's answer SDP to client so they can set it as their remote description
                await websocket.send(json.dumps({'type': pc.localDescription.type, 'target': data['target'], 'sdp': pc.localDescription.sdp}))
            
            # 2. to handle "trickle ICE" for non-local ICE candidates (might be unnecessary)
            elif data['type'] == 'candidate':
                print("Received ICE candidate")
                candidate = data['candidate']
                await pc.addIceCandidate(candidate)

            elif data['type'] == 'quit': # NOT initiator, received quit request from worker
                print("Received quit request from Client. Closing connection...")
                await clean_exit(pc, websocket)
                return

            # 3. error handling
            else:
                print(f"Unhandled message: {data}")
                # print("exiting...")
                # break
    
    except json.JSONDecodeError:
        print("Invalid JSON received")

    except Exception as e:
        print(f"Error handling message: {e}")

        
async def run_worker(pc, peer_id):
    # websockets are only necessary here for setting up exchange of SDP & ICE candidates to each other
    
    # 2. listen for incoming data channel messages on channel established by the client
    @pc.on("datachannel")
    def on_datachannel(channel):
        # listen for incoming messages on the channel
        print("channel(%s) %s" % (channel.label, "created by remote party & received."))

        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print(f"ICE connection state is now {pc.iceConnectionState}")
            if pc.iceConnectionState == "failed":
                print('ICE connection failed')
                await clean_exit(pc, websocket)
                return
            elif pc.iceConnectionState in ["failed", "disconnected"]:
                print("ICE connection failed/disconnected. Closing connection.")
                await clean_exit(pc, websocket)
                return
            elif pc.iceConnectionState == "closed":
                print("ICE connection closed.")
                await clean_exit(pc, websocket)
                return
            
        @channel.on("open")
        def on_channel_open():
            print(f'{channel.label} channel is open')
        
        @channel.on("message")
        async def on_message(message):
            # receive client message
            print(f"Worker received: {message}")

            if message.lower() == "sleap-label": # TEST RECEIVING COMMMAND AND EXECUTING INSIDE DOCKER CONTAINER
                print("Running SLEAP label command...")
                try:
                    result = subprocess.run(
                        message, 
                        capture_output=True,
                        text=True,
                        check=True,                        
                    )
                    print(result.stdout) # simple print for now
                except:
                    print("Error running SLEAP label command.")

            # if message.lower() == "quit":
            #     print("Quitting...")
            #     return
            
            # send message to client
            await send_worker_messages(channel, pc, websocket)


    # 1. worker registers with the signaling server (temp: localhost:8080) via websocket connection
    # this is how the worker will know the client peer exists
    async with websockets.connect("ws://host.docker.internal:8080") as websocket:
        # 1a. register the worker with the server
        await websocket.send(json.dumps({'type': 'register', 'peer_id': peer_id}))
        print(f"{peer_id} sent to signaling server for registration!")

        # 1b. handle incoming messages from server (e.g. answers)
        await handle_connection(pc, websocket)
        print(f"{peer_id} connected with client!" )


    # ICE, or Interactive Connectivity Establishment, is a protocol used in WebRTC to establish a connection
    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print(f"ICE connection state is now {pc.iceConnectionState}")
        if pc.iceConnectionState == "failed":
            print('ICE connection failed')
            await clean_exit(pc, websocket)
            return
        elif pc.iceConnectionState in ["failed", "disconnected"]:
            print("ICE connection failed/disconnected. Closing connection.")
            await clean_exit(pc, websocket)
            return
        elif pc.iceConnectionState == "closed":
            print("ICE connection closed.")
            await clean_exit(pc, websocket)
            return
         

    # try:
    #     await asyncio.sleep(3600)
    # except asyncio.CancelledError:
    #     print("Worker connection closed.")
    # finally:
    #     await pc.close()
    #     await websocket.close()
        
if __name__ == "__main__":
    pc = RTCPeerConnection()
    try:
        asyncio.run(run_worker(pc, "worker1"))
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")
    finally:
        print("exited")
        

    
