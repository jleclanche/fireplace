"""
Gift Exchange
"""

from ..utils import *


class TB_GiftExchange_Snowball:
	"""Hardpacked Snowballs"""
	play = Bounce(RANDOM_ENEMY_MINION) * 3


class TB_GiftExchange_Treasure:
	"""Winter Veil Gift"""
	deathrattle = Give(CURRENT_PLAYER, "TB_GiftExchange_Treasure_Spell")


class TB_GiftExchange_Treasure_Spell:
	"""Stolen Winter Veil Gift"""
	# Surely none of this even sort of works.
	RandomGift = RandomCollectible(
		# COST >= 5,
		card_class=Attr(Controller(OWNER), GameTag.CLASS)
	)
	play = Discover(RandomGift).then(Buff(Discover.CARDS, "TB_GiftExchange_Enchantment"))


# Cheap Gift
TB_GiftExchange_Enchantment = buff(cost=-5)
