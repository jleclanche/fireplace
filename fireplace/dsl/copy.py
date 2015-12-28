from ..logging import log
from .lazynum import LazyValue


class Copy(LazyValue):
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
		log.info("Creating a copy of %r", entity)
		return source.controller.card(entity.id, source)

	def evaluate(self, source) -> [str]:
		if isinstance(self.selector, LazyValue):
			entities = [self.selector.evaluate(source)]
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
