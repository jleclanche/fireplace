from ..utils import *


##
# Minions

class GVG_023:
	"""Goblin Auto-Barber"""
	play = Buff(FRIENDLY_WEAPON, "GVG_023a")


GVG_023a = buff(atk=1)


class GVG_025:
	"""One-eyed Cheat"""
	events = Summon(CONTROLLER, PIRATE - SELF).on(Stealth(SELF))


class GVG_027:
	"""Iron Sensei"""
	events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_027e"))


GVG_027e = buff(+2, +2)


class GVG_028:
	"""Trade Prince Gallywix"""
	events = Play(OPPONENT, SPELL - ID("GVG_028t")).on(
		Give(CONTROLLER, Copy(Play.CARD)),
		Give(OPPONENT, "GVG_028t")
	)


class GVG_028t:
	play = ManaThisTurn(CONTROLLER, 1)


class GVG_088:
	"""Ogre Ninja"""
	events = FORGETFUL


##
# Spells

class GVG_022:
	"""Tinker's Sharpsword Oil"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	play = Buff(FRIENDLY_WEAPON, "GVG_022a")
	combo = Buff(FRIENDLY_WEAPON, "GVG_022a"), Buff(RANDOM_FRIENDLY_CHARACTER, "GVG_022b")


GVG_022a = buff(atk=3)  # Weapon
GVG_022b = buff(atk=3)  # Minion


class GVG_047:
	"""Sabotage"""
	requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_MINION_TARGET: 0}
	play = Destroy(RANDOM_ENEMY_MINION)
	combo = Destroy(ENEMY_WEAPON | RANDOM_ENEMY_MINION)


##
# Weapons

class GVG_024:
	"""Cogmaster's Wrench"""
	update = Find(FRIENDLY_MINIONS + MECH) & Refresh(SELF, {GameTag.ATK: +2})
