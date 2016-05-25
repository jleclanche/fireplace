from ..utils import *


##
# Minions

class OG_006:
	"Vilefin Inquisitor"
	play = Summon(CONTROLLER, "OG_006b")

class OG_006b:
	"The Tidal Hand"
	activate = Summon(CONTROLLER, "OG_006a")


class OG_221:
	"Selfless Hero"
	deathrattle = GiveDivineShield(RANDOM_FRIENDLY_MINION)


class OG_229:
	"Ragnaros, Lightlord"
	events = OWN_TURN_END.on(Heal(RANDOM(FRIENDLY + DAMAGED_CHARACTERS), 8))


class OG_310:
	"Steward of Darkshire"
	events = Summon(CONTROLLER, MINION + (CURRENT_HEALTH == 1)).on(GiveDivineShield(Summon.CARD))


##
# Spells

class OG_223:
	"Divine Strength"
	play = Buff(TARGET, "OG_223e")

OG_223e = buff(+1, +2)


class OG_273:
	"Stand Against Darkness"
	play = Summon(CONTROLLER, "CS2_101t") * 5


class OG_311:
	"A Light in the Darkness"
	play = DISCOVER(RandomMinion()).then(Buff(Discover.CARDS, "OG_311e"))

OG_311e = buff(+1, +1)


##
# Weapons

class OG_222:
	"Rallying Blade"
	play = Buff(FRIENDLY_MINIONS + DIVINE_SHIELD, "OG_222e")

OG_222e = buff(+1, +1)
