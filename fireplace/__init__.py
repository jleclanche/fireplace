import logging
import random
from itertools import chain
from . import heroes
from .cards import Card, cardsForHero, THE_COIN
from .entity import Entity
from .enums import GameTag
from .exceptions import *
from .player import Player


class Deck(object):
	MAX_CARDS = 30
	MAX_UNIQUE_CARDS = 2
	MAX_UNIQUE_LEGENDARIES = 1

	@classmethod
	def randomDraft(cls, hero):
		"""
		Return a deck of 30 random cards from the \a hero's collection
		"""
		deck = []
		logging.info("Drafting a random deck for %r" % (hero))
		collection = cardsForHero(hero)
		heroCard = Card(hero)
		while len(deck) < cls.MAX_CARDS:
			card = random.choice(collection)
			if deck.count(card) < cls.MAX_UNIQUE_CARDS:
				# todo legendary check too
				deck.append(card)
		return Deck([Card(card) for card in deck], hero=heroCard)

	def __init__(self, cards, hero, name=None):
		self.cards = cards
		self.hero = hero
		if name is None:
			name = "Custom %s" % (hero)
		self.name = name

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s (%i cards)>" % (self.hero, len(self.cards))

	def __iter__(self):
		return self.cards.__iter__()

	def shuffle(self):
		logging.info("Shuffling %r..." % (self))
		random.shuffle(self.cards)


class Game(Entity):
	STATUS_BEGIN = 0
	STATUS_TURN = 1
	STATUS_END_TURN = 2
	STATUS_MULLIGAN = 3
	STATUS_END = 4
	TIMEOUT_TURN = 75
	TIMEOUT_MULLIGAN = 85
	MAX_MINIONS_ON_FIELD = 8
	# Game draws after 50 full turns (100 game turns)
	MAX_TURNS = 100

	def __init__(self, players):
		super().__init__()
		self.players = players
		for player in players:
			player.game = self
		self.turn = 0
		self.currentPlayer = None
		self.status = self.STATUS_BEGIN
		# Maybe auras should be elsewhere but they need to be somewhere global
		self.auras = []

	def waitForEvent(self, event, timeout):
		# Not implemented
		pass

	def __repr__(self):
		return "<%s %s>" % (self.__class__.__name__, self)

	def __str__(self):
		return "%r vs %r" % (self.players[0], self.players[1])

	@property
	def board(self):
		return self.currentPlayer.field + self.currentPlayer.opponent.field

	def tossCoin(self):
		outcome = random.randint(0, 1)
		# player who wins the outcome is the index
		winner = self.players[outcome]
		loser = winner.opponent
		logging.info("Tossing the coin... %s wins!" % (winner))
		return winner, loser

	def start(self):
		logging.info("Starting game: %r" % (self))
		for player in self.players:
			player.summon(player.deck.hero)
			player.deck.shuffle()
			player.draw(3)
		self.player1, self.player2 = self.tossCoin()
		self.player2.draw()
		self.beginMulligan()

	def onMulliganInput(self, player, cards):
		assert self.status == self.STATUS_MULLIGAN
		assert player.canMulligan
		logging.info("Received mulligan input from %r: %r" % (player, cards))
		drawn = player.draw(len(cards), hold=True)
		for i, index in enumerate(cards):
			player.placeCardInDeck(player.cards[card])
			player.insertToHand(drawn[i], index)
		player.canMulligan = False

	def beginMulligan(self):
		logging.info("Entering mulligan phase")
		self.status = self.STATUS_MULLIGAN
		self.waitForEvent("END_MULLIGAN", timeout=self.TIMEOUT_MULLIGAN)
		logging.info("%s gets The Coin (%s)" % (self.player2, THE_COIN))
		self.player2.addToHand(Card(THE_COIN))
		self.beginTurn(self.player1)

	def beginTurn(self, player):
		self.status = self.STATUS_TURN
		self.turn += 1
		self.playedThisTurn = []
		logging.info("%s begins turn %i" % (player, self.turn))
		if self.turn == self.MAX_TURNS:
			raise GameOver("It's a draw!")
		self.currentPlayer = player
		player.gainMana(1)
		player.availableMana = player.maxMana
		player.overload = player.nextOverload
		player.nextOverload = 0
		player.draw()
		# remove all summon sickness
		for minion in self.currentPlayer.field:
			minion.summoningSickness = False
			minion.setTag(GameTag.NUM_ATTACKS_THIS_TURN, 0)
		player.hero.setTag(GameTag.NUM_ATTACKS_THIS_TURN, 0)
		self.waitForEvent("END_TURN", timeout=self.TIMEOUT_TURN)

	def endTurn(self):
		logging.info("%s ends turn" % (self.currentPlayer))
		self.status = self.STATUS_END_TURN
		for entity in chain(self.board, self.currentPlayer.hero.slots):
			if hasattr(entity.data, "endTurn"):
				logging.info("Processing end of turn for %r" % (entity))
				entity.data.__class__.endTurn(entity)
			if entity.data.oneTurnEffect:
				logging.info("Ending One-Turn effect: %r" % (entity))
				entity.destroy()
			for slot in entity.slots:
				if hasattr(slot.data, "endTurn"):
					logging.info("Processing end of turn for slot %r of %r" % (slot, entity))
					slot.data.__class__.endTurn(slot)
		for minion in self.currentPlayer.field:
			if minion.frozen:
				minion.unfreeze()
		self.beginTurn(self.currentPlayer.opponent)
