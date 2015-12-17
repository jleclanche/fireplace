from ..utils import *


##
# Spells

# Medivh's Locket
class LOEA16_12:
	play = Morph(FRIENDLY_HAND, "GVG_003")


##
# Zinaar

RandomWish = RandomID("LOEA02_03", "LOEA02_04", "LOEA02_05", "LOEA02_06", "LOEA02_10")

# Djinn's Intuition
class LOEA02_02:
	activate = Draw(CONTROLLER), Give(OPPONENT, RandomWish)

class LOEA02_02h:
	activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1), Give(OPPONENT, RandomWish)


# Wish for Power
class LOEA02_03:
	play = Discover(RandomSpell())


# Wish for Valor
class LOEA02_04:
	play = Discover(RandomCollectible(cost=4))


# Wish for Glory
class LOEA02_05:
	play = Discover(RandomMinion())


# Wish for More Wishes
class LOEA02_06:
	play = Discover(RandomWish)


# Wish for Companionship
class LOEA02_10:
	play = Discover(RandomID("NEW1_032", "NEW1_033", "NEW1_034"))


# Leokk (Unused)
class LOEA02_10a:
	update = Refresh(FRIENDLY_MINIONS - SELF, buff="NEW1_033o")


##
# Temple Escape events

# Pit of Spikes
class LOEA04_06:
	choose = ("LOEA04_06a", "LOEA04_06b")

# Swing Across
class LOEA04_06a:
	play = COINFLIP & Hit(FRIENDLY_HERO, 10)

# Walk Across Gingerly
class LOEA04_06b:
	play = Hit(FRIENDLY_HERO, 5)


# A Glowing Pool
class LOEA04_28:
	choose = ("LOEA04_28a", "LOEA04_28b")

# Drink Deeply
class LOEA04_28a:
	play = Draw(CONTROLLER)

# Wade Through
class LOEA04_28b:
	play = GainMana(CONTROLLER, 1)


# The Eye
class LOEA04_29:
	choose = ("LOEA04_29a", "LOEA04_29b")

# Touch It
class LOEA04_29a:
	play = Heal(FRIENDLY_HERO, 10)

# Investigate the Runes
class LOEA04_29b:
	play = Draw(CONTROLLER) * 2


# The Darkness
class LOEA04_30:
	choose = ("LOEA04_30a", "LOEA04_31b")

# Take the Shortcut
class LOEA04_30a:
	play = Summon(OPPONENT, "CS2_186")

# Do Nothing
class LOEA04_31b:
	pass


##
# Mine Cart Rush

# Dynamite
class LOEA07_18:
	play = Hit(TARGET, 10)


# Boom!
class LOEA07_20:
	play = Hit(ENEMY_MINIONS, 3)


# Consult Brann
class LOEA07_26:
	play = Draw(CONTROLLER) * 3


# Repairs
class LOEA07_28:
	play = Heal(TARGET, 10)


# Throw Rocks
class LOEA07_29:
	play = Hit(RANDOM_ENEMY_MINION, 3)
