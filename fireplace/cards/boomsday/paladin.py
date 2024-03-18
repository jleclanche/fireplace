from ..utils import *


##
# Minions

class BOT_236:
	"""Crystalsmith Kangor"""
	# <b>Divine Shield</b>, <b>Lifesteal</b> Your healing is doubled.
	update = Refresh(CONTROLLER, {GameTag.HEALING_DOUBLE: 1})


class BOT_537:
	"""Mechano-Egg"""
	# <b>Deathrattle:</b> Summon an 8/8 Robosaur.
	deathrattle = Summon(CONTROLLER, "BOT_537t")


class BOT_906:
	"""Glow-Tron"""
	# <b>Magnetic</b>
	magnetic = MAGNETIC("BOT_906e")


class BOT_910:
	"""Glowstone Technician"""
	# <b>Battlecry:</b> Give all minions in your hand +2/+2.
	play = Buff(FRIENDLY_HAND + MINION, "BOT_910e")


BOT_910e = buff(+2, +2)


class BOT_911:
	"""Annoy-o-Module"""
	# <b>Magnetic</b> <b>Divine Shield</b> <b>Taunt</b>
	magnetic = MAGNETIC("BOT_911e")


class BOT_911e:
	tags = {GameTag.TAUNT: True}

	def apply(self, target):
		self.game.trigger(self, (GiveDivineShield(target), ), None)


##
# Spells

class BOT_234:
	"""Shrink Ray"""
	# Set the Attack and Health of all minions to 1.
	play = Buff(ALL_MINIONS, "BOT_234e")


class BOT_234e:
	atk = SET(1)
	max_health = SET(1)


class BOT_436:
	"""Prismatic Lens"""
	# Draw a minion and a spell from your deck. Swap their Costs.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
	}
	play = FindAll(
		FRIENDLY_DECK + MINION,
		FRIENDLY_DECK + SPELL
	) & SwapStateBuff(
		ForceDraw(RANDOM(FRIENDLY_DECK + MINION)),
		ForceDraw(RANDOM(FRIENDLY_DECK + SPELL)),
		"BOT_436e"
	) | (
		ForceDraw(RANDOM(FRIENDLY_DECK + MINION)),
		ForceDraw(RANDOM(FRIENDLY_DECK + SPELL)),
	)


class BOT_436e:
	cost = lambda self, i: self._xcost
	events = REMOVED_IN_PLAY


class BOT_908:
	"""Autodefense Matrix"""
	# <b>Secret:</b> When one of your minions is attacked, give it <b>Divine Shield</b>.
	secret = Attack(None, FRIENDLY_MINIONS).on(
		Reveal(SELF), GiveDivineShield(Attack.DEFENDER)
	)


class BOT_909:
	"""Crystology"""
	# [x]Draw two 1-Attack minions from your deck.
	play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 1)))


class BOT_912:
	"""Kangor's Endless Army"""
	# Resurrect 3 friendly Mechs. They keep any <b>Magnetic</b> upgrades.
	requirements = {
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
		PlayReq.REQ_FRIENDLY_MINIONS_OF_RACE_DIED_THIS_GAME: 17,
	}
	play = Summon(CONTROLLER, KeepMagneticCopy(RANDOM(FRIENDLY + KILLED + MECH) * 3))
