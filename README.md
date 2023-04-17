# Llamachop Bot

## new and improved llamachop bot

This is an updated version of my previous llamachop bot. It is written in python and utilizes blenderbot or OpenAI GPT-3.5 to generate responses. Right now I am getting it working on my twitch channel, but I eventually want to make it work for any twitch channel.

Code is set to to easily run the chatbot in terminal. Model can run locally on your GPU, I have not tested it on CPU. I am using a 1080ti. Code could be changed to allow for other models to be used easily, just change the path in config.json.

## Features

- Chat commands
  - !points
  - !addpoints username amount
  - !removepoints username amount
  - !quote
  - !addquote text
  - !removequote id
  - !addmod username
  - !removemod username

Chatbot will respond to chat messages, and will speak the responses with TTS. Chatbot can also manage points and quotes.

## Functionality

- Chat commands
  - To interact with the bot, type @llamachop_bot in chat at the start of your message.
    - at the moment, the model for the bot only runs locally, and I have only tested it on a GPU. There are other model options in BlenderChatbot.py that can be selected, you must uncomment the model you want to use and comment out the model you don't want to use.
  - !points
    - This will display the number of points the user has. These points are stored on a local database, so they will remain the same across streams.
  - !addpoints username amount
    - This will add points to the user. replace username with the username of the user you want to add points to, and replace amount with the amount of points you want to add.
    - must be a mod to use this command
  - !removepoints username amount
    - This will remove points from the user. replace username with the username of the user you want to remove points from, and replace amount with the amount of points you want to remove.
    - must be a mod to use this command
  - !quote
    - this will display a random quote from a saved list of quotes in the database.
  - !addquote text
    - This will add a quote to the database. replace text with the quote you want to add.
  - !removequote id
    - This will remove a quote from the database. replace id with the id of the quote you want to remove.
  - !addmod username
    - This will add a user to the mod list. replace username with the username of the user you want to add.
    - must be a mod
  - !removemod username
    - This will remove a user from the mod list. replace username with the username of the user you want to remove.
    - you cant remove the streamer from the mod list and must be a mod.
- Voice
  - hold alt to speak to the bot.

Hold Alt to speak to the bot. Info is automatically sent to Whisper AI to turn audio into text. The response from Whisper is sent to the bot, which then sends the response back to the streamer.

## Setup

to run the Twitch Chatbot:

clone the repo

install the requirements in requirements.txt

```bash
git clone <paste repo link here>
cd python-llamachop-bot
pip install -r requirements.txt
```
(optional) update the config file with your own configurations

create a .env file in the root directory of the project and add the following:

CLIENT_ID= ""

CLIENT_SECRET= ""

TARGET_CHANNEL= ""

OPENAI_API_KEY= ""

OPENAI_ORGANIZATION= ""

fill in the values with your own information.

Also go to google cloud and create a service account. Download the json file and save it in the root directory of the project.

```bash
python TwitchConnection.py
```

This will open the chatbot in the terminal and you can communicate with it directly. 

## Planned Features

- allow the bot to be used in multiple channels at once.
- fine tune my own model to be used for the bot. 
- find a good way to run local TTS on the bot's responses so Google Cloud is not needed.