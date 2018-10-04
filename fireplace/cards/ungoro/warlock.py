from ..utils import *


##
# Minions

class UNG_047:
	"""Ravenous Pterrordax"""
	play = Destroy(TARGET), Adapt(SELF), Adapt(SELF)


class UNG_049:
	"""Tar Lurker"""
	update = Find(CURRENT_PLAYER + CONTROLLER) | Refresh(SELF, {GameTag.ATK: +3})


class UNG_830:
	"""Cruel Dinomancer"""
	play = Summon(CONTROLLER, RANDOM(FRIENDLY + MINION + DISCARDED))


class UNG_833:
	"""Lakkari Felhound"""
	play = Discard(RANDOM(FRIENDLY_HAND)) * 2


class UNG_835:
	"""Chittering Tunneler"""
	play = Discover(CONTROLLER, RandomSpell()).then(
		Give(CONTROLLER, Discover.CARD), Hit(FRIENDLY_HERO, Discover.CARD)
	)


class UNG_836:
	"""Clutchmother Zavas"""
	events = Discard(SELF).on(Buff(SELF, "UNG_835e"), Give(CONTROLLER, SELF))


@custom_card
class UNG_835e:
	tags = {
		GameTag.CARDNAME: "Clutchmother Zavas Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.ATK: +2,
		GameTag.HEALTH: +2,
	}

##
# Spells

class UNG_829:
	"""Lakkari Sacrifice"""
	events = Discard(FRIENDLY).after(CompleteQuest(SELF))
	reward = Destroy(SELF), Give(CONTROLLER, "UNG_829t1")


class UNG_829t1:
	play = Summon(CONTROLLER, "UNG_829t2")


class UNG_829t2:
	events = OWN_TURN_END.on(Summon(CONTROLLER, "UNG_829t3") * 2)


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
	play = Hit(TARGET, 3), Summon(CONTROLLER, "UNG_834t1") * 3
