from ..utils import *


##
# Minions

# Twilight Guardian
class AT_017:
	play = HOLDING_DRAGON & Buff(SELF, "AT_017e")


# Sideshow Spelleater
class AT_098:
	play = Summon(CONTROLLER, Copy(ENEMY_HERO_POWER))


# Kodorider
class AT_099:
	inspire = Summon(CONTROLLER, "AT_099t")


# Master of Ceremonies
class AT_117:
	play = Find(FRIENDLY_MINIONS + SPELLPOWER) & Buff(SELF, "AT_117e")


# Frost Giant
class AT_120:
	cost = lambda self, i: i - self.controller.times_hero_power_used_this_game


# Crowd Favorite
class AT_121:
	events = Play(CONTROLLER, BATTLECRY).on(Buff(SELF, "AT_121e"))
