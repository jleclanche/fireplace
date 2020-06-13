from ..utils import *


##
# Minions

class AT_028:
	"""Shado-Pan Rider"""
	combo = Buff(SELF, "AT_028e")


AT_028e = buff(atk=3)


class AT_029:
	"""Buccaneer"""
	events = Summon(FRIENDLY_WEAPON).on(Buff(Summon.TARGET, "AT_029e"))


AT_029e = buff(atk=1)


class AT_030:
	"""Undercity Valiant"""
	requirements = {PlayReq.REQ_TARGET_FOR_COMBO: 0}
	combo = Hit(TARGET, 1)


class AT_031:
	"""Cutpurse"""
	events = Attack(SELF, HERO).on(Give(CONTROLLER, "GAME_005"))


class AT_032:
	"""Shady Dealer"""
	powered_up = Find(FRIENDLY_MINIONS + PIRATE)
	play = powered_up & Buff(SELF, "AT_032e")


AT_032e = buff(+1, +1)


class AT_036:
	"""Anub'arak"""
	deathrattle = Bounce(SELF), Summon(CONTROLLER, "AT_036t")


##
# Spells

class AT_033:
	"""Burgle"""
	play = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS)) * 2


class AT_035:
	"""Beneath the Grounds"""
	play = Shuffle(OPPONENT, "AT_035t") * 3


class AT_035t:
	draw = Destroy(SELF), Summon(OPPONENT, "AT_036t"), Draw(CONTROLLER)


##
# Weapons

class AT_034:
	"""Poisoned Blade"""
	inspire = Buff(SELF, "AT_034e")


AT_034e = buff(atk=1)
