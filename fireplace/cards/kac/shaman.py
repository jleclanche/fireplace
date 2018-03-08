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

class LOOT_064:
	"Lesser Sapphire Spellstone"
#	overload_count = 0
	play = Summon(CONTROLLER, Copy(TARGET))
#	class Hand:
#		events = Overload(CONTROLLER).on(overload_count -= 1) * Overload.AMOUNT)
#		events = GainArmor(FRIENDLY_HERO).on((overload_count < 3) | Morph(SELF, 'LOOT_064t1'))


class LOOT_064t1:
	"Sapphire Spellstone"
#	overload_count_2 = 0
	play = Summon(CONTROLLER, Copy(TARGET)) * 2
#	class Hand:
#		events = Overload(CONTROLLER).on(overload_count_2 -= 1) * Overload.AMOUNT)
#		events = GainArmor(FRIENDLY_HERO).on((overload_count_2 < 3) | Morph(SELF, 'LOOT_064t2'))

class LOOT_064t2:
	"Greater Sapphire Spellstone"
	play = Summon(CONTROLLER, Copy(TARGET)) * 3
