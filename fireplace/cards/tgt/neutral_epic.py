from ..utils import *


##
# Minions

class AT_017:
	"""Twilight Guardian"""
	powered_up = HOLDING_DRAGON
	play = powered_up & Buff(SELF, "AT_017e")


AT_017e = buff(atk=1, taunt=True)


class AT_080:
	"""Garrison Commander"""
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.HEROPOWER_ADDITIONAL_ACTIVATIONS: 1})


class AT_098:
	"""Sideshow Spelleater"""
	play = Summon(CONTROLLER, Copy(ENEMY_HERO_POWER))


class AT_099:
	"""Kodorider"""
	inspire = Summon(CONTROLLER, "AT_099t")


class AT_113:
	"""Recruiter"""
	inspire = Give(CONTROLLER, "CS2_152")


class AT_117:
	"""Master of Ceremonies"""
	powered_up = Find(FRIENDLY_MINIONS + SPELLPOWER)
	play = powered_up & Buff(SELF, "AT_117e")


AT_117e = buff(+2, +2)


class AT_118:
	"""Grand Crusader"""
	play = Give(CONTROLLER, RandomCollectible(card_class=CardClass.PALADIN))


class AT_120:
	"""Frost Giant"""
	cost_mod = -Attr(CONTROLLER, GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME)


class AT_121:
	"""Crowd Favorite"""
	events = Play(CONTROLLER, BATTLECRY).on(Buff(SELF, "AT_121e"))


AT_121e = buff(+1, +1)
