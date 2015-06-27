from ..utils import *


##
# Rogue

# Dagger Mastery
class CS2_083b:
	activate = [Summon(CONTROLLER, "CS2_082")]


##
# Minions

# Defias Ringleader
class EX1_131:
	combo = [Summon(CONTROLLER, "EX1_131t")]


# SI:7 Agent
class EX1_134:
	combo = [Hit(TARGET, 2)]


# Edwin VanCleef
class EX1_613:
	def combo(self):
		count = self.controller.cards_played_this_turn
		return [Buff(self, "EX1_613e") * count]


# Kidnapper
class NEW1_005:
	combo = [Bounce(TARGET)]


# Master of Disguise
class NEW1_014:
	action = [SetTag(TARGET, {GameTag.STEALTH: False})]


##
# Spells

# Backstab
class CS2_072:
	action = [Hit(TARGET, 2)]


# Cold Blood
class CS2_073:
	action = [Buff(TARGET, "CS2_073e")]
	combo = [Buff(TARGET, "CS2_073e2")]


# Deadly Poison
class CS2_074:
	action = [Buff(FRIENDLY_WEAPON, "CS2_074e")]


# Sinister Strike
class CS2_075:
	action = [Hit(ENEMY_HERO, 3)]


# Assassinate
class CS2_076:
	action = [Destroy(TARGET)]


# Sprint
class CS2_077:
	action = [Draw(CONTROLLER) * 4]


# Blade Flurry
class CS2_233:
	def action(self):
		return [Hit(ENEMY_CHARACTERS, self.controller.weapon.atk), Destroy(FRIENDLY_WEAPON)]


# Eviscerate
class EX1_124:
	action = [Hit(TARGET, 2)]
	combo = [Hit(TARGET, 4)]


# Betrayal
class EX1_126:
	def action(self, target):
		return [Hit(TARGET_ADJACENT, target.atk, target)]


# Conceal
class EX1_128:
	action = [Buff(FRIENDLY_MINIONS, "EX1_128e")]

class EX1_128e:
	events = [
		OWN_TURN_BEGIN.on(Destroy(SELF))
	]


# Fan of Knives
class EX1_129:
	action = [Hit(ENEMY_MINIONS, 1), Draw(CONTROLLER)]


# Headcrack
class EX1_137:
	action = [Hit(ENEMY_HERO, 2)]
	combo = action + [TURN_END.once(Give(CONTROLLER, "EX1_137"))]


# Shadowstep
class EX1_144:
	action = [Bounce(TARGET), Buff(TARGET, "EX1_144e")]


# Preparation
class EX1_145:
	action = [Buff(FRIENDLY_HERO, "EX1_145o")]

class EX1_145o:
	events = [
		OWN_SPELL_PLAY.after(
			lambda self, player, card, *args: card is not self.creator and [Destroy(self)] or []
		)
	]


# Shiv
class EX1_278:
	action = [Hit(TARGET, 1), Draw(CONTROLLER)]


# Sap
class EX1_581:
	action = [Bounce(TARGET)]


# Vanish
class NEW1_004:
	action = [Bounce(ALL_MINIONS)]


##
# Weapons

# Perdition's Blace
class EX1_133:
	action = [Hit(TARGET, 1)]
	combo = [Hit(TARGET, 2)]
