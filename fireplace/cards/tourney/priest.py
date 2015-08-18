from ..utils import *


##
# Minions

# Holy Champion
class AT_011:
	events = Heal().on(Buff(SELF, "AT_011e"))


# Spawn of Shadows
class AT_012:
	inspire = Hit(ALL_HEROES, 4)


##
# Spells

# Power Word: Glory
class AT_013:
	play = Buff(TARGET, "AT_013e")

class AT_013e:
	events = Attack(OWNER).on(Heal(FRIENDLY_HERO, 4))


# Convert
class AT_015:
	play = Give(CONTROLLER, Copy(TARGET))


# Confuse
class AT_016:
	play = Buff(ALL_MINIONS, "AT_016e")
