from .lazynum import LazyValue

class JadeGolem(LazyValue):
	def __init__(self):
		pass

	def __repr__(self):
		return "JadeGolem()"

	def evaluate(self, source):
		jade_counter = source.controller.jade_counter
		source.controller.jade_counter += 1
		return source.controller.card("CFM_712_t%.2d" % jade_counter)
