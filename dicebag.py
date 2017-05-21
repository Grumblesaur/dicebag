import sys
import asyncio
import discord
from auth import *
import dice
import turns
import info

client = discord.Client(max_messages=128)

print("Bot connected.")

@client.event
async def on_message(msg):
	assistance = info.parse(msg.content)
	rolls = dice.parse(msg.content)
	try:
		initiative = turns.parse(msg.content)
	except IndexError as e:
		initiative = [("Invalid keyword or number of arguments.", "error")]
	except KeyError as e:
		initiative = [("No tracker with given identifier.", "error")]
	if assistance:
		await client.send_message(
			msg.channel,
			info.help_message(assistance)
		)
	if rolls:
		await client.send_message(
			msg.channel,
			dice.dice_message(rolls, msg)
		)
	if initiative:
		await client send_message(
			msg.channel,
			turns.turn_message(initiative)
		)
	
client.run(bot_token)
print('client started')
