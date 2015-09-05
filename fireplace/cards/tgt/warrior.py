from ..utils import *


##
# Minions

# Orgrimmar Aspirant
class AT_066:
	inspire = Buff(FRIENDLY_WEAPON, "AT_066e")


# Magnataur Alpha
class AT_067:
	events = Attack(SELF).on(CLEAVE)


# Sparring Partner
class AT_069:
	play = SetTag(TARGET, {GameTag.TAUNT: True})


# Alexstrasza's Champion
class AT_071:
	play = HOLDING_DRAGON & Buff(SELF, "AT_071e")


# Sea Reaver
class AT_130:
	in_hand = Draw(CONTROLLER, SELF).on(Hit(FRIENDLY_MINIONS, 1))


##
# Spells

# Bash
class AT_064:
	play = Hit(TARGET, 3), GainArmor(FRIENDLY_HERO, 3)


# Bolster
class AT_068:
	play = Buff(FRIENDLY_MINIONS + TAUNT, "AT_068e")


##
# Weapons

# King's Defender
class AT_065:
	play = Find(FRIENDLY_MINIONS + TAUNT) & Buff(SELF, "AT_065e")
