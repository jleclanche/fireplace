from ..utils import *


##
# Minions

class ULD_133:
	"""Crystal Merchant"""
	# If you have any unspent Mana at the end of your turn, draw a card.
	pass


class ULD_137:
	"""Garden Gnome"""
	# [x]<b>Battlecry:</b> If you're holding a spell that costs (5) or more, summon two 2/2
	# Treants.
	pass


class ULD_138:
	"""Anubisath Defender"""
	# <b>Taunt</b>. Costs (0) if you've cast a spell that costs (5) or more this turn.
	pass


class ULD_139:
	"""Elise the Enlightened"""
	# <b>Battlecry:</b> If your deck has no duplicates, duplicate your hand.
	pass


class ULD_292:
	"""Oasis Surger"""
	# <b>Rush</b> <b>Choose One -</b> Gain +2/+2; or Summon a copy of this minion.
	pass


##
# Spells

class ULD_131:
	"""Untapped Potential"""
	# [x]<b>Quest:</b> End 4 turns with any unspent Mana. <b>Reward:</b> Ossirian Tear.
	pass


class ULD_134:
	"""BEEEES!!!"""
	# [x]Choose a minion. Summon four 1/1 Bees that attack it.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	pass


class ULD_135:
	"""Hidden Oasis"""
	# <b>Choose One</b> - Summon a 6/6 Ancient with <b>Taunt</b>; or Restore #12 Health.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	pass


class ULD_136:
	"""Worthy Expedition"""
	# <b>Discover</b> a <b>Choose One</b> card.
	pass


class ULD_273:
	"""Overflow"""
	# Restore #5 Health to all characters. Draw 5 cards.
	pass
