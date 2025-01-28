import asyncio
import websockets
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel

async def handle_connection(pc, websocket):
    try:
        async for message in websocket:
            data = json.loads(message)

            # 1. receive answer SDP from worker and set it as this peer's remote description
            if data['type'] == 'answer':
                print(f"Received answer from worker: {data}")

                await pc.setRemoteDescription(RTCSessionDescription(sdp=data['sdp'], type=data['type']))

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


async def run_client(pc, peer_id):

    channel = pc.createDataChannel("my-data-channel")
    print("channel(%s) %s" % (channel.label, "created by local party."))

    def send_client_messages():
        if channel.readyState != "open":
            print(f"Data channel not open. Ready state is: {channel.readyState}")
        
        message = input("Enter message to send (or type 'quit' to exit): ")
        if message.lower() == "quit":
            print("Quitting...")
            return 

        channel.send(message)
        print(f"Message sent to worker.")


    @channel.on("open")
    def on_channel_open():
        print(f"{channel.label} is open")
        send_client_messages()
    

    @channel.on("message")
    def on_message(message):
        print(f"Client received: {message}")
        if message.lower() == "quit":
            print("Quitting")
            return
        
        send_client_messages()

        # asyncio.create_task(send_receive_messages(data_channel))
        # data_channel_open_event.set()
        # print(data_channel_open_event)


    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print(f"ICE connection state is now {pc.iceConnectionState}")
        if pc.iceConnectionState in ["connected", "completed"]:
            print("ICE connection established.")
            # connected_event.set()
        elif pc.iceConnectionState in ["failed", "disconnected"]:
            print("ICE connection failed/disconnected. Closing connection.")


    # 1. client registers with the signaling server (temp: localhost:8080) via websocket connection
    # this is how the client will know the worker peer exists
    async with websockets.connect("ws://localhost:8080") as websocket:
        # 1a. register the client with the signaling server
        await websocket.send(json.dumps({'type': 'register', 'peer_id': peer_id}))
        print(f"{peer_id} sent to signaling server for registration!")

        # 1b. query for available workers
        await websocket.send(json.dumps({'type': 'query'}))
        response = await websocket.recv()
        available_workers = json.loads(response)["peers"]
        print(f"Available workers: {available_workers}")

        # 1c. select a worker to connect to (will implement firebase auth later)
        target_worker = available_workers[0] if available_workers else None
        print(f"Selected worker: {target_worker}")

        if not target_worker:
            print("No workers available")
            return
        
        # 2. create and send SDP offer to worker peer
        await pc.setLocalDescription(await pc.createOffer())
        await websocket.send(json.dumps({'type': pc.localDescription.type, 'target': target_worker, 'sdp': pc.localDescription.sdp}))
        print('Offer sent to worker')

        # 3. handle incoming messages from server (e.g. answer from worker)
        await handle_connection(pc, websocket)

    await pc.close()
    await websocket.close()



        # connected_event = asyncio.Event()
        # data_channel_open_event = asyncio.Event()
        
        # new
        # print(pc.iceConnectionState) 
    
                # connected_event.set()

        # @pc.on("icecandidate")
        # async def on_icecandidate(candidate):
        #     if candidate:
        #         await websocket.send(json.dumps({'type': 'candidate', 'candidate': candidate}))
        

        

        # @pc.on("datachannel")
        # def on_data_channel(channel):
        #     @channel.on("message")
        #     async def on_message(message):
        #         print(f"Client received: {message}")
        #         print("on_message")
        
        # await asyncio.gather(connected_event.wait(), data_channel_open_event.wait())

        # if pc.iceConnectionState in ["failed", "disconnected"]:
        #     print("ICE connection failed or disconnected. Closing connection.")
        #     return

        # send a message to the worker via the data channel
        # await data_channel.send("Hello, worker! I am the from client.")

        # try:
        #     await asyncio.sleep(3600)
        # except asyncio.CancelledError:
        #     print("Client connection closed.")
        # finally:
        #     await pc.close()

if __name__ == "__main__":
    pc = RTCPeerConnection()
    asyncio.run(run_client(pc, "client1"))
    