from ..utils import *


##
# Minions

class AT_075:
	"""Warhorse Trainer"""
	update = Refresh(FRIENDLY + ID("CS2_101t"), buff="AT_075e")


AT_075e = buff(atk=1)


class AT_076:
	"""Murloc Knight"""
	inspire = Summon(CONTROLLER, RandomMurloc())


class AT_079:
	"""Mysterious Challenger"""
	play = Summon(CONTROLLER, FRIENDLY_DECK + SECRET)


class AT_081:
	"""Eadric the Pure"""
	play = Buff(ENEMY_MINIONS, "AT_081e")


class AT_081e:
	atk = SET(1)


class AT_104:
	"""Tuskarr Jouster"""
	play = JOUST & Heal(FRIENDLY_HERO, 7)


##
# Spells

class AT_074:
	"""Seal of Champions"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "AT_074e2"), GiveDivineShield(TARGET)


AT_074e2 = buff(atk=3)


##
# Secrets

class AT_073:
	"""Competitive Spirit"""
	events = OWN_TURN_BEGIN.on(EMPTY_BOARD | (
		Reveal(SELF), Buff(FRIENDLY_MINIONS, "AT_073e")
	))


AT_073e = buff(+1, +1)


class AT_078:
	"""Enter the Coliseum"""
	play = Destroy(ALL_MINIONS - HIGHEST_ATK(FRIENDLY_MINIONS) - HIGHEST_ATK(ENEMY_MINIONS))


##
# Weapons

class AT_077:
	"""Argent Lance"""
	play = JOUST & Buff(SELF, "AT_077e")


AT_077e = buff(health=1)
