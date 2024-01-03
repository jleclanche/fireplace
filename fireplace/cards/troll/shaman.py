from ..utils import *


##
# Minions

class TRL_059:
	"""Bog Slosher"""
	# <b>Battlecry:</b> Return a friendly minion to your hand and give it +2/+2.
	pass


class TRL_060:
	"""Spirit of the Frog"""
	# [x]<b>Stealth</b> for 1 turn. Whenever you cast a spell, draw a spell from your deck
	# that costs (1) more.
	pass


class TRL_085:
	"""Zentimo"""
	# [x]Whenever you target a minion with a spell, cast it again on its neighbors.
	pass


class TRL_345:
	"""Krag'wa, the Frog"""
	# <b>Battlecry:</b> Return all spells you played last turn to_your hand.
	play = Give(CONTROLLER, Copy(CARDS_PLAYED_LAST_TRUN + SPELL))


class TRL_522:
	"""Wartbringer"""
	# <b>Battlecry:</b> If you played 2_spells this turn, deal 2_damage.
	powered_up = Count(CARDS_PLAYED_THIS_TRUN + SPELL) >= 2
	play = powered_up & Hit(TARGET, 2)


##
# Spells

class TRL_012:
	"""Totemic Smash"""
	# Deal $2 damage. <b>Overkill</b>: Summon a basic Totem.
	pass


class TRL_058:
	"""Haunting Visions"""
	# The next spell you cast this turn costs (3) less. <b>Discover</b> a spell.
	pass


class TRL_082:
	"""Big Bad Voodoo"""
	# Give a friendly minion "<b>Deathrattle:</b> Summon a random minion that costs (1)
	# more."
	pass


class TRL_351:
	"""Rain of Toads"""
	# Summon three 2/4 Toads with <b>Taunt</b>. <b>Overload:</b> (3)
	pass


##
# Weapons

class TRL_352:
	"""Likkim"""
	# Has +2 Attack while you have <b>Overloaded</b> Mana Crystals.
	pass
