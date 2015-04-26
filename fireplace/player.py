import logging
import random
import time
from calendar import timegm
from itertools import chain
from .actions import Play
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
		return [self.hero] + self.field

	@property
	def entities(self):
		ret = []
		for entity in self.field:
			ret += entity.entities
		# Secrets are only active on the opponent's turn
		if not self.currentPlayer:
			for entity in self.secrets:
				ret += entity.entities
		# Note: Board receives TURN_BEGIN before player
		return chain(list(self.hero.entities) if self.hero else [], ret, [self])

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
		"""
		Draws \a count card.
		If \a count is a BaseCard instance, draw that specific card.
		"""
		if isinstance(count, BaseCard):
			card = count
		elif count > 1:
			ret = []
			while count:
				ret.append(self.draw())
				count -= 1
			return ret
		else:
			if not self.deck:
				card = None
			else:
				card = self.deck[-1]

		if len(self.hand) == 10:
			return self.mill()

		self.game.broadcast("DRAW", self, card)
		logging.info("%s draws %r" % (self, card))
		return card

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
		logging.info("%s is now at %i mana crystals" % (self, amount))

	def takeControl(self, minion):
		logging.info("%s takes control of %r" % (self, minion))
		self.opponent.field.remove(minion)
		self.field.append(minion)
		minion.controller = self

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
		logging.debug("%s summons %r" % (self, card))
		card.summon()
		return card

	def play(self, card, target=None, choose=None):
		return self.game.queueActions(self, [Play(card, target, choose)])

	def _play(self, card, target, choose):
		"""
		Plays \a card from the player's hand
		"""
		logging.info("%s plays %r from their hand" % (self, card))
		assert card.controller
		cost = card.cost
		self.game.broadcast("CARD_PLAYED", self, card)
		if card.hasTarget():
			assert target
			card.target = target
		if self.tempMana:
			# The coin, Innervate etc
			cost -= self.tempMana
			self.tempMana = max(0, self.tempMana - card.cost)
		self.usedMana += cost
		self.summon(card)
		# Card must already be on the field for action()
		if choose:
			# Choose One cards replace the action on the played card
			assert choose in card.data.chooseCards
			chosen = self.game.card(choose)
			chosen.controller = self
			logging.info("Choose One from %r: %r", card, chosen)
			card.action = chosen.action
			if chosen.hasTarget():
				chosen.target = target
			chosen.action()
			if chosen.target:
				chosen.target = None
		else:
			card.action()
		if not self.combo:
			self.combo = True
		self.game.broadcast("AFTER_CARD_PLAYED", self, card)
		if card.target:
			card.target = None
		self.lastCardPlayed = card

	##
	# Events

	events = [
		"OWN_ATTACK",
		"TURN_BEGIN", "TURN_END",
		"OWN_DRAW",
		"OWN_DAMAGE", "OWN_HEAL",
		"OWN_CARD_PLAYED", "CARD_PLAYED",
		"AFTER_CARD_PLAYED", "AFTER_OWN_CARD_PLAYED",
		"OWN_MINION_DESTROY",
		"MINION_SUMMON",
	]

	def broadcast(self, event, *args):
		# Broadcast things to the hand if requested
		for entity in self.hand:
			for f in entity._eventListeners.get(event, []):
				if getattr(f, "zone", Zone.PLAY) == Zone.HAND:
					f(*args)
		super().broadcast(event, *args)

	def OWN_ATTACK(self, source, target):
		source.broadcast("SELF_ATTACK", target)

	def TURN_BEGIN(self, player):
		self.cardsDrawnThisTurn = 0
		self.cardsPlayedThisTurn = 0
		self.minionsKilledThisTurn = 0
		self.turnStart = timegm(time.gmtime())
		if player is self:
			self.minionsPlayedThisTurn = 0
			self.combo = False
			self.maxMana += 1
			self.usedMana = self.overloaded
			if self.overloaded:
				self.overloaded = 0
			self.draw()

	def TURN_END(self, *args):
		if self.tempMana:
			self.tempMana = 0

	def OWN_DRAW(self, card):
		if not card:
			self.fatigue()
			return

		if len(self.hand) > self.maxHandSize:
			logging.info("%s overdraws and loses %r!" % (self, card))
			card.destroy()
		else:
			card.zone = Zone.HAND
			self.cardsDrawnThisTurn += 1 # TODO: Is this increased on fatigue/mill?

	def OWN_CARD_PLAYED(self, card):
		if card.overload:
			logging.info("%s is overloaded for %i mana" % (self, self.overloaded))
			self.overloaded += card.overload

	def OWN_DAMAGE(self, source, target, amount):
		target.broadcast("SELF_DAMAGE", source, amount)

	def OWN_HEAL(self, source, target, amount):
		target.broadcast("SELF_HEAL", source, amount)

	def CARD_PLAYED(self, player, card):
		if player is self:
			card.controller.broadcast("OWN_CARD_PLAYED", card)
		card.broadcast("SELF_CARD_PLAYED")

	def AFTER_CARD_PLAYED(self, player, card):
		if player is self:
			card.controller.broadcast("AFTER_OWN_CARD_PLAYED", card)
		card.broadcast("AFTER_SELF_CARD_PLAYED")

	def AFTER_OWN_CARD_PLAYED(self, card):
		self.cardsPlayedThisTurn += 1
		if card.type == CardType.MINION:
			self.minionsPlayedThisTurn += 1

	def OWN_MINION_DESTROY(self, minion):
		self.minionsKilledThisTurn += 1

	def MINION_SUMMON(self, player, minion):
		if player is self:
			minion.controller.broadcast("OWN_MINION_SUMMON", minion)
