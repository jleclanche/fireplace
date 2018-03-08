from ..utils import *


##
# Minions

class LOOT_078:
	"Cave Hydra"
	events = Attack(SELF).on(CLEAVE)

##
# Spells

class LOOT_077:
	play = Hit(TARGET, 3), Summon(CONTROLLER, "LOOT_077t")

##
# Secrets

class LOOT_079:
	"Wandering Monster"
	secret = Attack(ALL_CHARACTERS, FRIENDLY_HERO).on(
		Reveal(SELF),
		Retarget(Attack.ATTACKER, Summon(CONTROLLER, RandomMinion(cost=3))))
