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

class CFM_693:
	"Gadgetzan Ferryman"
	combo = Bounce(TARGET)

class CFM_694:
	"Shadow Sensei"
	play = Buff(TARGET, "CFM_694e")

CFM_694e = buff(+2, +2)

class CFM_781:
	"Shaku, the Collector"
	events = Attack(SELF).on(Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS)))

##
# Spells

class CFM_630:
	"Counterfeit Coin"
	play = ManaThisTurn(CONTROLLER, 1)

#class CFM_690:
#	"Jade Shuriken"

