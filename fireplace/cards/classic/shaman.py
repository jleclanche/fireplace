from ..utils import *

##
# Minions

# Fire Elemental
class CS2_042:
	action = damageTarget(3)


# Dust Devil
class EX1_243:
	Recall = 2


# Earth Elemental
class EX1_250:
	Recall = 3


# Unbound Elemental
class EX1_258:
	def OWN_CARD_PLAYED(self, card):
		if card.overload:
			self.buff("EX1_258e")

class EX1_258e:
	Atk = 1
	Health = 1


# Flametongue Totem
class EX1_565:
	Aura = "EX1_565o"

class EX1_565o:
	Atk = 2
	targeting = TARGET_FRIENDLY_MINIONS


# Mana Tide Totem
class EX1_575:
	def OWN_TURN_END(self):
		self.controller.draw()


# Windspeaker
class EX1_587:
	action = buffTarget("EX1_587e")

class EX1_587e:
	windfury = True


##
# Spells

# Frost Shock
class CS2_037:
	def action(self, target):
		self.hit(target, 1)
		target.frozen = True


# Ancestral Spirit
class CS2_038:
	action = buffTarget("CS2_038e")

class CS2_038e:
	def deathrattle(self):
		self.controller.summon(self.id)


# Windfury
class CS2_039:
	def action(self, target):
		target.windfury = True


# Ancestral Healing
class CS2_041:
	def action(self, target):
		self.heal(target, target.maxHealth)
		target.buff("CS2_041e")


# Rockbiter Weapon
class CS2_045:
	action = buffTarget("CS2_045e")

class CS2_045e:
	Atk = 3


# Bloodlust
class CS2_046:
	def action(self):
		for target in self.controller.field:
			target.buff("CS2_046e")

class CS2_046e:
	Atk = 3


# Lightning Bolt
class EX1_238:
	action = damageTarget(3)


# Lava Burst
class EX1_241:
	Recall = 2
	action = damageTarget(5)


# Totemic Might
class EX1_244:
	def action(self):
		for target in self.controller.field:
			if target.race == Race.TOTEM:
				target.buff("EX1_244e")


class EX1_244e:
	Health = 2


class EX1_248:
	Recall = 2
	def action(self):
		self.owner.summon("EX1_tk11")
		self.owner.summon("EX1_tk11")


# Forked Lightning
class EX1_251:
	Recall = 2
	def action(self):
		targets = random.sample(self.controller.opponent.field, 2)
		for target in targets:
			self.hit(target, 2)


# Earth Shock
class EX1_245:
	def action(self, target):
		target.silence()
		self.hit(target, 1)


# Lightning Storm
class EX1_259:
	Recall = 2
	def action(self):
		for target in self.controller.opponent.field:
			self.hit(target, random.choice((2, 3)))


##
# Weapons

# Doomhammer
class EX1_567:
	Recall = 2
