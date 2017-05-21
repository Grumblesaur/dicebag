import turns

print(turns.turn_message(turns.parse("!initiative create evan")))
print(turns.turn_message(turns.parse("!initiative add evan Falwyn 12")))
print(turns.turn_message(turns.parse("!initiative add evan Heniele 15")))
print(turns.turn_message(turns.parse("!initiative add evan Caranya 19")))
print(turns.turn_message(turns.parse("!initiative add evan Vedam 8")))
print(turns.turn_message(turns.parse("!initiative start evan")))
for x in range(6):
	print(turns.turn_message(turns.parse("!initiative next evan")))
print(turns.turn_message(turns.parse("!initiative check evan")))
print(turns.turn_message(turns.parse("!initiative check evan")))
print(turns.turn_message(turns.parse("!initiative next evan")))
print(turns.turn_message(turns.parse("!initiative check evan")))
print(turns.turn_message(turns.parse("!initiative next evan")))
print(turns.turn_message(turns.parse("!initiative view evan")))
print(turns.turn_message(turns.parse("!initiative next evan")))

print(turns.turn_message(turns.parse("!initiative view evan")))

print(turns.turn_message(turns.parse("!initiative create james")))
print(turns.turn_message(turns.parse("!initiative add james Calvus 20")))
print(turns.turn_message(turns.parse("!initiative add james Darcielle 6")))
print(turns.turn_message(turns.parse("!initiative view james")))


