from ..utils import *


##
# Minions

# Attack Mode (Anodized Robo Cub)
class GVG_030a:
	action = buffSelf("GVG_030ae")

# Tank Mode (Anodized Robo Cub)
class GVG_030b:
	action = buffSelf("GVG_030be")


# Gift of Mana (Grove Tender)
class GVG_032a:
	def action(self):
		for player in self.game.players:
			player.maxMana += 1
			player.usedMana -= 1

# Gift of Cards (Grove Tender)
class GVG_032b:
	def action(self):
		for player in self.game.players:
			player.draw()


# Druid of the Fang
class GVG_080:
	def action(self):
		if self.poweredUp:
			self.morph("GVG_080t")


##
# Spells

# Tree of Life
class GVG_033:
	def action(self):
		for target in self.controller.getTargets(TARGET_ALL_CHARACTERS):
			self.heal(target, target.maxHealth)
