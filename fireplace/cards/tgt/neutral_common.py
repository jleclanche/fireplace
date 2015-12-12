from ..utils import *


##
# Minions

# Lowly Squire
class AT_082:
	inspire = Buff(SELF, "AT_082e")

AT_082e = buff(atk=1)


# Dragonhawk Rider
class AT_083:
	inspire = Buff(SELF, "AT_083e")

class AT_083e:
	windfury = SET(1)


# Lance Carrier
class AT_084:
	play = Buff(TARGET, "AT_084e")

AT_084e = buff(atk=2)


# Maiden of the Lake
class AT_085:
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(1)})


# Boneguard Lieutenant
class AT_089:
	inspire = Buff(SELF, "AT_089e")

AT_089e = buff(health=1)


# Mukla's Champion
class AT_090:
	inspire = Buff(FRIENDLY_MINIONS, "AT_090e")

AT_090e = buff(+1, +1)


# Tournament Medic
class AT_091:
	inspire = Heal(FRIENDLY_HERO, 2)


# Flame Juggler
class AT_094:
	play = Hit(RANDOM_ENEMY_CHARACTER, 1)


# Clockwork Knight
class AT_096:
	play = Buff(TARGET, "AT_096e")

AT_096e = buff(+1, +1)


# Silver Hand Regent
class AT_100:
	inspire = Summon(CONTROLLER, "CS2_101t")


# North Sea Kraken
class AT_103:
	play = Hit(TARGET, 4)


# Refreshment Vendor
class AT_111:
	play = Heal(ALL_HEROES, 4)


# Kvaldir Raider
class AT_119:
	inspire = Buff(SELF, "AT_119e")

AT_119e = buff(+2, +2)

# Gadgetzan Jouster
class AT_133:
	play = JOUST & Buff(SELF, "AT_133e")

AT_133e = buff(+1, +1)
