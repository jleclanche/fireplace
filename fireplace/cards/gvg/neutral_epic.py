from ..utils import *


##
# Minions

# Fel Reaver
class GVG_016:
	events = Play(OPPONENT).on(Mill(CONTROLLER, 3))


# Hobgoblin
class GVG_104:
	events = Play(CONTROLLER, MINION + (ATK == 1)).on(Buff(Play.CARD, "GVG_104a"))

GVG_104a = buff(+2, +2)


# Piloted Sky Golem
class GVG_105:
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=4))


# Junkbot
class GVG_106:
	events = Death(FRIENDLY + MECH).on(Buff(SELF, "GVG_106e"))

GVG_106e = buff(+2, +2)


# Enhance-o Mechano
class GVG_107:
	def play(self):
		for target in self.controller.field.exclude(self):
			tag = random.choice((GameTag.WINDFURY, GameTag.TAUNT, GameTag.DIVINE_SHIELD))
			yield SetTag(target, (tag, ))


# Recombobulator
class GVG_108:
	play = Morph(TARGET, RandomMinion(cost=COST(TARGET)))


# Clockwork Giant
class GVG_121:
	cost_mod = -Count(ENEMY_HAND)


# Wee Spellstopper
class GVG_122:
	update = Refresh(SELF_ADJACENT, {
		GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
		GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
	})
