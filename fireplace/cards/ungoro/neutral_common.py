from ..utils import *

##
# Minions

# class UNG_001:
# 	"Pterrodax Hatchling"

# class UNG_009:
# 	"Ravasaur Runt"

class UNG_010:
	"Sated Threshadon"
	deathrattle = Summon(CONTROLLER, "UNG_201t") * 3

class UNG_073:
	"Rockpool Hunter"
	powered_up = Find(FRIENDLY_MINIONS + MURLOC)
	play = Buff(TARGET, "UNG_073e")

UNG_073e = buff(atk=+1, health=+1)

class UNG_076:
	"Eggnapper"
	deathrattle = Summon(CONTROLLER, "UNG_076t1") * 2

# class UNG_082:
# 	"Thunder Lizard"

class UNG_084:
	"Fire Plume Phoenix"
	play = Hit(TARGET, 2)

class UNG_205:
	"Glacial Shard"
	play = Freeze(TARGET)

class UNG_801:
	"Nesting Roc"
	powered_up = Count(FRIENDLY_MINIONS - SELF) >= 2
	play = powered_up & Taunt(SELF)

class UNG_803:
	"Emerald Reaver"
	play = Hit(FRIENDLY_HERO, 1), Hit(ENEMY_HERO, 1)

class UNG_809:
	"Fire Fly"
	play = Give(CONTROLLER, "UNG_809t1")

class UNG_818:
	"Volatile Elemental"
	deathrattle = Hit(RANDOM_ENEMY_MINION, 3)

class UNG_845:
	"Igneous Elemental"
	deathrattle = Give(CONTROLLER, "UNG_809t1") * 2

# class UNG_928:
# 	"Tar Creeper"

class UNG_937:
	"Primalfin Lookout"
	powered_up = Find(FRIENDLY_MINIONS + MURLOC - SELF)
	play = powered_up & Give(CONTROLLER, RandomMurloc())
