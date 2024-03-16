from ..utils import *


##
# Minions

class DAL_372:
	"""Arcane Fletcher"""
	# [x]Whenever you play a 1-Cost minion, draw a spell from your deck.
	events = Play(CONTROLLER, MINION + (COST == 1)).on(
		ForceDraw(RANDOM(FRIENDLY_DECK + SPELL))
	)


class DAL_376:
	"""Oblivitron"""
	# [x]<b>Deathrattle:</b> Summon a Mech from your hand and trigger its
	# <b>Deathrattle</b>.
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MECH)).then(
		Deathrattle(Summon.CARD)
	)


class DAL_379:
	"""Vereesa Windrunner"""
	# <b>Battlecry:</b> Equip Thori'dal, the Stars' Fury.
	play = Summon(CONTROLLER, "DAL_379t")


class DAL_379t:
	events = Attack(FRIENDLY_HERO).after(Buff(CONTROLLER, "DAL_379e"))


DAL_379e = buff(spellpower=2)


class DAL_587:
	"""Shimmerfly"""
	# <b>Deathrattle:</b> Add a random Hunter spell to your hand.
	deathrattle = Give(CONTROLLER, RandomSpell(card_class=CardClass.HUNTER))


class DAL_604:
	"""Ursatron"""
	# <b>Deathrattle:</b> Draw a Mech from your deck.
	deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + MECH))


##
# Spells

class DAL_371:
	"""Marked Shot"""
	# Deal $4 damage to_a_minion. <b>Discover</b>_a_spell.
	play = Hit(TARGET, 4), DISCOVER(RandomSpell())


class DAL_373:
	"""Rapid Fire"""
	# <b>Twinspell</b> Deal $1 damage.
	play = Give(CONTROLLER, "DAL_373ts"), Hit(TARGET, 1)


class DAL_373ts:
	play = Hit(TARGET, 1)


class DAL_377:
	"""Nine Lives"""
	# <b>Discover</b> a friendly <b>Deathrattle</b> minion that died this game. Also
	# trigger its <b>Deathrattle</b>.
	play = GenericChoice(
		CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + DEATHRATTLE + MINION)) * 3)
	).then(
		Give(CONTROLLER, GenericChoice.CARD),
		Deathrattle(GenericChoice.CARD)
	)


class DAL_378:
	"""Unleash the Beast"""
	# <b>Twinspell</b> Summon a 5/5 Wyvern with <b>Rush</b>.
	play = Give(CONTROLLER, "DAL_378ts"), Summon(CONTROLLER, "DAL_378t1")


class DAL_378ts:
	play = Summon(CONTROLLER, "DAL_378t1")


class DAL_589:
	"""Hunting Party"""
	# Copy all Beasts in your_hand.
	play = Give(CONTROLLER, ExactCopy(FRIENDLY_HAND + BEAST))
