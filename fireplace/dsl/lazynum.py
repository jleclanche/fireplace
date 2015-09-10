import copy
import operator
import random
from .evaluator import Evaluator
from .selector import Selector


class LazyNum:
	def __init__(self):
		self._neg = False

	def evaluate(self, source) -> int:
		raise NotImplementedError

	def _cmp(op):
		def func(self, other):
			if isinstance(other, (int, LazyNum)):
				# When comparing a LazyNum with an int, turn it into an
				# Evaluator that compares the int to the result of the LazyNum
				return LazyNumEvaluator(self, other, getattr(operator, op))
			return getattr(super(), "__%s__" % (op))(other)
		return func

	__eq__ = _cmp("eq")
	__ge__ = _cmp("ge")
	__gt__ = _cmp("gt")
	__le__ = _cmp("le")
	__lt__ = _cmp("lt")

	def __neg__(self):
		ret = copy.copy(self)
		ret._neg = not self._neg
		return ret

	def num(self, n):
		return -n if self._neg else n

	def get_entities(self, source):
		if isinstance(self.selector, Selector):
			entities = self.selector.eval(source.game, source)
		else:
			# TODO assert that self.selector is a TargetedAction
			entities = sum(self.selector.trigger(source), [])
		return entities


class LazyNumEvaluator(Evaluator):
	def __init__(self, num, other, cmp):
		super().__init__()
		self.num = num
		self.other = other
		self.cmp = cmp

	def evaluate(self, source):
		num = self.num.evaluate(source)
		other = self.other
		if isinstance(other, LazyNum):
			other = other.evaluate(source)
		return self.cmp(num, other)


class Count(LazyNum):
	"""
	Lazily count the matches in a selector
	"""
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.selector)

	def evaluate(self, source):
		return self.num(len(self.get_entities(source)))


class Attr(LazyNum):
	"""
	Lazily evaluate the sum of all tags in a selector
	"""
	def __init__(self, selector, tag):
		super().__init__()
		self.selector = selector
		self.tag = tag

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.selector, self.tag)

	def evaluate(self, source):
		entities = self.get_entities(source)
		if isinstance(self.tag, str):
			ret = sum(getattr(e, self.tag) for e in entities)
		else:
			# XXX: int() because of CardList counter tags
			ret = sum(int(e.tags[self.tag]) for e in entities)
		return self.num(ret)


class RandomNumber(LazyNum):
	def __init__(self, *args):
		super().__init__()
		self.choices = args

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.choices)

	def evaluate(self, source):
		return self.num(random.choice(self.choices))
