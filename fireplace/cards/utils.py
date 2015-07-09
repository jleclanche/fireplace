import random
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


RandomCard = lambda **kw: RandomCardGenerator(**kw)
RandomCollectible = lambda **kw: RandomCardGenerator(collectible=True, **kw)
RandomMinion = lambda **kw: RandomCollectible(type=CardType.MINION, **kw)
RandomSpell = lambda **kw: RandomCollectible(type=CardType.SPELL, **kw)
RandomWeapon = lambda **kw: RandomCollectible(type=CardType.WEAPON, **kw)
RandomSparePart = lambda **kw: RandomCardGenerator(spare_part=True, **kw)
