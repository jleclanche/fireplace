from ..utils import *


##
# Minions

class GIL_634:
	"""Bellringer Sentry"""
	# <b>Battlecry and Deathrattle:</b> Put a <b>Secret</b> from your deck into the
	# battlefield.
	play = deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + SECRET))


class GIL_635:
	"""Cathedral Gargoyle"""
	# <b>Battlecry:</b> If you're holding a Dragon, gain <b>Taunt</b> and <b>Divine
	# Shield</b>.
	powered_up = HOLDING_DRAGON
	play = powered_up & (Taunt(SELF), GiveDivineShield(SELF))


class GIL_685:
	"""Paragon of Light"""
	# While this minion has 3 or more Attack, it has <b>Taunt</b> and <b>Lifesteal</b>.
	update = Find(SELF + (ATK >= 3)) & Refresh(SELF, {
		GameTag.TAUNT: True,
		GameTag.LIFESTEAL: True,
	})


class GIL_694:
	"""Prince Liam"""
	# [x]<b>Battlecry:</b> Transform all 1-Cost cards in your deck _into <b>Legendary</b>
	# minions.
	play = Morph(FRIENDLY_DECK + (COST == 1), RandomLegendaryMinion())


class GIL_817:
	"""The Glass Knight"""
	# [x]<b>Divine Shield</b> Whenever you restore Health, gain <b>Divine Shield</b>.
	events = Heal(source=FRIENDLY).on(GiveDivineShield(SELF))


##
# Spells

class GIL_145:
	"""Sound the Bells!"""
	# <b>Echo</b> Give a minion +1/+2.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Buff(TARGET, "GIL_145e")


GIL_145e = buff(+1, +2)


class GIL_203:
	"""Rebuke"""
	# Enemy spells cost (5) more next turn.
	play = Buff(OPPONENT, "GIL_203e")


class GIL_203e:
	update = CurrentPlayer(OWNER) & Refresh(ENEMY_HAND + SPELL, {GameTag.COST: +5})
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


class GIL_903:
	"""Hidden Wisdom"""
	# [x]<b>Secret:</b> After your opponent plays three cards in a turn, draw 2 cards.
	secret = Play(OPPONENT).after(
		(Count(OPPONENT_CARDS_PLAYED_THIS_TRUN) >= 3) & (
			Reveal(SELF), Draw(CONTROLLER, 2)
		)
	)


##
# Weapons

class GIL_596:
	"""Silver Sword"""
	# After your hero attacks, give your minions +1/+1.
	events = events = Attack(FRIENDLY_HERO).after(Buff(FRIENDLY_MINIONS, "GIL_596e"))


GIL_596e = buff(+1, +1)
