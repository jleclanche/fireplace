from ..utils import *


# Big Game Hunter
class EX1_005:
	play = Destroy(TARGET)


# Mountain Giant
class EX1_105:
	cost = lambda self, i: i - (len(self.controller.hand) - 1)


# Faceless Manipulator
class EX1_564:
	play = Morph(SELF, ExactCopy(TARGET))


# Sea Giant
class EX1_586:
	cost = lambda self, i: i - len(self.game.board)


# Blood Knight
class EX1_590:
	play = (
		Buff(SELF, "EX1_590e") * Count(ALL_MINIONS + DIVINE_SHIELD),
		SetTag(ALL_MINIONS, {GameTag.DIVINE_SHIELD: False})
	)


# Molten Giant
class EX1_620:
	cost = lambda self, i: i - self.controller.hero.damage


# Captain's Parrot
class NEW1_016:
	play = ForceDraw(CONTROLLER, CONTROLLER_DECK + PIRATE)


# Hungry Crab
class NEW1_017:
	play = Destroy(TARGET), Buff(SELF, "NEW1_017e")


# Doomsayer
class NEW1_021:
	events = OWN_TURN_BEGIN.on(Destroy(ALL_MINIONS))
