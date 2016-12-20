import sys
import asyncio
import discord
from auth import *
import dice

client = discord.Client(max_messages=128)

print("Bot connected.")

@client.event
async def on_message(msg):
	rolls = dice.parse_with_math(msg.content)
	if rolls:
		await client.send_message(
			msg.channel,
			dice.dice_message(rolls, msg)
		)

client.run(bot_token)
print('client started')
