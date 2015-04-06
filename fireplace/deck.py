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

	def __init__(self, cards, hero, name=None):
		super().__init__(cards)
		self.hero = hero
		if name is None:
			name = "Custom %s" % (hero)
		self.name = name
		for card in cards:
			# Don't use .zone directly as it would double-fill the deck
			card.tags[GameTag.ZONE] = Zone.DECK

	def __str__(self):
		return self.name

	def __repr__(self):
		return "<%s (%i cards)>" % (self.hero, len(self))

	def shuffle(self):
		logging.info("Shuffling %r..." % (self))
		random.shuffle(self)
