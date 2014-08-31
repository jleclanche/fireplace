import logging
from .cards import Card
from .entity import Entity


class Player(Entity):
	MAX_HAND = 10
	MAX_MANA = 10

	def __init__(self, name, deck):
		self.name = name
		self.deck = deck
		self.deck.hero.owner = self
		self.hand = []
		self.field = []
		self.buffs = []
		self.fatigueCounter = 0
		# set to False after the player has finished his mulligan
		self.canMulligan = True
		## Mana
		# total mana
		self.maxMana = 0
		# available mana (resets every turn)
		self.availableMana = 0
		# overloaded mana
		self.overload = 0
		# mana overload next turn
		self.nextOverload = 0

	def __str__(self):
		return self.name

	def __repr__(self):
		return "%s(name=%r, deck=%r)" % (self.__class__.__name__, self.name, self.deck)

	@property
	def slots(self):
		return self.buffs

	@property
	def mana(self):
		mana = self.availableMana
		for slot in self.slots:
			mana += slot.getProperty("mana")
		return mana - self.overload

	@property
	def opponent(self):
		# Hacky.
		return [p for p in self.game.players if p != self][0]

	# for debugging
	def give(self, id):
		card = Card(id)
		logging.debug("Giving %r to %s" % (card, self))
		self.addToHand(card)
		return card

	def addToHand(self, card):
		if len(self.hand) >= self.MAX_HAND:
			return
		card.owner = self # Cards are not necessarily from the deck
		self.hand.append(card)
		card.status = card.STATUS_HAND
		return card

	def getById(self, id):
		"Helper to get a card from the hand by its id"
		for card in self.hand:
			if card.id == id:
				return card
		raise ValueError

	def insertToHand(self, card, pos):
		# Same as addToHand but inserts (usually in place of a None)
		# used for mulligan
		logging.debug("%s: Inserting %r to hand" % (self, card))
		card.owner = self
		del self.hand[pos]
		self.hand.insert(card, pos)
		card.status = card.STATUS_HAND
		return card

	def draw(self, count=1, hold=False):
		drawn = []
		while count:
			count -= 1
			if not self.deck.cards:
				self.fatigue()
				continue
			card = self.deck.cards.pop()
			if not hold:
				self.addToHand(card)
			drawn.append(card)
		logging.info("%s draws: %r" % (self, drawn))
		return drawn

	def fatigue(self):
		self.fatigueCounter += 1
		logging.info("%s takes %i fatigue damage" % (self, self.fatigueCounter))
		self.hero.damage(self.fatigueCounter)

	def gainMana(self, amount):
		self.maxMana = min(self.MAX_MANA, self.maxMana + amount)
		logging.info("%s gains %i mana (now at %i)" % (self, amount, self.maxMana))

	def summon(self, minion):
		logging.info("Summoning %r" % (minion))
		if isinstance(minion, str):
			minion = Card(minion)
		assert minion.type == minion.TYPE_MINION
		# TODO index
		if len(self.field) >= self.game.MAX_MINIONS_ON_FIELD:
			return
		self.field.append(minion)
		return minion
