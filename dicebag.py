import sys
import asyncio
import discord
from auth import *
import dice
import turns
import info
import names

client = discord.Client(max_messages=128)

print("Bot connected.")

@client.event
async def on_message(msg):
	assistance = info.parse(msg.content)
	rolls = dice.parse(msg.content)
	nomen = names.parse(msg.content)
	try:
		initiative = turns.parse(msg.content)
	except IndexError as e:
		initiative = [("Invalid keyword or number of arguments.", "error")]
	except KeyError as e:
		initiative = [("No tracker with given identifier.", "error")]

	if assistance:
		await client.send_message(
			msg.channel,
			info.message(assistance)
		)

	if rolls:
		await client.send_message(
			msg.channel,
			dice.message(rolls, msg)
		)
	
	if nomen:
		await client.send_message(
			msg.channel,
			names.message(nomen)
		)
	
	if initiative:
		await client.send_message(
			msg.channel,
			turns.message(initiative)
		)
	
client.run(bot_token)
print('client started')
