"""
Who's the Boss Now?
"""

from ..utils import *

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


# Open the Gates
class BRMA09_2_TB:
	activate = Summon(CONTROLLER, "BRMA09_2t") * 3


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
		Dead(Hit.TARGET) & Summon(CONTROLLER, "NAX11_03")
	)


# Decimate
class NAX12_02H_2_TB:
	activate = Buff(ENEMY_MINIONS, "NAX12_02e")

# Decimate (Unused)
class NAX12_02H_2c_TB:
	play = Buff(ENEMY_MINIONS, "NAX12_02e")
