import sys
import asyncio
import discord
from random import randrange
from auth import *

class DiceParserException(Exception):
	pass

client = discord.Client(max_messages=128)

print("Bot connected.")

def roll(die):
	try:
		dice, sides = [int(x) for x in die.split('d')]
	except (ValueError, TypeError) as e:
		print(e)
		raise DiceParserException(die)
	return sum([randrange(sides) + 1 for x in range(dice)])
	
def parse(msg):
	tokens = msg.casefold().split()
	rolls = []
	for i in range(len(tokens) - 1):
		if tokens[i] == '!roll':
			try:
				rolls.append((roll(tokens[i+1]), tokens[i+1]))
			except DiceParserException as e:
				print('bad roll:', e)
				continue
	return rolls

@client.event
async def on_message(msg):
	print('on message:', msg.content)
	rolls = parse(msg.content)
	if rolls:
		try:
			username = msg.author.nick
		except AttributeError as e:
			print(e)
			username = msg.author.name
		out = 'User %s rolled:\n' % username
		out += '\n'.join(['%s (%s)' % roll for roll in rolls])
		await client.send_message(msg.channel, out)

client.run(bot_token)	
print('client started')
