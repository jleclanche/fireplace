import logging

class Entity(object):
	def getProperty(self, prop):
		ret = getattr(super(), prop)
		ret -= getattr(self, prop + "Counter", 0)
		for slot in self.slots:
			ret += slot.getProperty(prop)
		return ret

	def buff(self, card):
		if isinstance(card, str):
			from .cards import Card
			card = Card(card)
		card.owner = self
		logging.debug("%r receives buff: %r" % (self, card))
		assert card.type == card.TYPE_ENCHANTMENT, card.type
		self.buffs.append(card)
