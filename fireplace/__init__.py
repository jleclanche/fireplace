import logging
import random
from itertools import chain
from . import heroes
from .cards import Card, cardsForHero, THE_COIN
from .entity import Entity
from .enums import GameTag, Zone
from .exceptions import *
from .player import Player
from .utils import _TAG


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
		self.auras = []

	def __repr__(self):
		return "<%s %s>" % (self.__class__.__name__, self)

	def __str__(self):
		return "%r vs %r" % (self.players[0], self.players[1])

	@property
	def board(self):
		return self.currentPlayer.field + self.currentPlayer.opponent.field

	@property
	def entities(self):
		return self.player1.entities + self.player2.entities

	turn = _TAG(GameTag.TURN, 0)

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
			for card in player.deck:
				card.controller = player
				card.zone = Zone.DECK
			player.summon(player.deck.hero)
			player.deck.shuffle()
			player.draw(3)
		self.player1, self.player2 = self.tossCoin()
		self.player2.draw()
		self.beginMulligan()
		self.player1.setTag(GameTag.FIRST_PLAYER, True)

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
		logging.info("%s gets The Coin (%s)" % (self.player2, THE_COIN))
		self.player2.addToHand(Card(THE_COIN))
		self.broadcast("onTurnBegin", self.player1)

	def broadcast(self, event, *args):
		logging.debug("Broadcasting event %r to %r with arguments %r" % (event, self.entities, args))
		for entity in chain([self], self.players, self.entities, self.auras):
			if entity and hasattr(entity, event):
				getattr(entity, event)(*args)
		if event != "onUpdate":
			self.broadcast("onUpdate")

	def onUpdate(self):
		for card in self.board:
			if card.health == 0:
				card.destroy()

	def onTurnBegin(self, player):
		self.status = self.STATUS_TURN
		self.turn += 1
		logging.info("%s begins turn %i" % (player, self.turn))
		if self.turn == self.MAX_TURNS:
			raise GameOver("It's a draw!")
		if self.currentPlayer:
			self.currentPlayer.currentPlayer = False
		self.currentPlayer = player
		self.currentPlayer.currentPlayer = True

	def endTurn(self):
		logging.info("%s ends turn" % (self.currentPlayer))
		self.broadcast("onTurnEnd", self.currentPlayer)
		self.broadcast("onTurnBegin", self.currentPlayer.opponent)

	def onTurnEnd(self, player):
		self.status = self.STATUS_END_TURN
