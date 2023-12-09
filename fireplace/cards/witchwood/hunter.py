from ..utils import *


##
# Minions

class GIL_128:
	"""Emeriss"""
	# <b>Battlecry:</b> Double the Attack and Health of all minions in_your hand.
	play = Buff(FRIENDLY_HAND + MINION, "GIL_128e")


class GIL_128e:
	def apply(self, target):
		self._xatk = target.atk * 2
		self._xhealth = target.health * 2
		target.damage = 0

	atk = lambda self, _: self._xatk
	max_health = lambda self, _: self._xhealth


class GIL_200:
	"""Duskhaven Hunter"""
	# [x]<b>Stealth</b> Each turn this is in your hand, swap its Attack and Health.
	class Hand:
		events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_200t", "GIL_200e")))


class GIL_200t:
	"""Duskhaven Hunter"""
	# [x]<b>Stealth</b> Each turn this is in your hand, swap its Attack and Health.
	class Hand:
		events = OWN_TURN_BEGIN.on(Morph(SELF, Buff("GIL_200", "GIL_200e")))


class GIL_200e:
	def apply(self, target):
		self._xatk = self.source.health
		self._xhealth = self.source.atk
		target.damage = 0

	atk = lambda self, _: self._xatk
	max_health = lambda self, _: self._xhealth


class GIL_607:
	"""Toxmonger"""
	# [x]Whenever you play a 1-Cost minion, give it <b>Poisonous</b>.
	events = Play(CONTROLLER, MINION + (COST == 1)).then(GivePoisonous(Play.CARD))



class GIL_650:
	"""Houndmaster Shaw"""
	# Your other minions have <b>Rush</b>.
	update = Refresh(FRIENDLY_MINIONS - SELF, {GameTag.RUSH: True})


class GIL_905:
	"""Carrion Drake"""
	# <b>Battlecry:</b> If a minion died this turn, gain <b>Poisonous</b>.
	play = Find(KILLED_THIS_TURN) & GivePoisonous(SELF)


##
# Spells

class GIL_518:
	"""Wing Blast"""
	# Deal $4 damage to a minion. If a minion died this turn, this costs (1).
	play = Hit(TARGET, 4)
	class Hand:
		update = Find(KILLED_THIS_TURN) & Refresh(SELF, {GameTag.COST: SET(1)})


class GIL_577:
	"""Rat Trap"""
	# [x]<b>Secret:</b> After your opponent plays three cards in a turn, summon a 6/6 Rat.
	secret = Play(OPPONENT).after(
		(Attr(OPPONENT, GameTag.NUM_CARDS_PLAYED_THIS_TURN) >= 3) & (
			FULL_BOARD | (Reveal(SELF), Summon(CONTROLLER, "GIL_577t"))
		)
	)


class GIL_828:
	"""Dire Frenzy"""
	# Give a Beast +3/+3. Shuffle 3 copies into your deck with +3/+3.
	play = Buff(TARGET, "GIL_828e").then(
		Shuffle(CONTROLLER, ExactCopy(TARGET)) * 3
	)


GLI_828e = buff(+3, +3)
