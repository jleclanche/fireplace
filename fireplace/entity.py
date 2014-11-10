class Entity(object):
	def __init__(self):
		self.tags = {}

	def setTag(self, tag, value):
		self.tags[tag] = value

	def unsetTag(self, tag):
		del self.tags[tag]
