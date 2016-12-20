from ..utils import *

##
# Minions

class CFM_610:
	"Crystalweaver"
	play = Buff(FRIENDLY_MINIONS + DEMON, "CFM_610e")

CFM_610e = buff(+1, +1)

class CFM_663:
	"Kabal Trafficker"
	events = OWN_TURN_END.on(Give(CONTROLLER, RandomDemon()))

#class CFM_699:
#	"Seadevil Stinger"

class CFM_750:
	"Krul the Unshackled"
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & Summon(CONTROLLER, FRIENDLY_HAND + DEMON)

class CFM_751:
	"Abyssal Enforcer"
	play = Hit(ALL_CHARACTERS - SELF, 3)

class CFM_900:
	"Unlicensed Apothecary"
	events = Summon(CONTROLLER).on(Hit(FRIENDLY_HERO, 5))

##
# Spells

class CFM_094:
	"Felfire Potion"
	play = Hit(ALL_CHARACTERS, 5)

#class CFM_608:
#	"Blastcrystal Potion"

#class CFM_611:
#	"Bloodfury Potion"

