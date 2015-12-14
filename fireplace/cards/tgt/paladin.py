from ..utils import *


##
# Minions

# Warhorse Trainer
class AT_075:
	update = Refresh(FRIENDLY + ID("CS2_101t"), buff="AT_075e")

AT_075e = buff(atk=1)


# Murloc Knight
class AT_076:
	inspire = Summon(CONTROLLER, RandomMurloc())


# Mysterious Challenger
class AT_079:
	play = Summon(CONTROLLER, FRIENDLY_DECK + SECRET)


# Eadric the Pure
class AT_081:
	play = Buff(ENEMY_MINIONS, "AT_081e")

class AT_081e:
	atk = SET(1)


# Tuskarr Jouster
class AT_104:
	play = JOUST & Heal(FRIENDLY_HERO, 7)


##
# Spells

# Seal of Champions
class AT_074:
	play = Buff(TARGET, "AT_074e2"), GiveDivineShield(TARGET)

AT_074e2 = buff(atk=3)


##
# Secrets

# Competitive Spirit
class AT_073:
	events = OWN_TURN_BEGIN.on(EMPTY_BOARD | (
		Reveal(SELF), Buff(FRIENDLY_MINIONS, "AT_073e")
	))

AT_073e = buff(+1, +1)


##
# Weapons

# Argent Lance
class AT_077:
	play = JOUST & Buff(SELF, "AT_077e")

AT_077e = buff(health=1)
