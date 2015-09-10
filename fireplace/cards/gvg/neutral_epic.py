from ..utils import *


##
# Minions

# Fel Reaver
class GVG_016:
	events = Play(OPPONENT).on(Mill(CONTROLLER, 3))


# Hobgoblin
class GVG_104:
	events = Play(CONTROLLER, MINION + (ATK == 1)).on(Buff(Play.Args.CARD, "GVG_104a"))


# Piloted Sky Golem
class GVG_105:
	deathrattle = Summon(CONTROLLER, RandomMinion(cost=4))


# Junkbot
class GVG_106:
	events = Death(FRIENDLY + MECH).on(Buff(SELF, "GVG_106e"))


# Enhance-o Mechano
class GVG_107:
	def play(self):
		for target in self.controller.field.exclude(self):
			tag = random.choice((GameTag.WINDFURY, GameTag.TAUNT, GameTag.DIVINE_SHIELD))
			yield SetTag(target, {tag: True})


# Recombobulator
class GVG_108:
	play = Morph(TARGET, RandomMinion(cost=Attr(TARGET, GameTag.COST)))


# Clockwork Giant
class GVG_121:
	cost_mod = -Count(OPPONENT_HAND)


# Wee Spellstopper
class GVG_122:
	update = Refresh(SELF_ADJACENT, {
		GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
		GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
	})
