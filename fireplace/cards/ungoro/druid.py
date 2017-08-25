from ..utils import *

##
# Minions

# class UNG_078:
# 	"Tortollan Forager"

class UNG_086:
	"Giant Anaconda"
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION + (ATK >= 5)))

# class UNG_100:
#	"Verdant Longneck"

class UNG_101:
	"Shellshifter"
	choose = ("UNG_101a", "UNG_101b")

class UNG_101a:
	play = Morph(SELF, "UNG_101t")

class UNG_101b:
	play = Morph(SELF, "UNG_101t2")

# class UNG_109:
#	"Elder Longneck"

##
# Spells

# class UNG_103:
#	"Evolving Spores"

class UNG_108:
	"Earthen Scales"
	play = Buff(TARGET, "UNG_108e"), GainArmor(FRIENDLY_HERO, ATK(TARGET))

UNG_108e = buff(+1, +1)

# class UNG_111:
# 	"Living Mana"

class UNG_111t1:
	deathrattle = GainMana(CONTROLLER, 1)

# class UNG_116:
#	"Jungle Giants"
