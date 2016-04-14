import random
from hearthstone.enums import CardClass, CardType, Race, Rarity
from .lazynum import LazyValue
from ..cards import utils

class RandomCardPicker(LazyValue):
	"""
	Store filters and generate a random card matching the filters on pick()
	"""
	def __init__(self, *args, **filters):
		self.args = args
		self.filters = filters
		self.count = 1
		self._cards = None
		self._source = None

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.filters)

	def __mul__(self, other):
		ret = self.__class__(*self.args, **self.filters)
		ret._cards = self._cards
		ret._source = self._source
		ret.count = other
		return ret

	def _filter_cards(self, filters):
		from .. import cards
		return cards.filter(**filters)

	def _get_lazy_filtered_cards(self, source, filters):
		newFilters = filters.copy()
		# Iterate through the filters, evaluating the LazyValues as we go
		for k, v in newFilters.items():
			if isinstance(v, LazyValue):
				newFilters[k] = v.evaluate(source)
		return self._filter_cards(newFilters)

	def find_cards(self, source=None, **filters):
		if len(filters)==0:
			filters = self.filters

		if source is None:
			source = self._source

		if self._cards is None or filters != self.filters or source != self._source:
			lazy_filters = False
			for v in filters.values():
				if isinstance(v, LazyValue):
					lazy_filters = True
					break

			if lazy_filters:
				# If the card has lazy filters, we need to evaluate them
				self._cards = self._get_lazy_filtered_cards(source, filters)
			else:
				self._cards = self._filter_cards(filters)

		return self._cards

	def evaluate(self, source, cards=None) -> str:
		cards = cards or self.find_cards(source)
		ret = random.sample(cards, self.count)
		return [source.controller.card(card, source=source) for card in ret]


# get random card(s) matching the filter in the constructor plus one of several weighted filters
class RandomCardWeighted(RandomCardPicker):
	def __init__(self, *args, **filters):
		self._weights = []
		self._weightedfilters = []

		super().__init__(*args, **filters)

	# add a filter set
	def add(self, weight, **filters):
		self._weights.append(weight)
		self._weightedfilters.append(filters)
		return self

	# select number of cards to fetch (overrides base __mul__ because creating a new object will cause the derived members to be lost)
	def __mul__(self, other):
		ret = super().__mul__(other)
		ret._weights = self._weights
		ret._weightedfilters = self._weightedfilters
		return ret

	# This picks from a single combined card pool without replacement, weighting each filtered set of cards against the total
	def evaluate(self, source):

		# add the global filters to each set of filters
		self._weightedfilters[:] = [{ **x, **self.filters } for x in self._weightedfilters]

		# get all the cards matching each set of filters and create the weight line
		# (user does not have to normalize weighting from 0-1)
		cardlist = []
		weightedsegmentstarts = [0] * len(self._weightedfilters)
		weightlinelength = 0

		for i, f in enumerate(self._weightedfilters):
			nextset = self.find_cards(source, **f)
			weightedsegmentstarts[i] = len(cardlist)
			cardlist += nextset
			# higher weighted sets (segments) occupy more space per item on the weight line
			weightlinelength += len(nextset) * self._weights[i]

		ret = []

		# for each card
		for c in range(0, self.count):

			# pick a point along the weight line
			r = random.random() * weightlinelength
			pos = 0

			# figure out which segment it's in
			for i, w in enumerate(self._weights):
				segmentarraylength = ((len(cardlist) if i == len(self._weights)-1 else weightedsegmentstarts[i+1]) - weightedsegmentstarts[i])
				segmentlinelength = segmentarraylength * w
				# it's in this segment, find exact card
				if (r < pos + segmentlinelength):
					# find percentage along this segment we're at
					spc = (r - pos) / segmentlinelength
					# map percentage to array index, add card to selection, remove from weight line
					ret.append(cardlist.pop(weightedsegmentstarts[i] + int(spc * segmentarraylength)))
					# update weights
					weightlinelength -= w
					weightedsegmentstarts[i+1:] = [x-1 for x in weightedsegmentstarts[i+1:]]

					break

				pos += segmentlinelength

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
RandomDiscover = lambda *a, **kw: RandomCardWeighted(*a, collectible=True, **kw).add(1, card_class=CardClass.NEUTRAL).add(4, card_class=utils.FRIENDLY_DISCOVER_CLASS)


class RandomEntourage(RandomCardPicker):
	def evaluate(self, source):
		return super().evaluate(source, source.entourage)


class RandomID(RandomCardPicker):
	def evaluate(self, source):
		return super().evaluate(source, self.args)
