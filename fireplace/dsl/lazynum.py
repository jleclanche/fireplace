import operator
import random
from .evaluator import Evaluator


class LazyNum:
	def evaluate(self, source) -> int:
		raise NotImplementedError

	def _cmp(op):
		def func(self, other):
			if isinstance(other, int):
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


class LazyNumEvaluator(Evaluator):
	def __init__(self, num, other, cmp):
		super().__init__()
		self.num = num
		self.other = other
		self.cmp = cmp

	def evaluate(self, source):
		num = self.num.evaluate(source)
		return self.cmp(num, self.other)


class Count(LazyNum):
	"""
	Lazily count the matches in a selector
	"""
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def evaluate(self, source):
		return len(self.selector.eval(source.game, source))


class Attr(LazyNum):
	"""
	Lazily evaluate the sum of all tags in a selector
	"""
	def __init__(self, selector, tag):
		super().__init__()
		self.selector = selector
		self.tag = tag

	def evaluate(self, source):
		entities = self.selector.eval(source.game, source)
		if isinstance(self.tag, str):
			return sum(getattr(e, self.tag) for e in entities)
		else:
			return sum(e.tags[self.tag] for e in entities)


class RandomNumber(LazyNum):
	def __init__(self, *args):
		super().__init__()
		self.choices = args

	def evaluate(self, source):
		return random.choice(self.choices)
