from ..utils import *


##
# Hero Powers

# Pile On!
class BRMA01_2:
	activate = (
		Summon(CONTROLLER, RANDOM(CONTROLLER_DECK + MINION)),
		Summon(OPPONENT, RANDOM(OPPONENT_DECK + MINION))
	)

class BRMA01_2H:
	activate = (
		Summon(CONTROLLER, RANDOM(CONTROLLER_DECK + MINION) * 2),
		Summon(OPPONENT, RANDOM(OPPONENT_DECK + MINION))
	)


# Jeering Crowd
class BRMA02_2:
	activate = Summon(CONTROLLER, "BRMA02_2t")

class BRMA02_2H:
	activate = Summon(CONTROLLER, "BRMA02_2t")


# Power of the Firelord
class BRMA03_2:
	activate = Hit(TARGET, 2)


# Magma Pulse
class BRMA04_2:
	activate = Hit(ALL_MINIONS, 1)


# The Majordomo
class BRMA06_2:
	activate = Summon(CONTROLLER, "BRMA06_4")

class BRMA06_2H:
	activate = Summon(CONTROLLER, "BRMA06_4H")


# ME SMASH
class BRMA07_2:
	activate = Destroy(RANDOM(ENEMY_MINIONS + DAMAGED))

class BRMA07_2H:
	activate = Destroy(RANDOM_ENEMY_MINION)


# The Rookery
class BRMA10_3:
	activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(CONTROLLER, "BRMA10_4")

# The Rookery
class BRMA10_3H:
	activate = Buff(ALL_MINIONS + ID("BRMA10_4"), "BRMA10_3e"), Summon(CONTROLLER, "BRMA10_4")


# Essence of the Red
class BRMA11_2:
	activate = Draw(ALL_PLAYERS) * 2

class BRMA11_2H:
	activate = Draw(ALL_PLAYERS) * 3, GainMana(CONTROLLER, 1)


# Mutation (Unused)
class BRMA12_10:
	activate = Discard(RANDOM(CONTROLLER_HAND))


##
# Minions

# Son of the Flame
class BRMA13_5:
	play = Hit(TARGET, 6)


##
# Spells

# Flameheart
class BRMA_01:
	play = Draw(CONTROLLER) * 2, GainArmor(FRIENDLY_HERO, 4)


# Get 'em!
class BRMA01_4:
	play = Summon(CONTROLLER, "BRMA01_4t") * 4


# TIME FOR SMASH
class BRMA07_3:
	play = Hit(RANDOM_ENEMY_MINION, 5), GainArmor(FRIENDLY_HERO, 5)


# Drakkisath's Command
class BRMA08_3:
	play = Destroy(TARGET), GainArmor(FRIENDLY_HERO, 10)


# The True Warchief
class BRMA09_6:
	play = Destroy(TARGET)


# Rock Out
class BRMA04_4:
	play = Summon(CONTROLLER, "BRMA04_3") * 3

class BRMA04_4H:
	play = Summon(CONTROLLER, "BRMA04_3H") * 3


# Burning Adrenaline
class BRMA11_3:
	play = Hit(ENEMY_HERO, 2)


##
# Weapons

# Razorgore's Claws (Unused)
class BRMA10_6:
	events = Death(MINION + ID("BRMA10_4")).on(Buff(SELF, "BRMA10_6e"))
