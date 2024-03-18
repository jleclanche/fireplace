from ..utils import *


##
# Minions

class GIL_116:
	"""Arcane Keysmith"""
	# <b>Battlecry:</b> <b>Discover</b> a <b>Secret</b>. Put it into the battlefield.
	play = WITH_SECRECTS & (
		Discover(CONTROLLER, RandomSpell(secret=True)).then(
			Summon(CONTROLLER, Discover.CARD)
		)
	) | (
		Discover(CONTROLLER, RandomSpell(secret=True, card_class=CardClass.MAGE)).then(
			Summon(CONTROLLER, Discover.CARD)
		)
	)


class GIL_549:
	"""Toki, Time-Tinker"""
	# [x]<b>Battlecry:</b> Add a random <b>Legendary</b> minion from the past to your hand.
	play = Give(CONTROLLER, RandomLegendaryMinion(is_standard=False))


class GIL_640:
	"""Curio Collector"""
	# Whenever you draw a card, gain +1/+1.
	events = Draw(CONTROLLER).after(Buff(Draw.CARD, "GIL_640e"))


GIL_640e = buff(+1, +1)


class GIL_645:
	"""Bonfire Elemental"""
	# <b>Battlecry:</b> If you played an_Elemental last turn, draw a card.
	powered_up = ELEMENTAL_PLAYED_LAST_TURN
	play = powered_up & Draw(CONTROLLER)


class GIL_664:
	"""Vex Crow"""
	# Whenever you cast a spell, summon a random 2-Cost minion.
	events = Play(CONTROLLER, SPELL).after(Summon(CONTROLLER, RandomMinion(cost=2)))


class GIL_691:
	"""Archmage Arugal"""
	# Whenever you draw a minion, add a copy of it to_your hand.
	events = Draw(CONTROLLER, MINION).after(Give(CONTROLLER, ExactCopy(Draw.CARD)))


class GIL_838:
	"""Black Cat"""
	# <b>Spell Damage +1</b> <b>Battlecry:</b> If your deck has only odd-Cost cards, draw a
	# card.
	powered_up = OddCost(FRIENDLY_DECK)
	play = powered_up & Draw(CONTROLLER)


##
# Spells

class GIL_147:
	"""Cinderstorm"""
	# Deal $5 damage randomly split among all enemies.
	play = Hit(RANDOM_ENEMY_CHARACTER, 1) * SPELL_DAMAGE(5)


class GIL_548:
	"""Book of Specters"""
	# Draw 3 cards. Discard any spells drawn.
	play = Draw(CONTROLLER).then(Find(Draw.CARD + SPELL) & Discard(Draw.CARD)) * 3


class GIL_801:
	"""Snap Freeze"""
	# <b>Freeze</b> a minion. If it's already <b>Frozen</b>, destroy it.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Find(TARGET + FROZEN) & Destroy(TARGET) | Freeze(TARGET)
