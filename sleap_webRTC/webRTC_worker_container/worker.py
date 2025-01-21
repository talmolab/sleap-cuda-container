import asyncio
import websockets
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel

async def send_worker_messages(channel):
    while channel.readyState == "open": 
        message = input("Enter message to send (or type 'quit' to exit): ")
        if message.lower() == "quit":
            break
        await channel.send(message)
        print("Message sent to client.")

        async for msg in channel:
            print(f"received: {msg}")

    if channel.readyState != "open":
        print(f"Data channel not open. Ready state is: {channel.readyState}")

async def handle_connection(pc, websocket):
    # test print 
    print(f"the ICE connection state is now {pc.iceConnectionState}")

    async for message in websocket:
        print(message)
        try:
            data = json.loads(message)
            if data['type'] == "offer":
                # set the remote description of the RTCPeerConnection object
                await pc.setRemoteDescription(RTCSessionDescription(sdp=data['sdp'], type='offer')) 
                
                # create an answer to the offer
                await pc.setLocalDescription(await pc.createAnswer())
                
                # send the answer to the client
                await websocket.send(json.dumps({'type': pc.localDescription.type, 'target': data['target'], 'sdp': pc.localDescription.sdp}))
            elif data['type'] == 'candidate':
                print("Received ICE candidate")
                candidate = data['candidate']
                await pc.addIceCandidate(candidate)
            else:
                print(f"Unhandled message: {data}")
        
        except json.JSONDecodeError:
            print("Invalid JSON received")

        except Exception as e:
            print(f"Error handling message: {e}")

        
async def run_worker(peer_id):
    # worker connects to signaling server (temp: localhost:8080) via websocket
    async with websockets.connect("ws://localhost:8080") as websocket:
        # register the worker with the server
        await websocket.send(json.dumps({'type': 'register', 'peer_id': peer_id}))
        print("Worker started!")

        # create a new RTCPeerConnection object to handle WebRTC communication
        pc = RTCPeerConnection()
        data_channel = None

        # listen for incoming data channel -> set up event listener for incoming messages on that channel
        @pc.on("datachannel")
        def on_datachannel(channel):
            # listen for incoming messages on the channel
            nonlocal data_channel
            data_channel = channel
            @channel.on("message")
            async def on_message(message):
                # print to worker terminal and send to client terminal
                print(f"Worker received: {message}")
                if message.lower() == "quit":
                    print("Quitting")
                    await pc.close()
                    return
                
                asyncio.create_task(send_worker_messages(channel))
                
                
                # # Process the data and send a response
                # response = {"message": f"Worker received: {data['message']}"}
                # await channel.send(json.dumps(response))
        
        # ICE, or Interactive Connectivity Establishment, is a protocol used in WebRTC to establish a connection
        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print(f"ICE connection state is now {pc.iceConnectionState}")
            if pc.iceConnectionState == "failed":
                print('ICE connection failed')
                await pc.close()
                # await websocket.close()

        # handle incoming messages from server (e.g. answers)
        await handle_connection(pc, websocket)

        try:
            await asyncio.sleep(3600)
        except asyncio.CancelledError:
            print("Worker connection closed.")
        finally:
            await pc.close()
            await websocket.close()
        
if __name__ == "__main__":
    asyncio.run(run_worker("worker1"))
    

    