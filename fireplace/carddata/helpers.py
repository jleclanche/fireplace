import random


drawCard = lambda self: self.owner.draw()

selfBuff = lambda self, buff: self.owner.buff(buff)


def discard(count):
	def _discard(self):
		# discard at most x card
		discard = random.sample(self.owner.hand, min(count, len(self.owner.hand)))
		for card in discard:
			card.discard()
	return _discard


def healTarget(amount):
	def _healTarget(self, target):
		target.heal(amount)
	return _healTarget
