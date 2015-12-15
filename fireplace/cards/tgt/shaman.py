from ..utils import *


##
# Minions

# Tuskarr Totemic
class AT_046:
	play = Summon(CONTROLLER, RandomTotem())


# Draenei Totemcarver
class AT_047:
	play = Buff(SELF, "AT_047e") * Count(FRIENDLY_MINIONS + TOTEM)

AT_047e = buff(+1, +1)


# Thunder Bluff Valiant
class AT_049:
	inspire = Buff(FRIENDLY_MINIONS + TOTEM, "AT_049e")

AT_049e = buff(+1, +1)


# The Mistcaller
class AT_054:
	# The Enchantment ID is correct
	play = Buff(FRIENDLY_HAND | FRIENDLY_DECK, "AT_045e")

AT_045e = buff(+1, +1)


##
# Spells

# Healing Wave
class AT_048:
	play = JOUST & Heal(TARGET, 14) | Heal(TARGET, 7)


# Elemental Destruction
class AT_051:
	play = Hit(ALL_MINIONS, RandomNumber(4, 5))


# Ancestral Knowledge
class AT_053:
	play = Draw(CONTROLLER) * 2


##
# Weapons

# Charged Hammer
class AT_050:
	deathrattle = Summon(CONTROLLER, "AT_050t")

class AT_050t:
	activate = Hit(TARGET, 2)
