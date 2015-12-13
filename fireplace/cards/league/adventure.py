from ..utils import *


##
# Spells

# Medivh's Locket
class LOEA16_12:
	play = Morph(FRIENDLY_HAND, "GVG_003")


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
