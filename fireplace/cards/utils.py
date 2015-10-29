import random
from hearthstone.enums import CardClass, CardType, GameTag, Race, Rarity
from ..actions import *
from ..aura import Refresh
from ..dsl import *
from ..events import *


# For buffs which are removed when the card is moved to play (eg. cost buffs)
# This needs to be Summon, because of Summon from the hand
REMOVED_IN_PLAY = Summon(PLAYER, OWNER).after(Destroy(SELF))


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


Freeze = lambda target: SetTag(target, {GameTag.FROZEN: True})
Stealth = lambda target: SetTag(target, {GameTag.STEALTH: True})
Unstealth = lambda target: SetTag(target, {GameTag.STEALTH: False})
Taunt = lambda target: SetTag(target, {GameTag.TAUNT: True})


CLEAVE = Hit(TARGET_ADJACENT, Attr(SELF, GameTag.ATK))
COINFLIP = RandomNumber(0, 1) == 1
EMPTY_HAND = Count(CONTROLLER_HAND) == 0
HOLDING_DRAGON = Find(CONTROLLER_HAND + DRAGON)
JOUST = Joust(FRIENDLY + MINION + IN_DECK, ENEMY + MINION + IN_DECK)


def SET(amt):
	return lambda self, i: amt
