import os
from aiohttp import web

connected = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    connected.add(ws)
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.BINARY:
                # Relay audio to all other connected clients
                for client in connected:
                    if client != ws:
                        await client.send_bytes(msg.data)
    finally:
        connected.remove(ws)
    return ws

async def health(request):
    return web.Response(text="ok")

app = web.Application()
app.router.add_get("/", health)         # Health check endpoint
app.router.add_get("/ws", websocket_handler)  # WebSocket endpoint

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port)