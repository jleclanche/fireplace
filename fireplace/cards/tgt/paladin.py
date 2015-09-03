from ..utils import *


##
# Minions

# Warhorse Trainer
class AT_075:
	update = Refresh(FRIENDLY + ID("CS2_101t"), "AT_075e")


# Murloc Knight
class AT_076:
	inspire = Summon(CONTROLLER, RandomMurloc())


# Eadric the Pure
class AT_081:
	play = Buff(ENEMY_MINIONS, "AT_081e")

class AT_081e:
	atk = lambda self, i: 1


# Tuskarr Jouster
class AT_104:
	play = JOUST & Heal(FRIENDLY_HERO, 7)


##
# Spells

# Seal of Champions
class AT_074:
	play = Buff(TARGET, "AT_074e2")


##
# Secrets

# Competitive Spirit
class AT_073:
	events = OWN_TURN_BEGIN.on(
		Buff(FRIENDLY_MINIONS, "AT_073e"), Reveal(SELF)
	)


##
# Weapons

# Argent Lance
class AT_077:
	play = JOUST & Buff(SELF, "AT_077e")
