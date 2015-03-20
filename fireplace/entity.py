import logging
from .enums import Zone

class Entity(object):
	def __init__(self):
		self.tags = {}

		# Register the events
		self._registerEvents()

	def _registerEvents(self):
		self._eventListeners = {}
		for event in self.events:
			func = getattr(self, event, None)
			if func:
				self.register(event, func)

	def broadcast(self, event, *args):
		for entity in self.entities:
			for f in entity._eventListeners.get(event, []):
				if getattr(f, "zone", Zone.PLAY) == Zone.PLAY:
					f(*args)

				# clear out one-shot events
				if getattr(f, "once", False):
					entity._eventListeners[event].remove(f)

		if event != "UPDATE":
			self.broadcast("UPDATE")

	def register(self, event, callback, once=False):
		"""
		Register \a callback with \a event.
		If \a once is True, the callback will unregister when fired.
		"""
		if not event in self._eventListeners:
			self._eventListeners[event] = []

		if once:
			callback.once = True

		self._eventListeners[event].append(callback)

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

	def attributeScript(self, attr, value):
		"""
		Some values support a script that overrides/complements the attributes without
		requiring a special buff. (Molten Giant, Lightspawn...)
		"""
		if hasattr(self.data, attr):
			value = getattr(self.data, attr)(self, value)
		return value
