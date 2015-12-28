import random
from hearthstone.enums import CardType, Race, Rarity
from .lazynum import LazyValue


class RandomCardPicker(LazyValue):
	"""
	Store filters and generate a random card matching the filters on pick()
	"""
	def __init__(self, *args, **filters):
		self.args = args
		self.filters = filters
		self._cards = None
		self.lazy_filters = False
		for v in filters.values():
			if isinstance(v, LazyValue):
				self.lazy_filters = True
				break

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.filters)

	@property
	def cards(self):
		if self._cards is None:
			self._cards = self._filter_cards(self.filters)
		return self._cards

	def _filter_cards(self, filters):
		from .. import cards
		return cards.filter(**filters)

	def get_cards(self, source):
		filters = self.filters.copy()
		# Iterate through the filters, evaluating the LazyValues as we go
		for k, v in filters.items():
			if isinstance(v, LazyValue):
				filters[k] = v.evaluate(source)
		return self._filter_cards(filters)

	def evaluate(self, source, count=1) -> str:
		if self.lazy_filters:
			# If the card has lazy filters, we need to evaluate them
			cards = self.get_cards(source)
		else:
			cards = self.cards
		ret = random.sample(cards, count)
		return [source.controller.card(card, source=source) for card in ret]


RandomCard = lambda *a, **kw: RandomCardPicker(*a, **kw)
RandomCollectible = lambda *a, **kw: RandomCardPicker(*a, collectible=True, **kw)
RandomMinion = lambda *a, **kw: RandomCollectible(*a, type=CardType.MINION, **kw)
RandomBeast = lambda *a, **kw: RandomMinion(*a, race=Race.BEAST)
RandomMech = lambda *a, **kw: RandomMinion(*a, race=Race.MECHANICAL)
RandomMurloc = lambda *a, **kw: RandomMinion(*a, race=Race.MURLOC)
RandomSpell = lambda *a, **kw: RandomCollectible(*a, type=CardType.SPELL, **kw)
RandomTotem = lambda *a, **kw: RandomCardPicker(*a, race=Race.TOTEM)
RandomWeapon = lambda *a, **kw: RandomCollectible(*a, type=CardType.WEAPON, **kw)
RandomLegendaryMinion = lambda *a, **kw: RandomMinion(*a, rarity=Rarity.LEGENDARY, **kw)
RandomSparePart = lambda: RandomCardPicker(spare_part=True)


class RandomEntourage(RandomCardPicker):
	def evaluate(self, source, **kwargs):
		self._cards = source.entourage
		return super().evaluate(source, **kwargs)


class RandomID(RandomCardPicker):
	def evaluate(self, source, **kwargs):
		self._cards = self.args
		return super().evaluate(source, **kwargs)
