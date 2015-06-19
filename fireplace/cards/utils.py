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


def RandomCard(**kwargs):
	return random.choice(fireplace.cards.filter(**kwargs))


def randomCollectible(**kwargs):
	return RandomCard(collectible=True, **kwargs)


def SummonRandomLegendary(*args):
	legendary = randomCollectible(type=CardType.MINION, rarity=Rarity.LEGENDARY)
	return [Summon(CONTROLLER, legendary)]
