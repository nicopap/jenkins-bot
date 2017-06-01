"""Start and stop pretending to be doing work."""
import asyncio

import discord

from config import discord_conf

STOP_TYPING = 1
async def constantly_type(queue, client):
    """Sends discord a typing indicator in report channel until any
    message is sent in the queue.

    queue: the queue that the function should listen to for the STOP_TYPING
        signal.
    client: the discord client instance to use to pretend typing."""
    print('[INFO] Will be constantly typing until stop request')
    while queue.empty():
        await asyncio.sleep(10)
        await client.send_typing(client.get_channel(discord_conf.reportId))
    await queue.get()


async def start(client):
    """Starts pretending to be busy testing stuff.

    client: the discord client instance to use to send messages.

    returns: a queue on which to push a STOP_TYPING signal when the job
        is over."""
    print('[INFO] Started prentending to do stuff')
    queue = asyncio.Queue()
    await client.send_message(client.get_channel(discord_conf.reportId),
                              'Commencement d\'un job jenkins')
    client.loop.create_task(constantly_type(queue, client))
    await client.change_presence(
        game=discord.Game(name='Test du projet'),
        status=discord.Status.online)
    return queue


async def abort(queue, client, url):
    """Stop pretending to be busy testing stuff.

    queue: the queue on which to send the STOP_TYPING signal
    client: the discord client instance to use to send messages.
    url: the url of the jenkins job to link to in chat."""
    print('[INFO] Aborting job simulation!')
    await queue.put(STOP_TYPING)
    msg = ('**Le job jenkins a dû être interromput __SAD__**\n'
           + 'Il est possible que ce soit dû à une erreure détectée par '
           + f'Jenkins, veuillez vous référer à {url}')
    await client.send_message(client.get_channel(discord_conf.reportId), msg)
    await client.change_presence(
        game=discord.Game(name='à rien'),
        status=discord.Status.idle)


async def stop(queue, client, url):
    """Stop pretending to be busy testing stuff.

    queue: the queue on which to send the STOP_TYPING signal
    client: the discord client instance to use to send messages.
    url: the url of the jenkins job to link to in chat."""
    print('[INFO] Stopping cleanly job simulation.')
    await queue.put('Stop')
    msg = ('**Job Jenkins complet!! __Bravo__**\n'
           + f'url: {url}')
    await client.send_message(client.get_channel(discord_conf.reportId), msg)
    await client.change_presence(
        game=discord.Game(name='à rien'),
        status=discord.Status.idle)
