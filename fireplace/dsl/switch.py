class Switch:
	"""
	Switch statement on the ID of an entity
	Perform actions as described in the map
	"""
	def __init__(self, selector, map):
		self.selector = selector
		self.map = map

	@property
	def default(self):
		return self.map.get(None, ())
		return ret

	def evaluate(self, source):
		entities = self.selector.eval(source.game, source)
		if not entities:
			return self.default
		assert len(entities) == 1, "Switch() on more than 1 entity: %r" % (entities)
		id = entities[0].id
		if id not in self.map:
			return self.default
		return self.map[id]

	def trigger(self, source):
		action = self.evaluate(source)
		if action:
			action.trigger(source)
