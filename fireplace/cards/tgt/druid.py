from ..utils import *


##
# Minions

class AT_038:
	"Darnassus Aspirant"
	play = GainEmptyMana(CONTROLLER, 1)
	deathrattle = GainMana(CONTROLLER, -1)


class AT_039:
	"Savage Combatant"
	inspire = Buff(FRIENDLY_HERO, "AT_039e")

AT_039e = buff(atk=2)


class AT_040:
	"Wildwalker"
	play = Buff(TARGET, "AT_040e")

AT_040e = buff(health=3)


class AT_041:
	"Knight of the Wild"
	events = Summon(CONTROLLER, BEAST).on(Buff(SELF, "AT_041e"))

AT_041e = buff(cost=-1)


class AT_042:
	"Druid of the Saber"
	choose = ("AT_042a", "AT_042b")
	play = ChooseBoth(CONTROLLER) & Morph(SELF, "OG_044c")

class AT_042a:
	play = Morph(SELF, "AT_042t")

class AT_042b:
	play = Morph(SELF, "AT_042t2")


class AT_045:
	"Aviana"
	update = Refresh(FRIENDLY_HAND + MINION, {GameTag.COST: SET(1)})


##
# Spells

class AT_037:
	"Living Roots"
	choose = ("AT_037a", "AT_037b")
	play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 2), Summon(CONTROLLER, "AT_037t") * 2)

class AT_037a:
	play = Hit(TARGET, 2)

class AT_037b:
	play = Summon(CONTROLLER, "AT_037t") * 2


class AT_043:
	"Astral Communion"
	play = Discard(FRIENDLY_HAND), (
		AT_MAX_MANA(CONTROLLER) &
		Give(CONTROLLER, "CS2_013t") |
		GainMana(CONTROLLER, 10)
	)


class AT_044:
	"Mulch"
	play = Destroy(TARGET), Give(OPPONENT, RandomMinion())
