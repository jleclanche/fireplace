import random
from ..actions import *
from ..aura import Refresh
from ..dsl import *
from ..enums import CardClass, CardType, GameTag, Race, Rarity
from ..events import *


RandomCard = lambda **kw: RandomCardPicker(**kw)
RandomCollectible = lambda **kw: RandomCardPicker(collectible=True, **kw)
RandomMinion = lambda **kw: RandomCollectible(type=CardType.MINION, **kw)
RandomBeast = lambda **kw: RandomMinion(race=Race.BEAST)
RandomMurloc = lambda **kw: RandomMinion(race=Race.MURLOC)
RandomSpell = lambda **kw: RandomCollectible(type=CardType.SPELL, **kw)
RandomTotem = lambda **kw: RandomCardPicker(race=Race.TOTEM)
RandomWeapon = lambda **kw: RandomCollectible(type=CardType.WEAPON, **kw)
RandomSparePart = lambda **kw: RandomCardPicker(spare_part=True, **kw)

class RandomEntourage(RandomCardPicker):
	def pick(self, source):
		self._cards = source.entourage
		return super().pick(source)


HOLDING_DRAGON = Find(CONTROLLER_HAND + DRAGON)
JOUST = Joust(FRIENDLY + MINION + IN_DECK, ENEMY + MINION + IN_DECK)
