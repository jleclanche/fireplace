import logging
from .enums import Zone

class Entity(object):
	def __init__(self):
		self.tags = {}

		# Register the events
		self._registerEvents()

	def _registerEvents(self):
		self._eventListeners = {}
		for name in self.events:
			func = getattr(self, name, None)
			if func:
				self._eventListeners[name] = [func]

	def broadcast(self, event, *args):
		for entity in self.entities:
			for f in entity._eventListeners.get(event, []):
				if getattr(f, "zone", Zone.PLAY) == Zone.PLAY:
					f(*args)
		if event != "UPDATE":
			self.broadcast("UPDATE")

	def setTag(self, tag, value):
		logging.debug("%r::%r %r -> %r" % (self, tag, self.tags.get(tag, None), value))
		self.tags[tag] = value

	def unsetTag(self, tag):
		del self.tags[tag]

	def getIntProperty(self, tag):
		ret = self.tags.get(tag, 0)
		for slot in self.slots:
			_ret = slot.getIntProperty(tag)
			if isinstance(_ret, int):
				ret += _ret
			else:
				ret = _ret(ret)
		return ret

	def getBoolProperty(self, tag):
		if self.tags.get(tag, False):
			return True
		for slot in self.slots:
			if slot.getBoolProperty(tag):
				return True
		return
