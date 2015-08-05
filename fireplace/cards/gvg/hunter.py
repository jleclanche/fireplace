from ..utils import *


##
# Minions

# King of Beasts
class GVG_046:
	play = Buff(SELF, "GVG_046e") * Count(FRIENDLY_MINIONS + BEAST)


# Metaltooth Leaper
class GVG_048:
	play = Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_048e")


# Gahz'rilla
class GVG_049:
	events = SELF_DAMAGE.on(Buff(SELF, "GVG_049e"))

class GVG_049e:
	atk = lambda self, i: i * 2


# Steamwheedle Sniper
class GVG_087:
	aura = Buff(CONTROLLER, "GVG_087a")


##
# Spells

# Call Pet
class GVG_017:
	# TODO
	def play(self):
		card = self.controller.draw()
		if card.type == CardType.MINION and card.race == Race.BEAST:
			self.buff(card, "GVG_017e")


# Feign Death
class GVG_026:
	play = Deathrattle(FRIENDLY_MINIONS)


# Cobra Shot
class GVG_073:
	play = Hit(TARGET | ENEMY_HERO, 3)


##
# Weapons

# Glaivezooka
class GVG_043:
	play = Buff(RANDOM_FRIENDLY_MINION, "GVG_043e")
