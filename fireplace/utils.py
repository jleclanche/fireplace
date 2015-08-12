class CardList(list):
	def __contains__(self, x):
		for item in self:
			if x is item:
				return True
		return False

	def __getitem__(self, key):
		ret = super().__getitem__(key)
		if isinstance(key, slice):
			return self.__class__(ret)
		return ret

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

	def exclude(self, *args, **kwargs):
		if args:
			return self.__class__(e for e in self for arg in args if e is not arg)
		else:
			return self.__class__(e for k, v in kwargs.items() for e in self if getattr(e, k) != v)

	def filter(self, **kwargs):
		return self.__class__(e for k, v in kwargs.items() for e in self if getattr(e, k, 0) == v)


def random_draft(hero, exclude=[]):
	"""
	Return a deck of 30 random cards from the \a hero's collection
	"""
	import random
	from . import cards
	from .deck import Deck
	from .enums import CardType, Rarity

	deck = []
	collection = []
	hero = getattr(cards, hero)

	for card in cards.cardlist:
		if card in exclude:
			continue
		cls = getattr(cards, card)
		if not cls.collectible:
			continue
		if cls.type == CardType.HERO:
			# Heroes are collectible...
			continue
		if cls.card_class and cls.card_class != hero.card_class:
			continue
		collection.append(cls)

	while len(deck) < Deck.MAX_CARDS:
		card = random.choice(collection)
		if card.rarity == Rarity.LEGENDARY and card.id in deck:
			continue
		elif deck.count(card.id) < Deck.MAX_UNIQUE_CARDS:
			deck.append(card.id)

	return deck
