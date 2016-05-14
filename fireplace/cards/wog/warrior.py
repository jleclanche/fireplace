from ..utils import *


##
# Minions

class OG_149:
	"Ravaging Ghoul"
	play = Hit(ALL_MINIONS - SELF, 1)


class OG_218:
	"Bloodhoof Brave"
	enrage = Refresh(SELF, buff="OG_218e")

OG_218e = buff(atk=3)


class OG_220:
	"Malkorok"
	play = Summon(CONTROLLER, RandomWeapon())


class OG_312:
	"N'Zoth's First Mate"
	play = Summon(CONTROLLER, "OG_058")


class OG_315:
	"Bloodsail Cultist"
	play = Find(FRIENDLY_MINIONS + PIRATE - SELF) & Buff(FRIENDLY_WEAPON, "OG_315e")

OG_315e = buff(+1, +1)


##
# Spells

class OG_276:
	"Blood Warriors"
	play = Give(CONTROLLER, Copy(FRIENDLY_MINIONS + DAMAGED))


class OG_314:
	"Blood To Ichor"
	play = Hit(TARGET,1), Dead(TARGET) | Summon(CONTROLLER, "OG_314b")


##
# Weapons

class OG_033:
	"Tentacles for Arms"
	deathrattle = Bounce(SELF)
