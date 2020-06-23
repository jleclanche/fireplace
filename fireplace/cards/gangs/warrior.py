from ..utils import *


##
# Minions

class CFM_643:
	"""Hobart Grapplehammer"""
	play = Buff(FRIENDLY + WEAPON + (IN_HAND | IN_DECK), "CFM_643e")


CFM_643e = buff(atk=1)


class CFM_754:
	"""Grimy Gadgeteer"""
	events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_754e"))


CFM_754e = buff(+2, +2)


class CFM_755:
	"""Grimestreet Pawnbroker"""
	play = Buff(RANDOM(FRIENDLY_HAND + WEAPON), "CFM_755e")


CFM_755e = buff(+1, +1)


class CFM_756:
	"""Alley Armorsmith"""
	events = Damage(CHARACTER, None, SELF).on(GainArmor(FRIENDLY_HERO, Damage.AMOUNT))


##
# Spells

class CFM_716:
	"""Sleep with the Fishes"""
	play = Hit(ALL_MINIONS + DAMAGED, 3)


class CFM_752:
	"""Stolen Goods"""
	play = Buff(RANDOM(FRIENDLY_HAND + MINION + TAUNT), "CFM_752e")


CFM_752e = buff(+3, +3)


class CFM_940:
	"""I Know a Guy"""
	play = DISCOVER(RandomMinion(taunt=True))


##
# Weapons

class CFM_631:
	"""Brass Knuckles"""
	events = Attack(FRIENDLY_HERO).after(Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_631e"))


CFM_631e = buff(+1, +1)
