"""
Who's the Boss Now?
"""

from ..utils import *


class BRMA01_2H_2_TB:
	"""Pile On!!!"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = (
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))
	)


class BRMA02_2_2_TB:
	"""Jeering Crowd"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA02_2t")


class BRMA02_2_2c_TB:
	"""Jeering Crowd (Unused)"""
	play = Summon(CONTROLLER, "BRMA02_2t")


class BRMA06_2H_TB:
	"""The Majordomo"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA06_4H")


class BRMA07_2_2_TB:
	"""ME SMASH"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	activate = Destroy(RANDOM_ENEMY_MINION)


class BRMA07_2_2c_TB:
	"""ME SMASH (Unused)"""
	play = Destroy(RANDOM_ENEMY_MINION)


class BRMA09_2_TB:
	"""Open the Gates"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA09_2t") * 3


class BRMA14_10H_TB:
	"""Activate!"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	entourage = ["BRMA14_3", "BRMA14_5", "BRMA14_7", "BRMA14_9"]
	Summon(CONTROLLER, RandomEntourage())


class BRMA13_4_2_TB:
	"""Wild Magic"""
	activate = Give(CONTROLLER, RandomSpell(card_class=Attr(ENEMY_HERO, GameTag.CLASS)))


class BRMA17_5_TB:
	"""Bone Minions"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	activate = Summon(CONTROLLER, "BRMA17_6") * 2


class NAX3_02_TB:
	"""Web Wrap"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	activate = Bounce(RANDOM_ENEMY_MINION)


class NAX8_02H_TB:
	"""Harvest"""
	activate = Draw(CONTROLLER), GainMana(CONTROLLER, 1)


class NAX11_02H_2_TB:
	"""Poison Cloud"""
	activate = Hit(ENEMY_MINIONS, 1).then(
		Dead(Hit.TARGET) & Summon(CONTROLLER, "NAX11_03")
	)


class NAX12_02H_2_TB:
	"""Decimate"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	activate = Buff(ENEMY_MINIONS, "NAX12_02e")


class NAX12_02H_2c_TB:
	"""Decimate (Unused)"""
	play = Buff(ENEMY_MINIONS, "NAX12_02e")
