"""Start and stop pretending to be doing work."""
import asyncio
from queue import Queue

import discord

from config import discord_conf

async def constantly_type(queue, client):
    """Sends discord a typing indicator in report channel until any
    message is sent in the queue."""
    while queue.empty():
        await asyncio.sleep(10)
        await client.send_typing(client.get_channel(discord_conf.reportId))
    queue.get()


async def start(client):
    """Starts pretending to be busy testing stuff."""
    queue = Queue()
    await client.send_message(client.get_channel(discord_conf.reportId),
                              'Commencement d\'un job jenkins')
    client.loop.create_task(constantly_type(queue, client))
    await client.change_presence(
        game=discord.Game(name='Test du projet'),
        status=discord.Status.online)
    return queue


async def stop(queue, client):
    """Stop pretending to be busy testing stuff."""
    queue.put('Stop')
    await client.send_message(client.get_channel(discord_conf.reportId),
                              'Job Jenkins complet!')
    await client.change_presence(
        game=discord.Game(name='à rien'),
        status=discord.Status.idle)
