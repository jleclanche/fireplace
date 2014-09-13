import random


drawCard = lambda self: self.controller.draw()


def drawCards(amount):
	return lambda self: self.controller.draw(amount)


def discard(count):
	def _discard(self):
		# discard at most x card
		discard = random.sample(self.controller.hand, min(count, len(self.controller.hand)))
		for card in discard:
			card.discard()
	return _discard


def healTarget(amount):
	def _healTarget(self, target):
		target.heal(amount)
	return _healTarget


def damageTarget(amount):
	def _damageTarget(self, target, combo=None):
		target.damage(amount)
	return _damageTarget


def buffTarget(buff):
	def _buffTarget(self, target):
		target.buff(buff)
	return _buffTarget


def buffSelf(buff):
	def _buffSelf(self):
		self.controller.hero.buff(buff)
	return _buffSelf
