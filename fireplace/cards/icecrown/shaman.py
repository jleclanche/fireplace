from ..utils import *


##
# Minions

class ICC_058:
	"""Brrrloc"""
	play = Freeze(TARGET)


class ICC_088:
	"""Voodoo Hexxer"""
	events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class ICC_090:
	"""Snowfury Giant"""
	cost_mod = -Attr(CONTROLLER, GameTag.OVERLOAD_THIS_GAME)


class ICC_289:
	"""Moorabi"""
	events = SetTag(ALL_MINIONS - SELF, (GameTag.FROZEN, )).after(
		Give(CONTROLLER, Copy(SetTag.TARGET)))


##
# Spells

class ICC_056:
	"""Cryostasis"""
	play = Buff(TARGET, "ICC_056e"), Freeze(TARGET)


ICC_056e = buff(+3, +3)


class ICC_078:
	"""Avalanche"""
	play = Hit(TARGET, 3), Freeze(TARGET_ADJACENT)


class ICC_089:
	"""Ice Fishing"""
	play = ForceDraw(RANDOM(FRIENDLY_DECK + MURLOC)) * 2


##
# Weapons

class ICC_236:
	"""Ice Breaker"""
	events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
		Find(FROZEN + Attack.DEFENDER) & Destroy(Attack.DEFENDER)
	)


##
# Heros

class ICC_481:
	"""Thrall, Deathseer"""
	play = Evolve(FRIENDLY_MINIONS, 2)


class ICC_481p:
	activate = Evolve(TARGET, 1)
