from ..utils import *


##
# Minions

class LOOT_357:
	"""Marin the Fox"""
	# <b>Battlecry:</b> Summon a 0/8 Treasure Chest for your opponent. <i>(Break it for
	# awesome loot!)</i>
	play = Summon(OPPONENT, "LOOT_357l")


class LOOT_357l:
	entourage = ["LOOT_998h", "LOOT_998j", "LOOT_998l", "LOOT_998k"]
	deathrattle = Give(OPPONENT, RandomEntourage())


class LOOT_998h:
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)) * (
		MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
	))


class LOOT_998j:
	requirements = {
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	play = Discover(CONTROLLER, RandomLegendaryMinion()).then(
		Summon(CONTROLLER, Discover.CARD) * 2
	)


class LOOT_998l:
	play = (Draw(CONTROLLER) * 3).then(Buff(Draw.CARD, "LOOT_998le"))


class LOOT_998le:
	cost = SET(0)
	events = REMOVED_IN_PLAY


class LOOT_998k:
	play = Morph(FRIENDLY_HAND, RandomLegendaryMinion())


class LOOT_516:
	"""Zola the Gorgon"""
	# <b>Battlecry:</b> Choose a friendly minion. Add a Golden copy of it to your hand.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Give(CONTROLLER, Copy(TARGET))


class LOOT_521:
	"""Master Oakheart"""
	# <b>Battlecry:</b> <b>Recruit</b> a 1, 2, and 3-Attack minion.
	play = Recruit(COST == 1), Recruit(COST == 2), Recruit(COST == 3)


class LOOT_526:
	"""The Darkness"""
	# [x]Starts dormant. <b>Battlecry:</b> Shuffle 3 Candles into the enemy deck. When
	# drawn, this awakens.
	play = Morph(SELF, "LOOT_526d"), Shuffle(CONTROLLER, "LOOT_526t") * 3


class LOOT_526d:
	progress_total = 3
	reward = Morph(SELF, "LOOT_526")


class LOOT_526t:
	draw = (
		Destroy(SELF),
		AddProgress(FuncSelector(lambda entities, source: [source.creator.morphed]), SELF),
		Draw(CONTROLLER)
	)


class LOOT_541:
	"""King Togwaggle"""
	# [x]<b>Battlecry:</b> Swap decks with your opponent. Give them a Ransom spell to swap
	# back.
	play = SwapController(IN_DECK), Give(OPPONENT, "LOOT_541t")


class LOOT_541t:
	play = SwapController(IN_DECK)
