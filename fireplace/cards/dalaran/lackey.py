from ..utils import *


##
# Laykeys

class DAL_613:
	"""Faceless Lackey"""
	# <b>Battlecry:</b> Summon a random 2-Cost minion.
	play = Summon(CONTROLLER, RandomMinion(cost=2))


class DAL_614:
	"""Kobold Lackey"""
	# <b>Battlecry:</b> Deal 2 damage.
	play = Hit(TARGET, 2)


class DAL_615:
	"""Witchy Lackey"""
	# <b>Battlecry:</b> Transform a friendly minion into one that costs (1) more.
	play = Evolve(TARGET, 1)


class DAL_739:
	"""Goblin Lackey"""
	# <b>Battlecry:</b> Give a friendly minion +1 Attack and_<b>Rush</b>.
	play = Buff(TARGET, "DAL_739e")


DAL_739e = buff(atk=1, rush=True)


class DAL_741:
	"""Ethereal Lackey"""
	# <b>Battlecry:</b> <b>Discover</b> a spell.
	play = DISCOVER(RandomSpell())
