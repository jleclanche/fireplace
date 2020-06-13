from ..utils import *


##
# Minions

class UNG_011:
	"""Hydrologist"""
	pass


class UNG_015:
	"""Sunkeeper Tarim"""
	pass


class UNG_953:
	"""Primalfin Champion"""
	pass


class UNG_962:
	"""Lightfused Stegodon"""
	pass


##
# Spells

class UNG_004:
	"""Dinosize"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class UNG_952:
	"""Spikeridged Steed"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


class UNG_954:
	"""The Last Kaleidosaur"""
	pass


class UNG_960:
	"""Lost in the Jungle"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class UNG_961:
	"""Adaptation"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


##
# Weapons

class UNG_950:
	"""Vinecleaver"""
	pass
