import asyncio
from aiohttp import web, WSMsgType

clients = set()
clients_lock = asyncio.Lock()

async def websocket_handler(request):
    ws = web.WebSocketResponse(max_msg_size=2**24)
    await ws.prepare(request)
    async with clients_lock:
        clients.add(ws)
    print(f"[SERVER] New client connected: {request.remote} - Total: {len(clients)}")

    try:
        async for msg in ws:
            if msg.type == WSMsgType.BINARY:
                # Only relay *live* audio, never buffer or resend old
                to_remove = []
                async with clients_lock:
                    for client in clients:
                        if client is not ws:
                            try:
                                await client.send_bytes(msg.data)
                            except Exception as e:
                                print(f"[SERVER] Removing client (send_bytes failed): {e}")
                                to_remove.append(client)
                    for client in to_remove:
                        clients.discard(client)
            elif msg.type == WSMsgType.TEXT:
                text_data = msg.data.encode("utf-8")
                to_remove = []
                async with clients_lock:
                    for client in clients:
                        if client is not ws:
                            try:
                                await client.send_bytes(b"TEXT:" + text_data)
                            except Exception as e:
                                print(f"[SERVER] Removing client (send_str failed): {e}")
                                to_remove.append(client)
                    for client in to_remove:
                        clients.discard(client)
            elif msg.type == WSMsgType.ERROR:
                print(f"[SERVER] Connection closed with exception: {ws.exception()}")
                break
    except Exception as e:
        print(f"[SERVER] Handler exception: {e}")
    finally:
        async with clients_lock:
            clients.discard(ws)
        print(f"[SERVER] Client disconnected: {request.remote}, Total: {len(clients)}")
        await ws.close()
    return ws

async def health(request):
    return web.Response(text="OK")

def main():
    app = web.Application()
    app.router.add_get('/ws', websocket_handler)
    app.router.add_get('/health', health)
    print("[SERVER] Starting Audio WS Server on 0.0.0.0:8000 ...")
    web.run_app(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
