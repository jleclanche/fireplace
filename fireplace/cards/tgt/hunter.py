from ..utils import *


##
# Minions

# Ram Wrangler
class AT_010:
	play = Find(FRIENDLY_MINIONS + BEAST) & Summon(CONTROLLER, RandomBeast())


# Stablemaster
class AT_057:
	play = Buff(TARGET, "AT_057o")

AT_057o = buff(immune=True)


# King's Elekk
class AT_058:
	play = JOUST & Draw(CONTROLLER, Joust.CHALLENGER)


# Brave Archer
class AT_059:
	inspire = EMPTY_HAND & Hit(ENEMY_HERO, 2)


# Acidmaw
class AT_063:
	events = Damage(MINION - SELF).on(Destroy(Damage.TARGET))


# Dreadscale
class AT_063t:
	events = OWN_TURN_END.on(Hit(ALL_MINIONS - SELF, 1))


##
# Spells

# Powershot
class AT_056:
	play = Hit(TARGET | TARGET_ADJACENT, 2)


# Lock and Load
class AT_061:
	play = Buff(FRIENDLY_HERO, "AT_061e")

class AT_061e:
	events = OWN_SPELL_PLAY.on(
		Give(CONTROLLER, RandomCollectible(card_class=CardClass.HUNTER))
	)


# Ball of Spiders
class AT_062:
	play = Summon(CONTROLLER, "FP1_011") * 3


##
# Secrets

# Bear Trap
class AT_060:
	secret = Attack(CHARACTER, FRIENDLY_HERO).after(FULL_BOARD | (
		Reveal(SELF), Summon(CONTROLLER, "CS2_125")
	))
