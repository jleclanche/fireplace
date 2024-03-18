from ..utils import *


##
# Minions

class DAL_058:
	"""Hecklebot"""
	# <b>Taunt</b> <b>Battlecry:</b> Your opponent summons a minion from their deck.
	play = Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION))


class DAL_081:
	"""Spellward Jeweler"""
	# [x]<b>Battlecry:</b> Your hero can't be targeted by spells or Hero Powers until your
	# next turn.
	play = Buff(FRIENDLY_HERO, "DAL_081e")


class DAL_081e:
	tags = {
		GameTag.CANT_BE_TARGETED_BY_SPELLS: True,
		GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
	}
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


class DAL_434:
	"""Arcane Watcher"""
	# Can't attack unless you have <b>Spell Damage</b>.
	update = Find(FRIENDLY + SPELLPOWER) | Refresh(SELF, {GameTag.CANT_ATTACK: True})


class DAL_539:
	"""Sunreaver Warmage"""
	# <b>Battlecry:</b> If you're holding a spell that costs (5) or more, deal 4 damage.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE_AND_COST_5_OR_MORE_SPELL_IN_HAND: 0,
	}
	powered_up = Find(FRIENDLY_HAND + SPELL + (COST >= 5))
	play = powered_up & Hit(TARGET, 4)


class DAL_550:
	"""Underbelly Ooze"""
	# After this minion survives damage, summon a copy_of it.
	events = SELF_DAMAGE.on(Dead(SELF) | Summon(CONTROLLER, ExactCopy(SELF)))


class DAL_582:
	"""Portal Keeper"""
	# [x]<b>Battlecry:</b> Shuffle 3 Portals into your deck. When drawn, summon a 2/2 Demon
	# with <b>Rush</b>.
	play = Shuffle(CONTROLLER, "DAL_582t") * 3


class DAL_582t:
	play = Summon(CONTROLLER, "DAL_582t2")
	draw = CAST_WHEN_DRAWN


class DAL_749:
	"""Recurring Villain"""
	# <b>Deathrattle:</b> If this minion has 4 or more Attack, resummon it.
	deathrattle = (ATK(SELF) >= 4) & Summon(CONTROLLER, "DAL_749")


class DAL_751:
	"""Mad Summoner"""
	# [x]<b>Battlecry:</b> Fill each player's board with 1/1 Imps.
	play = (
		SummonBothSides(CONTROLLER, "DAL_751t") * 7,
		Summon(OPPONENT, "DAL_751t") * 7
	)


class DAL_774:
	"""Exotic Mountseller"""
	# Whenever you cast a spell, summon a random 3-Cost Beast.
	events = Play(CONTROLLER, SPELL).on(Summon(CONTROLLER, RandomBeast(cost=3)))


class DAL_775:
	"""Tunnel Blaster"""
	# [x]<b>Taunt</b> <b>Deathrattle:</b> Deal 3 damage to all minions.
	deathrattle = Hit(ALL_MINIONS, 3)
