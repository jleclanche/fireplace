from ..utils import *


##
# Minions

# Dreadsteed
class AT_019:
	deathrattle = Summon(CONTROLLER, "AT_019")


# Tiny Knight of Evil
class AT_021:
	events = Discard(FRIENDLY).on(Buff(SELF, "AT_021e"))

AT_021e = buff(+1, +1)


# Void Crusher
class AT_023:
	inspire = Destroy(RANDOM_ENEMY_MINION | RANDOM_FRIENDLY_MINION)


# Wrathguard
class AT_026:
	events = Damage(SELF).on(Hit(FRIENDLY_HERO, Damage.AMOUNT))


# Wilfred Fizzlebang
class AT_027:
	events = Draw(CONTROLLER, None, FRIENDLY_HERO_POWER).on(Buff(Draw.CARD, "AT_027e"))

class AT_027e:
	cost = SET(0)


##
# Spells

# Fist of Jaraxxus
class AT_022:
	play = Hit(RANDOM_ENEMY_CHARACTER, 4)

	class Hand:
		events = Discard(SELF).on(Hit(RANDOM_ENEMY_CHARACTER, 4))


# Demonfuse
class AT_024:
	play = Buff(TARGET, "AT_024e"), GainMana(OPPONENT, 1)

AT_024e = buff(+3, +3)


# Dark Bargain
class AT_025:
	play = Destroy(RANDOM(ENEMY_MINIONS) * 2), Discard(RANDOM(FRIENDLY_HAND) * 2)
