from ..utils import *


##
# Minions

class GVG_016:
	"""Fel Reaver"""
	events = Play(OPPONENT).on(Mill(CONTROLLER, 3))


class GVG_092:
	"""Gnomish Experimenter"""
	play = Draw(CONTROLLER).then(
		Find(MINION + Draw.CARD) & Morph(Draw.CARD, "GVG_092t")
	)


class GVG_104:
	"""Hobgoblin"""
	events = Play(CONTROLLER, MINION + (ATK == 1)).on(Buff(Play.CARD, "GVG_104a"))


GVG_104a = buff(+2, +2)


class GVG_105:
	"""Piloted Sky Golem"""
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=4))


class GVG_106:
	"""Junkbot"""
	events = Death(FRIENDLY + MECH).on(Buff(SELF, "GVG_106e"))


GVG_106e = buff(+2, +2)


class GVG_107:
	"""Enhance-o Mechano"""
	def play(self):
		for target in self.controller.field.exclude(self):
			tag = random.choice((GameTag.WINDFURY, GameTag.TAUNT, GameTag.DIVINE_SHIELD))
			yield SetTag(target, (tag, ))


class GVG_108:
	"""Recombobulator"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Morph(TARGET, RandomMinion(cost=COST(TARGET)))


class GVG_121:
	"""Clockwork Giant"""
	cost_mod = -Count(ENEMY_HAND)


class GVG_122:
	"""Wee Spellstopper"""
	update = Refresh(SELF_ADJACENT, {
		GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
		GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
	})
