"""
Upgraded Hero Powers from Justicar Trueheart (AT_132)
"""
from ..utils import *


##
# Hero Powers

# Dire Shapeshift
class AT_132_DRUID:
	activate = Buff(FRIENDLY_HERO, "AT_132_DRUIDe"), GainArmor(FRIENDLY_HERO, 2)

AT_132_DRUIDe = buff(atk=2)


# Ballista Shot
class AT_132_HUNTER:
	activate = Hit(ENEMY_HERO, 3)

# Ballista Shot (Alleria Windrunner)
class DS1h_292_H1_AT_132:
	activate = AT_132_HUNTER.activate


# Fireblast Rank 2
class AT_132_MAGE:
	activate = Hit(TARGET, 2)

# Fireblast Rank 2 (Medivh)
class CS2_034_H1_AT_132:
	activate = AT_132_MAGE.activate

# Fireblast Rank 2 (Khadgar)
class CS2_034_H2_AT_132:
	activate = AT_132_MAGE.activate


# The Silver Hand
class AT_132_PALADIN:
	activate = Summon(CONTROLLER, "CS2_101t") * 2

# The Silver Hand (Lady Liadrin)
class CS2_101_H1_AT_132:
	activate = AT_132_PALADIN.activate


# Heal
class AT_132_PRIEST:
	activate = Heal(TARGET, 4)


# Poisoned Daggers
class AT_132_ROGUE:
	activate = Summon(CONTROLLER, "AT_132_ROGUEt")


# Tank Up!
class AT_132_WARRIOR:
	activate = GainArmor(FRIENDLY_HERO, 4)

# Tank Up! (Magni Bronzebeard)
class CS2_102_H1_AT_132:
	activate = AT_132_WARRIOR.activate


# Soul Tap
class AT_132_WARLOCK:
	activate = Draw(CONTROLLER)


# Totemic Slam
class AT_132_SHAMAN:
	choose = ("AT_132_SHAMANa", "AT_132_SHAMANb", "AT_132_SHAMANc", "AT_132_SHAMANd")


# Healing Totem
class AT_132_SHAMANa:
	play = Summon(CONTROLLER, "NEW1_009")


# Searing Totem
class AT_132_SHAMANb:
	play = Summon(CONTROLLER, "CS2_050")


# Stoneclaw Totem
class AT_132_SHAMANc:
	play = Summon(CONTROLLER, "CS2_051")


# Wrath of Air Totem
class AT_132_SHAMANd:
	play = Summon(CONTROLLER, "CS2_052")
