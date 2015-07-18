from ..utils import *


# Big Game Hunter
class EX1_005:
	action = [Destroy(TARGET)]


# Mountain Giant
class EX1_105:
	def cost(self, value):
		return value - (len(self.controller.hand) - 1)


# Sea Giant
class EX1_586:
	def cost(self, value):
		return value - len(self.game.board)


# Blood Knight
class EX1_590:
	action = [
		Buff(SELF, "EX1_590e") * Count(ALL_MINIONS + DIVINE_SHIELD),
		SetTag(ALL_MINIONS, {GameTag.DIVINE_SHIELD: False})
	]


# Molten Giant
class EX1_620:
	def cost(self, value):
		return value - self.controller.hero.damage


# Captain's Parrot
class NEW1_016:
	action = [ForceDraw(CONTROLLER, CONTROLLER_DECK + PIRATE)]


# Hungry Crab
class NEW1_017:
	action = [Destroy(TARGET), Buff(SELF, "NEW1_017e")]


# Doomsayer
class NEW1_021:
	events = [
		OWN_TURN_BEGIN.on(Destroy(ALL_MINIONS))
	]
