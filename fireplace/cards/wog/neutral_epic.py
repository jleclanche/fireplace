from ..utils import *


##
# Minions

class OG_173:
	"""Blood of The Ancient One"""
	events = OWN_TURN_END.on(
		Dead(SELF) | (Find(FRIENDLY_MINIONS - SELF + ID("OG_173")) & (
			Destroy(SELF),
			Destroy(RANDOM(FRIENDLY_MINIONS - SELF + ID("OG_173"))),
			Deaths(),
			Summon(CONTROLLER, "OG_173a")
		))
	)


class OG_200:
	"""Validated Doomsayer"""
	events = OWN_TURN_BEGIN.on(Buff(SELF, "OG_200e"))


class OG_200e:
	"""Doom Free"""
	atk = SET(7)


class OG_271:
	"""Scaled Nightmare"""
	events = OWN_TURN_BEGIN.on(Buff(SELF, "OG_271e"))


class OG_271e:
	atk = lambda self, i: i * 2


class OG_272:
	"""Twilight Summoner"""
	deathrattle = Summon(CONTROLLER, "OG_272t")


class OG_290:
	"""Ancient Harbinger"""
	events = OWN_TURN_BEGIN.on(ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 10))))


class OG_337:
	"""Cyclopian Horror"""
	play = Buff(SELF, "OG_337e") * Count(ENEMY_MINIONS)


OG_337e = buff(health=1)


class OG_102:
	"""Darkspeaker"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = SwapState(TARGET, SELF, "OG_102e")


class OG_102e:
	max_health = lambda self, i: self.health


class OG_174:
	"""Faceless Shambler"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = CopyState(TARGET, "OG_174e")


class OG_174e:
	max_health = lambda self, i: self.health


class OG_321:
	"""Crazed Worshipper"""
	events = SELF_DAMAGE.on(Buff(CTHUN, "OG_281e", atk=2, max_health=2))


OG_321e = buff(+1, +1)
