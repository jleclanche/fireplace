from ..utils import *

##
# Minions

class LOOT_062:
	"Kobold Hermit"
	choose = ("CS2_050", "CS2_051", "CS2_052", "NEW1_009")
	play = Summon(CONTROLLER, choose)

##
# Spells

class LOOT_060:
	"Crushing Hand"
	play = Hit(TARGET, 8)