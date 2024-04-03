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
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = Hit(TARGET, 2)


class DAL_615:
	"""Witchy Lackey"""
	# <b>Battlecry:</b> Transform a friendly minion into one that costs (1) more.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
	}
	play = Evolve(TARGET, 1)


class DAL_739:
	"""Goblin Lackey"""
	# <b>Battlecry:</b> Give a friendly minion +1 Attack and_<b>Rush</b>.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
	}
	play = Buff(TARGET, "DAL_739e")


DAL_739e = buff(atk=1, rush=True)


class DAL_741:
	"""Ethereal Lackey"""
	# <b>Battlecry:</b> <b>Discover</b> a spell.
	play = DISCOVER(RandomSpell())


class ULD_616:
	"""Titanic Lackey"""
	# <b>Battlecry:</b> Give a friendly minion +2 Health and_<b>Taunt</b>.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
	}
	play = Buff(TARGET, "ULD_616e")


ULD_616e = buff(health=2, taunt=True)


class DRG_052:
	"""Draconic Lackey"""
	# <b>Battlecry:</b> <b>Discover</b> a Dragon.
	play = DISCOVER(RandomDragon())
