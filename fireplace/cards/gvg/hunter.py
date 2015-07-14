from ..utils import *


##
# Minions

# King of Beasts
class GVG_046:
	action = [Buff(SELF, "GVG_046e") * Count(FRIENDLY_MINIONS + BEAST)]


# Metaltooth Leaper
class GVG_048:
	action = [Buff(RANDOM(FRIENDLY_MINIONS + MECH - SELF), "GVG_048e")]


# Gahz'rilla
class GVG_049:
	events = [
		SELF_DAMAGE.on(Buff(SELF, "GVG_049e"))
	]

class GVG_049e:
	atk = lambda self, i: i * 2


##
# Spells

# Call Pet
class GVG_017:
	# TODO
	def action(self):
		card = self.controller.draw()
		if card.type == CardType.MINION and card.race == Race.BEAST:
			self.buff(card, "GVG_017e")


# Feign Death
class GVG_026:
	action = [Deathrattle(FRIENDLY_MINIONS)]


# Cobra Shot
class GVG_073:
	action = [Hit(TARGET | ENEMY_HERO, 3)]


##
# Weapons

# Glaivezooka
class GVG_043:
	action = [Buff(RANDOM_FRIENDLY_MINION, "GVG_043e")]
