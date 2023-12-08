from ..utils import *


##
# Minions

class GIL_130:
	"""Gloom Stag"""
	# <b>Taunt</b> <b>Battlecry:</b> If your deck has only odd-Cost cards, gain +2/+2.
	powered_up = OddCost(FRIENDLY_DECK)
	play = powered_up & Buff(SELF, "GIL_130e")


GIL_130e = buff(+2, +2)


class GIL_188:
	"""Druid of the Scythe"""
	# [x]<b>Choose One -</b> Transform into a 4/2 with <b>Rush</b>; or a 2/4 with
	# <b>Taunt</b>.
	pass


class GIL_507:
	"""Bewitched Guardian"""
	# [x]<b>Taunt</b> <b>Battlecry:</b> Gain +1 Health _for each card in your hand._
	pass


class GIL_658:
	"""Splintergraft"""
	# [x]<b>Battlecry:</b> Choose a friendly minion. Add a 10/10 copy to your hand that
	# costs (10).
	pass


class GIL_800:
	"""Duskfallen Aviana"""
	# On each player's turn, the first card played costs (0).
	pass


class GIL_833:
	"""Forest Guide"""
	# At the end of your turn, both players draw a card.
	pass


##
# Spells

class GIL_553:
	"""Wispering Woods"""
	# [x]Summon a 1/1 Wisp for each card in your hand.
	pass


class GIL_571:
	"""Witching Hour"""
	# Summon a random friendly Beast that died this game.
	pass


class GIL_637:
	"""Ferocious Howl"""
	# Draw a card. Gain 1 Armor for each card in your hand.
	pass


class GIL_663:
	"""Witchwood Apple"""
	# Add three 2/2 Treants to your hand.
	pass
