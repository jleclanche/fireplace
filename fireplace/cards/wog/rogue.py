from ..utils import *


##
# Minions

class OG_070:
	"Bladed Cultist"
	combo = Buff(SELF, "OG_070e")

OG_070e = buff(+1, +1)


class OG_080:
	"Xaril, Poisoned Mind"
	play = deathrattle = Give(CONTROLLER, RandomEntourage())


class OG_267:
	"Southsea Squidface"
	deathrattle = Buff(FRIENDLY_WEAPON, "OG_267e")

OG_267e = buff(atk=2)


class OG_330:
	"Undercity Huckster"
	deathrattle = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))


##
# Spells

class OG_072:
	"Journey Below"
	play = DISCOVER(RandomCollectible(deathrattle=True))


class OG_073:
	"Thistle Tea"
	play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)) * 2)


class OG_176:
	"Shadow Strike"
	play = Hit(TARGET, 5)
