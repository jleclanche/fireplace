from ..utils import *


##
# Minions

class GIL_152:
	"""Blackhowl Gunspire"""
	# [x]Can't attack. Whenever this minion takes damage, deal 3 damage to a random enemy.
	events = SELF_DAMAGE.on(Hit(RANDOM_ENEMY_CHARACTER, 3))


class GIL_155:
	"""Redband Wasp"""
	# <b>Rush</b> Has +3 Attack while damaged.
	enrage = Refresh(SELF, buff="GIL_155e")


GIL_155e = buff(atk=3)


class GIL_547:
	"""Darius Crowley"""
	# [x]<b>Rush</b> After this attacks and kills a minion, gain +2/+2.
	events = Attack(SELF, ALL_MINIONS).after(
		Dead(ALL_MINIONS + Attack.DEFENDER) & Buff(SELF, "GIL_547e")
	)


GIL_547e = buff(+2, +2)


class GIL_580:
	"""Town Crier"""
	# <b>Battlecry:</b> Draw a <b>Rush</b> minion from your deck.
	play = ForceDraw(RANDOM(FRIENDLY_DECK + RUSH))


class GIL_655:
	"""Festeroot Hulk"""
	# After a friendly minion attacks, gain +1 Attack.
	events = Attack(FRIENDLY_MINIONS).after(Buff(SELF, "GIL_655e"))


GIL_655e = buff(atk=1)


class GIL_803:
	"""Militia Commander"""
	# <b>Rush</b> <b>Battlecry:</b> Gain +3_Attack this turn.
	play = Buff(SELF, "GIL_803e")


GIL_803e = buff(atk=3)


##
# Spells

class GIL_537:
	"""Deadly Arsenal"""
	# Reveal a weapon from your deck. Deal its Attack to all minions.
	play = Reveal(RANDOM(FRIENDLY_DECK + WEAPON)).then(
		Hit(ALL_MINIONS, ATK(Reveal.TARGET))
	)


class GIL_654:
	"""Warpath"""
	# <b>Echo</b> Deal $1 damage to all_minions.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Hit(ALL_MINIONS, 1)


##
# Weapons

class GIL_653:
	"""Woodcutter's Axe"""
	# <b>Deathrattle:</b> Give +2/+1 to a random friendly <b>Rush</b> minion.
	deathrattle = Buff(RANDOM_FRIENDLY_MINION, "GIL_653e")


GIL_653e = buff(+2, +1, rush=True)
