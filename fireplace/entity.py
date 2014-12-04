class Entity(object):
	def __init__(self):
		self.tags = {}
		self._eventListeners = {}

		# Register the events
		for name in self.events:
			func = getattr(self, name, None)
			# TODO multiple defs for same event
			if func:
				self._eventListeners[name] = [func]

	def broadcast(self, event, *args):
		for entity in self.entities:
			if event in entity._eventListeners:
				for f in entity._eventListeners[event]:
					f(*args)
		if event != "UPDATE":
			self.broadcast("UPDATE")

	def setTag(self, tag, value):
		self.tags[tag] = value

	def unsetTag(self, tag):
		del self.tags[tag]

	def getIntProperty(self, tag):
		ret = self.tags.get(tag, 0)
		for slot in self.slots:
			ret += slot.getIntProperty(tag)
		return ret

	def getBoolProperty(self, tag):
		if self.tags.get(tag, False):
			return True
		for slot in self.slots:
			if slot.getBoolProperty(tag):
				return True
		return
