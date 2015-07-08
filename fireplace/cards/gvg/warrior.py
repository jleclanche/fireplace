from ..utils import *


##
# Minions

# Shieldmaiden
class GVG_053:
	action = [GainArmor(FRIENDLY_HERO, 5)]


# Screwjank Clunker
class GVG_055:
	action = [Buff(TARGET, "GVG_055e")]


# Iron Juggernaut
class GVG_056:
	action = [Shuffle(OPPONENT, "GVG_056t")]

# Burrowing Mine
class GVG_056t:
	action = [Hit(FRIENDLY_HERO, 10), Draw(CONTROLLER, 1)]


##
# Spells

# Bouncing Blade
class GVG_050:
	def action(self):
		while True:
			targets = self.game.board.filter(dead=False)
			targets = [t for t in targets if t.health > t.min_health]
			if not targets:
				break
			yield Hit(random.choice(targets), 1)


# Crush
class GVG_052:
	action = [Destroy(TARGET)]

	def cost(self, value):
		for minion in self.controller.field:
			if minion.damaged:
				return value - 4
		return value
