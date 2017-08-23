from ..utils import *

##
# Minions

class CFM_061:
	"Jinyu Waterspeaker"
	play = Heal(TARGET, 6)

#class CFM_312:
#	"Jade Chieftain"

class CFM_324:
	"White Eyes"
	deathrattle = Shuffle(CONTROLLER, "CFM_324t")

class CFM_697:
	"Lotus Illusionist"
	events = Attack(SELF, ENEMY_HERO).after(Morph(SELF, RandomMinion(cost=6)))

##
# Spells

class CFM_310:
	"Call in the Finishers"
	play = Summon(CONTROLLER, "CFM_310t") * 4

class CFM_313:
	"Finders Keepers"
	#Force Shaman class cards or else will not work for other classes
	play = DISCOVER(RandomCollectible(card_class=CardClass.SHAMAN, overload=True))

#class CFM_696:
#	"Devolve"

class CFM_707:
	"Jade Lightning"
	play = Hit(TARGET, 4), Summon(CONTROLLER, JadeGolem())

##
# Weapons

class CFM_717:
	"Jade Claws"
	play = Summon(CONTROLLER, JadeGolem())

