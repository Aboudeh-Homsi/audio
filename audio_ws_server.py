import asyncio
import websockets

connected = set()

async def relay(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                if conn != websocket:
                    if isinstance(message, bytes):
                        await conn.send(message)
                    else:
                        await conn.send(f"{websocket.remote_address}: {message}")
    finally:
        connected.remove(websocket)

async def main():
    async with websockets.serve(relay, "0.0.0.0", 8080, max_size=2**24):
        print("WebSocket audio relay server started on port 8080")
        await asyncio.Future()  # Run forever

if __name__ == "__main__":
    asyncio.run(main())