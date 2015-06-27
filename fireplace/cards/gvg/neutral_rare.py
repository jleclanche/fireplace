from ..utils import *


##
# Minions

# Kezan Mystic
class GVG_074:
	action = [TakeControl(RANDOM(ENEMY_SECRETS))]


# Jeeves
class GVG_094:
	events = [
		TURN_END.on(
			lambda self, player: [Draw(player) * max(0, 3 - len(player.hand))]
		)
	]


# Goblin Sapper
class GVG_095:
	def atk(self, i):
		if len(self.controller.opponent.hand) >= 6:
			return i + 4
		return i


# Lil' Exorcist
class GVG_097:
	def action(self):
		deathrattles = self.controller.opponent.field.filter(has_deathrattle=True)
		# The Enchantment ID is correct
		return [Buff(SELF, "GVG_101e") * len(deathrattles)]


# Bomb Lobber
class GVG_099:
	action = [Hit(RANDOM_ENEMY_MINION, 4)]
