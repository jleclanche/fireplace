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

class LOOT_043:
	"Lesser Amethyst Spellstone"
	play = Hit(TARGET, 3), Heal(FRIENDLY_HERO, 3)
	class Hand:
		events = Predamage(FRIENDLY_HERO, CONTROLLER).on(Morph(SELF, 'LOOT_043t2'))

class LOOT_043t2:
	"Amethyst Spellstone"
	play = Hit(TARGET, 5), Heal(FRIENDLY_HERO, 5)
	class Hand:
		events = Predamage(FRIENDLY_HERO, CONTROLLER).on(Morph(SELF, 'LOOT_043t3'))

class LOOT_043t3:
	"Greater Amethyst Spellstone"
	play = Hit(TARGET, 7), Heal(FRIENDLY_HERO, 7)

