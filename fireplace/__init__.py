import logging
import random
from itertools import chain
from . import heroes
from .cards import Card, cardsForHero, THE_COIN
from .entity import Entity
from .enums import CardType, GameTag, Zone
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
		self.auras = []

	def __repr__(self):
		return "<%s %s>" % (self.__class__.__name__, self)

	def __str__(self):
		if not hasattr(self, "players"):
			return "Uninitialized Game"
		return "%r vs %r" % (self.players[0], self.players[1])

	@property
	def board(self):
		return self.currentPlayer.field + self.currentPlayer.opponent.field

	@property
	def entities(self):
		return chain([self], self.auras, self.player1.entities, self.player2.entities)

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
		assert player.canMulligan
		logging.info("Received mulligan input from %r: %r" % (player, cards))
		drawn = player.draw(len(cards), hold=True)
		for i, index in enumerate(cards):
			player.placeCardInDeck(player.cards[card])
			player.insertToHand(drawn[i], index)
		player.canMulligan = False

	def beginMulligan(self):
		logging.info("Entering mulligan phase")
		logging.info("%s gets The Coin (%s)" % (self.player2, THE_COIN))
		self.player2.addToHand(Card(THE_COIN))
		self.broadcast("TURN_BEGIN", self.player1)

	def endTurn(self):
		logging.info("%s ends turn" % (self.currentPlayer))
		self.broadcast("TURN_END", self.currentPlayer)
		self.broadcast("TURN_BEGIN", self.currentPlayer.opponent)

	##
	# Events

	events = ["UPDATE", "TURN_BEGIN", "TURN_END", "DAMAGE", "HEAL", "CARD_DESTROYED", "MINION_DESTROYED"]

	def UPDATE(self):
		for card in self.board:
			if card.health == 0:
				card.destroy()

	def TURN_BEGIN(self, player):
		self.turn += 1
		logging.info("%s begins turn %i" % (player, self.turn))
		if self.turn == self.MAX_TURNS:
			raise GameOver("It's a draw!")
		if self.currentPlayer:
			self.currentPlayer.currentPlayer = False
		self.currentPlayer = player
		self.currentPlayer.currentPlayer = True
		player.broadcast("OWN_TURN_BEGIN")

	def TURN_END(self, player):
		player.broadcast("OWN_TURN_END")

	def DAMAGE(self, source, target, amount):
		target.controller.broadcast("OWN_DAMAGE", source, target, amount)

	def HEAL(self, source, target, amount):
		source.controller.broadcast("OWN_HEAL", source, target, amount)

	def MINION_DESTROYED(self, minion):
		minion.controller.broadcast("OWN_MINION_DESTROYED", minion)

	def CARD_DESTROYED(self, card):
		card.controller.broadcast("OWN_CARD_DESTROYED", card)
		if card.type == CardType.MINION:
			self.broadcast("MINION_DESTROYED", card)
