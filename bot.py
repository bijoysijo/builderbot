import discord
from dotenv import load_dotenv
import os
import requests

load_dotenv()

#establish connection with discord client
client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

#intializer event
@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.content.startswith('!hello'):
    await message.channel.send('Hello!')

  if message.content.startswith('!inspire'):
    quote = get_quote()
    await message.channel.send(quote)

#to establish connection with client using bot token
client.run(os.getenv('TOKEN', 'Token not found'))
















