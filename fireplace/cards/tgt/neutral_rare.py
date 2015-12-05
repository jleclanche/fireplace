from ..utils import *


##
# Minions

# Saboteur
class AT_086:
	play = Buff(OPPONENT, "AT_086e")

class AT_086e:
	update = CurrentPlayer(OWNER) & Refresh(ENEMY_HERO_POWER, {GameTag.COST: +5})
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


# Injured Kvaldir
class AT_105:
	play = Hit(SELF, 3)


# Light's Champion
class AT_106:
	play = Silence(TARGET)


# Armored Warhorse
class AT_108:
	play = JOUST & GiveCharge(SELF)


# Argent Watchman
class AT_109:
	inspire = Buff(SELF, "AT_109e")

AT_109e = buff(cant_attack=False)


# Coliseum Manager
class AT_110:
	inspire = Bounce(SELF)


# Master Jouster
class AT_112:
	play = JOUST & SetTag(SELF, (GameTag.TAUNT, GameTag.DIVINE_SHIELD))


# Fencing Coach
class AT_115:
	play = Buff(CONTROLLER, "AT_115e")

class AT_115e:
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: -2})
	events = Activate(CONTROLLER, HERO_POWER).on(Destroy(SELF))
