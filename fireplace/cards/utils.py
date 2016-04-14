import random
from hearthstone.enums import CardClass, CardType, GameTag, Race, Rarity
from ..actions import *
from ..aura import Refresh
from ..dsl import *
from ..events import *


# For buffs which are removed when the card is moved to play (eg. cost buffs)
# This needs to be Summon, because of Summon from the hand
REMOVED_IN_PLAY = Summon(PLAYER, OWNER).after(Destroy(SELF))

FRIENDLY_CLASS = Attr(FRIENDLY_HERO, GameTag.CLASS)
ENEMY_CLASS = Attr(ENEMY_HERO, GameTag.CLASS)


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
HOLDING_DRAGON = Find(FRIENDLY_HAND + DRAGON - SELF)

DISCOVER = lambda *args: Discover(CONTROLLER, *args)

# Determine which class's cards to use in the card pool when a Discover choice is started
def get_discover_class_source(entities, source):
	if entities.current_player.hero.data.card_class != CardClass.NEUTRAL:
		return [entities.current_player.hero]

	if source.data.card_class != CardClass.NEUTRAL:
		return [source]

	from .. import cards
	return [cards.db[random.choice(cards.filter(collectible=True, type=CardType.HERO))]]

# The class card type to use for the next Discover action (takes non-standard heroes into account)
FRIENDLY_DISCOVER_CLASS = Attr(FuncSelector(get_discover_class_source), GameTag.CLASS)


# 50% chance to attack the wrong enemy.
FORGETFUL = Attack(SELF).on(COINFLIP & Retarget(SELF, RANDOM(ALL_CHARACTERS - Attack.DEFENDER - CONTROLLED_BY(SELF))))

AT_MAX_MANA = lambda s: MANA(s) == 10


class JoustHelper(Evaluator):
	"""
	A helper evaluator class for jousts to allow JOUST & ... syntax.
	"""
	def __init__(self, challenger, defender):
		self.challenger = challenger
		self.defender = defender
		super().__init__()

	def trigger(self, source):
		action = Joust(self.challenger, self.defender).then(
			JoustEvaluator(Joust.CHALLENGER, Joust.DEFENDER) & self._if | self._else
		)

		return action.trigger(source)

JOUST = JoustHelper(
	RANDOM(FRIENDLY_DECK + MINION),
	RANDOM(ENEMY_DECK + MINION)
)


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


def AttackHealthSwapBuff():
	def apply(self, target):
		self._xatk = target.health
		self._xhealth = target.atk
		target.damage = 0

	cls = buff()
	cls.atk = lambda self, i: self._xatk
	cls.max_health = lambda self, i: self._xhealth
	cls.apply = apply

	return cls


def GainEmptyMana(selector, amount):
	"""
	Helper to gain an empty mana crystal (gains mana, then spends it)
	"""
	return GainMana(selector, amount), SpendMana(selector, amount)


def custom_card(cls):
	from . import CardDB, db
	id = cls.__name__
	if GameTag.CARDNAME not in cls.tags:
		raise ValueError("No name provided for custom card %r" % (cls))
	db[id] = CardDB.merge(id, None, cls)
	# Give the card its fake name
	db[id]._localized_tags = {
		GameTag.CARDNAME: {"enUS": cls.tags[GameTag.CARDNAME]},
		GameTag.CARDTEXT_INHAND: {"enUS": ""}
	}
	return cls
