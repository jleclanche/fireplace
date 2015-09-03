from ..utils import *


##
# Hero Powers

# Lightning Jolt
class AT_050t:
	play = Hit(TARGET, 2)


##
# Minions

# Tuskarr Totemic
class AT_046:
	play = Summon(CONTROLLER, RandomTotem())


# Draenei Totemcarver
class AT_047:
	play = Buff(SELF, "AT_047e") * Count(FRIENDLY_MINIONS + TOTEM)


# Thunder Bluff Valiant
class AT_049:
	inspire = Buff(FRIENDLY_MINIONS + TOTEM, "AT_049e")


# The Mistcaller
class AT_054:
	# The Enchantment ID is correct
	play = Buff(FRIENDLY + (IN_DECK | IN_HAND), "AT_045e")


##
# Spells

# Healing Wave
class AT_048:
	play = JOUST & Heal(TARGET, 7) | Heal(TARGET, 14)


# Elemental Destruction
class AT_051:
	play = Hit(ALL_MINIONS, RandomNumber(4, 5))


# Ancestral Knowledge
class AT_053:
	play = Draw(CONTROLLER) * 2


##
# Weapons

#  Charged Hammer
class AT_050:
	deathrattle = Summon(CONTROLLER, "AT_050t")
