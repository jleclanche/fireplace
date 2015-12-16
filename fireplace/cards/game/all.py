"""
GAME set and other special cards
"""
from ..utils import *


# Luck of the Coin
GAME_001 = buff(health=3)


# Coin's Vengeance
class GAME_003:
	events = Play(CONTROLLER, MINION).on(Buff(Play.CARD, "GAME_003e"), Destroy(SELF))

GAME_003e = buff(+1, +1)


# AFK
class GAME_004:
	update = Refresh(CONTROLLER, {GameTag.TIMEOUT: 10})


# The Coin
class GAME_005:
	play = ManaThisTurn(CONTROLLER, 1)


# Big Banana
class TB_006:
	play = Buff(TARGET, "TB_006e")

TB_006e = buff(+2, +2)


# Deviate Banana
class TB_007:
	play = SwapAttackAndHealth(TARGET, "TB_007e")


# Rotten Banana
class TB_008:
	play = Hit(TARGET, 1)


# Tarnished Coin
class TB_011:
	play = ManaThisTurn(CONTROLLER, 1)


# Hello! Hello! Hello!
class TB_MechWar_Boss1_HeroPower:
	activate = SetTag(LOWEST_ATK(FRIENDLY_MINIONS), (GameTag.TAUNT, GameTag.DIVINE_SHIELD))


# Boom Bot Jr.
class TB_MechWar_Boss2_HeroPower:
	activate = Hit(RANDOM_ENEMY_CHARACTER, 1) * 2


# Mysterious Pilot
class TB_Pilot1:
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=COST(SELF)))
	tags = {GameTag.DEATHRATTLE: True}


##
# Tavern Brawl: Who's The Boss Now?

# Pile On!!!
class BRMA01_2H_2_TB:
	activate = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))
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


# Bone Minions
class BRMA17_5_TB:
	activate = Summon(CONTROLLER, "BRMA17_6") * 2


# Web Wrap
class NAX3_02_TB:
	activate = Bounce(RANDOM_ENEMY_MINION)


# Harvest
class NAX8_02H_TB:
	activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1)


# Poison Cloud
class NAX11_02H_2_TB:
	activate = Hit(ENEMY_MINIONS, 1).then(
		Dead(Hit.TARGETS) & Summon(CONTROLLER, "NAX11_03")
	)


# Decimate
class NAX12_02H_2_TB:
	activate = Buff(ENEMY_MINIONS, "NAX12_02e")

# Decimate (Unused)
class NAX12_02H_2c_TB:
	play = Buff(ENEMY_MINIONS, "NAX12_02e")
