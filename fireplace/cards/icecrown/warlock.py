from ..utils import *


##
# Minions

class ICC_075:
	"""Despicable Dreadlord"""
	events = OWN_TURN_END.on(Hit(ENEMY_MINIONS, 1))


class ICC_218:
	"""Howlfiend"""
	events = SELF_DAMAGE.on(Discard(RANDOM(FRIENDLY_HAND)))


class ICC_407:
	"""Gnomeferatu"""
	play = Mill(OPPONENT)


class ICC_841:
	"""Blood-Queen Lana'thel"""
	update = Refresh(SELF, {GameTag.ATK: Count(FRIENDLY + DISCARDED)})


class ICC_903:
	"""Sanguine Reveler"""
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Destroy(TARGET), Buff(SELF, "ICC_903t")


ICC_903t = buff(+2, +2)


##
# Spells

class ICC_041:
	"""Defile"""
	progress_total = 14
	play = Hit(ALL_MINIONS, 1), Dead(ALL_MINIONS) & (
		Deaths(),
		AddProgress(SELF, None),
		FINISH_PROGRESS | CastSpell(SELF)
	)


class ICC_055:
	"""Drain Soul"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 2)


class ICC_206:
	"""Treachery"""
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Steal(TARGET, OPPONENT)


class ICC_469:
	"""Unwilling Sacrifice"""
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Destroy(TARGET), Destroy(RANDOM_ENEMY_MINION)


##
# Heros

class ICC_831:
	"""Bloodreaver Gul'dan"""
	play = Summon(CONTROLLER, Copy(FRIENDLY + KILLED + DEMON))


class ICC_831p:
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	activate = Hit(TARGET, 3)
