from ..utils import *


##
# Minions

class ULD_151:
	"""Ramkahen Wildtamer"""
	# <b>Battlecry:</b> Copy a random Beast in your hand.
	pass


class ULD_154:
	"""Hyena Alpha"""
	# [x]<b>Battlecry:</b> If you control a <b>Secret</b>, summon two 2/2 Hyenas.
	pass


class ULD_156:
	"""Dinotamer Brann"""
	# <b>Battlecry:</b> If your deck has no duplicates, summon King Krush.
	pass


class ULD_212:
	"""Wild Bloodstinger"""
	# <b>Battlecry:</b> Summon a minion from your opponent's hand. Attack it.
	pass


class ULD_410:
	"""Scarlet Webweaver"""
	# <b>Battlecry:</b> Reduce the Cost of a random Beast in your_hand by (5).
	pass


##
# Spells

class ULD_152:
	"""Pressure Plate"""
	# <b>Secret:</b> After your opponent casts a spell, destroy a random enemy_minion.
	pass


class ULD_155:
	"""Unseal the Vault"""
	# <b>Quest:</b> Summon 20_minions. <b>Reward:</b> Ramkahen Roar.
	pass


class ULD_429:
	"""Hunter's Pack"""
	# Add a random Hunter Beast, <b>Secret</b>, and weapon to your_hand.
	pass


class ULD_713:
	"""Swarm of Locusts"""
	# Summon seven 1/1 Locusts with <b>Rush</b>.
	requirements = {
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	pass


##
# Weapons

class ULD_430:
	"""Desert Spear"""
	# After your hero attacks, summon a 1/1 Locust with <b>Rush</b>.
	pass
