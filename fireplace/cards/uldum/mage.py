from ..utils import *


##
# Minions

class ULD_236:
	"""Tortollan Pilgrim"""
	# [x]<b>Battlecry</b>: <b>Discover</b> a copy of a spell in your deck and cast it with
	# random targets.
	pass


class ULD_238:
	"""Reno the Relicologist"""
	# <b>Battlecry:</b> If your deck has no duplicates, deal 10 damage randomly split among
	# all enemy minions.
	pass


class ULD_240:
	"""Arcane Flakmage"""
	# After you play a <b>Secret</b>, deal 2 damage to all enemy minions.
	pass


class ULD_293:
	"""Cloud Prince"""
	# <b>Battlecry:</b> If you control a <b>Secret</b>, deal 6 damage.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE_AND_MINIMUM_FRIENDLY_SECRETS: 1,
	}
	pass


class ULD_329:
	"""Dune Sculptor"""
	# [x]After you cast a spell, add a random Mage minion to your hand.
	pass


class ULD_435:
	"""Naga Sand Witch"""
	# [x]<b>Battlecry:</b> Change the Cost of spells in your hand to (5).
	pass


##
# Spells

class ULD_216:
	"""Puzzle Box of Yogg-Saron"""
	# Cast 10 random spells <i>(targets chosen randomly).</i>
	pass


class ULD_239:
	"""Flame Ward"""
	# <b>Secret:</b> After a minion attacks your hero, deal $3 damage to all enemy minions.
	pass


class ULD_433:
	"""Raid the Sky Temple"""
	# <b>Quest:</b> Cast 10 spells. <b>Reward: </b>Ascendant Scroll.
	pass


class ULD_726:
	"""Ancient Mysteries"""
	# Draw a <b>Secret</b> from your deck. It costs (0).
	pass
