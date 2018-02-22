from ..utils import *


##
# Minions

class OG_102:
	"Darkspeaker"
	play = SwapState(SELF, TARGET, "OG_102e")

class OG_102e:
	max_health = lambda self, i: self.health


class OG_173:
	"Blood of The Ancient One"
	events = OWN_TURN_END.on(
		Dead(SELF) | (Find(FRIENDLY_MINIONS - SELF + ID("OG_173")) & (
			Destroy(SELF),
			Destroy(SelectorOne(FRIENDLY_MINIONS - SELF + ID("OG_173"))),
			Deaths(),
			Summon(CONTROLLER, "OG_173a")
		))
	)

class OG_174:
	"Faceless Shambler"
	play = SetState(SELF, TARGET, "OG_174e")

class OG_174e:
	max_health = lambda self, i: self.health

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


class OG_321:
	"Crazed Worshipper"
	events = SELF_DAMAGE.on(Buff(CTHUN, "OG_321e"))

OG_321e = buff(+1, +1)


class OG_337:
	"Cyclopian Horror"
	play = Buff(SELF, "OG_337e") * Count(ENEMY_MINIONS)

OG_337e = buff(health=1)
