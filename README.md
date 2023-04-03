# Llamachop Bot

## new and improved llamachop bot

This is an updated version of my previous llamachop bot. It is written in python and utilizes blenderbot to generate responses. Right now I am getting it working on my twitch channel, but I eventually want to make it work for any twitch channel.

Code is set to to easily run the chatbot in terminal. Model runs locally on GPU, I have not tested it on CPU. I am using a 1080ti. Code could be changed to allow for other models to be used, might add in an easy way to connect with an API in the future. 

## Functionality

- Chat commands
  - To interact with the bot, type !bot in chat at the start of your message.
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

## Planned Features

- Add a way to connect to an API to run the model.
- allow the bot to be used in multiple channels at once.