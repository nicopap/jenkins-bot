"""Listen to webhooks and reports back when they have been awaken."""
import asyncio
from aiohttp import web

SUBCRIPTION_BOOK = {}
def subscribe_to(path, callback):
    """Calls callback when the queried path is requested over the wire"""
    SUBCRIPTION_BOOK[path] = callback

def unsubscribe_from(path):
    """Remove the subscription entry from the SUBCRIPTION_BOOK."""
    del SUBCRIPTION_BOOK[path]

async def send_event(request):
    """Dispatches the request to URL to the subscribed callbacks."""
    print(f'[INFO] got a request for {request}')
    for subcribed_path in SUBCRIPTION_BOOK.keys():
        if subcribed_path == request:
            print('[INFO] sending request to subscribed function')
            request_content = request.json
            SUBCRIPTION_BOOK[subcribed_path](request)
            return web.Response(text="An event has been triggered.")
    else:
        return web.Response(text="You did call the wrong URL.")

async def runserver(loop):
    """Starts the listening server for websocket calls."""
    server = web.Server(send_event)
    await loop.create_server(server, '0.0.0.0', 8080)
    print("[INFO] Server running")
