import random
from copy import copy
from hearthstone.enums import CardType, Race, Rarity
from typing import List, Optional
from .lazynum import LazyValue
from .selector import Selector


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

	def __mul__(self, other) -> "RandomCardPicker":
		ret = copy(self)
		ret.count = other
		return ret

	@property
	def cards(self):
		if self._cards is None:
			self._cards = self._filter_cards(self.filters)
		return self._cards

	def _filter_cards(self, filters) -> List[str]:
		from .. import cards
		return cards.filter(**filters)

	def get_cards(self, source)  -> List[str]:
		filters = self.filters.copy()
		# Iterate through the filters, evaluating the LazyValues as we go
		for k, v in filters.items():
			if isinstance(v, LazyValue):
				filters[k] = v.evaluate(source)
		return self._filter_cards(filters)

	# TODO(smallnamespace): Fix error importing .card.Card
	def evaluate(self, source) -> List["Card"]:
		if self.lazy_filters:
			# If the card has lazy filters, we need to evaluate them
			cards = self.get_cards(source)
		else:
			cards = self.cards
		ret = random.sample(cards, self.count)
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
	def __init__(self, *args, exclude: Optional[Selector]=None, **filters):
		self.exclude = exclude
		super().__init__(*args, **filters)

	def evaluate(self, source, **kwargs):
		card_ids = source.entourage
		if self.exclude:
			excluded = set(entity.id for entity in self.exclude.eval(source.game, source))
			card_ids = [card_id for card_id in card_ids if card_id not in excluded]

		self._cards = card_ids
		return super().evaluate(source, **kwargs)


class RandomID(RandomCardPicker):
	def evaluate(self, source, **kwargs):
		self._cards = self.args
		return super().evaluate(source, **kwargs)
