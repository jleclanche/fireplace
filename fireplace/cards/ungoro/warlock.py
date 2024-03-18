from ..utils import *


##
# Minions

class UNG_047:
	"""Ravenous Pterrordax"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
	}
	play = Destroy(TARGET), Adapt(SELF) * 2


class UNG_049:
	"""Tar Lurker"""
	update = CurrentPlayer(OPPONENT) & Refresh(SELF, {GameTag.ATK: +3})


class UNG_830:
	"""Cruel Dinomancer"""
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY + DISCARDED + MINION))


class UNG_833:
	"""Lakkari Felhound"""
	play = Discard(RANDOM(FRIENDLY_HAND) * 2)


class UNG_835:
	"""Chittering Tunneler"""
	play = Discover(CONTROLLER, RandomSpell()).then(
		Give(CONTROLLER, Discover.CARD),
		Hit(FRIENDLY_HERO, COST(Discover.CARD))
	)


class UNG_836:
	"""Clutchmother Zavas"""
	discard = Give(CONTROLLER, SELF), Buff(SELF, "UNG_836e")


UNG_836e = buff(+2, +2)


##
# Spells

class UNG_829:
	"""Lakkari Sacrifice"""
	progress_total = 6
	quest = Discard(FRIENDLY).after(AddProgress(SELF, Discard.TARGET))
	reward = Give(CONTROLLER, "UNG_829t1")


class UNG_829t1:
	requirements = {
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	play = Summon(CONTROLLER, "UNG_829t2")


class UNG_829t2:
	events = OWN_TURN_END.on(SummonBothSides(CONTROLLER, "UNG_829t3") * 2)


class UNG_831:
	"""Corrupting Mist"""
	play = Buff(ALL_MINIONS, "UNG_831e")


class UNG_831e:
	events = OWN_TURN_BEGIN.on(Destroy(OWNER))


class UNG_832:
	"""Bloodbloom"""
	play = Buff(CONTROLLER, "UNG_832e")


class UNG_832e:
	events = OWN_SPELL_PLAY.on(Destroy(SELF))
	update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})


class UNG_834:
	"""Feeding Time"""
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Hit(TARGET, 3), Summon(CONTROLLER, "UNG_834t1") * 3
