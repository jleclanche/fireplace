import random
from ..actions import *
from ..dsl import *
from ..enums import CardClass, CardType, GameTag, Race, Rarity, Zone
from ..events import *


def hand(func):
	"""
	@hand helper decorator
	The decorated event listener will only listen while in the HAND Zone
	"""
	func.zone = Zone.HAND
	return func


RandomCard = lambda **kw: RandomCardPicker(**kw)
RandomCollectible = lambda **kw: RandomCardPicker(collectible=True, **kw)
RandomMinion = lambda **kw: RandomCollectible(type=CardType.MINION, **kw)
RandomSpell = lambda **kw: RandomCollectible(type=CardType.SPELL, **kw)
RandomTotem = lambda **kw: RandomCardPicker(race=Race.TOTEM)
RandomWeapon = lambda **kw: RandomCollectible(type=CardType.WEAPON, **kw)
RandomSparePart = lambda **kw: RandomCardPicker(spare_part=True, **kw)

class RandomEntourage(RandomCardPicker):
	def pick(self, source):
		self._cards = source.entourage
		return super().pick(source)


HOLDING_DRAGON = Find(CONTROLLER_HAND + DRAGON)
