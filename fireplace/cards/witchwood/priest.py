from ..utils import *


##
# Minions

class GIL_142:
	"""Chameleos"""
	# Each turn this is in your hand, transform it into a card your opponent is holding.
	class Hand:
		events = OWN_TURN_BEGIN.on(
			Find(ENEMY_HAND) & (
				Morph(SELF, ExactCopy(RANDOM(ENEMY_HAND))).then(Buff(Morph.CARD, "GIL_142e"))
			)
		)


class GIL_142e:
	class Hand:
		events = OWN_TURN_BEGIN.on(
			Find(ENEMY_HAND) & (
				Morph(OWNER, ExactCopy(RANDOM(ENEMY_HAND))).then(Buff(Morph.CARD, "GIL_142e"))
			)
		)
	events = REMOVED_IN_PLAY


class GIL_156:
	"""Quartz Elemental"""
	# Can't attack while damaged.
	update = Find(DAMAGED + SELF) & Refresh(SELF, {GameTag.CANT_ATTACK: True})


class GIL_190:
	"""Nightscale Matriarch"""
	# Whenever a friendly minion is healed, summon a 3/3_Whelp.
	events = Heal(FRIENDLY_MINIONS).on(Summon(CONTROLLER, "GIL_190t"))


class GIL_805:
	"""Coffin Crasher"""
	# <b>Deathrattle:</b> Summon a <b>Deathrattle</b> minion from your hand.
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEATHRATTLE))


class GIL_835:
	"""Squashling"""
	# [x]<b>Echo</b> <b>Battlecry:</b> Restore 2 Health.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = Heal(TARGET, 2)


class GIL_837:
	"""Glitter Moth"""
	# <b>Battlecry:</b> If your deck has only odd-Cost cards, double the Health of your
	# other minions.
	powered_up = OddCost(FRIENDLY_DECK)
	play = powered_up & Buff(FRIENDLY_MINIONS - SELF, "GIL_837e")


class GIL_837e:
	def apply(self, target):
		self._xhealth = target.health * 2

	max_health = lambda self, _: self._xhealth


class GIL_840:
	"""Lady in White"""
	# [x]<b>Battlecry:</b> Cast 'Inner Fire' _on every minion in your deck_ <i>(set Attack
	# equal to Health).</i>
	play = CastSpell("CS1_129", FRIENDLY_DECK + MINION)


##
# Spells

class GIL_134:
	"""Holy Water"""
	# Deal $4 damage to a minion. If that kills it, add a copy of it to your_hand.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Hit(TARGET, 4), Dead(TARGET) & Give(CONTROLLER, Copy(TARGET))


class GIL_661:
	"""Divine Hymn"""
	# Restore #6 Health to all friendly characters.
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Heal(FRIENDLY_CHARACTERS, 6)


class GIL_813:
	"""Vivid Nightmare"""
	# [x]Choose a friendly minion. Summon a copy of it with 1 Health remaining.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
	}
	play = Summon(CONTROLLER, SetCurrentHealth(ExactCopy(TARGET), 1))
