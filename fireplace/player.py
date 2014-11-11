import logging
from .cards import Card
from .entity import Entity
from .enums import CardType, GameTag, Zone
from .targeting import *


class CardList(list):
	def __contains__(self, x):
		for item in self:
			if x is item:
				return True
		return False

	def contains(self, x):
		"True if list contains any instance of x"
		for item in self:
			if x == item:
				return True
		return False

	def index(self, x):
		for i, item in enumerate(self):
			if x is item:
				return i
		raise ValueError


class Player(Entity):
	MAX_HAND = 10
	MAX_MANA = 10

	def __init__(self, name, deck):
		super().__init__()
		self.name = name
		self.deck = deck
		self.deck.hero.controller = self
		self.hand = CardList()
		self.field = CardList()
		self.buffs = CardList()
		self.secrets = CardList()
		self.fatigueCounter = 0
		# set to False after the player has finished his mulligan
		self.canMulligan = True
		## Mana
		# available mana (resets every turn)
		self.availableMana = 0
		# overloaded mana
		self.overload = 0

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

	def getTargets(self, t):
		ret = []
		if t & TARGET_FRIENDLY:
			if t & TARGET_HERO:
				ret.append(self.hero)
			if t & TARGET_MULTIPLE:
				if t & TARGET_MINION:
					ret += self.field
		if t & TARGET_ENEMY:
			if t & TARGET_HERO:
				ret.append(self.opponent.hero)
			if t & TARGET_MULTIPLE:
				if t & TARGET_MINION:
					ret += self.opponent.field
		return ret

	def addToHand(self, card):
		if len(self.hand) >= self.MAX_HAND:
			return
		card.controller = self # Cards are not necessarily from the deck
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
		card.controller = self
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
		self.hero.hit(self.hero, self.fatigueCounter)

	@property
	def nextOverload(self):
		return self.tags.get(GameTag.RECALL_OWED, 0)

	@nextOverload.setter
	def nextOverload(self, amount):
		self.tags[GameTag.RECALL_OWED] = amount

	@property
	def maxMana(self):
		return self.tags.get(GameTag.RESOURCES, 0)

	@maxMana.setter
	def maxMana(self, amount):
		self.tags[GameTag.RESOURCES] = min(self.MAX_MANA, max(0, amount))
		logging.info("%s is now at %i mana crystals" % (self, amount))

	def takeControl(self, minion):
		logging.info("%s takes control of %r" % (self, minion))
		self.opponent.field.remove(minion)
		self.field.append(minion)
		minion.owner = self

	def summon(self, card, target=None):
		"""
		Puts \a card in the PLAY zone
		"""
		if isinstance(card, str):
			card = Card(card)
			card.controller = self
		logging.debug("%s summons %r" % (self, card))
		card.zone = Zone.PLAY
		if target:
			card.summon(target)
		else:
			card.summon()
		return card

	def play(self, card, target=None):
		"""
		Plays \a card from the player's hand
		"""
		logging.info("%s plays %r from their hand" % (self, card))
		assert card.controller
		self.availableMana -= card.cost
		if card.data.overload:
			self.nextOverload += card.data.overload
			logging.info("%s is overloaded for %i mana" % (self, self.nextOverload))
		self.hand.remove(card)
		self.summon(card)
		# Card must already be on the field for action()
		if self.tags[GameTag.COMBO_ACTIVE]:
			card.action(target, combo=self.tags[GameTag.NUM_CARDS_PLAYED_THIS_TURN])
		else:
			card.action(target, combo=None)
			self.setTag(GameTag.COMBO_ACTIVE, True)
		self.tags[GameTag.NUM_CARDS_PLAYED_THIS_TURN] += 1
