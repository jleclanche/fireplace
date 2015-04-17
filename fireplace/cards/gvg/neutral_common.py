from ..utils import *


##
# Minions

# Cogmaster
class GVG_013:
	def atk(self, i):
		if self.controller.field.filter(race=Race.MECHANICAL):
			return i + 2
		return i


# Stonesplinter Trogg
class GVG_067:
	def CARD_PLAYED(self, player, card):
		if player is not self.controller and card.type == CardType.SPELL:
			self.buff(self, "GVG_067a")


# Burly Rockjaw Trogg
class GVG_068:
	def CARD_PLAYED(self, player, card):
		if player is not self.controller and card.type == CardType.SPELL:
			self.buff(self, "GVG_068a")


# Antique Healbot
class GVG_069:
	action = healHero(8)


# Ship's Cannon
class GVG_075:
	def OWN_MINION_SUMMON(self, minion):
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
