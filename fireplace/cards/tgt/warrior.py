from ..utils import *


##
# Minions

# Orgrimmar Aspirant
class AT_066:
	inspire = Buff(FRIENDLY_WEAPON, "AT_066e")

AT_066e = buff(atk=1)


# Magnataur Alpha
class AT_067:
	events = Attack(SELF).on(CLEAVE)


# Sparring Partner
class AT_069:
	play = Taunt(TARGET)


# Alexstrasza's Champion
class AT_071:
	play = HOLDING_DRAGON & Buff(SELF, "AT_071e")

AT_071e = buff(atk=1, charge=True)


# Varian Wrynn
class AT_072:
	play = (Draw(CONTROLLER) * 3).then(
		Find(MINION + Draw.CARD) & Summon(CONTROLLER, Draw.CARD)
	)


# Sea Reaver
class AT_130:
	draw = Hit(FRIENDLY_MINIONS, 1)


##
# Spells

# Bash
class AT_064:
	play = Hit(TARGET, 3), GainArmor(FRIENDLY_HERO, 3)


# Bolster
class AT_068:
	play = Buff(FRIENDLY_MINIONS + TAUNT, "AT_068e")

AT_068e = buff(+2, +2)


##
# Weapons

# King's Defender
class AT_065:
	play = Find(FRIENDLY_MINIONS + TAUNT) & Buff(SELF, "AT_065e")

AT_065e = buff(health=1)
