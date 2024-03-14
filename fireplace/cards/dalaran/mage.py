from ..utils import *


##
# Minions

class DAL_163:
	"""Messenger Raven"""
	# <b>Battlecry:</b> <b>Discover</b> a Mage minion.
	play = DISCOVER(RandomMinion(card_class=CardClass.MAGE))


class DAL_182:
	"""Magic Dart Frog"""
	# After you cast a spell, deal 1 damage to a random enemy minion.
	pass


class DAL_575:
	"""Khadgar"""
	# Your cards that summon minions summon twice_as_many.
	events = Summon(CONTROLLER, MINION, source=-PLAYER - ID("DAL_575")).after(
		Summon(CONTROLLER, ExactCopy(Summon.CARD))
	)


class DAL_576:
	"""Kirin Tor Tricaster"""
	# <b>Spell Damage +3</b> Your spells cost (1) more.
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: 1})


class DAL_603:
	"""Mana Cyclone"""
	# [x]<b>Battlecry:</b> For each spell you've cast this turn, add a random Mage spell to
	# your hand.
	play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)) * Count(
		CARDS_PLAYED_THIS_TRUN + SPELL)


class DAL_609:
	"""Kalecgos"""
	# Your first spell each turn costs (0). <b>Battlecry:</b> <b>Discover</b> a spell.
	update = (
		(Count(CARDS_PLAYED_THIS_TRUN + SPELL) == 0) &
		Refresh(FRIENDLY_HAND + SPELL, buff="DAL_609e")
	)


class DAL_609e:
	cost = SET(0)
	events = REMOVED_IN_PLAY


##
# Spells

class DAL_177:
	"""Conjurer's Calling"""
	# <b>Twinspell</b> Destroy a minion. Summon 2 minions of the same Cost to replace it.
	play = (
		Give(CONTROLLER, "DAL_177ts"),
		Destroy(TARGET), Summon(CONTROLLER, RandomMinion(cost=COST(TARGET))) * 2
	)


class DAL_177ts:
	play = Destroy(TARGET), Summon(CONTROLLER, RandomMinion(cost=COST(TARGET))) * 2


class DAL_577:
	"""Ray of Frost"""
	# <b>Twinspell</b> <b>Freeze</b> a minion. If it's already <b>Frozen</b>, deal $2
	# damage to it.
	play = (
		Give(CONTROLLER, "DAL_577ts"),
		Find(TARGET + FROZEN) & Hit(TARGET, 2) | Freeze(TARGET)
	)


class DAL_577ts:
	play = Find(TARGET + FROZEN) & Hit(TARGET, 2) | Freeze(TARGET)


class DAL_578:
	"""Power of Creation"""
	# <b>Discover</b> a 6-Cost minion. Summon two copies of it.
	play = Discover(CONTROLLER, RandomMinion(cost=6)).then(
		Summon(CONTROLLER, Discover.CARD) * 2
	)


class DAL_608:
	"""Magic Trick"""
	# <b>Discover</b> a spell that costs (3) or less.
	play = DISCOVER(RandomSpell(cost=list(range(0, 4))))
