from ..utils import *


##
# Spells

# Ancestor's Call
class GVG_029:
	def action(self):
		for player in self.game.players:
			minions = player.hand.filter(type=CardType.MINION)
			if minions:
				player.summon(random.choice(minions))
