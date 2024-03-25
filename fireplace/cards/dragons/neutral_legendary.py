from ..utils import *


##
# Minions

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
