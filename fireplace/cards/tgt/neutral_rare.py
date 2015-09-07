from ..utils import *


##
# Minions

# Injured Kvaldir
class AT_105:
	play = Hit(SELF, 3)


# Light's Champion
class AT_106:
	play = Silence(TARGET)


# Armored Warhorse
class AT_108:
	play = JOUST & SetTag(SELF, {GameTag.CHARGE: True})


# Argent Watchman
class AT_109:
	inspire = Buff(SELF, "AT_109e")


# Coliseum Manager
class AT_110:
	inspire = Bounce(SELF)


# Master Jouster
class AT_112:
	play = JOUST & SetTag(SELF, {GameTag.TAUNT: True, GameTag.DIVINE_SHIELD: True})
