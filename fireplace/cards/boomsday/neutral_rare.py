from ..utils import *


##
# Minions

class BOT_066:
	"""Mechanical Whelp"""
	# <b>Deathrattle:</b> Summon a 7/7 Mechanical Dragon.
	deathrattle = Summon(CONTROLLER, "BOT_066t")


class BOT_098:
	"""Unpowered Mauler"""
	# Can only attack if you cast a spell this turn.
	update = Find(CARDS_PLAYED_THIS_TURN + SPELL) | Refresh(SELF, {GameTag.CANT_ATTACK: True})


class BOT_102:
	"""Spark Drill"""
	# <b>Rush</b> <b>Deathrattle:</b> Add two 1/1 Sparks with <b>Rush</b> to your hand.
	deathrattle = Give(CONTROLLER, "BOT_102t") * 2


class BOT_107:
	"""Missile Launcher"""
	# [x]<b>Magnetic</b> At the end of your turn, deal 1 damage to all other characters.
	magnetic = MAGNETIC("BOT_107e")
	events = OWN_TURN_END.on(Hit(ALL_CHARACTERS - SELF, 1))


class BOT_107e:
	events = OWN_TURN_END.on(Hit(ALL_CHARACTERS - OWNER, 1))


class BOT_270:
	"""Giggling Inventor"""
	# <b>Battlecry:</b> Summon two 1/2 Mechs with <b>Taunt</b> and_<b>Divine Shield</b>.
	play = SummonBothSides(CONTROLLER, "BOT_270t")


class BOT_312:
	"""Replicating Menace"""
	# <b>Magnetic</b> <b>Deathrattle:</b> Summon three 1/1 Microbots.
	magnetic = MAGNETIC("BOT_312e")
	deathrattle = Summon(CONTROLLER, "BOT_312t") * 3


class BOT_312e:
	tags = {GameTag.DEATHRATTLE: True}
	deathrattle = Summon(CONTROLLER, "BOT_312t") * 3


class BOT_538:
	"""Spark Engine"""
	# <b>Battlecry:</b> Add a 1/1 Spark with <b>Rush</b> to_your hand.
	play = Give(CONTROLLER, "BOT_102t")


class BOT_539:
	"""Arcane Dynamo"""
	# <b>Battlecry:</b> <b>Discover</b> a spell that costs (5) or more.
	play = DISCOVER(RandomSpell(cost=range(5, 100)))


class BOT_907:
	"""Galvanizer"""
	# [x]<b>Battlecry:</b> Reduce the Cost of Mechs in your hand by (1).
	play = Buff(FRIENDLY_HAND + MECH, "BOT_907e")


class BOT_907e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -1}
