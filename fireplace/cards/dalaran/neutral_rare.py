from ..utils import *


##
# Minions

class DAL_058:
	"""Hecklebot"""
	# <b>Taunt</b> <b>Battlecry:</b> Your opponent summons a minion from their deck.
	pass


class DAL_081:
	"""Spellward Jeweler"""
	# [x]<b>Battlecry:</b> Your hero can't be targeted by spells or Hero Powers until your
	# next turn.
	pass


class DAL_434:
	"""Arcane Watcher"""
	# Can't attack unless you have <b>Spell Damage</b>.
	pass


class DAL_539:
	"""Sunreaver Warmage"""
	# <b>Battlecry:</b> If you're holding a spell that costs (5) or more, deal 4 damage.
	pass


class DAL_550:
	"""Underbelly Ooze"""
	# After this minion survives damage, summon a copy_of it.
	pass


class DAL_582:
	"""Portal Keeper"""
	# [x]<b>Battlecry:</b> Shuffle 3 Portals into your deck. When drawn, summon a 2/2 Demon
	# with <b>Rush</b>.
	pass


class DAL_582t:
	play = Summon(CONTROLLER, "DAL_582t2")
	draw = CAST_WHEN_DRAWN


class DAL_749:
	"""Recurring Villain"""
	# <b>Deathrattle:</b> If this minion has 4 or more Attack, resummon it.
	pass


class DAL_751:
	"""Mad Summoner"""
	# [x]<b>Battlecry:</b> Fill each player's board with 1/1 Imps.
	pass


class DAL_774:
	"""Exotic Mountseller"""
	# Whenever you cast a spell, summon a random 3-Cost Beast.
	pass


class DAL_775:
	"""Tunnel Blaster"""
	# [x]<b>Taunt</b> <b>Deathrattle:</b> Deal 3 damage to all minions.
	pass
