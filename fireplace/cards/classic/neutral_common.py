from ..utils import *

##
# Free basic minions

# Raid Leader
class CS2_122:
	Aura = "CS2_122e"

class CS2_122e:
	Atk = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target is not self.source


# Venture Co. Mercenary
class CS2_227:
	class Aura:
		Name = "Venture Co. Virtual Aura"
		targeting = TARGET_FRIENDLY_HAND
		Cost = 3
		def isValidTarget(self, target):
			return target.type == CardType.MINION


# Frostwolf Warlord
class CS2_226:
	def action(self):
		for target in self.controller.field:
			self.buff(self, "CS2_226e")

class CS2_226e:
	Atk = 1
	Health = 1

# RFG: Has +1/+1 for each other friendly minion on the battlefield.
# class CS2_226o:
#	pass


# Voodoo Doctor
class EX1_011:
	action = healTarget(2)


# Novice Engineer
class EX1_015:
	action = drawCard


# Mad Bomber
class EX1_082:
	def action(self):
		for i in range(3):
			target = random.choice(self.controller.getTargets(TARGET_ALL_CHARACTERS))
			self.hit(target, 1)


# Demolisher
class EX1_102:
	def OWN_TURN_BEGIN(self):
		self.hit(random.choice(self.controller.getTargets(TARGET_ENEMY_CHARACTERS)), 2)


# Tauren Warrior
class EX1_390:
	class Enrage:
		Atk = 3


# Amani Berserker
class EX1_393:
	class Enrage:
		Atk = 3


# Arathi Weaponsmith
class EX1_398:
	def action(self):
		self.controller.summon("EX1_398t")


# Gurubashi Berserker
class EX1_399:
	def SELF_DAMAGE(self, amount, source):
		self.buff(self, "EX1_399e")

class EX1_399e:
	Atk = 3


# Nightblade
class EX1_593:
	action = damageEnemyHero(3)


# Cult Master
class EX1_595:
	def OWN_MINION_DESTROY(self, minion):
		self.controller.draw()


##
# Common basic minions

# Earthen Ring Farseer
class CS2_117:
	action = healTarget(3)


# Ironforge Rifleman
class CS2_141:
	action = damageTarget(1)


# Gnomish Inventor
class CS2_147:
	action = drawCard


# Stormpike Commando
class CS2_150:
	action = damageTarget(2)


# Silver Hand Knight
class CS2_151:
	action = summonMinion("CS2_152")


# Elven Archer
class CS2_189:
	action = damageTarget(1)


# Abusive Sergeant
class CS2_188:
	action = buffTarget("CS2_188o")

class CS2_188o:
	Atk = 2


# Razorfen Hunter
class CS2_196:
	action = summonMinion("CS2_boar")


# Spiteful Smith
class CS2_221:
	class Enrage:
		Aura = "CS2_221e"

class CS2_221e:
	Atk = 2
	targeting = TARGET_FRIENDLY_WEAPON


# Stormwind Champion
class CS2_222:
	Aura = "CS2_222o"

class CS2_222o:
	Atk = 1
	Health = 1
	targeting = TARGET_FRIENDLY_MINIONS
	def isValidTarget(self, target):
		return target is not self.source


# Darkscale Healer
class DS1_055:
	def action(self):
		for target in self.controller.getTargets(TARGET_FRIENDLY_CHARACTERS):
			self.heal(target, 2)


# Acolyte of Pain
class EX1_007:
	SELF_DAMAGE = drawCard


# Shattered Sun Cleric
class EX1_019:
	action = buffTarget("EX1_019e")

class EX1_019e:
	Atk = 1
	Health = 1


# Dragonling Mechanic
class EX1_025:
	action = summonMinion("EX1_025t")


# Leper Gnome
class EX1_029:
	deathrattle = damageEnemyHero(2)


# Dark Iron Dwarf
class EX1_046:
	action = buffTarget("EX1_046e")

class EX1_046e:
	Atk = 2


# Spellbreaker
class EX1_048:
	action = silenceTarget


# Youthful Brewmaster
class EX1_049:
	action = bounceTarget


# Ancient Brewmaster
class EX1_057:
	action = bounceTarget


# Acidic Swamp Ooze
class EX1_066:
	def action(self):
		if self.controller.opponent.hero.weapon:
			self.controller.opponent.hero.weapon.destroy()


# Loot Hoarder
class EX1_096:
	deathrattle = drawCard


# Dire Wolf Alpha
class EX1_162:
	Aura = "EX1_162o"

class EX1_162o:
	Atk = 1
	targeting = TARGET_FRIENDLY_MINIONS


# Raging Worgen
class EX1_412:
	class Enrage:
		Atk = 1
		Windfury = True

# Frost Elemental
class EX1_283:
	# The Freeze tag is for Water Elem/Snowchugger
	Freeze = False
	def action(self, target):
		target.frozen = True


# Murloc Tidehunter
class EX1_506:
	action = summonMinion("EX1_506a")


# Grimscale Oracle
class EX1_508:
	Aura = "EX1_508o"

class EX1_508o:
	targeting = TARGET_FRIENDLY_MINIONS
	Atk = 1
	def isValidTarget(self, target):
		return target.race == Race.MURLOC and target is not self.source


# Harvest Golem
class EX1_556:
	deathrattle = summonMinion("skele21")


# Priestess of Elune
class EX1_583:
	action = healHero(4)


# Bloodsail Raider
class NEW1_018:
	def action(self):
		if self.controller.hero.weapon:
			self.buff(self, "NEW1_018e", atk=self.controller.hero.weapon.atk)


# Faerie Dragon
class NEW1_023:
	Chromatic = True


# Flesheating Ghoul
class tt_004:
	def MINION_DESTROY(self):
		self.buff(self, "tt_004o")

class tt_004o:
	Atk = 1
