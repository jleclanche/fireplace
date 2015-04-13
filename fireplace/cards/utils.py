import random
import fireplace.cards
from ..enums import CardType, Race, Zone
from ..targeting import *


def hand(func):
	"""
	@hand helper decorator
	The decorated event listener will only listen while in the HAND Zone
	"""
	func.zone = Zone.HAND
	return func

drawCard = lambda self, *args: self.controller.draw()


def drawCards(amount):
	return lambda self, *args: self.controller.draw(amount)


def discard(count):
	def _discard(self):
		# discard at most x card
		discard = random.sample(self.controller.hand, min(count, len(self.controller.hand)))
		for card in discard:
			card.discard()
	return _discard


def randomCollectible(**kwargs):
	return random.choice(fireplace.cards.filter(collectible=True, **kwargs))


bounceTarget = lambda self, target: target.bounce()
destroyTarget = lambda self, target: target.destroy()
silenceTarget = lambda self, target: target.silence()
giveSparePart = lambda self: self.controller.give(random.choice(self.data.entourage))


def gainArmor(amount):
	def _gainArmor(self):
		self.controller.hero.armor += amount
	return _gainArmor


def healHero(amount):
	def _healHero(self):
		self.heal(self.controller.hero, amount)
	return _healHero


def healTarget(amount):
	def _healTarget(self, target):
		self.heal(target, amount)
	return _healTarget


def damageTarget(amount):
	def _damageTarget(self, target):
		self.hit(target, amount)
	return _damageTarget


def damageHero(amount):
	def _damageHero(self):
		self.hit(self.controller.hero, amount)
	return _damageHero


def damageEnemyHero(amount):
	def _damageEnemyHero(self):
		self.hit(self.controller.opponent.hero, amount)
	return _damageEnemyHero


def morphTarget(id):
	def _morphTarget(self, target):
		target.morph(id)
	return _morphTarget


def buffTarget(buff):
	def _buffTarget(self, target):
		self.buff(target, buff)
	return _buffTarget


def buffSelf(buff):
	def _buffSelf(self):
		self.buff(self.controller.hero, buff)
	return _buffSelf


def buffWeapon(buff):
	def _buffWeapon(self):
		if self.controller.weapon:
			self.buff(self.controller.weapon, buff)
	return _buffWeapon


def summonMinion(minion):
	def _summonMinion(self):
		self.controller.summon(minion)
	return _summonMinion

# equipping a weapon and summoning a minion is the same
equipWeapon = summonMinion
