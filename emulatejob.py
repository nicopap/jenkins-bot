"""Start and stop pretending to be doing work."""
import asyncio

import discord

from config import discord_conf

async def constantly_type(queue, client):
    """Sends discord a typing indicator in report channel until any
    message is sent in the queue."""
    print('[INFO] Will be constantly typing until stop request')
    while queue.empty():
        await asyncio.sleep(10)
        await client.send_typing(client.get_channel(discord_conf.reportId))
    await queue.get()


async def start(client):
    """Starts pretending to be busy testing stuff."""
    print('[INFO] Started prentending to do stuff')
    queue = asyncio.Queue()
    await client.send_message(client.get_channel(discord_conf.reportId),
                              'Commencement d\'un job jenkins')
    client.loop.create_task(constantly_type(queue, client))
    await client.change_presence(
        game=discord.Game(name='Test du projet'),
        status=discord.Status.online)
    return queue


async def abort(queue, client):
    """Stop pretending to be busy testing stuff."""
    print('[INFO] Aborting job simulation!')
    await queue.put('Stop')
    msg = ('Le job jenkins a dû être interromput pour une raison'
           + ' inconnue. Réferrez-vous à la log de jenkins-bot pour de plus'
           + ' ample informations.')
    await client.send_message(client.get_channel(discord_conf.reportId), msg)
    await client.change_presence(
        game=discord.Game(name='à rien'),
        status=discord.Status.idle)


async def stop(queue, client, url):
    """Stop pretending to be busy testing stuff."""
    print('[INFO] Stopping cleanly job simulation.')
    await queue.put('Stop')
    msg = ('**Job Jenkins complet!! __Bravo__**\n'
           + f'url: {url}')
    await client.send_message(client.get_channel(discord_conf.reportId), msg)
    await client.change_presence(
        game=discord.Game(name='à rien'),
        status=discord.Status.idle)
