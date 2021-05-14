import discord
from dotenv import load_dotenv
import os
import requests
import json
import random
from deta import Deta

load_dotenv()

#deta base
deta = Deta(os.getenv('DETA_PROJECT_KEY'))

#method to return db
def getdb(name):
  return deta.Base(name)

#establish connection with discord client
client = discord.Client()

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def update_encouragements_table(encouraging_message):
  db = getdb("encouragements")
  if db.get("encouragements"):
    updates = {"cheers": db.util.append(encouraging_message)}
    db.update(updates, "encouragements")
  else:
    db.put({"cheers": [encouraging_message]}, "encouragements")

sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = ["Cheer up!", "Hang in there.", "You are a great person / bot!"]

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

  if any(word in message.content for word in sad_words):
    await message.channel.send(random.choice(starter_encouragements))

  if message.content.startswith('!new'):
    encouraging_message = message.content.split('!new ', 1)[1]
    update_encouragements_table(encouraging_message)
    await message.channel.send("New encouraging message added")

#to establish connection with client using bot token
client.run(os.getenv('TOKEN', 'Token not found'))
















