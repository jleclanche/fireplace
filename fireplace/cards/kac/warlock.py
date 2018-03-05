from ..utils import *

##
# Minions

class LOOT_013:
	"Vulgar Homunculus"
	play = Hit(FRIENDLY_HERO, 2)

class LOOT_014:
	"Kobold Librarian"
	play = Draw(CONTROLLER), Hit(FRIENDLY_HERO, 2)

class LOOT_018:
	"Hooked Reaver"
	powered_up = CURRENT_HEALTH(FRIENDLY_HERO) <= 15
	play = powered_up & Buff(SELF, "LOOT_018e")

LOOT_018e = buff(+3, +3, taunt=True)

##
# Spells

class LOOT_017:
	"Dark Pact"
	play = Destroy(TARGET), Heal(FRIENDLY_HERO, 8)
