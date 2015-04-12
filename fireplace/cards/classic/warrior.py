from ..utils import *


##
# Minions

# Armorsmith
class EX1_402:
	def OWN_DAMAGE(self, source, target, amount):
		if target.type == CardType.MINION:
			self.controller.hero.armor += 1


# Cruel Taskmaster
class EX1_603:
	def action(self, target):
		self.buff(target, "EX1_603e")
		self.hit(target, 1)


# Frothing Berserker
class EX1_604:
	def DAMAGE(self, source, target, amount):
		if target.type == CardType.MINION:
			self.buff(self, "EX1_604o")


##
# Spells

# Charge
class CS2_103:
	action = buffTarget("CS2_103e2")


# Rampage
class CS2_104:
	action = buffTarget("CS2_104e")


# Heroic Strike
class CS2_105:
	action = buffSelf("CS2_105e")


# Execute
class CS2_108:
	action = destroyTarget


# Cleave
class CS2_114:
	def action(self):
		targets = random.sample(self.controller.opponent.field, 2)
		for target in targets:
			self.hit(target, 2)


# Slam
class EX1_391:
	def action(self, target):
		self.hit(target, 2)
		if not target.dead:
			self.controller.draw()


# Battle Rage
class EX1_392:
	def action(self):
		for target in self.controller.getTargets(TARGET_FRIENDLY_CHARACTERS):
			if target.damage:
				self.controller.draw()


# Whirlwind
class EX1_400:
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			self.hit(target, 1)


# Brawl
class EX1_407:
	def action(self):
		board = self.controller.getTargets(TARGET_ALL_MINIONS)
		for minion in random.sample(board, len(board) - 1):
			minion.destroy()


# Mortal Strike
class EX1_408:
	def action(self, target):
		self.hit(target, 6 if self.controller.hero.health <= 12 else 4)


# Upgrade!
class EX1_409:
	def action(self):
		if self.controller.hero.weapon:
			self.buff(self.controller.hero.weapon, "EX1_409e")
		else:
			self.controller.summon("EX1_409t")


# Shield Slam
class EX1_410:
	def action(self, target):
		self.hit(target, self.controller.hero.armor)


# Shield Block
class EX1_606:
	def action(self):
		self.controller.hero.armor += 5
		self.controller.draw()


# Inner Rage
class EX1_607:
	def action(self, target):
		self.buff(target, "EX1_607e")
		self.hit(target, 1)


# Commanding Shout
class NEW1_036:
	def action(self):
		for target in self.controller.field:
			self.buff(target, "NEW1_036e")
