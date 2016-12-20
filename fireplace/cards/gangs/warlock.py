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

#class CFM_750:
#	"Krul the Unshackled"

#class CFM_751:
#	"Abyssal Enforcer"

#class CFM_900:
#	"Unlicensed Apothecary"

##
# Spells

#class CFM_094:
#	"Felfire Potion"

#class CFM_608:
#	"Blastcrystal Potion"

#class CFM_611:
#	"Bloodfury Potion"

