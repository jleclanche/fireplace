from ..utils import *


##
# Hero Powers

class HERO_10bp:
	"""Demon Claws"""
	activate = Buff(FRIENDLY_HERO, "HERO_10bpe")


HERO_10bpe = buff(atk=1)


##
# Minions

class BT_142:
	"""Shadowhoof Slayer"""
	play = Buff(FRIENDLY_HERO, "BT_142e")


BT_142e = buff(atk=1)


class BT_323:
	"""Sightless Watcher"""
	play = Choice(CONTROLLER, RANDOM(FRIENDLY_DECK) * 3).then(
		PutOnTop(CONTROLLER, Choice.CARD))


class BT_352:
	"""Satyr Overseer"""
	events = Attack(FRIENDLY_HERO).after(
		Summon(CONTROLLER, "BT_352t")
	)


class BT_495:
	"""Glaivebound Adept"""
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE_AND_HERO_ATTACKED_THIS_TURN: 0}
	play = Hit(TARGET, 4)

##
# Spells


class BT_036:
	"""Coordinated Strike"""
	play = Summon(CONTROLLER, "BT_036t") * 3


class Prologue_ChaosStrike:
	"""Chaos Strike"""
	play = Buff(FRIENDLY_HERO, "BT_035e"), Draw(CONTROLLER)


BT_035e = buff(atk=2)


class BT_740:
	"""Soul Cleave"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	play = Hit(RANDOM_ENEMY_MINION * 2, 2)


class Prologue_ChaosNova:
	"""Chaos Nova"""
	play = Hit(ALL_MINIONS, 4)


class BT_512:
	"""Inner Demon"""
	play = Buff(CONTROLLER, "BT_512e")


BT_512e = buff(atk=8)
