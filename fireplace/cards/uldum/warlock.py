from ..utils import *


##
# Minions

class ULD_161:
	"""Neferset Thrasher"""
	# Whenever this attacks, deal 3 damage to your_hero.
	pass


class ULD_162:
	"""EVIL Recruiter"""
	# <b>Battlecry:</b> Destroy a friendly <b>Lackey</b> to summon a 5/5 Demon.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_LACKEY: 0,
	}
	pass


class ULD_163:
	"""Expired Merchant"""
	# [x]<b>Battlecry:</b> Discard your highest Cost card. <b>Deathrattle:</b> Add 2 copies
	# of it to your hand.
	pass


class ULD_165:
	"""Riftcleaver"""
	# <b>Battlecry:</b> Destroy a minion. Your hero takes damage equal to its Health.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	pass


class ULD_167:
	"""Diseased Vulture"""
	# After your hero takes damage on your turn, summon a random 3-Cost minion.
	pass


class ULD_168:
	"""Dark Pharaoh Tekahn"""
	# <b>Battlecry:</b> For the rest of the game, your <b>Lackeys</b> are 4/4.
	pass


##
# Spells

class ULD_140:
	"""Supreme Archaeology"""
	# <b>Quest:</b> Draw 20 cards. <b>Reward:</b> Tome of Origination.
	pass


class ULD_160:
	"""Sinister Deal"""
	# <b>Discover</b> a <b>Lackey</b>.
	pass


class ULD_324:
	"""Impbalming"""
	# Destroy a minion. Shuffle 3 Worthless Imps into your deck.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	pass


class ULD_717:
	"""Plague of Flames"""
	# [x]Destroy all your minions. For each one, destroy a random enemy minion.
	pass
