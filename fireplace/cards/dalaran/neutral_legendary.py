from ..utils import *


##
# Minions

class DAL_546:
	"""Barista Lynchen"""
	# <b>Battlecry:</b> Add a copy of each of your other <b>Battlecry</b>
	# minions_to_your_hand.
	play = Give(CONTROLLER, Copy(FRIENDLY_HAND + BATTLECRY + MINION))


class DAL_554:
	"""Chef Nomi"""
	# <b>Battlecry:</b> If your deck is empty, summon six 6/6 Greasefire_Elementals.
	play = Find(FRIENDLY_DECK) | SummonBothSides(CONTROLLER, "DAL_554t") * 6


class DAL_558:
	"""Archmage Vargoth"""
	# [x]At the end of your turn, cast a spell you've cast this turn <i>(targets are
	# random)</i>.
	events = OWN_TURN_END.on(CastSpell(Copy(RANDOM(CARDS_PLAYED_THIS_TRUN + SPELL))))


class DAL_736:
	"""Archivist Elysiana"""
	# <b>Battlecry:</b> <b>Discover</b> 5 cards. Replace your deck with 2_copies of each.
	play = (
		Destroy(FRIENDLY_DECK),
		Discover(CONTROLLER, RandomCollectible()).then(
			Shuffle(CONTROLLER, Copy(Discover.CARD)) * 2
		) * 5
	)


class DAL_752:
	"""Jepetto Joybuzz"""
	# <b>Battlecry:</b> Draw 2 minions from your deck. Set their Attack, Health, and Cost
	# to 1.
	play = Buff(Buff(ForceDraw(RANDOM(FRIENDLY_DECK + MINION)), "DAL_752e"), "DAL_752e2") * 2


class DAL_752e:
	atk = SET(1)
	max_health = SET(1)


class DAL_752e2:
	cost = SET(1)
	events = REMOVED_IN_PLAY
