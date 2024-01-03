from ..utils import *


##
# Minions

class TRL_311:
	"""Arcanosaur"""
	# <b>Battlecry:</b> If you played an_Elemental last turn, deal_3_damage_to_all other
	# minions.
	pass


class TRL_315:
	"""Pyromaniac"""
	# Whenever your Hero Power_kills a minion, draw a card.
	pass


class TRL_316:
	"""Jan'alai, the Dragonhawk"""
	# [x]<b>Battlecry:</b> If your Hero Power dealt 8 damage this game, summon Ragnaros the
	# Firelord.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
	pass


class TRL_318:
	"""Hex Lord Malacrass"""
	# <b>Battlecry</b>: Add a copy of your opening hand to your hand <i>(except this
	# card)</i>.
	play = Give(CONTROLLER, Copy(STARTING_HAND - SELF))


class TRL_319:
	"""Spirit of the Dragonhawk"""
	# [x]<b>Stealth</b> for 1 turn. Your Hero Power also targets adjacent minions.
	pass


class TRL_390:
	"""Daring Fire-Eater"""
	# <b>Battlecry:</b> Your next Hero Power this turn deals 2_more damage.
	pass


##
# Spells

class TRL_310:
	"""Elemental Evocation"""
	# The next Elemental you_play this turn costs (2) less.
	pass


class TRL_313:
	"""Scorch"""
	# [x]Deal $4 damage to a minion. Costs (1) if you played an Elemental last turn.
	pass


class TRL_317:
	"""Blast Wave"""
	# Deal $2 damage to_all minions. <b>Overkill</b>: Add a random Mage spell to your hand.
	pass


class TRL_400:
	"""Splitting Image"""
	# <b>Secret:</b> When one of your minions is attacked, summon a copy of it.
	pass
