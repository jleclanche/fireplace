from ..utils import *

##
# Minions

class CFM_315:
	"Alleycat"
	play = Summon(CONTROLLER, "CFM_315t")

#class CFM_316:
#	"Rat Pack"

#class CFM_333:
#	"Knuckles"

#class CFM_335:
#	"Dispatch Kodo"

class CFM_336:
	"Shaky Zipgunner"
	deathrattle = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_336e")

CFM_336e = buff(+2, +2)

#class CFM_338:
#	"Trogg Beastrager"

##
# Spells

#class CFM_026:
#	"Hidden Cache"

#class CFM_334:
#	"Smuggler's Crate"

##
# Weapons

#class CFM_337:
	#"Piranha Launcher"

