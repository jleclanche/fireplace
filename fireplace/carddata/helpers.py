import random


drawCard = lambda self: self.owner.draw()


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


def damageTarget(amount):
	def _damageTarget(self, target):
		target.damage(amount)
	return _damageTarget


def buffTarget(buff):
	def _buffTarget(self, target):
		target.buff(buff)
	return _buffTarget


def buffSelf(buff):
	def _buffSelf(self):
		self.owner.hero.buff(buff)
	return _buffSelf
