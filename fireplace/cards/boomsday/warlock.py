from ..utils import *


##
# Minions

class BOT_224:
	"""Doubling Imp"""
	pass


class BOT_226:
	"""Nethersoul Buster"""
	pass


class BOT_433:
	"""Dr. Morrigan"""
	pass


class BOT_443:
	"""Void Analyst"""
	pass


class BOT_536:
	"""Omega Agent"""
	pass


##
# Spells

class BOT_222:
	"""Spirit Bomb"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class BOT_263:
	"""Soul Infusion"""
	pass


class BOT_521:
	"""Ectomancy"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class BOT_568:
	"""The Soularium"""
	pass


class BOT_913:
	"""Demonic Project"""
	pass
