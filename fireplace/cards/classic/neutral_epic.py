from ..utils import *


class EX1_005:
	"""Big Game Hunter"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_MIN_ATTACK: 7}
	play = Destroy(TARGET)


class EX1_105:
	"""Mountain Giant"""
	cost_mod = -Count(FRIENDLY_HAND - SELF)


class EX1_507:
	"""Murloc Warleader"""
	update = Refresh(FRIENDLY_MINIONS + MURLOC - SELF, buff="EX1_507e")


EX1_507e = buff(atk=2)


class EX1_564:
	"""Faceless Manipulator"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_NONSELF_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Morph(SELF, ExactCopy(TARGET))


class EX1_586:
	"""Sea Giant"""
	cost_mod = -Count(ALL_MINIONS)


class EX1_590:
	"""Blood Knight"""
	play = (
		Buff(SELF, "EX1_590e") * Count(ALL_MINIONS + DIVINE_SHIELD),
		UnsetTag(ALL_MINIONS, (GameTag.DIVINE_SHIELD, ))
	)


EX1_590e = buff(+3, +3)


class EX1_620:
	"""Molten Giant"""
	cost_mod = -DAMAGE(FRIENDLY_HERO)


class NEW1_016:
	"""Captain's Parrot"""
	play = ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE))


class NEW1_017:
	"""Hungry Crab"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0, PlayReq.REQ_TARGET_WITH_RACE: 14}
	play = Destroy(TARGET), Buff(SELF, "NEW1_017e")


NEW1_017e = buff(+2, +2)


class NEW1_021:
	"""Doomsayer"""
	events = OWN_TURN_BEGIN.on(Destroy(ALL_MINIONS))


class NEW1_027:
	"""Southsea Captain"""
	update = Refresh(FRIENDLY_MINIONS + PIRATE - SELF, buff="NEW1_027e")


NEW1_027e = buff(+1, +1)
