from ..utils import *


##
# Minions

# Kezan Mystic
class GVG_074:
	action = [TakeControl(RANDOM(ENEMY_SECRETS))]


# Jeeves
class GVG_094:
	def TURN_END(self, player):
		return [Draw(CONTROLLER, max(0, 3 - len(player.hand)))]


# Goblin Sapper
class GVG_095:
	def atk(self, i):
		if len(self.controller.opponent.hand) >= 6:
			return i + 4
		return i


# Bomb Lobber
class GVG_099:
	action = [Hit(RANDOM_ENEMY_MINION, 4)]
