from ..utils import *


##
# Minions

class CFM_308:
	"""Kun the Forgotten King"""
	pass


class CFM_343:
	"""Jade Behemoth"""
	play = SummonJadeGolem(CONTROLLER)


class CFM_617:
	"""Celestial Dreamer"""
	pass


class CFM_816:
	"""Virmen Sensei"""
	pass


##
# Spells

class CFM_602:
	"""Jade Idol"""
	choose = ("CFM_602a", "CFM_602b")
	play = ChooseBoth(CONTROLLER) & (
		SummonJadeGolem(CONTROLLER), Shuffle(CONTROLLER, "CFM_602") * 3
	)


class CFM_602a:
	play = SummonJadeGolem(CONTROLLER)


class CFM_602b:
	play = Shuffle(CONTROLLER, "CFM_602") * 3


class CFM_614:
	"""Mark of the Lotus"""
	pass


class CFM_616:
	"""Pilfered Power"""
	pass


class CFM_713:
	"""Jade Blossom"""
	play = SummonJadeGolem(CONTROLLER), GainMana(CONTROLLER, 1), SpendMana(CONTROLLER, 1)


class CFM_811:
	"""Lunar Visions"""
	pass
