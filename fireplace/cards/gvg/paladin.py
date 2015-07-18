from ..utils import *


##
# Minions

# Quartermaster
class GVG_060:
	def play(self):
		for recruit in self.controller.field.filter(id="CS2_101t"):
			yield Buff(recruit, "GVG_060e")


# Cobalt Guardian
class GVG_062:
	events = Summon(CONTROLLER, MECH).on(SetTag(SELF, {GameTag.DIVINE_SHIELD: True}))


# Bolvar Fordragon
class GVG_063:
	events = Death(FRIENDLY + MINION).on(Buff(SELF, "GVG_063a"), zone=Zone.HAND)


# Scarlet Purifier
class GVG_101:
	play = Hit(ALL_MINIONS + DEATHRATTLE, 2)


##
# Spells

# Seal of Light
class GVG_057:
	play = Heal(FRIENDLY_HERO, 4), Buff(FRIENDLY_HERO, "GVG_057a")


# Muster for Battle
class GVG_061:
	play = Summon(CONTROLLER, "CS2_101t") * 3, Summon(CONTROLLER, "CS2_091")


##
# Weapons

# Coghammer
class GVG_059:
	play = SetTag(RANDOM_FRIENDLY_MINION, {GameTag.TAUNT: True, GameTag.DIVINE_SHIELD: True})
