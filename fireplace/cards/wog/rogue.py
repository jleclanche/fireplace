from ..utils import *


##
# Minions

class OG_070:
	"""Bladed Cultist"""
	combo = Buff(SELF, "OG_070e")


OG_070e = buff(+1, +1)


class OG_080:
	"""Xaril, Poisoned Mind"""
	play = deathrattle = Give(CONTROLLER, RandomEntourage())


class OG_267:
	"""Southsea Squidface"""
	deathrattle = Buff(FRIENDLY_WEAPON, "OG_267e")


OG_267e = buff(atk=2)


class OG_330:
	"""Undercity Huckster"""
	deathrattle = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS))


class OG_291:
	"""Shadowcaster"""
	play = Give(CONTROLLER, Buff(Copy(TARGET), "OG_291e"))


class OG_291e:
	atk = SET(1)
	max_health = SET(1)


class OG_282:
	def play(self):
		atk = self.target.atk
		health = self.target.health
		yield Destory(TARGET)
		yield Buff(CTHUN, "OG_282e", atk=atk, max_health=health)


##
# Spells

class OG_072:
	"""Journey Below"""
	play = DISCOVER(RandomCollectible(deathrattle=True))


class OG_073:
	"""Thistle Tea"""
	play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)) * 2)


class OG_176:
	"""Shadow Strike"""
	play = Hit(TARGET, 5)
