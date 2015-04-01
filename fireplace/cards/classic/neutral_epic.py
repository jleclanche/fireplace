from ..utils import *


# Big Game Hunter
class EX1_005:
	action = destroyTarget


# Mountain Giant
class EX1_105:
	def cost(self, value):
		return value - (len(self.controller.hand) - 1)


# Mrgglaargl! (Murloc Warleader)
class EX1_507e:
	requirements = {
		PlayReq.REQ_NONSELF_TARGET: True,
		PlayReq.REQ_TARGET_WITH_RACE: Race.MURLOC,
	}


# Sea Giant
class EX1_586:
	def cost(self, value):
		return value - len(self.game.board)


# Blood Knight
class EX1_590:
	def action(self):
		for target in self.game.board:
			if target.divineShield:
				target.divineShield = False
				self.buff(self, "EX1_590e")


# Molten Giant
class EX1_620:
	def cost(self, value):
		return value - self.controller.hero.damage


# Captain's Parrot
class NEW1_016:
	def action(self):
		pirates = self.controller.deck.filterByRace(Race.PIRATE)
		if pirates:
			self.controller.draw(random.choice(pirates))


# Hungry Crab
class NEW1_017:
	def action(self, target):
		target.destroy()
		self.buff(self, "NEW1_017e")


# Doomsayer
class NEW1_021:
	def OWN_TURN_BEGIN(self):
		for target in self.controller.getTargets(TARGET_ALL_MINIONS):
			target.destroy()


# Yarrr! (Southsea Captain)
class NEW1_027e:
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_NONSELF_TARGET: True,
		PlayReq.REQ_TARGET_WITH_RACE: Race.PIRATE,
	}
