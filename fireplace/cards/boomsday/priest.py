from ..utils import *


##
# Minions

class BOT_216:
	"""Omega Medic"""
	pass


class BOT_258:
	"""Zerek, Master Cloner"""
	pass


class BOT_509:
	"""Dead Ringer"""
	pass


class BOT_558:
	"""Test Subject"""
	pass


class BOT_566:
	"""Reckless Experimenter"""
	pass


##
# Spells

class BOT_219:
	"""Extra Arms"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class BOT_435:
	"""Cloning Device"""
	pass


class BOT_517:
	"""Topsy Turvy"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class BOT_529:
	"""Power Word: Replicate"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class BOT_567:
	"""Zerek's Cloning Gallery"""
	pass
