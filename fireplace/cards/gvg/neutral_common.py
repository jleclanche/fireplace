from ..utils import *


##
# Minions

# Stonesplinter Trogg
class GVG_067:
	def CARD_PLAYED(self, player, card):
		if player is not self.controller and card.type == CardType.SPELL:
			self.buff("GVG_067a")

class GVG_067a:
	Atk = 1


# Burly Rockjaw Trogg
class GVG_068:
	def CARD_PLAYED(self, player, card):
		if player is not self.controller and card.type == CardType.SPELL:
			self.buff("GVG_068a")

class GVG_068a:
	Atk = 2


# Antique Healbot
class GVG_069:
	action = healHero(8)


# Ship's Cannon
class GVG_075:
	def OWN_MINION_SUMMONED(self, minion):
		if minion.race == Race.PIRATE:
			targets = self.controller.getTargets(TARGET_ENEMY_CHARACTERS)
			self.hit(random.choice(targets), 2)


# Explosive Sheep
class GVG_076:
	def deathrattle(self):
		for target in self.game.board:
			self.hit(target, 2)


# Mechanical Yeti
class GVG_078:
	def deathrattle(self):
		for player in self.game.players:
			player.give(random.choice(self.data.entourage))


# Clockwork Gnome
class GVG_082:
	deathrattle = giveSparePart


# Micro Machine
class GVG_103:
	def TURN_BEGIN(self, player):
		# That card ID is not a mistake
		self.buff(self, "GVG_076a")

# Pistons
class GVG_076a:
	Atk = 1
