from ..utils import *


##
# Minions

class ULD_186:
	"""Pharaoh Cat"""
	# <b>Battlecry:</b> Add a random <b>Reborn</b> minion to your_hand.
	pass


class ULD_231:
	"""Whirlkick Master"""
	# Whenever you play a <b>Combo</b> card, add a random <b>Combo</b> card to your hand.
	pass


class ULD_280:
	"""Sahket Sapper"""
	# <b>Deathrattle:</b> Return a _random enemy minion to_ your_opponent's_hand.
	pass


class ULD_288:
	"""Anka, the Buried"""
	# <b>Battlecry:</b> Change each <b>Deathrattle</b> minion in your hand into a 1/1 that
	# costs (1).
	pass


class ULD_327:
	"""Bazaar Mugger"""
	# <b>Rush</b> <b>Battlecry:</b> Add a random minion from another class to your hand.
	pass


##
# Spells

class ULD_286:
	"""Shadow of Death"""
	# Choose a minion. Shuffle 3 'Shadows' into your deck that summon a copy when drawn.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	pass


class ULD_326:
	"""Bazaar Burglary"""
	# [x]<b>Quest:</b> Add 4 cards from other classes to your hand. <b>Reward: </b>Ancient
	# Blades.
	pass


class ULD_328:
	"""Clever Disguise"""
	# Add 2 random spells from another class to_your hand.
	pass


class ULD_715:
	"""Plague of Madness"""
	# Each player equips a 2/2 Knife with <b>Poisonous</b>.
	pass


##
# Weapons

class ULD_285:
	"""Hooked Scimitar"""
	# [x]<b>Combo:</b> Gain +2 Attack.
	pass
