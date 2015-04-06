import logging
import random
from .card import Card
from .enums import GameTag, Zone
from .utils import CardList


class Deck(CardList):
	MAX_CARDS = 30
	MAX_UNIQUE_CARDS = 2
	MAX_UNIQUE_LEGENDARIES = 1

	@classmethod
	def fromList(cls, cards, hero):
		return cls([Card(card) for card in cards], Card(hero))

	def __init__(self, cards, hero):
		super().__init__(cards)
		self.hero = hero
		for card in cards:
			# Don't use .zone directly as it would double-fill the deck
			card.tags[GameTag.ZONE] = Zone.DECK

	def __repr__(self):
		return "<Deck(hero=%r, count=%i)>" % (self.hero, len(self))

	def shuffle(self):
		logging.info("Shuffling %r..." % (self))
		random.shuffle(self)
