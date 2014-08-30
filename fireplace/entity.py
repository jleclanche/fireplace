class Entity(object):
	def getProperty(self, prop):
		ret = getattr(super(), prop)
		ret -= getattr(self, prop + "Counter", 0)
		for slot in self.slots:
			ret += slot.getProperty(prop)
		return ret
