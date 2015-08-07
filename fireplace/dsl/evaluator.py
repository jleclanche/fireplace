import copy
import logging


class Evaluator:
	"""
	Lazily evaluate a condition at runtime.
	"""
	def __init__(self):
		self._if = None
		self._else = None

	def __and__(self, action):
		ret = copy.copy(self)
		ret._if = action
		return ret

	def __or__(self, action):
		ret = copy.copy(self)
		ret._else = action
		return ret

	def get_actions(self, source):
		from ..actions import Action
		ret = self.evaluate(source)
		if ret:
			if self._if:
				if isinstance(self._if, Action):
					return [self._if]
				return self._if
		elif self._else:
			if isinstance(self._else, Action):
				return [self._else]
			return [self._else]
		return []

	def trigger(self, source):
		for action in self.get_actions(source):
			action.trigger(source)


class Dead(Evaluator):
	"""
	Evaluates to True if every target in \a selector is dead
	"""
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def evaluate(self, source):
		for target in self.selector.eval(source.game, source):
			if not target.dead:
				return False
		return True


class Find(Evaluator):
	"""
	Evaluates to True if \a selector has a match.
	"""
	def __init__(self, selector, count=1):
		super().__init__()
		self.selector = selector
		self.count = count

	def evaluate(self, source):
		return len(self.selector.eval(source.game, source)) >= self.count


class Joust(Evaluator):
	"""
	Compare the sum of the costs of \a selector1 versus \a selector2.
	Evaluates to True if the mana cost of \a selector1 is higher.
	"""
	def __init__(self, selector1, selector2):
		super().__init__()
		self.selector1 = selector1
		self.selector2 = selector2

	def evaluate(self, source):
		t1 = self.selector1.eval(source.game, source)
		t2 = self.selector2.eval(source.game, source)
		diff = sum(t.cost for t in t1) - sum(t.cost for t in t2)
		logging.info("Jousting %r vs %r -> %i difference", t1, t2, diff)
		return diff > 0
