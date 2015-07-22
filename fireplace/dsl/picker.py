import random


class Picker:
	def pick(self, source) -> [str]:
		raise NotImplementedError


class RandomCardPicker(Picker):
	"""
	Store filters and generate a random card matching the filters on pick()
	"""
	def __init__(self, **filters):
		self.filters = filters
		self._cards = None

	@property
	def cards(self):
		if self._cards is None:
			from .. import cards
			self._cards = cards.filter(**self.filters)
		return self._cards

	def pick(self, source) -> str:
		return [random.choice(self.cards)]


class Copy(Picker):
	"""
	Lazily return a list of copies of the target
	"""
	def __init__(self, selector):
		self.selector = selector
		self.fallback = None

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.selector)

	def __or__(self, other):
		self.fallback = other
		return self

	def pick(self, source) -> [str]:
		ret = self.selector.eval(source.game, source)
		if not ret and self.fallback:
			return [self.fallback]
		return ret
