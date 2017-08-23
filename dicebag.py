import sys
import asyncio
import discord
from auth import *
import dice
import turns
import info
import names
import char
import gen

client = discord.Client(max_messages=128)

print("Bot connected.")

char.load_config()
turns.load_config()

@client.event
async def on_message(msg):
	assistance = info.parse(msg.content)
	rolls = dice.parse(msg.content)
	nomen = names.parse(msg.content)
	stats = char.parse(msg.content)
	new_character = gen.parse(msg.content)
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
	
	if stats:
		await client.send_message(
			msg.channel,
			char.message(stats)
		)
	
	if new_character:
		await client.send_messaage(
			msg.channel,
			gen.message(new_character)
		)
	
	if "!dicebag save" in msg.content:
		char.save_config()
		turns.save_config()
		await client.send_message(
			msg.channel,
			"Configuration saved."
		)	

for attempt in range(100):
	try:	
		client.run(bot_token)
	except ConnectionResetError as e:
		print(e)
	else:
		print('client started')
else:
	print("unrecoverable")

client.run(bot_token)
print('client started')
