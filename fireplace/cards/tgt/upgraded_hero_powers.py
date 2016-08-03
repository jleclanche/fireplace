"""
Upgraded Hero Powers from Justicar Trueheart (AT_132)
"""
from ..utils import *


##
# Hero Powers

class AT_132_DRUID:
	"Dire Shapeshift"
	activate = Buff(FRIENDLY_HERO, "AT_132_DRUIDe"), GainArmor(FRIENDLY_HERO, 2)

AT_132_DRUIDe = buff(atk=2)


class AT_132_HUNTER:
	"Ballista Shot"
	activate = Hit(ENEMY_HERO, 3)

class DS1h_292_H1_AT_132:
	"Ballista Shot (Alleria Windrunner)"
	activate = AT_132_HUNTER.activate


class AT_132_MAGE:
	"Fireblast Rank 2"
	activate = Hit(TARGET, 2)

class CS2_034_H1_AT_132:
	"Fireblast Rank 2 (Medivh)"
	activate = AT_132_MAGE.activate

class CS2_034_H2_AT_132:
	"Fireblast Rank 2 (Khadgar)"
	activate = AT_132_MAGE.activate


class AT_132_PALADIN:
	"The Silver Hand"
	activate = Summon(CONTROLLER, "CS2_101t") * 2

class CS2_101_H1_AT_132:
	"The Silver Hand (Lady Liadrin)"
	activate = AT_132_PALADIN.activate


class AT_132_PRIEST:
	"Heal"
	activate = Heal(TARGET, 4)


class AT_132_ROGUE:
	"Poisoned Daggers"
	activate = Summon(CONTROLLER, "AT_132_ROGUEt")


class AT_132_WARRIOR:
	"Tank Up!"
	activate = GainArmor(FRIENDLY_HERO, 4)

class CS2_102_H1_AT_132:
	"Tank Up! (Magni Bronzebeard)"
	activate = AT_132_WARRIOR.activate


class AT_132_WARLOCK:
	"Soul Tap"
	activate = Draw(CONTROLLER)


class AT_132_SHAMAN:
	"Totemic Slam"
	choose = ("AT_132_SHAMANa", "AT_132_SHAMANb", "AT_132_SHAMANc", "AT_132_SHAMANd")

class CS2_049_H1_AT_132:
	"Totemic Slam (Morgl the Oracle)"
	choose = AT_132_SHAMAN.choose


class AT_132_SHAMANa:
	"Healing Totem"
	play = Summon(CONTROLLER, "NEW1_009")


class AT_132_SHAMANb:
	"Searing Totem"
	play = Summon(CONTROLLER, "CS2_050")


class AT_132_SHAMANc:
	"Stoneclaw Totem"
	play = Summon(CONTROLLER, "CS2_051")


class AT_132_SHAMANd:
	"Wrath of Air Totem"
	play = Summon(CONTROLLER, "CS2_052")
