import random
from . import heroes
from .cards import cardsForHero, THE_COIN

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
		collection = cardsForHero(hero)
		while len(deck) < cls.MAX_CARDS:
			card = random.choice(collection)
			if deck.count(card) < cls.MAX_UNIQUE_CARDS: # this probably doesnt work right because dicts
				# todo legendary check too
				deck.append(card)
		return Deck(deck)

	def __init__(self, cards):
		self.cards = cards

	def shuffle(self):
		random.shuffle(self.cards)


class Player(object):
	MAX_HAND = 10
	def __init__(self, name, deck):
		self.name = name
		self.deck = deck
		self.hand = []

	def addToHand(self, card):
		if len(self.hand) >= self.MAX_HAND:
			return
		self.hand.append(card)

	def draw(self, count=1):
		while count:
			card = self.deck.cards.pop()
			self.addToHand(card)
			count -= 1


class Game(object):
	def __init__(self, players):
		self.players = players
		self.player1 = self.players[0]
		self.player2 = self.players[1]
		self.turn = 0
		self.playerTurn = None

	def tossCoin(self):
		outcome = random.randint(0, 1)
		# player who wins the outcome is the index
		winner = self.players[outcome]
		# T_T
		loser = [p for p in self.players if p != winner][0]
		return winner, loser

	def start(self):
		for player in self.players:
			player.deck.shuffle()
			player.draw(3)
		winner, loser = self.tossCoin()
		loser.draw()
		# TODO mulligan phase
		loser.addToHand(THE_COIN)
		self.beginTurn(winner)

	def beginTurn(self, player):
		self.turn += 1
		self.playerTurn = player
