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

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.selector)

	def copy(self, source, entity):
		"""
		Return a copy of \a entity
		"""
		return source.game.card(entity.id)

	def pick(self, source) -> [str]:
		from ..actions import Action
		if isinstance(self.selector, Action.Args):
			# TODO cleanup DRY with actions.py
			assert source.event_args
			entities = [source.event_args[self.selector]]
		else:
			entities = self.selector.eval(source.game, source)

		return [self.copy(source, e) for e in entities]


class ExactCopy(Copy):
	"""
	Lazily create an exact copy of the target.
	An exact copy will include buffs and all tags.
	"""
	def copy(self, source, entity):
		ret = super().copy(source, entity)
		for k in entity.silenceable_attributes:
			v = getattr(entity, k)
			setattr(ret, k, v)
		ret.silenced = entity.silenced
		ret.damage = entity.damage
		for buff in entity.buffs:
			# Recreate the buff stack
			entity.buff(ret, buff.id)
		return ret
