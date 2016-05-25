from ..utils import *


##
# Minions

class OG_200:
	"Validated Doomsayer"
	events = OWN_TURN_BEGIN.on(Buff(SELF, "OG_200e"))

class OG_200e:
	"Doom Free"
	atk = SET(7)


class OG_271:
	"Scaled Nightmare"
	events = OWN_TURN_BEGIN.on(Buff(SELF, "OG_271e"))

class OG_271e:
	atk = lambda self, i: i * 2


class OG_272:
	"Twilight Summoner"
	deathrattle = Summon(CONTROLLER, "OG_272t")


class OG_290:
	"Ancient Harbinger"
	events = OWN_TURN_BEGIN.on(ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 10))))


class OG_337:
	"Cyclopian Horror"
	play = Buff(SELF, "OG_337e") * Count(ENEMY_MINIONS)

OG_337e = buff(health=1)
