"""
GAME set and other special cards
"""
from ..utils import *


# AFK
class GAME_004:
	update = Refresh(CONTROLLER, {GameTag.TIMEOUT: 10})


# The Coin
class GAME_005:
	play = ManaThisTurn(CONTROLLER, 1)


# Big Banana
class TB_006:
	play = Buff(TARGET, "TB_006e")


# Deviate Banana
class TB_007:
	play = SwapAttackAndHealth(TARGET, "TB_007e")


# Rotten Banana
class TB_008:
	play = Hit(TARGET, 1)


# Boom Bot Jr.
class TB_MechWar_Boss2_HeroPower:
	activate = Hit(RANDOM_ENEMY_CHARACTER, 1) * 2


# Mysterious Pilot
class TB_Pilot1:
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=Attr(SELF, GameTag.COST)))


##
# Tavern Brawl: Who's The Boss Now?

# Pile On!!!
class BRMA01_2H_2_TB:
	activate = (
		Summon(CONTROLLER, RANDOM(CONTROLLER_DECK + MINION)),
		Summon(OPPONENT, RANDOM(OPPONENT_DECK + MINION))
	)


# Jeering Crowd
class BRMA02_2_2_TB:
	activate = Summon(CONTROLLER, "BRMA02_2t")

# Jeering Crowd (Unused)
class BRMA02_2_2c_TB:
	play = Summon(CONTROLLER, "BRMA02_2t")


# The Majordomo
class BRMA06_2H_TB:
	activate = Summon(CONTROLLER, "BRMA06_4H")


# ME SMASH!
class BRMA07_2_2_TB:
	activate = Destroy(RANDOM_ENEMY_MINION)

# ME SMASH! (Unused)
class BRMA07_2_2c_TB:
	play = Destroy(RANDOM_ENEMY_MINION)


# Activate!
class BRMA14_10H_TB:
	Summon(CONTROLLER, RandomEntourage())


# Wild Magic
class BRMA13_4_2_TB:
	activate = Give(CONTROLLER, RandomSpell(card_class=Attr(ENEMY_HERO, GameTag.CLASS)))


# Web Wrap
class NAX3_02_TB:
	activate = Bounce(RANDOM_ENEMY_MINION)


# Harvest
class NAX8_02H_TB:
	activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1)


# Decimate
class NAX12_02H_2_TB:
	activate = Buff(ENEMY_MINIONS, "NAX12_02e")

# Decimate (Unused)
class NAX12_02H_2c_TB:
	play = Buff(ENEMY_MINIONS, "NAX12_02e")
