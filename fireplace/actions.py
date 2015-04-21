import logging
from .entity import Entity


class Action: # Lawsuit
	args = ()
	def __init__(self, target, *args, **kwargs):
		self.target = target
		self.times = 1
		self._args = args
		for k, v in zip(self.args, args):
			setattr(self, k, v)

	def __repr__(self):
		args = ["%s=%r" % (k, v) for k, v in zip(self.args, self._args)]
		return "<Action: %s(%s)>" % (self.__class__.__name__, ", ".join(args))

	def __mul__(self, value):
		self.times *= value
		return self

	def eval(self, selector, source, game):
		if isinstance(selector, Entity):
			return [selector]
		else:
			return selector.eval(game, source)

	def trigger(self, source, game):
		targets = self.eval(self.target, source, game)
		for i in range(self.times):
			logging.info("%r triggering %r targeting %r", source, self, targets)
			for target in targets:
				self.do(source, target, game)
