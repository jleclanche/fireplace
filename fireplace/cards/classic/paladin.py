from ..utils import *


##
# Minions

# Guardian of Kings
class CS2_088:
	def action(self):
		self.heal(self.controller.hero, 6)


# Argent Protector
class EX1_362:
	def action(self, target):
		target.divineShield = True


# Aldor Peacekeeper
class EX1_382:
	action = buffTarget("EX1_382e")

class EX1_382e:
	atk = lambda self, i: 1


# Tirion Fordring
class EX1_383:
	action = equipWeapon("EX1_383t")


##
# Spells

# Blessing of Might
class CS2_087:
	action = buffTarget("CS2_087e")


# Holy Light
class CS2_089:
	action = healTarget(6)


# Blessing of Kings
class CS2_092:
	action = buffTarget("CS2_092e")


# Consecration
class CS2_093:
	def action(self):
		for target in self.controller.getTargets(TARGET_ENEMY_CHARACTERS):
			self.hit(target, 2)


# Hammer of Wrath
class CS2_094:
	def action(self, target):
		self.hit(target, 3)
		self.controller.draw()


# Divine Favor
class EX1_349:
	def action(self):
		diff = len(self.controller.opponent.hand) - len(self.controller.hand)
		self.controller.draw(max(0, diff))


# Lay on Hands
class EX1_354:
	def action(self, target):
		self.heal(target, 8)
		self.controller.draw(3)


# Blessed Champion
class EX1_355:
	action = buffTarget("EX1_355e")

class EX1_355e:
	atk = lambda self, i: i*2


# Humility
class EX1_360:
	action = buffTarget("EX1_360e")

class EX1_360e:
	atk = lambda self, i: 1


# Blessing of Wisdom
class EX1_363:
	action = buffTarget("EX1_363e")

class EX1_363e:
	def SELF_ATTACK(self, target):
		self.controller.draw()


# Holy Wrath
class EX1_365:
	def action(self, target):
		drawn = self.controller.draw()
		self.hit(target, drawn[0].cost)


# Hand of Protection
class EX1_371:
	def action(self, target):
		target.shield = True


# Avenging Wrath
class EX1_384:
	def action(self):
		for i in range(8 + self.controller.spellpower):
			target = random.choice(self.controller.getTargets(TARGET_ENEMY_CHARACTERS))
			self.hit(target, 1)


# Equality
class EX1_619:
	def action(self):
		for target in self.game.board:
			self.buff(target, "EX1_619e")

class EX1_619e:
	maxHealth = lambda self, i: 1


##
# Weapons

# Truesilver Champion
class CS2_097:
	def BEFORE_SELF_ATTACK(self, target):
		self.heal(self.controller.hero, 2)


# Sword of Justice
class EX1_366:
	def OWN_MINION_SUMMON(self, minion):
		self.buff(minion, "EX1_366e")
		self.loseDurability()
