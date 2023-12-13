import random
from copy import copy, deepcopy

from hearthstone.enums import CardType, Race, Rarity

from .lazynum import LazyValue
from .selector import Selector


class RandomCardPicker(LazyValue):
	"""
	Store filters and generate a random card matching the filters on pick()
	Constructor takes a single global set of filters, default weighting of 1
	Additional weighted filter sets can be added with add(),
	these will be merged with the global filters
	"""
	def __init__(self, **filters):
		self.weights = []
		self.weightedfilters = []
		self.filters = filters
		self.count = 1

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.filters)

	def clone(self, memo):
		# deepcopy functionality is here because parent __deepcopy__ is
		# difficult to call from subclasses
		ret = copy(self)
		ret.weights = list(self.weights)
		ret.filters = deepcopy(self.filters, memo)
		ret.weightedfilters = deepcopy(self.weightedfilters, memo)
		ret.count = self.count

		return ret

	def __deepcopy__(self, memo):
		return self.clone(memo)

	# select number of cards to fetch
	def __mul__(self, other):
		ret = deepcopy(self)
		ret.count = other
		return ret

	# add a filter set
	def copy_with_weighting(self, weight, **filters):
		ret = deepcopy(self)
		ret.weights.append(weight)
		ret.weightedfilters.append(filters)
		return ret

	def find_cards(self, source, **filters):
		"""
		Generate a card pool with all cards matching specified filters
		"""
		if not filters:
			new_filters = self.filters.copy()
		else:
			new_filters = filters.copy()

		if source.game.is_standard and "is_standard" not in new_filters:
			new_filters["is_standard"] = True

		for k, v in new_filters.items():
			if isinstance(v, LazyValue):
				new_filters[k] = v.evaluate(source)
			elif isinstance(v, Selector):
				new_filters[k] = v.eval(source.game, source)

		from .. import cards
		return cards.filter(**new_filters)

	def evaluate(self, source, cards=None) -> str:
		"""
		This picks from a single combined card pool without replacement,
		weighting each filtered set of cards against the total
		"""
		from ..utils import weighted_card_choice

		if cards:
			# Use specific card list if given
			self.weights = [1]
			if "exclude" in self.filters:
				exclude = self.filters["exclude"]
				if isinstance(exclude, LazyValue):
					exclude = exclude.evaluate(source)
				elif isinstance(exclude, Selector):
					exclude = exclude.eval(source.game, source)
				exclude = [card.id for card in exclude]
				cards = [card for card in cards if card not in exclude]
			card_sets = [list(cards)]
		elif not self.weightedfilters:
			# Use global filters if no weighted filter sets given
			self.weights = [1]
			card_sets = [self.find_cards(source)]
		else:
			# Otherwise find cards for each set of filters
			# add the global filters to each set of filters
			wf = [{**x, **self.filters} for x in self.weightedfilters]
			card_sets = [self.find_cards(source, **x) for x in wf]

		# get weighted sample of card pools
		return weighted_card_choice(source, self.weights, card_sets, self.count)


RandomCard = lambda **kw: RandomCardPicker(**kw)
RandomCollectible = lambda **kw: RandomCardPicker(collectible=True, **kw)
RandomMinion = lambda **kw: RandomCollectible(type=CardType.MINION, **kw)
RandomBeast = lambda **kw: RandomMinion(race=Race.BEAST, **kw)
RandomDemon = lambda **kw: RandomMinion(race=Race.DEMON, **kw)
RandomDragon = lambda **kw: RandomMinion(race=Race.DRAGON, **kw)
RandomMech = lambda **kw: RandomMinion(race=Race.MECHANICAL, **kw)
RandomMurloc = lambda **kw: RandomMinion(race=Race.MURLOC, **kw)
RandomSpell = lambda **kw: RandomCollectible(type=CardType.SPELL, **kw)
RandomTotem = lambda **kw: RandomCardPicker(race=Race.TOTEM, **kw)
RandomElemental = lambda **kw: RandomMinion(race=Race.ELEMENTAL, **kw)
RandomWeapon = lambda **kw: RandomCollectible(type=CardType.WEAPON, **kw)
RandomLegendaryMinion = lambda **kw: RandomMinion(rarity=Rarity.LEGENDARY, **kw)
RandomSparePart = lambda: RandomCardPicker(spare_part=True)


class RandomEntourage(RandomCardPicker):
	def evaluate(self, source):
		return super().evaluate(source, source.entourage)


class RandomID(RandomCardPicker):
	def __init__(self, *args, **kw):
		super().__init__(**kw)
		self._cards = args

	def clone(self, memo):
		ret = super().clone(memo)
		ret._cards = deepcopy(self._cards, memo)
		return ret

	def evaluate(self, source):
		return super().evaluate(source, self._cards)
