class CardList(list):
	def __contains__(self, x):
		for item in self:
			if x is item:
				return True
		return False

	def contains(self, x):
		"True if list contains any instance of x"
		for item in self:
			if x == item:
				return True
		return False

	def index(self, x):
		for i, item in enumerate(self):
			if x is item:
				return i
		raise ValueError

	def remove(self, x):
		for i, item in enumerate(self):
			if x is item:
				del self[i]
				return
		raise ValueError

	def filter(self, **kwargs):
		return [e for k, v in kwargs.items() for e in self if getattr(e, k) == v]


def randomDraft(hero, exclude=[]):
	"""
	Return a deck of 30 random cards from the \a hero's collection
	"""
	import random
	from . import cards
	from .deck import Deck
	from .card import Card
	from .enums import CardType, GameTag

	deck = []
	collection = []
	hero = Card(hero)

	for card in cards.cardlist:
		if card in exclude:
			continue
		cls = getattr(cards, card)
		if not cls.tags.get(GameTag.Collectible):
			continue
		if cls.tags[GameTag.CARDTYPE] == CardType.HERO:
			# Heroes are collectible...
			continue
		if cls.tags.get(GameTag.CLASS, hero.tags[GameTag.CLASS]) != hero.tags[GameTag.CLASS]:
			continue
		collection.append(cls)

	while len(deck) < Deck.MAX_CARDS:
		card = random.choice(collection)
		if card.tags.get(GameTag.RARITY) == 5 and deck.count(card.id):
			continue
		if deck.count(card.id) < Deck.MAX_UNIQUE_CARDS:
			deck.append(card.id)

	return deck
