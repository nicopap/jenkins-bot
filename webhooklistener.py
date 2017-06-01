"""Listen to webhooks and reports back when they have been awaken."""
import asyncio

from aiohttp import web

SUBCRIPTION_BOOK = {}
def subscribe_to(path, callback):
    """Calls callback when the queried path is requested over the wire"""
    print(f'[INFO] adding callback {callback.__name__} to {path}')
    SUBCRIPTION_BOOK[path] = callback

def unsubscribe_from(path):
    """Remove the subscription entry from the SUBCRIPTION_BOOK."""
    print(f'[INFO] removing callback from {path}')
    del SUBCRIPTION_BOOK[path]

async def send_event(request):
    """Dispatches the request to URL to the subscribed callbacks."""
    print(f'[INFO] got a request for {request}')
    print(f'[INFO] BOOKKEEPING RECORDS: {SUBCRIPTION_BOOK}.')
    for subcribed_path in SUBCRIPTION_BOOK:
        if subcribed_path == request.url.path:
            print('[INFO] sending request to subscribed function')
            request_body = await request.json()
            await SUBCRIPTION_BOOK[subcribed_path](request_body)
            return web.Response(text="**Plays zelda puzzle solution tune**")
    return web.Response(text="T")

async def runserver(loop):
    """Starts the listening server for websocket calls."""
    server = web.Server(send_event)
    await loop.create_server(server, '0.0.0.0', 8080)
    print("[INFO] Server running")
