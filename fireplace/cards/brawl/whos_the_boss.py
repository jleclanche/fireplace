"""
Who's the Boss Now?
"""

from ..utils import *

class BRMA01_2H_2_TB:
	"Pile On!!!"
	activate = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))
	)


class BRMA02_2_2_TB:
	"Jeering Crowd"
	activate = Summon(CONTROLLER, "BRMA02_2t")

class BRMA02_2_2c_TB:
	"Jeering Crowd (Unused)"
	play = Summon(CONTROLLER, "BRMA02_2t")


class BRMA06_2H_TB:
	"The Majordomo"
	activate = Summon(CONTROLLER, "BRMA06_4H")


class BRMA07_2_2_TB:
	"ME SMASH"
	activate = Destroy(RANDOM_ENEMY_MINION)

class BRMA07_2_2c_TB:
	"ME SMASH (Unused)"
	play = Destroy(RANDOM_ENEMY_MINION)


class BRMA09_2_TB:
	"Open the Gates"
	activate = Summon(CONTROLLER, "BRMA09_2t") * 3


class BRMA14_10H_TB:
	"Activate!"
	Summon(CONTROLLER, RandomEntourage())


class BRMA13_4_2_TB:
	"Wild Magic"
	activate = Give(CONTROLLER, RandomSpell(card_class=Attr(ENEMY_HERO, GameTag.CLASS)))


class BRMA17_5_TB:
	"Bone Minions"
	activate = Summon(CONTROLLER, "BRMA17_6") * 2


class NAX3_02_TB:
	"Web Wrap"
	activate = Bounce(RANDOM_ENEMY_MINION)


class NAX8_02H_TB:
	"Harvest"
	activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1)


class NAX11_02H_2_TB:
	"Poison Cloud"
	activate = Hit(ENEMY_MINIONS, 1).then(
		Dead(Hit.TARGET) & Summon(CONTROLLER, "NAX11_03")
	)


class NAX12_02H_2_TB:
	"Decimate"
	activate = Buff(ENEMY_MINIONS, "NAX12_02e")

class NAX12_02H_2c_TB:
	"Decimate (Unused)"
	play = Buff(ENEMY_MINIONS, "NAX12_02e")
