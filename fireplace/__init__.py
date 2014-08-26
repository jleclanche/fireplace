import random
from . import heroes
from .cards import Card, cardsForHero, THE_COIN

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
			if deck.count(card) < cls.MAX_UNIQUE_CARDS:
				# todo legendary check too
				deck.append(card)
		return Deck([Card.byId(card) for card in deck])

	def __init__(self, cards):
		self.cards = cards

	def shuffle(self):
		random.shuffle(self.cards)


class Player(object):
	MAX_HAND = 10
	MAX_MANA = 10

	def __init__(self, name, deck):
		self.name = name
		self.deck = deck
		self.hand = []
		self.field = []
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

	@property
	def mana(self):
		return self.manaCrystals - self.usedMana - self.overload + self.additionalCrystals

	def addToHand(self, card):
		if len(self.hand) >= self.MAX_HAND:
			return
		card.owner = self # Cards are not necessarily from the deck
		self.hand.append(card)
		card.status = card.STATUS_HAND
		return card

	def insertToHand(self, card, pos):
		# Same as addToHand but inserts (usually in place of a None)
		# used for mulligan
		card.owner = self
		del self.hand[pos]
		self.hand.insert(card, pos)
		card.status = card.STATUS_HAND
		return card

	def draw(self, count=1, hold=False):
		drawn = []
		while count:
			card = self.deck.cards.pop()
			count -= 1
			if not hold:
				self.addToHand(card)
			drawn.append(card)
		return drawn

	def gainMana(self, amount):
		self.manaCrystals = min(self.MAX_MANA, self.manaCrystals + amount)


class Game(object):
	STATUS_BEGIN = 0
	STATUS_TURN = 1
	STATUS_END_TURN = 2
	STATUS_MULLIGAN = 3
	STATUS_END = 4
	TIMEOUT_TURN = 75
	TIMEOUT_MULLIGAN = 85

	def __init__(self, players):
		self.players = players
		self.turn = 0
		self.playerTurn = None
		self.status = self.STATUS_BEGIN

	def waitForEvent(self, event, timeout):
		# Not implemented
		pass

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
		self.player1, self.player2 = self.tossCoin()
		self.player2.draw()
		self.beginMulligan()

	def onMulliganInput(self, player, cards):
		assert self.status == self.STATUS_MULLIGAN
		assert player.canMulligan
		drawn = player.draw(len(cards), hold=True)
		for i, index in enumerate(cards):
			player.placeCardInDeck(player.cards[card])
			player.insertToHand(drawn[i], index)
		player.canMulligan = False

	def beginMulligan(self):
		self.status = self.STATUS_MULLIGAN
		self.waitForEvent("END_MULLIGAN", timeout=self.TIMEOUT_MULLIGAN)
		self.player2.addToHand(Card.byId(THE_COIN))
		self.beginTurn(self.player1)

	def beginTurn(self, player):
		self.status = self.STATUS_TURN
		self.turn += 1
		self.playerTurn = player
		player.gainMana(1)
		player.usedMana = 0
		player.overload = player.nextOverload
		player.nextOverload = 0
		player.draw()
		self.waitForEvent("END_TURN", timeout=self.TIMEOUT_TURN)

	def endTurn(self):
		self.status = self.STATUS_ENDTURN
		self.playerTurn.additionalCrystals = 0
