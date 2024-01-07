from ..utils import *


##
# Minions

class TRL_096:
	"""Griftah"""
	# [x]<b>Battlecry:</b> <b>Discover</b> two cards. Give one to your opponent at random.
	play = GriftahAction(CONTROLLER)


class TRL_537:
	"""Da Undatakah"""
	# [x]<b>Battlecry:</b> Gain the <b>Deathrattle</b> effects of 3 friendly minions that
	# died this game.
	play = CopyDeathrattleBuff(
		RANDOM(FRIENDLY + KILLED + MINION + DEATHRATTLE) * 3, "TRL_537e"
	)


class TRL_541:
	"""Hakkar, the Soulflayer"""
	# <b>Deathrattle:</b> Shuffle a Corrupted Blood into each player's deck.
	deathrattle = Shuffle(PLAYER, "TRL_541t")


class TRL_541t:
	"""Corrupted Blood"""
	# <b>Casts When Drawn</b> Take 3 damage. After you draw, shuffle two copies of this
	# into your deck.
	play = Hit(FRIENDLY_HERO, 3), Shuffle(CONTROLLER, "TRL_541t") * 2
	draw = CAST_WHEN_DRAWN


class TRL_542:
	"""Oondasta"""
	# <b>Rush</b> <b>Overkill:</b> Summon a Beast from your hand.
	overkill = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + BEAST))


class TRL_564:
	"""Mojomaster Zihi"""
	# <b>Battlecry:</b> Set each player to 5 Mana Crystals.
	play = SetMana(PLAYER, 5)
