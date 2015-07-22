class Evaluator:
	"""
	Lazily evaluate a condition at runtime.
	"""
	def __init__(self):
		self._if = None
		self._else = None

	def __and__(self, action):
		self._if = action
		return self

	def __or__(self, action):
		self._else = action
		return self

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
