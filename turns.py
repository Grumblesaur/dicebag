tracker = { }

class TurnOrderException(Exception):
	pass

def save_config():
	with open('turn.config', 'w') as t:
		t.write(str(tracker))

def load_config():
	global tracker
	try:
		with open('turn.config', 'r') as t:
			tracker = eval(t.read())
	except Exception as e:
		print(e)
		tracker = { }

class turn_order(object):
	def __init__(self):
		""" Creates a turn order object where
			`order` is a list of tuples of (player name, initiative),
			`current` is the current step through the turn order,
			`round` is the number of times the turn order has been iterated, and
			`active` indicates that the turn order is in use
		"""
		self.order = []
		self.new_waiting = []
		self.dead_waiting = []
		self.turns = 0
		self.rounds = 1
		self.active = False
		self.new = False
		self.dead = False
		
	def __len__(self):
		return len(self.order)
	
	def __getitem__(self, index):
		return self.order[index]
		
	def add(self, name, initiative):
		""" Adds an actor to the turn order; actors who join during an active
			turn order are staged to be added at the start of the next round.
			`name` is a string
			`initiative` is an integer
		"""
		if not self.active:
			self.order.append((name, initiative))
		else:
			self.new_waiting.append((name, initiative))
			self.new = True
	
	def remove(self, name):
		if not self.active:
			self.order.remove(name)
		else:
			self.dead_waiting += [
				actor for actor in self.order if actor[0] == name
			]
			self.dead = True
			
	def rotate(self):
		""" Returns the next actor in the turn order. If actors are new_waiting to
			enter an active turn order, they are inserted at the beginning of a
			round.
		"""
		out = self[self.turns % len(self)][0]
		self.turns += 1
		if self.turns % len(self) == 0:
			self.rounds += 1
			if self.dead:
				self.order = list(set(self.order) - set(self.dead_waiting))
				self.dead_waiting = []
				self.dead = False
				self.turns = 0
				self.order = sorted(self.order, key=lambda x: x[1], reverse=True)
			if self.new:
				self.order += self.new_waiting
				self.new_waiting = []
				self.new = False
				self.turns = 0
				self.order = sorted(self.order, key=lambda x: x[1], reverse=True)
		return out
	
	def check(self):
		""" See who's up next without iterating the order."""
		return self[self.turns % len(self)][0]
	
	def view(self):
		""" See the entire turn order and the current round. """
		return (self.rounds, self.order)
		
	def start(self):
		""" Begin using a turn order. """
		self.order = sorted(self.order, key=lambda x: x[1], reverse=True)
		self.active = True
	
	def stop(self):
		""" Stop and reset a turn order. """
		self.active = self.dead = self.new = False
		self.turns = 0
		self.rounds = 1
		self.order += self.new_waiting
		self.order = list(set(self.order) - set(self.dead_waiting))
		self.new_waiting = self.dead_waiting = []
	
	def clear(self):
		""" Empty out an initiative order (must be stopped first). """
		if self.active:
			raise TurnOrderException("You must stop a turn order to clear it")
		self.order = []
		
	
def parse(msg):
	if "!initiative" not in msg:
		return []
	tokens = msg.split("!initiative")[1].split()
	tokens[1] = tokens[1].lower()
	if not tokens:
		return [
			("active turn order trackers:\n\t" + '\n\t'.join(tracker.keys()),
				"none"
			)
		]
	
	if tokens[0] == "create":
		tracker[tokens[1]] = turn_order()
		return [("Created new turn order with name `%s`." % tokens[1], "create")]
	if tokens[0] == "add":
		tracker[tokens[1]].add(tokens[2], int(tokens[3]))
		return [(
			"Added `%s` to the turn order `%s`." % (tokens[2], tokens[1]),
			"add"
		)]
	if tokens[0] == "remove":
		tracker[tokens[1]].remove(tokens[2])
		return [(
			"Removed `%s` from the turn order `%s`." % (tokens[2], tokens[1]),
			"remove"
		)]
	if tokens[0] == "start":
		tracker[tokens[1]].start()
		return [("Started turn order `%s`." % tokens[1], "start")]
	
	if (tokens[0] == "next") and tracker[tokens[1]].active:
		actor = tracker[tokens[1]].rotate()
		genitive = '' if actor.endswith('s') else 's'
		return [("It's %s'%s turn." % (actor, genitive), "next")]
	
	if tokens[0] == "check" and tracker[tokens[1]].active:
		actor = tracker[tokens[1]].check()
		return [("%s is on deck." % actor, "check")]
	
	if tokens[0] == "view":
		current_round, actors = tracker[tokens[1]].view()
		return [
			(
				"It's round %s in turn order `%s`." % (current_round, tokens[1]),
				"view",
			)
		] + actors
	
	if tokens[0] == "stop":
		tracker[tokens[1]].stop()
		return [("Stopped and reset turn order `%s`." % tokens[1], "stop")]
	
	if tokens[0] == "clear":
		try:
			tracker[tokens[1]].clear()
		except TurnOrderException as e:
			pass
		finally:
			return [
				("%s." % e or ("Turn order `%s` cleared" % token[1]), "clear")
		]
	
	if tokens[0] == "delete":
		del tracker[tokens[1]]
		return [("Deleted turn order %s." % tokens[1], "delete")]
	
	return []

def message(pairs):
	out = "%s (%s)" % pairs[0]
	out = out + '\n' + '\n'.join(
		["\t%s (%s)" % p for p in pairs[1:]]
	) if len(pairs) > 1 else out
	return out
