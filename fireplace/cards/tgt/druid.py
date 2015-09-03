from ..utils import *


##
# Minions

# Darnassus Aspirant
class AT_038:
	play = GainEmptyMana(CONTROLLER, 1)
	deathrattle = GainMana(CONTROLLER, -1)


# Savage Combatant
class AT_039:
	inspire = Buff(FRIENDLY_HERO, "AT_039e")


# Wildwalker
class AT_040:
	play = Buff(TARGET, "AT_040e")


# Knight of the Wild
class AT_041:
	events = Summon(CONTROLLER, BEAST).on(Buff(SELF, "AT_041e"))


# Lion Form (Druid of the Saber)
class AT_042a:
	play = Morph(SELF, "AT_042t")


# Panther Form (Druid of the Saber)
class AT_042b:
	play = Morph(SELF, "AT_042t2")


# Aviana
class AT_045:
	update = Refresh(CONTROLLER_HAND + MINION, {GameTag.COST: lambda self, i: 1})


##
# Spells

# Living Roots (Deal 2 damage)
class AT_037a:
	play = Hit(TARGET, 2)

# Living Roots (Summon two saplings)
class AT_037b:
	play = Summon(CONTROLLER, "AT_037t") * 2


# Astral Communion
class AT_043:
	play = GainMana(CONTROLLER, 10), Discard(CONTROLLER_HAND)


# Mulch
class AT_044:
	play = Destroy(TARGET), Give(OPPONENT, RandomMinion())
