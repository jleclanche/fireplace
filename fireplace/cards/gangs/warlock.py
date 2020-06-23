from ..utils import *


##
# Minions

class CFM_610:
	"""Crystalweaver"""
	play = Buff(FRIENDLY_MINIONS + DEMON, "CFM_610e")


CFM_610e = buff(+1, +1)


class CFM_663:
	"""Kabal Trafficker"""
	events = OWN_TURN_END.on(Give(CONTROLLER, RandomDemon()))


class CFM_699:
	"""Seadevil Stinger"""
	play = Buff(CONTROLLER, "CFM_699e")


class CFM_699e:
	events = Play(CONTROLLER, MURLOC).on(Destroy(SELF))
	update = Refresh(CONTROLLER, {enums.MURLOCS_COST_HEALTH: True})


class CFM_750:
	"""Krul the Unshackled"""
	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & Summon(CONTROLLER, FRIENDLY_HAND + DEMON)


class CFM_751:
	"""Abyssal Enforcer"""
	play = Hit(ALL_CHARACTERS - SELF, 3)


class CFM_900:
	"""Unlicensed Apothecary"""
	events = Summon(CONTROLLER).on(Hit(FRIENDLY_HERO, 5))


##
# Spells

class CFM_094:
	"""Felfire Potion"""
	play = Hit(ALL_CHARACTERS, 5)


class CFM_608:
	"""Blastcrystal Potion"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Destroy(TARGET), GainMana(CONTROLLER, -1), SpendMana(CONTROLLER, -1)


class CFM_611:
	"""Bloodfury Potion"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = (
		Find(TARGET + FRIENDLY + DEMON) &
		Buff(TARGET, "CFM_611e2") |
		Buff(TARGET, "CFM_611e")
	)


CFM_611e = buff(+3)
CFM_611e2 = buff(+3, +3)
