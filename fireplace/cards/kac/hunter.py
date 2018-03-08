from ..utils import *


##
# Minions

class LOOT_078:
	"Cave Hydra"
	events = Attack(SELF).on(CLEAVE)

##
# Spells

class LOOT_077:
	play = Hit(TARGET, 3), Summon(CONTROLLER, "LOOT_077t")