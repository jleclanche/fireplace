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

GVG_055e = buff(+2, +2)


# Iron Juggernaut
class GVG_056:
	play = Shuffle(OPPONENT, "GVG_056t")

# Burrowing Mine
class GVG_056t:
	draw = Destroy(SELF), Hit(FRIENDLY_HERO, 10), Draw(CONTROLLER)


# Siege Engine
class GVG_086:
	events = GainArmor(FRIENDLY_HERO).on(Buff(SELF, "GVG_086e"))

GVG_086e = buff(atk=1)


##
# Spells

# Bouncing Blade
class GVG_050:
	def play(self):
		targets = self.game.board.filter(dead=False)
		while True:
			live_targets = [t for t in targets if t.health > t.min_health]
			if live_targets != targets:
				break
			yield Hit(random.choice(targets), 1)


# Crush
class GVG_052:
	play = Destroy(TARGET)
	cost_mod = Find(FRIENDLY_MINIONS + DAMAGED) & -4
