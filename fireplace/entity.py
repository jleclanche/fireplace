import uuid

class Entity(object):
	def __init__(self):
		self.manager = self.Manager(self)
		self.tags = self.manager
		self.uuid = uuid.uuid4()
		self.ignore_events = False

		scripts = getattr(self.data, "scripts", None)
		self._events = getattr(scripts, "events", [])[:]

	def _getattr(self, attr, i):
		i += getattr(self, "_" + attr, 0)
		for slot in self.slots:
			i = slot._getattr(attr, i)
		if self.silenced:
			return i
		return getattr(self.data.scripts, attr, lambda s, x: x)(self, i)


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
