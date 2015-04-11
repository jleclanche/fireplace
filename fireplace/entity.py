import logging
from .enums import Zone

class Entity(object):
	def __init__(self):
		# Register the events
		self._registerEvents()
		self.tags = self.Manager(self)

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

	def _getattr(self, attr, i):
		i += getattr(self, "_" + attr, 0)
		for slot in self.slots:
			i = slot._getattr(attr, i)
		if self.silenced:
			return i
		return getattr(self.data, attr, lambda s, x: x)(self, i)


def slotProperty(attr):
	@property
	def func(self):
		return any(getattr(slot, attr, False) for slot in self.slots)
	return func


def booleanProperty(attr):
	@property
	def func(self):
		return getattr(self, "_" + attr, False) \
			or any(getattr(slot, attr, False) for slot in self.slots) \
			or getattr(self.data, attr, lambda s, x: x)(self, False)

	@func.setter
	def func(self, value):
		setattr(self, "_" + attr, value)

	return func

def intProperty(attr):
	@property
	def func(self):
		ret = self._getattr(attr, 0)
		return max(0, ret)

	@func.setter
	def func(self, value):
		setattr(self, "_" + attr, value)

	return func
