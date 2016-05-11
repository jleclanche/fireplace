from ..utils import *


##
# Minions

class GVG_051:
	"Warbot"
	enrage = Refresh(SELF, buff="GVG_051e")

GVG_051e = buff(atk=1)


class GVG_053:
	"Shieldmaiden"
	play = GainArmor(FRIENDLY_HERO, 5)


class GVG_055:
	"Screwjank Clunker"
	powered_up = Find(FRIENDLY_MINIONS + MECH)
	play = Buff(TARGET, "GVG_055e")

GVG_055e = buff(+2, +2)


class GVG_056:
	"Iron Juggernaut"
	play = Shuffle(OPPONENT, "GVG_056t")

class GVG_056t:
	"Burrowing Mine"
	draw = Destroy(SELF), Hit(FRIENDLY_HERO, 10), Draw(CONTROLLER)


class GVG_086:
	"Siege Engine"
	events = GainArmor(FRIENDLY_HERO).on(Buff(SELF, "GVG_086e"))

GVG_086e = buff(atk=1)


##
# Spells

class GVG_050:
	"Bouncing Blade"
	def play(self):
		targets = self.game.board.filter(dead=False)
		while True:
			live_targets = [t for t in targets if t.health > t.min_health]
			if live_targets != targets:
				break
			yield Hit(random.choice(targets), 1)


class GVG_052:
	"Crush"
	play = Destroy(TARGET)
	cost_mod = Find(FRIENDLY_MINIONS + DAMAGED) & -4


##
# Weapons

class GVG_054:
	"Ogre Warmaul"
	events = FORGETFUL
