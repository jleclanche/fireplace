from ..utils import *

##
# Minions

class CFM_315:
	"Alleycat"
	play = Summon(CONTROLLER, "CFM_315t")

# class CFM_316:
# 	"Rat Pack"
#	TODO: Find a way to cache the atk value before death
# 	deathrattle = Summon(CONTROLLER, "CFM_316t") * ATK(SELF)

#class CFM_333:
#	"Knuckles"

# class CFM_335:
# 	"Dispatch Kodo"
#	TODO: Battlecry needs to resolve after aura refresh to be accurate
# 	play = Hit(TARGET, ATK(SELF))

class CFM_336:
	"Shaky Zipgunner"
	deathrattle = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_336e")

CFM_336e = buff(+2, +2)

class CFM_338:
	"Trogg Beastrager"
	play = Buff(RANDOM(FRIENDLY_HAND + MINION + BEAST), "CFM_338e")

CFM_338e = buff(+1, +1)

##
# Spells

class CFM_026:
	"Hidden Cache"
	secret = Play(OPPONENT, MINION).after(
		(Count(FRIENDLY_HAND + MINION) == 0) |
		(Reveal(SELF), Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_026e"))
		)

CFM_026e = buff(+2, +2)

class CFM_334:
	"Smuggler's Crate"
	play = Buff(RANDOM(FRIENDLY_HAND + MINION + BEAST), "CFM_334e")

CFM_334e = buff(+2, +2)

##
# Weapons

#class CFM_337:
	#"Piranha Launcher"

