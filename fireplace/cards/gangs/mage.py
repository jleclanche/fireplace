from ..utils import *

##
# Minions

class CFM_066:
	"Kabal Lackey"
	play = Buff(CONTROLLER, "EX1_612o")

class CFM_660:
	"Manic Soulcaster"
	play = Shuffle(CONTROLLER, Copy(TARGET))

class CFM_671:
	"Cryomancer"
	powered_up = Find(ENEMY_CHARACTERS + FROZEN)
	play = powered_up & Buff(SELF, "CFM_671e")

CFM_671e = buff(+2, +2)

#class CFM_687:
#	"Inkmaster Solia"

#class CFM_760:
#	"Kabal Crystal Runner"

##
# Spells

#class CFM_021:
#	"Freezing Potion"

#class CFM_065:
#	"Volcanic Potion"

#class CFM_620:
#	"Potion of Polymorph"

#class CFM_623:
#	"Greater Arcane Missiles"

