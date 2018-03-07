from ..utils import *

##
# Minions

##
# Spells

class LOOT_047:
	"Barkskin"
	play = Buff(TARGET, 'LOOT_047e'), GainArmor(FRIENDLY_HERO, 3)

LOOT_047e = buff(health=3)

##
# Weapons

