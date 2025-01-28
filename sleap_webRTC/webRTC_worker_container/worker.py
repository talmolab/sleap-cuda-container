import asyncio
import websockets
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel

def send_worker_messages(channel, peer_id):
    if channel.readyState != "open":
        print(f"Data channel not open. Ready state is: {channel.readyState}")
        return
   
    message = input("Enter message to send (or type 'quit' to exit): ")
    if message.lower() == "quit":
        print("Quitting...")
        return
    channel.send(message)
    print(f"Message sent to {peer_id}.")


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

            # 3. error handling
            else:
                print(f"Unhandled message: {data}")
                print("exiting...")
                break
    
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
        
        @channel.on("message")
        def on_message(message):
            # receive client message
            print(f"Worker received: {message}")
            if message.lower() == "quit":
                print("Quitting...")
                return
            
            # send message to client
            send_worker_messages(channel, peer_id)


    # 1. worker registers with the signaling server (temp: localhost:8080) via websocket connection
    # this is how the worker will know the client peer exists
    async with websockets.connect("ws://localhost:8080") as websocket:
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
            await pc.close()
            await websocket.close()
         

    # try:
    #     await asyncio.sleep(3600)
    # except asyncio.CancelledError:
    #     print("Worker connection closed.")
    # finally:
    #     await pc.close()
    #     await websocket.close()
        
if __name__ == "__main__":
    pc = RTCPeerConnection()
    asyncio.run(run_worker(pc, "worker1"))

    
