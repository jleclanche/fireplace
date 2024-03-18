from ..utils import *


##
# Minions

class ULD_145:
	"""Brazen Zealot"""
	# Whenever you summon a minion, gain +1 Attack.
	pass


class ULD_207:
	"""Ancestral Guardian"""
	# <b>Lifesteal</b> <b>Reborn</b>
	pass


class ULD_217:
	"""Micro Mummy"""
	# [x]<b>Reborn</b> At the end of your turn, give another random friendly minion +1
	# Attack.
	pass


class ULD_438:
	"""Salhet's Pride"""
	# <b>Deathrattle:</b> Draw two 1-Health minions from your_deck.
	pass


class ULD_439:
	"""Sandwasp Queen"""
	# <b>Battlecry:</b> Add two 2/1 Sandwasps to your hand.
	pass


class ULD_500:
	"""Sir Finley of the Sands"""
	# [x]<b>Battlecry:</b> If your deck has no duplicates, <b>Discover</b> an upgraded Hero
	# Power.
	pass


##
# Spells

class ULD_143:
	"""Pharaoh's Blessing"""
	# Give a minion +4/+4, <b>Divine Shield</b>, and <b>Taunt</b>.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	pass


class ULD_431:
	"""Making Mummies"""
	# [x]<b>Quest:</b> Play 5 <b>Reborn</b> minions. <b>Reward:</b> Emperor Wraps.
	pass


class ULD_716:
	"""Tip the Scales"""
	# Summon 7 Murlocs from your deck.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
	}
	pass


class ULD_728:
	"""Subdue"""
	# Set a minion's Attack and Health to 1.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	pass
