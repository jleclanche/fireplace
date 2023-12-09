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
	choose = ("GIL_188a", "GIL_188b")
	play = ChooseBoth(CONTROLLER) & Morph(SELF, "GIL_188t3")


class GIL_188a:
	play = Morph(SELF, "GIL_188t")


class GIL_188b:
	play = Morph(SELF, "GIL_188t2")


class GIL_507:
	"""Bewitched Guardian"""
	# [x]<b>Taunt</b> <b>Battlecry:</b> Gain +1 Health _for each card in your hand._
	play = Buff(SELF, "GIL_507e") * Count(FRIENDLY_HAND)


GIL_507e = buff(health=1)


class GIL_658:
	"""Splintergraft"""
	# [x]<b>Battlecry:</b> Choose a friendly minion. Add a 10/10 copy to your hand that
	# costs (10).
	play = Give(CONTROLLER, Buff(Copy(TARGET), "GIL_658e"))


class GIL_658e:
	atk = SET(10)
	max_health = SET(10)
	cost = SET(10)


class GIL_800:
	"""Duskfallen Aviana"""
	# On each player's turn, the first card played costs (0).
	events = TURN_BEGIN.on(Buff(CURRENT_PLAYER, "GIL_800e2"))


class GIL_800e2:
	update = Refresh(FRIENDLY_HAND, {GameTag.COST: SET(0)})
	events = Play(CONTROLLER).on(Destroy(SELF))


class GIL_833:
	"""Forest Guide"""
	# At the end of your turn, both players draw a card.
	events = OWN_TURN_END.on(Draw(PLAYER))


##
# Spells

class GIL_553:
	"""Wispering Woods"""
	# [x]Summon a 1/1 Wisp for each card in your hand.
	play = Summon(CONTROLLER, "GIL_553t") * Count(FRIENDLY_HAND)


class GIL_571:
	"""Witching Hour"""
	# Summon a random friendly Beast that died this game.
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + BEAST)))


class GIL_637:
	"""Ferocious Howl"""
	# Draw a card. Gain 1 Armor for each card in your hand.
	play = Draw(CONTROLLER), GainArmor(CONTROLLER, Count(FRIENDLY_HAND))


class GIL_663:
	"""Witchwood Apple"""
	# Add three 2/2 Treants to your hand.
	play = Give(CONTROLLER, "GIL_663t") * 2
