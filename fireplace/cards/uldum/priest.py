from ..utils import *


##
# Minions

class ULD_262:
	"""High Priest Amet"""
	# [x]Whenever you summon a minion, set its Health equal to this minion's.
	pass


class ULD_266:
	"""Grandmummy"""
	# [x]<b>Reborn</b> <b>Deathrattle:</b> Give a random friendly minion +1/+1.
	pass


class ULD_268:
	"""Psychopomp"""
	# [x]<b>Battlecry:</b> Summon a random friendly minion that died this game. Give it
	# <b>Reborn</b>.
	pass


class ULD_269:
	"""Wretched Reclaimer"""
	# [x]<b>Battlecry:</b> Destroy a friendly minion, then return it to life with full
	# Health.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
	}
	pass


class ULD_270:
	"""Sandhoof Waterbearer"""
	# At the end of your turn, restore #5 Health to a damaged friendly character.
	pass


##
# Spells

class ULD_265:
	"""Embalming Ritual"""
	# Give a minion <b>Reborn</b>.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	pass


class ULD_272:
	"""Holy Ripple"""
	# Deal $1 damage to all enemies. Restore #1_Health to all friendly characters.
	pass


class ULD_714:
	"""Penance"""
	# <b>Lifesteal</b> Deal $3 damage to a_minion.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	pass


class ULD_718:
	"""Plague of Death"""
	# <b>Silence</b> and destroy all_minions.
	pass


class ULD_724:
	"""Activate the Obelisk"""
	# <b>Quest:</b> Restore 15_Health. <b>Reward:</b> Obelisk's Eye.
	pass
