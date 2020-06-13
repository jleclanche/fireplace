from ..utils import *


##
# Minions

class AT_006:
	"""Dalaran Aspirant"""
	inspire = Buff(SELF, "AT_006e")


AT_006e = buff(spellpower=1)


class AT_007:
	"""Spellslinger"""
	play = Give(ALL_PLAYERS, RandomSpell())


class AT_008:
	"""Coldarra Drake"""
	update = Refresh(FRIENDLY_HERO_POWER, {GameTag.HEROPOWER_ADDITIONAL_ACTIVATIONS: SET(-1)})


class AT_009:
	"""Rhonin"""
	deathrattle = Give(CONTROLLER, "EX1_277") * 3


##
# Spells

class AT_001:
	"""Flame Lance"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 8)


class AT_004:
	"""Arcane Blast"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 2)


class AT_005:
	"""Polymorph: Boar"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Morph(TARGET, "AT_005t")


##
# Secrets

class AT_002:
	"""Effigy"""
	secret = Death(FRIENDLY + MINION).on(FULL_BOARD | (
		Reveal(SELF),
		Summon(CONTROLLER, RandomMinion(cost=COST(Death.ENTITY)))
	))
