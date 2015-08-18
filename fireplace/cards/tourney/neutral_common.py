from ..utils import *


##
# Minions

# Lowly Squire
class AT_082:
	inspire = Buff(SELF, "AT_082e")


# Lance Carrier
class AT_084:
	play = Buff(TARGET, "AT_084e")


# Boneguard Lieutenant
class AT_089:
	inspire = Buff(SELF, "AT_089e")


# Mukla's Champion
class AT_090:
	inspire = Buff(FRIENDLY_MINIONS, "AT_090e")


# Tournament Medic
class AT_091:
	inspire = Heal(FRIENDLY_HERO, 2)


# Flame Juggler
class AT_094:
	play = Hit(RANDOM_ENEMY_CHARACTER, 1)


# Kodorider
class AT_099:
	inspire = Summon(CONTROLLER, "AT_099t")


# Silver Hand Regent
class AT_100:
	inspire = Summon(CONTROLLER, "CS2_101t")


# North Sea Kraken
class AT_103:
	play = Hit(TARGET, 4)


# Injured Kvaldir
class AT_105:
	play = Hit(SELF, 3)


# Refreshment Vendor
class AT_111:
	play = Heal(ALL_HEROES, 4)


# Recruiter
class AT_113:
	inspire = Draw(CONTROLLER, "CS2_152")


# Grand Crusader
class AT_118:
	play = Give(CONTROLLER, RandomCollectible(card_class=CardClass.PALADIN))


# Kvaldir Raider
class AT_119:
	inspire = Buff(SELF, "AT_119e")
