import asyncio
import websockets
import json
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel

async def send_message(channel):
    if channel.readyState == "open":
        await channel.send("Hello, worker! I am the client.")
    else:
        print(f"Data channel not open. Ready state is: {channel.readyState}")

async def run_client(peer_id):
    async with websockets.connect("ws://localhost:8080") as websocket:
        # register the client with the signaling server
        await websocket.send(json.dumps({'type': 'register', 'peer_id': peer_id}))
        print("Client registered!")

        # query the signaling server for available workers
        await websocket.send(json.dumps({'type': 'query'}))
        response = await websocket.recv()
        available_workers = json.loads(response)["peers"]
        print(f"Available workers: {available_workers}")

        # select a worker to connect to (will implement firebase auth later)
        target_worker = available_workers[0] if available_workers else None
        print(f"Selected worker: {target_worker}")

        if not target_worker:
            print("No workers available")
            return

        # create a new RTCPeerConnection object to handle WebRTC communication
        pc = RTCPeerConnection()

        # # create a data channel
        # data_channel = pc.createDataChannel("my-data-channel")

        connected_event = asyncio.Event()
        data_channel_open_event = asyncio.Event()
        
        # new
        print(pc.iceConnectionState) 
    
        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print(f"ICE connection state is now {pc.iceConnectionState}")
            if pc.iceConnectionState == "failed":
                connected_event.set()
                print('ICE connection failed')
            elif pc.iceConnectionState == "connected":
                connected_event.set()
                print('ICE connection succeeded')

        @pc.on("icecandidate")
        async def on_icecandidate(candidate):
            if candidate:
                await websocket.send(json.dumps({'type': 'candidate', 'candidate': candidate}))
        
        data_channel = pc.createDataChannel("my-data-channel")

        @data_channel.on("open")
        def on_data_channel_open():
            print("Data channel is open")
            asyncio.create_task(send_message(data_channel))
            data_channel_open_event.set()

        # register an event handler for the 'message' event on the RTCPeerConnection object
        @data_channel.on("message")
        async def on_message(message):
            print(f"Client received: {message}")

        @pc.on("datachannel")
        def on_data_channel(channel):
            @channel.on("message")
            async def on_message(message):
                print(f"Client received: {message}")


        await pc.setLocalDescription(await pc.createOffer())
        await websocket.send(json.dumps({'type': pc.localDescription.type, 'target': target_worker, 'sdp': pc.localDescription.sdp}))
        # test print
        print('Offer sent to worker')

        # handle incoming messages from server (e.g. answers)
        async for message in websocket:
            data = json.loads(message)
            if data['type'] == 'answer':
                print(f"Received answer from worker: {data}")
                await pc.setRemoteDescription(RTCSessionDescription(sdp=data['sdp'], type=data['type']))
            elif data['type'] == 'candidate':
                candidate = data['candidate']
                await pc.addIceCandidate(candidate)
        
        await asyncio.gather(connected_event.wait(), data_channel_open_event.wait())

        if pc.iceConnectionState == "failed":
            print("ICE connection failed. Closing connection.")
            return

        # send a message to the worker via the data channel
        # await data_channel.send("Hello, worker! I am the from client.")

        await asyncio.sleep(10)
        await pc.close()
        print("Client closed connection.")

if __name__ == "__main__":
    asyncio.run(run_client("client1"))