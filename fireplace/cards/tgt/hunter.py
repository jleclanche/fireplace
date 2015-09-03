from ..utils import *


##
# Minions

# Ram Wrangler
class AT_010:
	play = Find(FRIENDLY_MINIONS + BEAST) & Summon(CONTROLLER, RandomBeast())


# Stablemaster
class AT_057:
	play = Buff(TARGET, "AT_057o")


# Brave Archer
class AT_059:
	inspire = Find(CONTROLLER_HAND) | Hit(ENEMY_HERO, 2)


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
	events = Attack(CHARACTER, FRIENDLY_HERO).after(Summon(CONTROLLER, "CS2_125"))
