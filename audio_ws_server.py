import asyncio
from aiohttp import web

clients = set()

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    clients.add(ws)
    print(f"New client connected: {request.remote}")
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.BINARY:
                disconnected_clients = set()
                for client in list(clients):
                    if client is not ws:
                        try:
                            await client.send_bytes(msg.data)
                        except Exception as e:
                            print(f"Removing client {client}: {e}")
                            disconnected_clients.add(client)
                clients.difference_update(disconnected_clients)
            elif msg.type == web.WSMsgType.TEXT:
                # Optionally, broadcast text to all other clients
                disconnected_clients = set()
                for client in list(clients):
                    if client is not ws:
                        try:
                            await client.send_str(msg.data)
                        except Exception as e:
                            print(f"Removing client {client}: {e}")
                            disconnected_clients.add(client)
                clients.difference_update(disconnected_clients)
            elif msg.type == web.WSMsgType.ERROR:
                print(f"Connection error: {ws.exception()}")
    finally:
        clients.discard(ws)
        print(f"Client disconnected: {request.remote}")
    return ws

app = web.Application()
app.router.add_get('/ws', websocket_handler)

if __name__ == "__main__":
    web.run_app(app, port=8000)
