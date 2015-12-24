from ..utils import *


##
# Minions

# Shado-Pan Rider
class AT_028:
	combo = Buff(SELF, "AT_028e")

AT_028e = buff(atk=3)


# Buccaneer
class AT_029:
	events = Summon(FRIENDLY_WEAPON).on(Buff(Summon.TARGET, "AT_029e"))

AT_029e = buff(atk=1)


# Undercity Valiant
class AT_030:
	combo = Hit(TARGET, 1)


# Cutpurse
class AT_031:
	events = Attack(SELF, HERO).on(Give(CONTROLLER, "GAME_005"))


# Shady Dealer
class AT_032:
	play = Find(FRIENDLY_MINIONS + PIRATE) & Buff(SELF, "AT_032e")

AT_032e = buff(+1, +1)


# Anub'arak
class AT_036:
	deathrattle = Bounce(SELF), Summon(CONTROLLER, "AT_036t")


##
# Spells

# Burgle
class AT_033:
	play = Give(CONTROLLER, RandomCollectible(card_class=ENEMY_CLASS)) * 2


# Beneath the Grounds
class AT_035:
	play = Shuffle(OPPONENT, "AT_035t") * 3

class AT_035t:
	draw = Destroy(SELF), Summon(OPPONENT, "AT_036t"), Draw(CONTROLLER)


##
# Weapons

# Poisoned Blade
class AT_034:
	inspire = Buff(SELF, "AT_034e")

AT_034e = buff(atk=1)
