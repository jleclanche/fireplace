from ..utils import *


##
# Minions

class BT_202:
	"""Helboar"""
	deathrattle = Buff(RANDOM(FRIENDLY_HAND + BEAST), "BT_202e")


BT_202e = buff(atk=1, health=1)


class BT_211:
	"""Imprisoned Felmaw"""
	dormant = 2
	awaken = Attack(SELF, RANDOM_ENEMY_CHARACTER)


class BT_201:
	"""Augmented Porcupine"""
	deathrattle = Hit(RANDOM_ENEMY_CHARACTER, 1) * ATK(SELF)


class BT_210:
	"""Zixor, Apex Predator"""
	deathrattle = Shuffle(CONTROLLER, "BT_210t")


class BT_210t:
	play = Summon(CONTROLLER, ExactCopy(SELF)) * 2


class BT_212:
	"""Mok'Nathal Lion"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	play = Buff(SELF, "BT_212e").then(CopyDeathrattles(Buff.BUFF, TARGET))


BT_212e = buff(deathrattle=True)


class BT_214:
	"""Beastmaster Leoroxx"""
	play = Summon(CONTROLLER, FRIENDLY_HAND + BEAST) * 3


##
# Spells

class BT_213:
	"""Scavenger's Ingenuity"""
	play = ForceDraw(RANDOM(FRIENDLY_DECK + BEAST)).then(
		Buff(ForceDraw.TARGET, "BT_213e"))


BT_213e = buff(atk=2, health=2)


class BT_203:
	"""Pack Tactics"""
	secret = Attack(CHARACTER, FRIENDLY_MINIONS).on(FULL_BOARD | (
		Summon(CONTROLLER, ExactCopy(Attack.DEFENDER)).then(
			Buff(Summon.CARD, "BT_203e")
		)))


class BT_203e:
	atk = SET(3)
	max_health = SET(3)


class BT_205:
	"""Scrap Shot"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 3), Buff(FRIENDLY_HAND + BEAST, "BT_205e")


BT_205e = buff(atk=3, health=3)


class BT_163:
	"""Nagrand Slam"""
	play = Summon(CONTROLLER, "BT_163t").then(
		Attack(Summon.CARD, RANDOM_ENEMY_CHARACTER)) * 4
