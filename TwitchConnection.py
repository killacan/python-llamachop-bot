from twitchAPI import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio
from dotenv import load_dotenv
import os
from BlenderChatbot import ChatBot
import json
import sqlite3

# this is to be able to use the .env file in the same directory
load_dotenv()

# set up the authentication stuff
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TARGET_CHANNEL = os.getenv("TARGET_CHANNEL")
USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

# initialize the bot
ai = ChatBot()

conn = None

try:
    conn = sqlite3.connect('app.db')

    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    table_exists = cursor.fetchone() is not None
    
    if not table_exists:
        # Create the users table if it doesn't exist
        conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT, points INTEGER)')
        conn.execute('CREATE TABLE mods (id INTEGER PRIMARY KEY, name TEXT)')
        conn.execute('CREATE TABLE quotes (id INTEGER PRIMARY KEY, quote TEXT, author TEXT)')
        conn.execute('INSERT INTO mods (name) VALUES (?)', (TARGET_CHANNEL,))
        conn.execute('INSERT INTO mods (name) VALUES (?)', ('llamachop_bot',))
        conn.commit()
except sqlite3.Error as e:
    print(e)
finally:
    if conn:
        conn.close() 


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
    # if user does not exist in database, add them
    # if user does exist, increment their points
    # if user is a mod, they have full control over other users' points

    conn = sqlite3.connect('app.db')
    messageUser = conn.execute('SELECT * FROM users WHERE name = ?', (msg.user.name,)).fetchone()
    if messageUser is None:
        conn.execute('INSERT INTO users (name, points) VALUES (?, ?)', (msg.user.name, 10))

    if conn.execute('SELECT * FROM mods WHERE name = ?', (msg.user.name,)).fetchone():
        mod = True
    else:
        mod = False

    if msg.text.startswith('@llamachop_bot'):
        await bot_command_handler(msg)
    elif msg.text.startswith('!points'):
        await points_command_handler(msg)
    elif msg.text.startswith('!addpoints') & mod:
        await add_command_handler(msg)
    elif msg.text.startswith('!removepoints') & mod:
        await remove_command_handler(msg)
    elif msg.text.startswith('!quote'):
        await quote_command_handler(msg)
    elif msg.text.startswith('!addquote') & mod:
        await addquote_command_handler(msg)
    elif msg.text.startswith('!removequote') & mod:
        await removequote_command_handler(msg)
    elif msg.text.startswith('!addmod') & mod:
        await addmod_command_handler(msg)
    elif msg.text.startswith('!removemod') & mod:
        await removemod_command_handler(msg)
    elif msg.text.startswith('!gamble'):
        await gamble_command_handler(msg)
    elif msg.text.startswith('!duel'):
        await duel_command_handler(msg)
    
    
    conn.commit()
    conn.close()
# here we need to put in a function that will be executed when a user messages !bot in chat
async def bot_command_handler(cmd: ChatCommand):
    trueMessage = cmd.text[15:]
    print(trueMessage)
    reply = ai.text_output(utterance=cmd.text)
    await cmd.reply(f'{cmd.user.name}: {reply[3:-4]}')

async def points_command_handler(cmd: ChatCommand):
    # this is going to access the database and return the number of points the user has
    conn = sqlite3.connect('app.db')
    reply = conn.execute('SELECT points FROM users WHERE name = ?', (cmd.user.name,)).fetchone()
    conn.close()
    await cmd.reply(f'{cmd.user.name} has {reply[0]} points')

async def add_command_handler(cmd: ChatCommand):
    # this is going to add the specified number of points to the specified user
    name = cmd.text.split(' ')[1]
    points = cmd.text.split(' ')[2]
    conn = sqlite3.connect('app.db')
    conn.execute('UPDATE users SET points = points + ? WHERE name = ?', (points, name)).fetchone()
    conn.commit()
    conn.close()

