#!/usr/bin/env python3.6
"""The main module, loads stuff."""
from urllib.parse import quote
from logging import basicConfig
import sys

import discord

from config import discord_conf, global_conf, sonar_conf
import jenkins
from githublistener import listen_to_github
from webhooklistener import runserver

basicConfig(stream=sys.stdout)
client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    listen_to_github(sonar_report, client)
    await client.change_presence(
        game=discord.Game(name='à rien'),
        status=discord.Status.idle)


@client.event
async def on_message(message):
    """When we command the bot to send ci job to Jenkins"""
    if message.channel.id == discord_conf.activateId \
           and message.author.id == discord_conf.masterId \
           and message.content.startswith(discord_conf.trigger):
        print(f'[INFO] started ci job, cause: {discord_conf.trigger} command')
        await jenkins.request_continuous_integration(sonar_report, client)


def last_channel_msg(channel_id):
    """Returns the last message sent on the channel with id channel_id."""
    channel = client.get_channel(channel_id)
    logs = client.logs_from(channel, limit=1)
    last_message = yield logs
    logs.close()
    return last_message


async def sonar_report(sonar_json):
    print('[INFO] in form_report in module main')
    projname = sonar_json['project']['name']
    projid = sonar_json['project']['key']
    status = sonar_json['status']
    url = (global_conf.site + sonar_conf.prefix
           + '/dashboard?id=' + quote(projid))
    summary = (f'   **Analyse du code de {projname}**\n'
               f'status: {status}\n'
               f'url: {url}')
    await client.send_message(client.get_channel(discord_conf.reportId),
                              summary)
    print(sonar_json)

def main():
    client.loop.create_task(runserver(client.loop))
    client.run(discord_conf.token)


if __name__ == '__main__':
    main()
