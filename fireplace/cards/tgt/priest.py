from ..utils import *


##
# Minions

# Holy Champion
class AT_011:
	events = Heal().on(Buff(SELF, "AT_011e"))

AT_011e = buff(atk=2)


# Spawn of Shadows
class AT_012:
	inspire = Hit(ALL_HEROES, 4)


# Shadowfiend
class AT_014:
	events = Draw(CONTROLLER).on(Buff(Draw.CARD, "AT_014e"))

AT_014e = buff(cost=-1)


# Wyrmrest Agent
class AT_116:
	play = HOLDING_DRAGON & Buff(SELF, "AT_116e")

AT_116e = buff(atk=1, taunt=True)


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

AT_016e = AttackHealthSwapBuff()


# Flash Heal
class AT_055:
	play = Heal(TARGET, 5)
