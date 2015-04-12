from ..utils import *


##
# Minions

# Mistress of Pain
class GVG_018:
	def DAMAGE(self, source, target, amount):
		if source is self:
			self.heal(self.controller.hero, amount)


# Fel Cannon
class GVG_020:
	def OWN_TURN_END(self):
		targets = self.game.board.exclude(race=Race.MECHANICAL)
		if targets:
			self.hit(random.choice(targets))


##
# Spells

# Darkbomb
class GVG_015:
	action = damageTarget(3)


# Demonheart
class GVG_019:
	def action(self, target):
		if target.controller == self.controller and target.race == Race.DEMON:
			self.buff(target, "GVG_019e")
		else:
			self.hit(target, 5)
