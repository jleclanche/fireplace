from ..utils import *


##
# Minions

# Goblin Auto-Barber
class GVG_023:
	action = buffWeapon("GVG_023a")


# One-eyed Cheat
class GVG_025:
	def OWN_MINION_SUMMON(self, minion):
		if minion.race == Race.PIRATE and minion != self:
			self.stealth = True


# Iron Sensei
class GVG_027:
	def OWN_TURN_END(self):
		mechs = self.controller.field.filter(race=Race.MECHANICAL).exclude(self)
		if mechs:
			self.buff(random.choice(mechs), "GVG_027e")


# Trade Prince Gallywix
class GVG_028:
	def CARD_PLAYED(self, player, card):
		if player is not self.controller and card.type == CardType.SPELL:
			if card.id != "GVG_028t":
				player.opponent.give(card.id)
				player.give("GVG_028t")

class GVG_028t:
	def action(self):
		self.controller.tempMana += 1


##
# Spells

# Tinker's Sharpsword Oil
class GVG_022:
	action = buffWeapon("GVG_022a")

	def action(self):
		if self.controller.weapon:
			self.buff(self.controller.weapon, "GVG_022a")
		if self.controller.field:
			self.buff(random.choice(self.controller.field), "GVG_022b")


##
# Weapons

# Cogmaster's Wrench
class GVG_024:
	def atk(self, i):
		if self.controller.field.filter(race=Race.MECHANICAL):
			return i + 2
		return i
