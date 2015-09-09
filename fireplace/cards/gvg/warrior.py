from ..utils import *


##
# Minions

# Warbot
class GVG_051:
	enrage = Refresh(SELF, {GameTag.ATK: +1})


# Shieldmaiden
class GVG_053:
	play = GainArmor(FRIENDLY_HERO, 5)


# Screwjank Clunker
class GVG_055:
	powered_up = Find(FRIENDLY_MINIONS + MECH)
	play = Buff(TARGET, "GVG_055e")


# Iron Juggernaut
class GVG_056:
	play = Shuffle(OPPONENT, "GVG_056t")

# Burrowing Mine
class GVG_056t:
	draw = Hit(FRIENDLY_HERO, 10), Draw(CONTROLLER), Destroy(SELF)


# Siege Engine
class GVG_086:
	events = GainArmor(FRIENDLY_HERO).on(Buff(SELF, "GVG_086e"))


##
# Spells

# Bouncing Blade
class GVG_050:
	def play(self):
		while True:
			targets = self.game.board.filter(dead=False)
			targets = [t for t in targets if t.health > t.min_health]
			if not targets:
				break
			yield Hit(random.choice(targets), 1)


# Crush
class GVG_052:
	play = Destroy(TARGET)

	def cost(self, value):
		for minion in self.controller.field:
			if minion.damaged:
				return value - 4
		return value
