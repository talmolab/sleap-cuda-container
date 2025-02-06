import asyncio
import websockets
import json
from aiortc import RTCPeerConnection, RTCSessionDescription

# key: peer_id, value: specific peer websocket 
connected_peers = {} 


async def handle_client(websocket):
    """Handles incoming messages between peers to facilitate exchange of SDP & ICE candidates.

    Registers both peers and links them together to forward SDP & ICE candidates.
    Takes SDP arguments from for registration, query (seek available workers), offer, and answer.

    Args:
		websocket: A websocket connection object between peer1 (client) and peer2 (worker)
    
	Returns:
		None
    
	Raises:
		JSONDecodeError: Invalid JSON received
		Exception: An error occurred while handling the client
    
    """
    
    peer_id = None
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"Received message: {data}")

                if data['type'] == "register":
                    # formatted as "register:peer_id"
                    peer_id = data['peer_id']

                    # add peer_id to connected_peers dictionary & update server terminal
                    connected_peers[peer_id] = websocket
                    print(f"Registered peer: {peer_id}")
                                    
                elif data['type'] == "query":
                    # send available peers to client terminal via websocket
                    response = {'type': 'available_peers', 'peers': list(connected_peers.keys())}
                    await websocket.send(json.dumps(response))

                elif data['type'] == "offer":
                    # handle offer/exchange between peers
                    # formatted as "offer:peer_id" or "answer:peer_id"
                    target_peer_id = data['target']
                    target_websocket = connected_peers.get(target_peer_id)

                    # if target_peer_id exists, send message to target_peer_id
                    # update server terminal
                    if target_websocket:
                        print(f"Forwarding message from {peer_id} to {target_peer_id}")
                        await target_websocket.send(json.dumps(data))
                    else:
                        print(f"Peer not found: {target_peer_id}")

                elif data['type'] == "answer":
                    # hardcoded for now
                    target_peer_id = 'client1'
                    target_websocket = connected_peers.get(target_peer_id)

                    # if target_peer_id exists, send message to target_peer_id
                    # update server terminal
                    if target_websocket:
                        print(f"Forwarding message from {peer_id} to {target_peer_id}")
                        await target_websocket.send(json.dumps(data))
                    else:
                        print(f"Peer not found: {target_peer_id}")

            except json.JSONDecodeError:
                print("Invalid JSON received")

    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected cleanly.")
    
    except Exception as e:
        print(f"Error handling client: {e}")
    
    finally:
        if peer_id:
            # disconnect the peer
            del connected_peers[peer_id]
            print(f"Peer disconnected: {peer_id}")
        
async def main():
    """Main function to run server indefinitely.
    
    Creates a websocket server to handle incoming connections and passes them to handle_client.
    
    Args:
		None
    
	Returns:
		None
    
	Raises:
		JSONDecodeError: Invalid JSON received
		Exception: An error occurred while handling the client
    """

    async with websockets.serve(handle_client, "localhost", 8080):
        # run server indefinitely
        print("Server started!")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())