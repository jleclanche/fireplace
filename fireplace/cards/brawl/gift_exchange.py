"""
Gift Exchange
"""

from ..utils import *


# Hardpacked Snowballs
class TB_GiftExchange_Snowball:
	play = Bounce(RANDOM_ENEMY_MINION) * 3


# Winter's Veil Gift
class TB_GiftExchange_Treasure:
	deathrattle = Give(CURRENT_PLAYER, "TB_GiftExchange_Treasure_Spell")


# Stolen Winter's Veil Gift
class TB_GiftExchange_Treasure_Spell:
	# Surely none of this even sort of works.
	RandomGift = RandomCollectible(
		COST >= 5,
		CLASS_CARD=Attr(Controller(OWNER), GameTag.CLASS)
	)
	play = Discover(RandomGift).then(Buff(Discover.CARDS, "TB_GiftExchange_Enchantment"))


# Cheap Gift
TB_GiftExchange_Enchantment = buff(cost=-5)
