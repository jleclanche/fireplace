from ..utils import *


##
# Minions

class AT_019:
	"""Dreadsteed"""
	deathrattle = Buff(CONTROLLER, "AT_019e")


class AT_019e:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "AT_019"), Destroy(SELF))


class AT_021:
	"""Tiny Knight of Evil"""
	events = Discard(FRIENDLY).on(Buff(SELF, "AT_021e"))


AT_021e = buff(+1, +1)


class AT_023:
	"""Void Crusher"""
	inspire = Destroy(RANDOM_ENEMY_MINION | RANDOM_FRIENDLY_MINION)


class AT_026:
	"""Wrathguard"""
	events = Damage(SELF).on(Hit(FRIENDLY_HERO, Damage.AMOUNT))


class AT_027:
	"""Wilfred Fizzlebang"""
	events = Draw(CONTROLLER, None, FRIENDLY_HERO_POWER).on(Buff(Draw.CARD, "AT_027e"))


class AT_027e:
	cost = SET(0)


##
# Spells

class AT_022:
	"""Fist of Jaraxxus"""
	play = Hit(RANDOM_ENEMY_CHARACTER, 4)

	class Hand:
		events = Discard(SELF).on(Hit(RANDOM_ENEMY_CHARACTER, 4))


class AT_024:
	"""Demonfuse"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 15}
	play = Buff(TARGET, "AT_024e"), GainMana(OPPONENT, 1)


AT_024e = buff(+3, +3)


class AT_025:
	"""Dark Bargain"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	play = Destroy(RANDOM(ENEMY_MINIONS) * 2), Discard(RANDOM(FRIENDLY_HAND) * 2)
