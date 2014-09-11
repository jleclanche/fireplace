import logging
from .cards import Card
from .enums import CardType, Zone
from .targeting import *


class Player(object):
	MAX_HAND = 10
	MAX_MANA = 10

	def __init__(self, name, deck):
		self.name = name
		self.deck = deck
		self.deck.hero.owner = self
		self.hand = []
		self.field = []
		self.buffs = []
		self.secrets = []
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
	def mana(self):
		mana = self.availableMana
		# also check for the hero's extra mana
		for slot in self.deck.hero.slots:
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
		assert self.addToHand(card), "Hand is full!"
		return card

	def getTargets(owner, t):
		ret = []
		if t & TARGET_FRIENDLY:
			if t & TARGET_HERO:
				ret.append(owner.hero)
			if t & TARGET_MULTIPLE:
				if t & TARGET_MINION:
					ret += owner.field
		if t & TARGET_ENEMY:
			if t & TARGET_HERO:
				ret.append(owner.opponent.hero)
			if t & TARGET_MULTIPLE:
				if t & TARGET_MINION:
					ret += owner.opponent.field
		return ret

	def addToHand(self, card):
		if len(self.hand) >= self.MAX_HAND:
			return
		card.owner = self # Cards are not necessarily from the deck
		self.hand.append(card)
		card.zone = Zone.HAND
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
		card.zone = Zone.HAND
		return card

	def draw(self, count=1, hold=False):
		drawn = []
		while count:
			count -= 1
			if not self.deck.cards:
				self.fatigue()
				continue
			card = self.deck.cards.pop()
			if len(self.hand) >= self.MAX_HAND:
				logging.info("%s overdraws and loses %r!" % (self, card))
				continue
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
		logging.info("%s gains %i mana crystal (now at %i)" % (self, amount, self.maxMana))

	def loseMana(self, amount):
		self.maxMana = max(0, self.maxMana - amount)
		logging.info("%s loses %i mana crystal (now at %i)" % (self, amount, self.maxMana))

	def summon(self, card):
		"""
		Puts \a card in the PLAY zone
		"""
		if isinstance(card, str):
			card = Card(card)
			card.owner = self
		logging.debug("%s summons %r" % (self, card))
		card.summon()
		return card

	def play(self, card, target=None):
		"""
		Plays \a card from the player's hand
		"""
		logging.info("%s plays %r from their hand" % (self, card))
		assert card.owner
		self.availableMana -= card.cost
		self.hand.remove(card)
		card.zone = Zone.PLAY
		self.summon(card)
		# Card must already be on the field for activate()
		card.activate(target)
