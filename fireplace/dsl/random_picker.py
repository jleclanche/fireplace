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
		self.count = 1
		self._cards = None
		self.lazy_filters = False
		for v in filters.values():
			if isinstance(v, LazyValue):
				self.lazy_filters = True
				break

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.filters)

	def __mul__(self, other):
		ret = self.__class__(*self.args, **self.filters)
		ret.count = other
		return ret

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

	def evaluate(self, source) -> str:
		if self.lazy_filters:
			# If the card has lazy filters, we need to evaluate them
			cards = self.get_cards(source)
		else:
			cards = self.cards
		ret = random.sample(cards, self.count)
		return [source.controller.card(card, source=source) for card in ret]


RandomCard = lambda **kw: RandomCardPicker(**kw)
RandomCollectible = lambda **kw: RandomCardPicker(collectible=True, **kw)
RandomMinion = lambda **kw: RandomCollectible(type=CardType.MINION, **kw)
RandomBeast = lambda **kw: RandomMinion(race=Race.BEAST)
RandomMech = lambda **kw: RandomMinion(race=Race.MECHANICAL)
RandomMurloc = lambda **kw: RandomMinion(race=Race.MURLOC)
RandomSpell = lambda **kw: RandomCollectible(type=CardType.SPELL, **kw)
RandomTotem = lambda **kw: RandomCardPicker(race=Race.TOTEM)
RandomWeapon = lambda **kw: RandomCollectible(type=CardType.WEAPON, **kw)
RandomLegendaryMinion = lambda **kw: RandomMinion(rarity=Rarity.LEGENDARY, **kw)
RandomSparePart = lambda: RandomCardPicker(spare_part=True)


class RandomEntourage(RandomCardPicker):
	def evaluate(self, source, **kwargs):
		self._cards = source.entourage
		return super().evaluate(source, **kwargs)


class RandomID(RandomCardPicker):
	def evaluate(self, source, **kwargs):
		self._cards = self.args
		return super().evaluate(source, **kwargs)
