from ..utils import *


##
# Minions

# Goblin Auto-Barber
class GVG_023:
	action = [Buff(FRIENDLY_WEAPON, "GVG_023a")]


# One-eyed Cheat
class GVG_025:
	def OWN_MINION_SUMMON(self, minion):
		if minion.race == Race.PIRATE and minion != self:
			return [GiveStealth(SELF)]


# Iron Sensei
class GVG_027:
	OWN_TURN_END = [Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_027e")]


# Trade Prince Gallywix
class GVG_028:
	def CARD_PLAYED(self, player, card):
		if player is not self.controller and card.type == CardType.SPELL:
			if card.id != "GVG_028t":
				return [Give(player.opponent, card.id), Give(player, "GVG_028t")]

class GVG_028t:
	action = [ManaThisTurn(CONTROLLER, 1)]


##
# Spells

# Tinker's Sharpsword Oil
class GVG_022:
	action = [Buff(FRIENDLY_WEAPON, "GVG_022a")]
	combo = [Buff(FRIENDLY_WEAPON, "GVG_022a"), Buff(RANDOM_FRIENDLY_CHARACTER, "GVG_022b")]


##
# Weapons

# Cogmaster's Wrench
class GVG_024:
	def atk(self, i):
		if self.controller.field.filter(race=Race.MECHANICAL):
			return i + 2
		return i
