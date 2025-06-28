import asyncio
import websockets

connected = set()

async def relay(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            # If audio, relay as binary; if text, relay as text
            for conn in connected:
                if conn != websocket:
                    if isinstance(message, bytes):
                        await conn.send(message)
                    else:
                        await conn.send(f"{websocket.remote_address}: {message}")
    finally:
        connected.remove(websocket)

start_server = websockets.serve(relay, "0.0.0.0", 8080, max_size=2**24)  # use your preferred port

asyncio.get_event_loop().run_until_complete(start_server)
print("WebSocket audio relay server started on port 8080")
asyncio.get_event_loop().run_forever()