async def remove_command_handler(cmd: ChatCommand):
    # this is going to remove the specified number of points from the specified user
    name = cmd.text.split(' ')[1]
    points = cmd.text.split(' ')[2]
    conn = sqlite3.connect('app.db')
    conn.execute('UPDATE users SET points = points - ? WHERE name = ?', (points, name)).fetchone()
    conn.commit()
    conn.close()

async def quote_command_handler(cmd: ChatCommand):
    # this is going to return a random quote from the database
    conn = sqlite3.connect('app.db')
    res = conn.execute('SELECT id, quote FROM quotes ORDER BY RANDOM() LIMIT 1').fetchone()
    conn.close()
    print(res)
    if res is not None:
        id, text = res
        await cmd.reply(f'#{id}: {text}')

async def addquote_command_handler(cmd: ChatCommand):
    # this is going to add the specified quote to the database
    quote = cmd.text[10:]
    conn = sqlite3.connect('app.db')
    conn.execute('INSERT INTO quotes (quote, author) VALUES (?, ?)', (quote, cmd.user.name))
    cmd.reply(f'Added quote: {quote}')
    conn.commit()
    conn.close()

async def removequote_command_handler(cmd: ChatCommand):
    # this is going to remove the specified quote from the database
    quote = cmd.text.split(' ')[1]
    conn = sqlite3.connect('app.db')
    conn.execute('DELETE FROM quotes WHERE id = ?', (quote,))
    cmd.reply(f'Removed quote #{quote}')
    conn.commit()
    conn.close()

async def addmod_command_handler(cmd: ChatCommand):
    # this is going to add the specified user to the mods table
    name = cmd.text.split(' ')[1]
    conn = sqlite3.connect('app.db')
    conn.execute('INSERT INTO mods (name) VALUES (?)', (name,))
    cmd.reply(f'{name} has been added to the mods list')
    conn.commit()
    conn.close()

async def removemod_command_handler(cmd: ChatCommand):
    # this is going to remove the specified user from the mods table
    name = cmd.text.split(' ')[1]
    conn = sqlite3.connect('app.db')
    if name != TARGET_CHANNEL:
        conn.execute('DELETE FROM mods WHERE name = ?', (name,))
        cmd.reply(f'{name} has been removed from the mods list')
    else:
        cmd.reply(f'{name} cannot be removed from the mods list')
    conn.commit()
    conn.close()

async def gamble_command_handler(cmd: ChatCommand):
    # this is going to allow the user to gamble their points
    # for this to work we need a function that will return a random number between 1 and 2.
    random_number = random.randint(1, 2)
    points = cmd.text.split(' ')[1]
    conn = sqlite3.connect('app.db')
    if random_number == 1:
        conn.execute('UPDATE users SET points = points + ? WHERE name = ?', (points, cmd.user.name)).fetchone()
        cmd.reply(f'{cmd.user.name} has won {points} points')
    else:
        conn.execute('UPDATE users SET points = points - ? WHERE name = ?', (points, cmd.user.name)).fetchone()
        cmd.reply(f'{cmd.user.name} has lost {points} points')
    conn.commit()

async def duel_command_handler(cmd: ChatCommand):
    # this is going to allow the user to duel another user
    # for this we are also going to need a function that returns a random number between 1 and 2.
    random_number = random.randint(1, 2)
    opponent = cmd.text.split(' ')[1]
    points = cmd.text.split(' ')[2]
    conn = sqlite3.connect('app.db')
    if random_number == 1:
        conn.execute('UPDATE users SET points = points + ? WHERE name = ?', (points, cmd.user.name)).fetchone()
        conn.execute('UPDATE users SET points = points - ? WHERE name = ?', (points, opponent)).fetchone()
        cmd.reply(f'{cmd.user.name} has beat {opponent}! they won {points} points')
    else:
        conn.execute('UPDATE users SET points = points - ? WHERE name = ?', (points, cmd.user.name)).fetchone()
        conn.execute('UPDATE users SET points = points + ? WHERE name = ?', (points, opponent)).fetchone()
        cmd.reply(f'{cmd.user.name} has lost to {opponent}! they lost {points} points')
    conn.commit()

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
