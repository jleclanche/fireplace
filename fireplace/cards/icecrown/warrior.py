from ..utils import *


##
# Minions

class ICC_062:
	"""Mountainfire Armor"""
	deathrattle = CurrentPlayer(OPPONENT) & GainArmor(FRIENDLY_HERO, 6)


class ICC_238:
	"""Animated Berserker"""
	events = Play(CONTROLLER, MINION).after(Hit(Play.CARD, 1))


class ICC_405:
	"""Rotface"""
	events = SELF_DAMAGE.on(Summon(CONTROLLER, RandomLegendaryMinion()))


class ICC_408:
	"""Val'kyr Soulclaimer"""
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "ICC_900t"))


class ICC_450:
	"""Death Revenant"""
	play = Buff(SELF, "ICC_450e") * Count(ALL_MINIONS + DAMAGED)


ICC_450e = buff(+1, +1)


##
# Spells

class ICC_091:
	"""Dead Man's Hand"""
	play = Shuffle(CONTROLLER, ExactCopy(FRIENDLY_HAND))


class ICC_281:
	"""Forge of Souls"""
	play = ForceDraw(RANDOM(FRIENDLY_DECK + WEAPON)) * 2


class ICC_837:
	"""Bring It On!"""
	play = GainArmor(FRIENDLY_HERO, 10), Buff(ENEMY_HAND + MINION, "ICC_837e")


class ICC_837e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -2}


##
# Weapons

class ICC_064:
	"""Blood Razor"""
	play = Hit(ALL_MINIONS, 1)
	deathrattle = Hit(ALL_MINIONS, 1)


##
# Heros

class ICC_834:
	"""Scourgelord Garrosh"""
	play = Summon(CONTROLLER, "ICC_834w")


class ICC_834h:
	activate = Hit(ALL_MINIONS, 1)


class ICC_834w:
	events = Attack(FRIENDLY_HERO).on(Hit(ADJACENT(Attack.DEFENDER), ATK(FRIENDLY_HERO)))
