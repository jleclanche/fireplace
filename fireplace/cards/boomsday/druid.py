from ..utils import *


##
# Minions

class BOT_419:
	"""Dendrologist"""
	# <b>Battlecry:</b> If you control a Treant, <b>Discover</b> a spell.
	play = Find(FRIENDLY_MINIONS + TREANT) & DISCOVER(RandomSpell())


class BOT_422:
	"""Tending Tauren"""
	# [x]<b>Choose One -</b> Give your other minions +1/+1; or Summon two 2/2 Treants.
	choose = ("BOT_422a", "BOT_422b")
	play = ChooseBoth(CONTROLLER) & (
		SummonBothSides(CONTROLLER, "EX1_158t") * 2, Buff(FRIENDLY_MINIONS - SELF, "BOT_422ae")
	)


class BOT_422a:
	play = Buff(FRIENDLY_MINIONS - SELF, "BOT_422ae")


BOT_422ae = buff(+1, +1)


class BOT_422b:
	play = SummonBothSides(CONTROLLER, "EX1_158t") * 2


class BOT_423:
	"""Dreampetal Florist"""
	# At the end of your turn, reduce the Cost of a random minion in your hand by (7).
	events = OWN_TURN_END.on(Buff(RANDOM(FRIENDLY_HAND + MINION), "BOT_423e"))


class BOT_423e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -7}


class BOT_434:
	"""Flobbidinous Floop"""
	# While in your hand, this is a 3/4 copy of the last minion you played.
	class Hand:
		events = Play(CONTROLLER).after(
			Morph(SELF, Copy(Play.CARD)).then(Buff(Morph.CARD, "BOT_434e"))
		)


class BOT_434e:
	class Hand:
		events = Play(CONTROLLER).after(
			Morph(OWNER, Copy(Play.CARD)).then(Buff(Morph.CARD, "BOT_434e"))
		)


class BOT_507:
	"""Gloop Sprayer"""
	# <b>Battlecry:</b> Summon a copy of each adjacent minion.
	play = Summon(CONTROLLER, ExactCopy(SELF_ADJACENT))


class BOT_523:
	"""Mulchmuncher"""
	# <b>Rush</b>. Costs (1) less for each friendly Treant that died this game.
	cost_mod = -Count(FRIENDLY + KILLED + TREANT)


##
# Spells

class BOT_054:
	"""Biology Project"""
	# Each player gains 2_Mana Crystals.
	play = GainMana(PLAYER, 2)


class BOT_404:
	"""Juicy Psychmelon"""
	# Draw a 7, 8, 9, and 10-Cost minion from your deck.
	play = (
		ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 7))),
		ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 8))),
		ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 9))),
		ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 10))),
	)


class BOT_420:
	"""Landscaping"""
	# Summon two 2/2 Treants.
	play = Summon(CONTROLLER, "EX1_158t") * 2


class BOT_444:
	"""Floop's Glorious Gloop"""
	# Whenever a minion dies this turn, gain 1 Mana Crystal this turn only.
	play = Buff(CONTROLLER, "BOT_444e")


class BOT_444e:
	events = Death(MINION).on(ManaThisTurn(CONTROLLER, 1))
