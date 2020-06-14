from ..utils import *


##
# Minions

class ICC_047:
	"""Fatespinner"""


class ICC_051:
	"""Druid of the Swarm"""
	pass


class ICC_807:
	"""Strongshell Scavenger"""
	pass


class ICC_808:
	"""Crypt Lord"""
	pass


class ICC_835:
	"""Hadronox"""
	pass


##
# Spells

class ICC_050:
	"""Webweave"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class ICC_054:
	"""Spreading Plague"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	pass


class ICC_079:
	"""Gnash"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	pass


class ICC_085:
	"""Ultimate Infestation"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	pass


##
# Heros

class ICC_832:
	"""Malfurion the Pestilent"""
	pass
