from ..utils import *


##
# Minions

class DRG_089:
	"""Dragonqueen Alexstrasza"""
	# [x]<b>Battlecry:</b> If your deck has no duplicates, add 2 other random Dragons to
	# your hand. They cost (0).
	pass


class DRG_091:
	"""Shu'ma"""
	# At the end of your turn, fill your board with 1/1_Tentacles.
	pass


class DRG_099:
	"""Kronx Dragonhoof"""
	# [x]<b>Battlecry:</b> Draw Galakrond. If you're already Galakrond, unleash a
	# Devastation.
	pass


class DRG_257:
	"""Frizz Kindleroost"""
	# <b>Battlecry:</b> Reduce the Cost of Dragons in your deck by_(2).
	pass


class DRG_402:
	"""Sathrovarr"""
	# <b>Battlecry:</b> Choose a friendly minion. Add a copy of it to_your hand, deck, and
	# battlefield.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
	}
	play = (
		Give(CONTROLLER, Copy(TARGET)),
		Shuffle(CONTROLLER, Copy(TARGET)),
		Summon(CONTROLLER, ExactCopy(TARGET)),
	)
