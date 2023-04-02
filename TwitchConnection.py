from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
from dotenv import load_dotenv
import os
from BlenderChatbot import ChatBot
import json

# this is to be able to use the .env file in the same directory
load_dotenv()

# set up the authentication stuff
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

# initialize the bot
ai = ChatBot()

try:
    with open('user_credentials.json', 'r') as f:
        user_credentials = json.load(f)
        print("User credentials loaded")
except FileNotFoundError:
    print("User credentials not found")
    user_credentials = None

async def on_ready(ready_event: EventData):
    await ready_event.chat.join_room(TARGET_CHANNEL)

async def on_message(msg: ChatMessage):
    # print(msg.text)
    if msg.text.startswith('!bot'):
        await bot_command_handler(msg)

# here we need to put in a function that will be executed when a user messages !bot in chat
async def bot_command_handler(cmd: ChatCommand):
    trueMessage = cmd.text[5:]
    print(trueMessage)
    reply = ai.text_output(utterance=cmd.text)
    await cmd.reply(f'{cmd.user.name}: {reply[3:-4]}')

# set up the connection to Twitch
async def twitch_connect():
    twitch = await Twitch(CLIENT_ID, CLIENT_SECRET)
    if user_credentials is not None:
        token = user_credentials['token']
        refresh_token = user_credentials['refresh_token']
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        print("User credentials loaded")
    else:
        auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False)
        token, refresh_token = await auth.authenticate()
        await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)
        with open('user_credentials.json', 'w') as f:
            json.dump({'token': token, 'refresh_token': refresh_token}, f)
            print("User credentials saved")
    
    print("Twitch connection established")

    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.start()

    try:
        input("Press enter to stop the bot...\n")
    finally:
        chat.stop()
        await twitch.close()

asyncio.run(twitch_connect())
