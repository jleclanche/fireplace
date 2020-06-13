from ..utils import *


##
# Minions

class BOT_243:
	"""Myra Rotspring"""
	pass


class BOT_283:
	"""Pogo-Hopper"""
	pass


class BOT_288:
	"""Lab Recruiter"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	pass


class BOT_565:
	"""Blightnozzle Crawler"""
	pass


class BOT_576:
	"""Crazed Chemist"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_FOR_COMBO: 0}
	pass


##
# Spells

class BOT_084:
	"""Violet Haze"""
	pass


class BOT_087:
	"""Academic Espionage"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	pass


class BOT_242:
	"""Myra's Unstable Element"""
	pass


class BOT_508:
	"""Necrium Vial"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	pass


##
# Weapons

class BOT_286:
	"""Necrium Blade"""
	pass
