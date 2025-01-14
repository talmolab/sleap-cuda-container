# Dummy client for testing purposes
import asyncio
import websockets
import json
from aiortc import RTCPeerConnection, RTCSessionDescription

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

        # create a data channel
        data_channel = pc.createDataChannel("my-data-channel")

        # register an event handler for the 'message' event on the RTCPeerConnection object
        @data_channel.on("message")
        async def on_message(message):
            print(f"Client received: {message}")
        
        print(pc.iceConnectionState)
        @pc.on("iceconnectionstatechange")
        async def on_iceconnectionstatechange():
            print(f"ICE connection state is now {pc.iceConnectionState}")
            if pc.iceConnectionState == "failed":
                await pc.close()

        await pc.setLocalDescription(await pc.createOffer())
        await websocket.send(json.dumps({'type': 'offer', 'target': target_worker, 'sdp': pc.localDescription.sdp}))

        # handle incoming messages from server (e.g. answers)
        answer = json.loads(await websocket.recv())
        await pc.setRemoteDescription(RTCSessionDescription(**answer))

        # send a message to the worker
        await data_channel.send("Hello, worker! I am the from client.")

        await asyncio.sleep(10)
        await pc.close()
        print("Client closed connection.")

if __name__ == "__main__":
    asyncio.run(run_client("client1"))