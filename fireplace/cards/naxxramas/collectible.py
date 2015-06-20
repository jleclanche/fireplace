from ..utils import *


##
# Minions

# Zombie Chow
class FP1_001:
	deathrattle = [Heal(ENEMY_HERO, 5)]


# Haunted Creeper
class FP1_002:
	deathrattle = [Summon(CONTROLLER, "FP1_002t"), Summon(CONTROLLER, "FP1_002t")]


# Mad Scientist
class FP1_004:
	deathrattle = [ForcePlay(CONTROLLER, RANDOM(CONTROLLER_DECK + SECRET))]


# Shade of Naxxramas
class FP1_005:
	events = [
		OWN_TURN_BEGIN.on(Buff(SELF, "FP1_005e"))
	]


# Nerubian Egg
class FP1_007:
	deathrattle = [Summon(CONTROLLER, "FP1_007t")]


# Deathlord
class FP1_009:
	deathrattle = [ForcePlay(OPPONENT, RANDOM(OPPONENT_DECK + MINION))]


# Webspinner
class FP1_011:
	deathrattle = [Give(CONTROLLER, RandomMinion(race=Race.BEAST))]


# Sludge Belcher
class FP1_012:
	deathrattle = [Summon(CONTROLLER, "FP1_012t")]


# Wailing Soul
class FP1_016:
	action = [Silence(FRIENDLY_MINIONS)]


# Voidcaller
class FP1_022:
	deathrattle = [ForcePlay(CONTROLLER, RANDOM(CONTROLLER_HAND + DEMON))]


# Dark Cultist
class FP1_023:
	deathrattle = [Buff(RANDOM_FRIENDLY_MINION, "FP1_023e")]


# Unstable Ghoul
class FP1_024:
	deathrattle = [Hit(ALL_MINIONS, 1)]


# Anub'ar Ambusher
class FP1_026:
	deathrattle = [Bounce(RANDOM_FRIENDLY_MINION)]


# Stoneskin Gargoyle
class FP1_027:
	events = [
		OWN_TURN_BEGIN.on(
			lambda self, player: [Heal(self, self.damage)]
		)
	]


# Undertaker
class FP1_028:
	events = [
		Summon(CONTROLLER, MINION + DEATHRATTLE).on(Buff(SELF, "FP1_028e"))
	]


# Dancing Swords
class FP1_029:
	deathrattle = [Draw(OPPONENT)]


# Loatheb
class FP1_030:
	action = [
		Buff(ENEMY_HERO, "FP1_030e")
	]

class FP1_030e:
	events = [
		OWN_TURN_END.on(Destroy(SELF))
	]

class FP1_030ea:
	cost = lambda self, i: i+5


##
# Spells

# Reincarnate
class FP1_025:
	def action(self, target):
		return [Destroy(TARGET), Summon(CONTROLLER, target.id)]


##
# Weapons

# Death's Bite
class FP1_021:
	deathrattle = [Hit(ALL_MINIONS, 1)]
