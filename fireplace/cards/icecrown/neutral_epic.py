from ..utils import *


##
# Minions

class ICC_025:
	"""Rattling Rascal"""
	play = Summon(CONTROLLER, "ICC_025t")
	deathrattle = Summon(OPPONENT, "ICC_025t")


class ICC_096:
	"""Furnacefire Colossus"""
	play = Discard(IN_HAND + WEAPON).then(
		Buff(SELF, "ICC_096e", atk=ATK(Discard.TARGET), health=CURRENT_HEALTH(Discard.TARGET))
	)


class ICC_098:
	"""Tomb Lurker"""
	play = Give(CONTROLLER, Copy(RANDOM(KILLED + MINION + DEATHRATTLE)))


class ICC_701:
	"""Skulking Geist"""
	play = Destroy((IN_DECK | IN_HAND) + (COST == 1) + SPELL)


class ICC_706:
	"""Nerubian Unraveler"""
	update = Refresh(IN_HAND + SPELL, {GameTag.COST: +2})


class ICC_810:
	"""Deathaxe Punisher"""
	play = Buff(RANDOM(FRIENDLY_HAND + LIFESTEAL + MINION), "ICC_810e")


ICC_810e = buff(+2, +2)


class ICC_812:
	"""Meat Wagon"""
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (ATK <= ATK(SELF))))


class ICC_901:
	"""Drakkari Enchanter"""
	update = Refresh(CONTROLLER, {enums.EXTRA_END_TURN_EFFECT: True})


class ICC_912:
	"""Corpsetaker"""
	play = (
		Find(FRIENDLY_DECK + MINION + TAUNT) & Taunt(SELF),
		Find(FRIENDLY_DECK + MINION + DIVINE_SHIELD) & GiveDivineShield(SELF),
		Find(FRIENDLY_DECK + MINION + LIFESTEAL) & GiveLifesteal(SELF),
		Find(FRIENDLY_DECK + MINION + WINDFURY) & GiveWindfury(SELF),
	)
