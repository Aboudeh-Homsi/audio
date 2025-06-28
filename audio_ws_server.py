import os
import asyncio
from aiohttp import web
import websockets
import socket

connected = set()

async def relay(websocket):
    connected.add(websocket)
    try:
        async for message in websocket:
            for conn in connected:
                if conn != websocket:
                    await conn.send(message)
    finally:
        connected.remove(websocket)

async def websocket_handler(request):
    ws_current = web.WebSocketResponse()
    await ws_current.prepare(request)

    # Convert aiohttp WebSocket to websockets WebSocket
    ws_protocol = ws_current._req.transport._protocol
    ws = websockets.server.WebSocketServerProtocol()
    ws.connection_made(ws_protocol)
    connected.add(ws)
    try:
        async for msg in ws_current:
            if msg.type == web.WSMsgType.BINARY:
                for conn in connected:
                    if conn != ws:
                        await conn.send(msg.data)
    finally:
        connected.remove(ws)
    return ws_current

async def health(request):
    return web.Response(text="ok")

def main():
    app = web.Application()
    app.router.add_get('/', health)  # Health check endpoint
    app.router.add_get('/ws', websocket_handler)  # WebSocket endpoint

    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, port=port)

if __name__ == "__main__":
    main()