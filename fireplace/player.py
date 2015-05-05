import logging
import random
from itertools import chain
from .actions import Draw, Play, Summon
from .card import BaseCard
from .deck import Deck
from .entity import Entity
from .enums import CardType, PowSubType, Zone
from .entity import slotProperty
from .managers import PlayerManager
from .targeting import *
from .utils import CardList


class Player(Entity):
	Manager = PlayerManager
	extraDeathrattles = slotProperty("extraDeathrattles")
	outgoingHealingAdjustment = slotProperty("outgoingHealingAdjustment")
	type = CardType.PLAYER

	def __init__(self, name):
		self.data = None
		super().__init__()
		self.name = name
		self.deck = Deck()
		self.hand = CardList()
		self.field = CardList()
		self.secrets = CardList()
		self.buffs = []
		self.maxHandSize = 10
		self.maxResources = 10
		self.currentPlayer = False
		self.fatigueCounter = 0
		self.hero = None
		self.lastCardPlayed = None
		self.overloaded = 0
		self.maxMana = 0
		self.tempMana = 0
		self.timeout = 75
		self.timesHeroPowerUsedThisGame = 0
		self.weapon = None
		self.zone = Zone.INVALID

	def __str__(self):
		return self.name

	def __repr__(self):
		return "%s(name=%r, hero=%r)" % (self.__class__.__name__, self.name, self.hero)

	@property
	def controller(self):
		return self

	@property
	def slots(self):
		return self.buffs

	@property
	def mana(self):
		mana = max(0, self.maxMana - self.usedMana) + self.tempMana
		return mana

	@property
	def spellpower(self):
		return sum(minion.spellpower for minion in self.field)

	@property
	def characters(self):
		return CardList(chain([self.hero] if self.hero else [], self.field))

	@property
	def entities(self):
		ret = []
		for entity in self.field:
			ret += entity.entities
		# Secrets are only active on the opponent's turn
		if not self.currentPlayer:
			for entity in self.secrets:
				ret += entity.entities
		return CardList(chain(list(self.hero.entities) if self.hero else [], ret, [self]))

	@property
	def liveEntities(self):
		ret = self.field[:]
		if self.weapon:
			ret.append(self.weapon)
		return ret

	@property
	def opponent(self):
		# Hacky.
		return [p for p in self.game.players if p != self][0]

	# for debugging
	def give(self, id):
		card = self.game.card(id)
		logging.debug("Giving %r to %s" % (card, self))
		card.controller = self
		card.zone = Zone.HAND
		return card

	def getById(self, id):
		"Helper to get a card from the hand by its id"
		for card in self.hand:
			if card.id == id:
				return card
		raise ValueError

	def prepareDeck(self, cards, hero):
		self.originalDeck = Deck.fromList(cards)
		self.originalDeck.hero = hero

	def discardHand(self):
		logging.info("%r discards his entire hand!" % (self))
		# iterate the list in reverse so we don't skip over cards in the process
		# yes it's stupid.
		for card in self.hand[::-1]:
			card.discard()

	def draw(self, count=1):
		ret = self.game.queueActions(self, [Draw(self) * count])[0]
		if count == 1:
			return ret[0]
		return ret

	def mill(self, count=1):
		if count == 1:
			if not self.deck:
				return
			else:
				card = self.deck[-1]
			logging.info("%s mills %r" % (self, card))
			card.destroy()
			return card
		else:
			ret = []
			while count:
				ret.append(self.mill())
				count -= 1
			return ret

	def fatigue(self):
		self.fatigueCounter += 1
		logging.info("%s takes %i fatigue damage" % (self, self.fatigueCounter))
		self.hero.hit(self.hero, self.fatigueCounter)

	@property
	def maxMana(self):
		return self._maxMana

	@maxMana.setter
	def maxMana(self, amount):
		self._maxMana = min(self.maxResources, max(0, amount))
		logging.info("%s is now at %i mana crystals", self, self._maxMana)

	def takeControl(self, card):
		logging.info("%s takes control of %r", self, card)
		zone = card.zone
		card.zone = Zone.SETASIDE
		card.controller = self
		card.zone = zone

	def shuffleDeck(self):
		logging.info("%r shuffles their deck", self)
		random.shuffle(self.deck)

	def summon(self, card):
		"""
		Puts \a card in the PLAY zone
		"""
		if isinstance(card, str):
			card = self.game.card(card)
			card.controller = self
		self.game.queueActions(self, [Summon(self, card)])
		return card

	def play(self, card, target=None, choose=None):
		return self.game.queueActions(self, [Play(card, target, choose)])

	def _play(self, card):
		"""
		Plays \a card from the player's hand
		"""
		logging.info("%s plays %r from their hand" % (self, card))
		assert card.controller
		cost = card.cost
		if self.tempMana:
			# The coin, Innervate etc
			cost -= self.tempMana
			self.tempMana = max(0, self.tempMana - card.cost)
		self.usedMana += cost
		if card.overload:
			logging.info("%s overloads for %i mana", self, card.overload)
			self.overloaded += card.overload
		self.lastCardPlayed = card
		self.summon(card)
		self.combo = True
		self.cardsPlayedThisTurn += 1
		if card.type == CardType.MINION:
			self.minionsPlayedThisTurn += 1
