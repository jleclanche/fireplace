from ..utils import *

##
# Spells

# Claw
class CS2_005:
	def action(self):
		buffSelf(self, "CS2_005o")
		self.controller.hero.armor += 2

class CS2_005o:
	Atk = 2


# Healing Touch
class CS2_007:
	action = healTarget(8)


# Moonfire
class CS2_008:
	action = damageTarget(1)


# Mark of the Wild
class CS2_009:
	action = buffTarget("CS2_009e")

class CS2_009e:
	Atk = 2
	Health = 2
	taunt = True


# Savage Roar
class CS2_011:
	def action(self):
		for target in self.controller.getTargets(TARGET_FRIENDLY_CHARACTERS):
			self.buff(target, "CS2_011o")

class CS2_011o:
	Atk = 2


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
		if self.controller.maxMana < self.controller.MAX_MANA:
			self.controller.maxMana += 1
		else:
			self.controller.give("CS2_013t")

class CS2_013t:
	action = drawCard


# Mark of Nature
class EX1_155:
	ChooseOne = ("EX1_155a", "EX1_155b")

class EX1_155a:
	action = buffTarget("EX1_155ae")

class EX1_155ae:
	Atk = 4

class EX1_155b:
	action = buffTarget("EX1_155be")

class EX1_155be:
	Health = 4
	Taunt = True


# Soul of the Forest
class EX1_158:
	def action(self):
		for target in self.controller.field:
			self.buff(target, "EX1_158e")

class EX1_158e:
	Deathrattle = True
	def deathrattle(self):
		self.controller.summon("EX1_158t")


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

class EX1_570e:
	Atk = 4


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
