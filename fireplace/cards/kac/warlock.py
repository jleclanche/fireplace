from ..utils import *

##
# Minions

class LOOT_013:
	"Vulgar Homunculus"
	play = Hit(FRIENDLY_HERO, 2)

class LOOT_014:
	"Kobold Librarian"
	play = Draw(CONTROLLER), Hit(FRIENDLY_HERO, 2)

##
# Spells

