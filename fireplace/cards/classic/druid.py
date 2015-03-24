from ..utils import *


##
# Minions

# Cat Form (Druid of the Claw)
class EX1_165a:
	def action(self):
		self.morph("EX1_165t1")

# Bear Form (Druid of the Claw)
class EX1_165b:
	def action(self):
		self.morph("EX1_165t2")


# Rooted (Ancient of War)
class EX1_178a:
	action = buffSelf("EX1_178ae")


# Uproot (Ancient of War)
class EX1_178b:
	action = buffSelf("EX1_178be")

# Ancient Teachings (Ancient of Lore)
class NEW1_008a:
	action = drawCards(2)

# Ancient Secrets (Ancient of Lore)
class NEW1_008b:
	action = healTarget(5)


##
# Spells

# Claw
class CS2_005:
	def action(self):
		buffSelf(self, "CS2_005o")
		self.controller.hero.armor += 2


# Healing Touch
class CS2_007:
	action = healTarget(8)


# Moonfire
class CS2_008:
	action = damageTarget(1)


# Mark of the Wild
class CS2_009:
	action = buffTarget("CS2_009e")


# Savage Roar
class CS2_011:
	def action(self):
		for target in self.controller.getTargets(TARGET_FRIENDLY_CHARACTERS):
			self.buff(target, "CS2_011o")


# Swipe
class CS2_012:
	def action(self, target):
		for character in self.controller.getTargets(TARGET_ENEMY_CHARACTERS):
			if character is target:
				self.hit(character, 4)
			else:
				self.hit(character, 1)


# Wild Growth
class CS2_013:
	def action(self):
		if self.controller.maxMana < self.controller.maxResources:
			self.controller.maxMana += 1
		else:
			self.controller.give("CS2_013t")

class CS2_013t:
	action = drawCard


# Wrath (3 Damage)
class EX1_154a:
	action = damageTarget(3)

# Wrath (1 Damage)
class EX1_154b:
	def action(self, target):
		self.hit(target, 1)
		self.controller.draw()


# Mark of Nature (Attack)
class EX1_155a:
	action = buffTarget("EX1_155ae")

# Mark of Nature (Health)
class EX1_155b:
	action = buffTarget("EX1_155be")


# Soul of the Forest
class EX1_158:
	def action(self):
		for target in self.controller.field:
			self.buff(target, "EX1_158e")

class EX1_158e:
	DEATHRATTLE = True
	def deathrattle(self):
		self.controller.summon("EX1_158t")


# Summon a Panther (Power of the Wild)
class EX1_160a:
	action = summonMinion("EX1_160t")

# Leader of the Pack (Power of the Wild)
class EX1_160b:
	def action(self):
		for target in self.controller.field:
			target.buff("EX1_160be")


# Naturalize
class EX1_161:
	def action(self, target):
		target.destroy()
		self.controller.opponent.draw(2)


# Innervate
class EX1_169:
	def action(self):
		self.controller.tempMana += 2


# Starfire
class EX1_173:
	def action(self, target):
		self.hit(character, 5)
		self.controller.draw()


# Bite
class EX1_570:
	def action(self):
		buffSelf(self, "EX1_570e")
		self.controller.hero.armor += 4


# Force of Nature
class EX1_571:
	def action(self):
		for i in range(3):
			self.controller.summon("EX1_tk9")

class EX1_tk9:
	def TURN_END(self, player):
		self.destroy()


# Savagery
class EX1_578:
	def action(self, target):
		self.hit(target, self.controller.hero.atk)


# Starfall (2 Damage to All)
class NEW1_007a:
	def action(self):
		for target in self.controller.opponent.field:
			self.hit(target, 2)

# Starfall (5 Damage to One)
class NEW1_007b:
	action = damageTarget(5)
