from ..utils import *

##
# Minions

class CFM_020:
	"Raza the Chained"
	play = Buff(CONTROLLER, "CFM_020e")

class CFM_020e:
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.COST: SET(0)})

#class CFM_605:
#	"Drakonid Operative"

class CFM_606:
	"Mana Geode"
	events = Heal(SELF).on(Summon(CONTROLLER, "CFM_606t"))

#class CFM_626:
#	"Kabal Talonpriest"

#class CFM_657:
#	"Kabal Songstealer"

##
# Spells

#class CFM_603:
#	"Potion of Madness"

#class CFM_604:
#	"Greater Healing Potion"

#class CFM_661:
#	"Pint-Size Potion"

#class CFM_662:
#	"Dragonfire Potion"

