import random
import fireplace.cards
from ..actions import *
from ..enums import CardClass, CardType, GameTag, Race, Rarity, Zone
from ..events import *
from ..targeting import *


def hand(func):
	"""
	@hand helper decorator
	The decorated event listener will only listen while in the HAND Zone
	"""
	func.zone = Zone.HAND
	return func

drawCard = lambda self, *args: self.controller.draw()


RandomCollectible = lambda **kw: RandomCardGenerator(collectible=True, **kw)
RandomMinion = lambda **kw: RandomCollectible(type=CardType.MINION, **kw)


def RandomCard(**kwargs):
	return random.choice(fireplace.cards.filter(**kwargs))


def randomCollectible(**kwargs):
	return RandomCard(collectible=True, **kwargs)
