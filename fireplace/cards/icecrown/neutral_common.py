from ..utils import *


##
# Minions

class ICC_019:
	"""Skelemancer"""
	deathrattle = CurrentPlayer(OPPONENT) & Summon(CONTROLLER, "ICC_019t")


class ICC_026:
	"""Grim Necromancer"""
	play = Summon(CONTROLLER, "ICC_026t") * 2


ICC_028e = buff(health=2)


class ICC_028:
	"""Sunborne Val'kyr"""
	play = Buff(SELF_ADJACENT, "ICC_028e")


class ICC_029:
	"""Cobalt Scalebane"""
	events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "ICC_029e"))


ICC_029e = buff(atk=3)


class ICC_031:
	"""Night Howler"""
	events = Damage(SELF).on(Buff(SELF, "ICC_031e"))


ICC_031e = buff(atk=2)


class ICC_067:
	"""Vryghoul"""
	deathrattle = CurrentPlayer(OPPONENT) & Summon(CONTROLLER, "ICC_900t")


class ICC_092:
	"""Acherus Veteran"""
	play = Buff(TARGET, "ICC_092e")


ICC_092e = buff(atk=1)


class ICC_093:
	"""Tuskarr Fisherman"""
	play = Buff(TARGET, "ICC_093e")


ICC_093e = buff(spellpower=1)


class ICC_094:
	"""Fallen Sun Cleric"""
	play = Buff(TARGET, "ICC_094e")


ICC_094e = buff(+1, +1)


class ICC_097:
	"""Grave Shambler"""
	events = Death(FRIENDLY + WEAPON).on(Buff(SELF, "ICC_097e"))


ICC_097e = buff(+1, +1)


class ICC_467:
	"""Deathspeaker"""
	play = Buff(TARGET, "ICC_467e")


ICC_467e = buff(immune=True)


class ICC_468:
	"""Wretched Tiller"""
	events = Attack(SELF).on(Hit(ENEMY_HERO, 2))


class ICC_705:
	"""Bonemare"""
	play = Buff(TARGET, "ICC_705e")


ICC_705e = buff(+4, +4, taunt=True)


class ICC_855:
	"""Hyldnir Frostrider"""
	play = Freeze(FRIENDLY_MINIONS - SELF)


class ICC_900:
	"""Necrotic Geist"""
	events = Death(FRIENDLY_MINIONS - SELF).on(Summon(CONTROLLER, "ICC_900t"))


class ICC_904:
	"""Wicked Skeleton"""
	play = Buff(SELF, "ICC_904e") * Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


ICC_904e = buff(+1, +1)
