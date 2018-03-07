from ..utils import *

##
# Minions

class LOOT_048:
	"Ironwood Golem"
	update = (ARMOR(FRIENDLY_HERO) < 3) & Refresh(SELF, {GameTag.CANT_ATTACK: True})

##
# Spells

class LOOT_047:
	"Barkskin"
	play = Buff(TARGET, 'LOOT_047e'), GainArmor(FRIENDLY_HERO, 3)

LOOT_047e = buff(health=3)

##
# Weapons

