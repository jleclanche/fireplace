from ..utils import *

##
# Minions

class CFM_342:
	"Luckydo Buccaneer"
	powered_up = Find(FRIENDLY_WEAPON + (ATK >= 3)) 
	play = powered_up & Buff(SELF, "CFM_342e")

CFM_342e = buff(+4, +4)

#class CFM_634:
#	"Lotus Assassin"

#class CFM_691:
#	"Jade Swarmer"

#class CFM_693:
#	"Gadgetzan Ferryman"

#class CFM_694:
#	"Shadow Sensei"

#class CFM_781:
#	"Shaku, the Collector"

##
# Spells

#class CFM_630:
#	"Counterfeit Coin"

#class CFM_690:
#	"Jade Shuriken"

