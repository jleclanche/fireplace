from ..utils import *


##
# Minions

class OG_271:
	"Scaled Nightmare"
	events = OWN_TURN_BEGIN.on(Buff(SELF, "OG_271e"))

class OG_271e:
	atk = lambda self, i: i * 2


class OG_272:
	"Twilight Summoner"
	deathrattle = Summon(CONTROLLER, "OG_272t")


class OG_337:
	"Cyclopian Horror"
	play = Buff(SELF, "OG_337e") * Count(ENEMY_MINIONS)

OG_337e = buff(health=1)
