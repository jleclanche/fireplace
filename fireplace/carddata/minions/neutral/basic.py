from fireplace.enums import GameTag, Race
from ...card import *


##
# Free basic minions

# Raid Leader
class CS2_122(Card):
	aura = "CS2_122e"

class CS2_122e(Card):
	Atk = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target is not self.source


# Voodoo Doctor
class EX1_011(Card):
	action = healTarget(2)


# Novice Engineer
class EX1_015(Card):
	action = drawCard


# Demolisher
class EX1_102(Card):
	def OWN_TURN_BEGIN(self):
		self.hit(random.choice(self.controller.getTargets(TARGET_ENEMY_CHARACTERS)), 2)


# Nightblade
class EX1_593(Card):
	action = damageEnemyHero(3)


# Cult Master
class EX1_595(Card):
	def OWN_MINION_DESTROYED(self, minion):
		self.controller.draw()


##
# Common basic minions

# Earthen Ring Farseer
class CS2_117(Card):
	action = healTarget(3)


# Ironforge Rifleman
class CS2_141(Card):
	action = damageTarget(1)


# Gnomish Inventor
class CS2_147(Card):
	action = drawCard


# Stormpike Commando
class CS2_150(Card):
	action = damageTarget(2)


# Silver Hand Knight
class CS2_151(Card):
	action = summonMinion("CS2_152")


# Elven Archer
class CS2_189(Card):
	action = damageTarget(1)


# Abusive Sergeant
class CS2_188(Card):
	action = buffTarget("CS2_188o")

class CS2_188o(Card):
	Atk = 2


# Razorfen Hunter
class CS2_196(Card):
	action = summonMinion("CS2_boar")


# Stormwind Champion
class CS2_222(Card):
	aura = "CS2_222o"

class CS2_222o(Card):
	Atk = 1
	Health = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target is not self.source


# Darkscale Healer
class DS1_055(Card):
	def action(self):
		for target in self.controller.getTargets(TARGET_FRIENDLY_CHARACTERS):
			self.heal(target, 2)


# Shattered Sun Cleric
class EX1_019(Card):
	action = buffTarget("EX1_019e")

class EX1_019e(Card):
	Atk = 1
	Health = 1


# Dragonling Mechanic
class EX1_025(Card):
	action = summonMinion("EX1_025t")


# Leper Gnome
class EX1_029(Card):
	deathrattle = damageEnemyHero(2)


# Dark Iron Dwarf
class EX1_046(Card):
	action = buffTarget("EX1_046e")

class EX1_046e(Card):
	Atk = 2


# Youthful Brewmaster
class EX1_049(Card):
	action = bounceTarget


# Ancient Brewmaster
class EX1_057(Card):
	action = bounceTarget


# Acidic Swamp Ooze
class EX1_066(Card):
	def action(self):
		if self.controller.opponent.hero.weapon:
			self.controller.opponent.hero.weapon.destroy()


# Loot Hoarder
class EX1_096(Card):
	deathrattle = drawCard


# Dire Wolf Alpha
class EX1_162(Card):
	aura = "EX1_162o"

class EX1_162o(Card):
	Atk = 1
	targeting = TARGET_FRIENDLY_MINIONS


# Frost Elemental
class EX1_283(Card):
	def action(self, target):
		target.frozen = True


# Murloc Tidehunter
class EX1_506(Card):
	action = summonMinion("EX1_506a")


# Grimscale Oracle
class EX1_508(Card):
	aura = "EX1_508o"

class EX1_508o(Card):
	targeting = TARGET_FRIENDLY_MINIONS
	Atk = 1
	def isValidTarget(self, target):
		return target.race == Race.MURLOC and target is not self.source


# Harvest Golem
class EX1_556(Card):
	deathrattle = summonMinion("skele21")


# Priestess of Elune
class EX1_583(Card):
	def action(self):
		self.heal(self.controller.hero, 4)


# Zombie Chow
class FP1_001(Card):
	def deathrattle(self):
		self.heal(self.controller.opponent.hero, 5)


# Haunted Creeper
class FP1_002(Card):
	def deathrattle(self):
		self.controller.summon("FP1_002t")
		self.controller.summon("FP1_002t")


# Mad Scientist
class FP1_004(Card):
	def deathrattle(self):
		secrets = self.controller.deck.filterByTag(GameTag.SECRET)
		if secrets:
			self.controller.summon(random.choice(secrets))


# Unstable Ghoul
class FP1_024(Card):
	def deathrattle(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			self.hit(target, 1)


# Stoneskin Gargoyle
class FP1_027(Card):
	def OWN_TURN_BEGIN(self):
		self.heal(self, self.damage)


# Dancing Swords
class FP1_029(Card):
	def deathrattle(self):
		self.controller.opponent.draw()
