from ..utils import *


##
# Minions

# Twilight Guardian
class AT_017:
	play = HOLDING_DRAGON & Buff(SELF, "AT_017e")

AT_017e = buff(atk=1, taunt=True)


# Garrison Commander
class AT_080:
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.HEROPOWER_ADDITIONAL_ACTIVATIONS: 1})


# Sideshow Spelleater
class AT_098:
	play = Summon(CONTROLLER, Copy(ENEMY_HERO_POWER))


# Kodorider
class AT_099:
	inspire = Summon(CONTROLLER, "AT_099t")


# Recruiter
class AT_113:
	inspire = Give(CONTROLLER, "CS2_152")


# Master of Ceremonies
class AT_117:
	play = Find(FRIENDLY_MINIONS + SPELLPOWER) & Buff(SELF, "AT_117e")

AT_117e = buff(+2, +2)


# Grand Crusader
class AT_118:
	play = Give(CONTROLLER, RandomCollectible(card_class=CardClass.PALADIN))


# Frost Giant
class AT_120:
	cost_mod = -Attr(CONTROLLER, GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME)


# Crowd Favorite
class AT_121:
	events = Play(CONTROLLER, BATTLECRY).on(Buff(SELF, "AT_121e"))

AT_121e = buff(+1, +1)
