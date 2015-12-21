from ..utils import *


##
# Minions

# Kezan Mystic
class GVG_074:
	play = Steal(RANDOM(ENEMY_SECRETS))


# Jeeves
class GVG_094:
	events = EndTurn().on(DrawUntil(EndTurn.PLAYER, 3))


# Goblin Sapper
class GVG_095:
	update = (Count(ENEMY_HAND) >= 6) & Refresh(SELF, {GameTag.ATK: +4})


# Lil' Exorcist
class GVG_097:
	# The Enchantment ID is correct
	play = Buff(SELF, "GVG_101e") * Count(ENEMY_MINIONS + DEATHRATTLE)

GVG_101e = buff(+1, +1)


# Bomb Lobber
class GVG_099:
	play = Hit(RANDOM_ENEMY_MINION, 4)
