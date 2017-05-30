#!/usr/bin/env python3.6
"""The main module, loads stuff."""
import asyncio

import discord

from config import discord_conf
from jenkins import request_continuous_integration
from githublistener import listen_to_github
from webhooklistener import runserver

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    listen_to_github(form_report)

@client.event
async def on_message(message):
    """When we command the bot to send ci job to Jenkins"""
    if message.channel.id == discord_conf.activateId \
           and message.author.id == discord_conf.masterId \
           and message.content.startswith('!SCRUM'):
        print("[INFO] started continuously integrated, cause: !SCRUM command")
        await request_continuous_integration(form_report)

def last_channel_msg(channel_id):
    """Returns the last message sent on the channel with id channel_id."""
    channel = client.get_channel(channel_id)
    logs = client.logs_from(channel, limit=1)
    last_message = yield logs
    logs.close()
    return last_message

def form_report(sonar_json):
    print('[INFO] in form_report in module main')
    client.send_message(discord_conf.reportId,
                        content='[WIP] The sonar server sent me a report')
    print(sonar_json)

def main():
    client.loop.create_task(runserver(client.loop))
    client.run(discord_conf.token)

if __name__ == "__main__":
    main()
