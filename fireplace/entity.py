class Entity(object):
	def __init__(self):
		self.tags = {}

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
