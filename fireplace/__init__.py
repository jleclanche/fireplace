import logging
import random
from . import heroes
from .cards import Card, cardsForHero, THE_COIN
from .exceptions import *


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

	def shuffle(self):
		logging.info("Shuffling %r..." % (self))
		random.shuffle(self.cards)


class Player(object):
	MAX_HAND = 10
	MAX_MANA = 10

	def __init__(self, name, deck):
		self.name = name
		self.deck = deck
		self.deck.hero.owner = self
		self.hero = self.deck.hero
		self.hand = []
		self.field = []
		self.fatigueCounter = 0
		# set to False after the player has finished his mulligan
		self.canMulligan = True
		## Mana
		# total crystals
		self.manaCrystals = 0
		# additional crystals this turn
		self.additionalCrystals = 0
		# mana used this turn
		self.usedMana = 0
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
		return self.manaCrystals - self.usedMana - self.overload + self.additionalCrystals

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
		self.manaCrystals = min(self.MAX_MANA, self.manaCrystals + amount)
		logging.info("%s gains %i mana (now at %i)" % (self, amount, self.manaCrystals))

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


class Game(object):
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
		self.players = players
		for player in players:
			player.game = self
		self.turn = 0
		self.currentPlayer = None
		self.status = self.STATUS_BEGIN

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
		logging.info("%s begins turn %i" % (player, self.turn))
		if self.turn == self.MAX_TURNS:
			raise GameOver("It's a draw!")
		self.currentPlayer = player
		player.gainMana(1)
		player.usedMana = 0
		player.overload = player.nextOverload
		player.nextOverload = 0
		player.draw()
		# remove all summon sickness
		for minion in self.currentPlayer.field:
			minion.summoningSickness = False
		self.waitForEvent("END_TURN", timeout=self.TIMEOUT_TURN)

	def endTurn(self):
		logging.info("%s ends turn" % (self.currentPlayer))
		self.status = self.STATUS_END_TURN
		self.currentPlayer.additionalCrystals = 0
		for minion in self.board:
			if hasattr(minion, "endTurn"):
				minion.endTurn()
		self.beginTurn(self.currentPlayer.opponent)
