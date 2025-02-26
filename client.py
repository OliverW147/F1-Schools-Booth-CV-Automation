import discord
from discord.ext.commands import when_mentioned_or
import keyboard
import time

intents = discord.Intents.all()
client = discord.Client(command_prefix=when_mentioned_or("/"), intents=intents)

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.channel.name == 'fingercast':  # Replace channel-name with the name of your channel
        print(message.content)
        if int(message.content) == 4:
            keyboard.press_and_release(str(int(message.content) + 1))
            time.sleep(.05)
            keyboard.press_and_release('enter')
            time.sleep(.05)
            keyboard.press_and_release('enter')
            time.sleep(.05)
        else:
            keyboard.press_and_release(str(int(message.content) + 1))
            time.sleep(.05)
            keyboard.press_and_release('enter')
            time.sleep(.05)

client.run('')  # Replace your-bot-token with your bot's token