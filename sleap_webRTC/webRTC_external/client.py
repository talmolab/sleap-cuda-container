import asyncio
import websockets
import json
import logging

from aiortc import RTCPeerConnection, RTCSessionDescription, RTCDataChannel
from websockets import WebSocketClientProtocol

async def clean_exit(pc, websocket):
    print("Closing WebRTC connection...")
    await pc.close()

    print("Closing websocket connection...")
    await websocket.close()

    print("Client shutdown complete. Exiting...")


async def handle_connection(pc: RTCPeerConnection, websocket):
    """Handles receiving SDP answer from Worker and ICE candidates from Worker.

    Args:
        pc: RTCPeerConnection object
        websocket: websocket connection object 
    
    Returns:
		None
        
    Raises:
		JSONDecodeError: Invalid JSON received
		Exception: An error occurred while handling the message
    """

    try:
        async for message in websocket:
            data = json.loads(message)

            # 1. receive answer SDP from worker and set it as this peer's remote description
            if data.get('type') == 'answer':
                print(f"Received answer from worker: {data}")

                await pc.setRemoteDescription(RTCSessionDescription(sdp=data.get('sdp'), type=data.get('type')))

            # 2. to handle "trickle ICE" for non-local ICE candidates (might be unnecessary)
            elif data.get('type') == 'candidate':
                print("Received ICE candidate")
                candidate = data.get('candidate')
                await pc.addIceCandidate(candidate)

            elif data.get('type') == 'quit': # NOT initiator, received quit request from worker
                print("Worker has quit. Closing connection...")
                await clean_exit(pc, websocket)
                break

            # 3. error handling
            else:
                print(f"Unhandled message: {data}")
                print("exiting...")
                break
    
    except json.JSONDecodeError:
        print("Invalid JSON received")

    except Exception as e:
        print(f"Error handling message: {e}")


async def run_client(pc, peer_id: str):
    """Sends initial SDP offer to worker peer and establishes both connection & datachannel to be used by both parties.
	
		Initializes websocket to select worker peer and sends datachannel object to worker.
	
    Args:
		pc: RTCPeerConnection object
		peer_id: unique str identifier for client
        
    Returns:
		None
        
    Raises:
		Exception: An error occurred while running the client
    """

    channel = pc.createDataChannel("my-data-channel")
    print("channel(%s) %s" % (channel.label, "created by local party."))

    async def send_client_messages():
        """Handles typed messages from client to be sent to worker peer.
        
		Takes input from client and sends it to worker peer via datachannel.
	
        Args:
			None
        
		Returns:
			None
        
        """
        message = input("Enter message to send (or type 'quit' to exit): ")

        if message.lower() == "quit": # client is initiator, send quit request to worker
            print("Quitting...")
            await pc.close()
            return 

        if channel.readyState != "open":
            print(f"Data channel not open. Ready state is: {channel.readyState}")
            return 
        
        channel.send(message)
        print(f"Message sent to worker.")


    @channel.on("open")
    async def on_channel_open():
        """Event handler function for when the datachannel is open.
        Args:
			None
            
        Returns:
			None
        """

        print(f"{channel.label} is open")
        await send_client_messages()
    

    @channel.on("message")
    async def on_message(message):
        print(f"Client received: {message}")
        await send_client_messages()


    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print(f"ICE connection state is now {pc.iceConnectionState}")
        if pc.iceConnectionState in ["connected", "completed"]:
            print("ICE connection established.")
            # connected_event.set()
        elif pc.iceConnectionState in ["failed", "disconnected"]:
            print("ICE connection failed/disconnected. Closing connection.")
            await clean_exit(pc, websocket)
            return
        elif pc.iceConnectionState == "closed":
            print("ICE connection closed.")
            await clean_exit(pc, websocket)
            return


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
    

if __name__ == "__main__":
    pc = RTCPeerConnection()
    try: 
        asyncio.run(run_client(pc, "client1"))
    except KeyboardInterrupt:
        print("KeyboardInterrupt: Exiting...")
    finally:
        print("exited")

    