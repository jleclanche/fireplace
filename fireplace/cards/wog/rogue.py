from ..utils import *


##
# Minions

class OG_070:
	"Bladed Cultist"
	combo = Buff(SELF, "OG_070e")

OG_070e = buff(+1, +1)


class OG_267:
	"Southsea Squidface"
	deathrattle = Buff(FRIENDLY_WEAPON, "OG_267e")

OG_267e = buff(atk=2)


##
# Spells

class OG_073:
	"Thistle Tea"
	play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)) * 2)


class OG_176:
	"Shadow Strike"
	play = Hit(TARGET, 5)
