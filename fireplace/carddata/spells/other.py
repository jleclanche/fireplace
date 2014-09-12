from ..card import *


# The Coin
class GAME_005(Card):
	action = buffSelf("GAME_005e")

class GAME_005e(Card):
	mana = 1
	oneTurnEffect = True
