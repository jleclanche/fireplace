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
		cost=range(5, 100),
		card_class=Attr(Controller(OWNER), GameTag.CLASS)
	)
	play = DISCOVER(RandomGift).then(Buff(Discover.CARDS, "TB_GiftExchange_Enchantment"))


# Cheap Gift
class TB_GiftExchange_Enchantment:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -5}
