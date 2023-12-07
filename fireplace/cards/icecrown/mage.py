from ..utils import *


##
# Minions

class ICC_068:
	"""Ice Walker"""
	events = Activate(CONTROLLER, FRIENDLY_HERO_POWER).after(
		Find(Activate.TARGET) & Freeze(Activate.TARGET)
	)


class ICC_069:
	"""Ghastly Conjurer"""
	play = Give(CONTROLLER, "CS2_027")


class ICC_083:
	"""Doomed Apprentice"""
	update = Refresh(ENEMY_HAND + SPELL, {GameTag.COST: 1})


class ICC_252:
	"""Coldwraith"""
	play = Find(ENEMY + FROZEN) & Draw(CONTROLLER)


class ICC_838:
	"""Sindragosa"""
	play = SummonBothSides(CONTROLLER, "ICC_838t") * 2


class ICC_838t:
	deathrattle = Give(CONTROLLER, RandomLegendaryMinion())


##
# Spells

class ICC_082:
	"""Frozen Clone"""
	secret = Play(OPPONENT, MINION).after(
		Reveal(SELF), Give(CONTROLLER, Copy(Play.CARD)) * 2
	)


class ICC_086:
	"""Glacial Mysteries"""
	play = Summon(CONTROLLER, FRIENDLY_DECK + SECRET)


class ICC_823:
	"""Simulacrum"""
	play = Give(CONTROLLER, ExactCopy(RANDOM(LOWEST_COST(FRIENDLY_HAND))))


class ICC_836:
	"""Breath of Sindragosa"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	play = Hit(RANDOM_ENEMY_MINION, 2).then(Freeze(Hit.TARGET))


##
# Heros

class ICC_833:
	"""Frost Lich Jaina"""
	play = (
		Summon(CONTROLLER, "ICC_833t"),
		Buff(CONTROLLER, "ICC_833e")
	)


class ICC_833h:
	activate = Hit(TARGET, 1).then(Dead(TARGET) & Summon(CONTROLLER, "ICC_833t"))


class ICC_833t:
	events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class ICC_833e:
	update = Refresh(FRIENDLY_MINIONS + ELEMENTAL, {GameTag.LIFESTEAL: True})
