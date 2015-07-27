import uuid

class Entity(object):
	def __init__(self):
		self.manager = self.Manager(self)
		self.tags = self.manager
		self.uuid = uuid.uuid4()

		scripts = getattr(self.data, "scripts", None)
		events = getattr(scripts, "events", [])
		if not isinstance(events, list):
			self._events = [events]
		else:
			self._events = events[:]

	@property
	def events(self):
		return self._events

	def _getattr(self, attr, i):
		i += getattr(self, "_" + attr, 0)
		for slot in self.slots:
			i = slot._getattr(attr, i)
		if self.silenced:
			return i
		return getattr(self.data.scripts, attr, lambda s, x: x)(self, i)

	def trigger_event(self, source, event, args):
		"""
		Trigger an event on the Entity
		* \a source: The source of the event
		* \a event: The event being triggered
		* \a args: A list of arguments to pass to the callback
		"""
		actions = []
		for action in event.actions:
			if callable(action):
				ac = action(self, *args)
				if not ac:
					# Handle falsy returns
					continue
				if not hasattr(ac, "__iter__"):
					actions.append(ac)
				else:
					actions += action(self, *args)
			else:
				actions.append(action)
		# XXX This is racey. Replace with something more solid.
		self.event_args = args
		source.game.queue_actions(self, actions)
		self.event_args = None
		if event.once:
			self._events.remove(event)


def slot_property(attr, f=any):
	@property
	def func(self):
		return f(getattr(slot, attr, False) for slot in self.slots)
	return func


def boolean_property(attr):
	@property
	def func(self):
		return getattr(self, "_" + attr, False) \
			or any(getattr(slot, attr, False) for slot in self.slots) \
			or getattr(self.data.scripts, attr, lambda s, x: x)(self, False)

	@func.setter
	def func(self, value):
		setattr(self, "_" + attr, value)

	return func


def int_property(attr):
	@property
	def func(self):
		ret = self._getattr(attr, 0)
		return max(0, ret)

	@func.setter
	def func(self, value):
		setattr(self, "_" + attr, value)

	return func
