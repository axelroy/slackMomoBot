"""Sample Slack ping bot using asyncio and websockets."""
import asyncio
import json
import sys
import argparse
from urllib.request import urlopen
from urllib.error import URLError
from aiohttp import ClientSession, errors
from pollmanager import PollManager
import aiohttp

from api import api_call

DEBUG = True
from bot_token import TOKEN
RUNNING = True

async def answer(user_token, message):
    data = {"token": TOKEN, "channel": user_token,"text": message}
    await api_call("chat.postMessage", data, TOKEN)


async def consumer(message, rtm):
    """Display the message."""

    BOT_TAG = '<@' + rtm['self']['id'] + '>: '
    message_user = message.get('user')
    message_contenant = message.get('text');

    """Check if the bot is conserned by the message"""
    if message.get('type') == 'message' and message_user != None :
        #print(BOT_TAG)
        if BOT_TAG == message_contenant[:len(BOT_TAG)] :
            await answer(message.get('channel'), parse_command(message_contenant[len(BOT_TAG):], message_user)[1])


async def bot(token=TOKEN):

    """Create a bot that joins Slack."""
    rtm = await api_call("rtm.start")
    assert rtm['ok'], "Error connecting to RTM."

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(rtm["url"]) as ws:
            async for msg in ws:
                assert msg.tp == aiohttp.MsgType.text
                message = json.loads(msg.data)
                asyncio.ensure_future(consumer(message, rtm))

def stop():
    """Gracefully stop the bot."""
    global RUNNING
    RUNNING = False
    print("Stopping... closing connections.")

#=============================================================
#   PARSER MANAGEMENT
#=============================================================

def parse_command(message, user):
    args = [c for c in message.split(' ') if c]
    command = args[0]

    if command in "help" :
        return poll_manager.help()

    if len(args) < 2:
        return "Not enough arguments [command] [poll] [arg(if command need it)]"

    poll = args[1]
    data = " ".join(args[2:]) if len(args) >= 3 else ""

    if command in "create" :
        return poll_manager.create_poll(poll, user, question=data)

    if command in "question" :
        return poll_manager.set_question(poll, user, question=data)

    if command in "choices" :
        return poll_manager.set_choices(poll, user, choices=data.split(u";"))

    if command in "answer" :
        return poll_manager.answer_poll(poll, user, answer=data)

    if command in "close" :
        return poll_manager.close_poll(poll, user)

    if command in "start" :
        return poll_manager.start_poll(poll, user)

    if command in "show" :
        return poll_manager.show_poll(poll, user)

    if command in "remove" :
        return poll_manager.remove_poll(poll, user)

    return "The command \""+command+"\" does not exit"


#=============================================================
#   MAIN
#=============================================================

poll_manager = PollManager()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot())
    loop.close()
