from ..utils import *


##
# Minions

class ULD_195:
	"""Frightened Flunky"""
	# <b>Taunt</b> <b>Battlecry:</b> <b>Discover</b> a <b>Taunt</b>_minion.
	pass


class ULD_206:
	"""Restless Mummy"""
	# <b>Rush</b> <b>Reborn</b>
	pass


class ULD_253:
	"""Tomb Warden"""
	# <b>Taunt</b> <b>Battlecry:</b> Summon a copy of this minion.
	pass


class ULD_258:
	"""Armagedillo"""
	# [x]<b>Taunt</b> At the end of your turn, give all <b>Taunt</b> minions in your hand
	# +2/+2.
	pass


class ULD_709:
	"""Armored Goon"""
	# Whenever your hero attacks, gain 5 Armor.
	pass


class ULD_720:
	"""Bloodsworn Mercenary"""
	# [x]<b>Battlecry</b>: Choose a damaged friendly minion. Summon a copy of it.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_DAMAGED_TARGET: 0,
	}
	pass


##
# Spells

class ULD_256:
	"""Into the Fray"""
	# Give all <b>Taunt</b> minions in your hand +2/+2.
	pass


class ULD_707:
	"""Plague of Wrath"""
	# Destroy all damaged minions.
	pass


class ULD_711:
	"""Hack the System"""
	# [x]<b>Quest:</b> Attack 5 times with your hero. <b>Reward:</b> Anraphet's Core.
	pass


##
# Weapons

class ULD_708:
	"""Livewire Lance"""
	# After your Hero attacks, add a <b>Lackey</b> to your_hand.
	pass
