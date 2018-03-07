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

class LOOT_051:
	"Lesser Jasper Spellstone"
#	armor_count = 0
	play = Hit(TARGET, 2)
#	class Hand:
#		armor_count += GainArmor(FRIENDLY_HERO)
#		events = GainArmor(FRIENDLY_HERO).on((armor_count < 3) | Morph(SELF, 'LOOT_051t2'))

class LOOT_051t2:
	"Jasper Spellstone"
#	armor_count_2 = 0
	play = Hit(TARGET, 4)
#	class Hand:
#		armor_count_2 += GainArmor(FRIENDLY_HERO)
#		events = GainArmor(FRIENDLY_HERO).on((armor_count_2 < 3) | Morph(SELF, 'LOOT_051t3'))

class LOOT_051t3:
	"Greater Jasper Spellstone"
	play = Hit(TARGET, 6)

##
# Weapons

