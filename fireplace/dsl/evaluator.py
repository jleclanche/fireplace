import copy
from hearthstone.enums import CardType
from ..logging import log


class Evaluator:
	"""
	Lazily evaluate a condition at runtime.

	Evaluators must implement the check() method, which determines whether they
	evaluate to True in the current state.
	"""
	def __init__(self):
		self._if = None
		self._else = None
		self._neg = False

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.selector)

	def __neg__(self):
		ret = copy.copy(self)
		ret._neg = not self._neg
		return ret

	def __and__(self, action):
		ret = copy.copy(self)
		ret._if = action
		return ret

	def __or__(self, action):
		ret = copy.copy(self)
		ret._else = action
		return ret

	def evaluate(self, source):
		"""
		Evaluates the board state from `source` and returns an iterable of
		Actions as a result.
		"""
		ret = self.check(source)
		if self._neg:
			ret = not ret
		if ret:
			if self._if:
				return self._if
		elif self._else:
			return self._else

	def trigger(self, source):
		"""
		Triggers all actions meant to trigger on the board state from `source`.
		"""
		actions = self.evaluate(source)
		if actions:
			if not hasattr(actions, "__iter__"):
				actions = (actions, )
			source.game.trigger_actions(source, actions)


class Attacking(Evaluator):
	"""
	Evaluates to True if any target in \a selector1 is attacking
	any target in \a selector2.
	"""
	def __init__(self, selector1, selector2):
		super().__init__()
		self.selector1 = selector1
		self.selector2 = selector2

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.selector1, self.selector2)

	def check(self, source):
		t1 = self.selector1.eval(source.game, source)
		t2 = self.selector2.eval(source.game, source)
		for entity in t1:
			if entity.attacking:
				return entity.attack_target in t2
		return False


class ChooseBoth(Evaluator):
	"""
	Evaluates to True if \a selector choose_both is True
	"""
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def check(self, source):
		entities = self.selector.eval(source.game, source)
		return entities[0].choose_both


class CurrentPlayer(Evaluator):
	"""
	Evaluates to True if the selector is the current player.
	Selector must evaluate to only one player.
	"""
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def check(self, source):
		for target in self.selector.eval(source.game, source):
			if not target.controller.current_player:
				return False
		return True


class Dead(Evaluator):
	"""
	Evaluates to True if every target in \a selector is dead
	"""
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def check(self, source):
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

	def check(self, source):
		return bool(len(self.selector.eval(source.game, source)))


class FindDuplicates(Evaluator):
	"""
	Evaluates to True if \a selector has duplicates.
	"""
	def __init__(self, selector, count=1):
		super().__init__()
		self.selector = selector

	def check(self, source):
		entities = self.selector.eval(source.game, source)
		return len(set(entities)) < len(entities)


class JoustEvaluator(Evaluator):
	"""
	Compare the sum of the costs of \a selector versus \a selector2.
	Considers the joust won if the mana cost of \a selector1 is higher.
	If a side is empty, it automatically loses.
	A draw is treated as a loss.
	"""
	def __init__(self, selector1, selector2):
		super().__init__()
		self.selector1 = selector1
		self.selector2 = selector2

	def __repr__(self):
		return "%s(%r, %r)" % (self.__class__.__name__, self.selector1, self.selector2)

	def check(self, source):
		challenger = self.selector1.evaluate(source)
		defender = self.selector2.evaluate(source)
		if not challenger:
			return False
		if not defender:
			return True
		return challenger.cost > defender.cost


class Lethal(Evaluator):
	"""
	Evaluates to True if \a amount damage would destroy *all* entities
	in \a selector (including armor).
	"""
	def __init__(self, selector, amount):
		super().__init__()
		self.selector = selector
		self.amount = amount

	def check(self, source):
		entities = self.selector.eval(source.game, source)
		amount = self.amount.evaluate(source)
		for entity in entities:
			health = entity.health
			if entity.type == CardType.HERO:
				health += entity.armor
			if health > amount:
				return False
		return True
