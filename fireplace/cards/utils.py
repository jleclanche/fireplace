import random
from hearthstone.enums import CardClass, CardType, GameTag, Race, Rarity
from ..actions import *
from ..aura import Refresh
from ..dsl import *
from ..events import *
from ..utils import custom_card


# For buffs which are removed when the card is moved to play (eg. cost buffs)
# This needs to be Summon, because of Summon from the hand
REMOVED_IN_PLAY = Summon(PLAYER, OWNER).after(Destroy(SELF))

ENEMY_CLASS = Attr(ENEMY_HERO, GameTag.CLASS)


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


class RandomID(RandomCardPicker):
	def pick(self, source):
		self._cards = self.args
		return super().pick(source)


Freeze = lambda target: SetTag(target, (GameTag.FROZEN, ))
Stealth = lambda target: SetTag(target, (GameTag.STEALTH, ))
Unstealth = lambda target: UnsetTag(target, (GameTag.STEALTH, ))
Taunt = lambda target: SetTag(target, (GameTag.TAUNT, ))
GiveCharge = lambda target: SetTag(target, (GameTag.CHARGE, ))
GiveDivineShield = lambda target: SetTag(target, (GameTag.DIVINE_SHIELD, ))
GiveWindfury = lambda target: SetTag(target, (GameTag.WINDFURY, ))


CLEAVE = Hit(TARGET_ADJACENT, ATK(SELF))
COINFLIP = RandomNumber(0, 1) == 1
EMPTY_BOARD = Count(FRIENDLY_MINIONS) == 0
EMPTY_HAND = Count(FRIENDLY_HAND) == 0
FULL_BOARD = Count(FRIENDLY_MINIONS) == 7
FULL_HAND = Count(FRIENDLY_HAND) == 10
HOLDING_DRAGON = Find(FRIENDLY_HAND + DRAGON)
JOUST = Joust(RANDOM(FRIENDLY_DECK + MINION), RANDOM(ENEMY_DECK + MINION))


def SET(amt):
	return lambda self, i: amt


# Buff helper
def buff(atk=0, health=0, **kwargs):
	buff_tags = {}
	if atk:
		buff_tags[GameTag.ATK] = atk
	if health:
		buff_tags[GameTag.HEALTH] = health

	for tag in GameTag:
		if tag.name.lower() in kwargs.copy():
			buff_tags[tag] = kwargs.pop(tag.name.lower())

	if "immune" in kwargs:
		value = kwargs.pop("immune")
		buff_tags[GameTag.CANT_BE_DAMAGED] = value
		buff_tags[GameTag.CANT_BE_TARGETED_BY_OPPONENTS] = value

	if kwargs:
		raise NotImplementedError(kwargs)

	class Buff:
		tags = buff_tags

	return Buff
