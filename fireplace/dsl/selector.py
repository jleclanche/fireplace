import operator
import random
from abc import ABCMeta, abstractmethod
from enum import IntEnum
from hearthstone.enums import CardType, GameTag, Race, Rarity, Zone, CardClass
from typing import Any, Union, List, Callable, Iterable, Optional, Set
from .. import enums
from ..entity import BaseEntity
from .lazynum import Attr, LazyValue, OpAttr


# Type aliases
SelectorLike = Union["Selector", LazyValue]
BinaryOp = Callable[[Any, Any], bool]


class Selector:
	"""
	Selectors take entity lists and returns a sub-list. Selectors
	are closed under addition, subtraction, complementation, and ORing.

	Note that addition means set intersection and OR means set union. For
	convenience, LazyValues can also treated as selectors.

	Set operations preserve ordering (necessary for cards like Echo of
	Medivh, where ordering matters)
	"""
	def eval(self, entities: List[BaseEntity], source: BaseEntity) -> List[BaseEntity]:
		return entities

	def __add__(self, other: SelectorLike) -> "Selector":
		return SetOpSelector(operator.and_, self, other)

	def __or__(self, other: SelectorLike) -> "Selector":
		return SetOpSelector(operator.or_, self, other)

	def __neg__(self) -> "Selector":
		# Note that here we define negation in terms of subtraction, and
		# not the other way around, because selectors are implemented using
		# concrete set operations instead of boolean manipulation
		return self.__class__() - self

	def __sub__(self, other: SelectorLike) -> "Selector":
		return SetOpSelector(operator.sub, self, other)

	def __rsub__(self, other: SelectorLike) -> "Selector":
		if isinstance(other, LazyValue):
			other = LazyValueSelector(other)
		return other - self

	def __radd__(self, other: SelectorLike) -> "Selector":
		return self + other

	def __ror__(self, other: SelectorLike) -> "Selector":
		return self | other

	def __getitem__(self, val: Union[int, slice]) -> "Selector":
		if isinstance(val, int):
			val = slice(val)
		return SliceSelector(self, val)


class EnumSelector(Selector):
	def __init__(self, tag_enum=None):
		self.tag_enum = tag_enum

	def eval(self, entities, source):
		if not self.tag_enum or not hasattr(self.tag_enum, "test"):
			raise RuntimeError("Unsupported enum type {}".format(str(self.tag_enum)))
		return [e for e in entities if self.tag_enum.test(e, source)]

	def __repr__(self):
		return "<%s>" % (self.tag_enum.name)


class SelectorEntityValue(metaclass=ABCMeta):
	"""
	SelectorEntityValues can be compared to arbitrary objects LazyValues;
	the comparison's boolean result forms a selector on entities.
	"""
	@abstractmethod
	def value(self, entity, source):
		pass

	def __eq__(self, other) -> Selector:
		return ComparisonSelector(operator.eq, self, other)

	def __gt__(self, other) -> Selector:
		return ComparisonSelector(operator.gt, self, other)

	def __lt__(self, other) -> Selector:
		return ComparisonSelector(operator.lt, self, other)

	def __ge__(self, other) -> Selector:
		return ComparisonSelector(operator.ge, self, other)

	def __le__(self, other) -> Selector:
		return ComparisonSelector(operator.le, self, other)

	def __ne__(self, other) -> Selector:
		return ComparisonSelector(operator.ne, self, other)


class AttrValue(SelectorEntityValue):
	"""Extracts attribute values from an entity to allow for boolean comparisons."""
	def __init__(self, tag):
		self.tag = tag

	def value(self, entity, source):
		if isinstance(self.tag, str):
			return getattr(entity, self.tag, 0)
		return entity.tags.get(self.tag, 0)

	def __call__(self, selector):
		"""Convenience function to support uses like ARMOR(SELF)"""
		return Attr(selector, self.tag)

	def __repr__(self):
		return "<%s>" % (getattr(self.tag, "name", int(self.tag)))


ARMOR = AttrValue(GameTag.ARMOR)
ATK = AttrValue(GameTag.ATK)
CONTROLLER = AttrValue(GameTag.CONTROLLER)
CURRENT_HEALTH = AttrValue("health")
COST = AttrValue(GameTag.COST)
COST_ADD = AttrValue("cost_add")
COST_DEC = AttrValue("cost_dec")
DAMAGE = AttrValue(GameTag.DAMAGE)
MANA = AttrValue(GameTag.RESOURCES)
USED_MANA = AttrValue(GameTag.RESOURCES_USED)
NUM_ATTACKS_THIS_TURN = AttrValue(GameTag.NUM_ATTACKS_THIS_TURN)


class ComparisonSelector(Selector):
	"""A ComparisonSelector compares values of entities to
	other values. Lazy values are evaluated at selector runtime."""
	def __init__(self, op: BinaryOp, left: SelectorEntityValue, right):
		self.op = op
		self.left = left
		self.right = right

	def eval(self, entities, source):
		right_value = (self.right.evaluate(source)
					   if isinstance(self.right, LazyValue)
					   else self.right)
		return [e for e in entities if
				self.op(self.left.value(e, source), right_value)]

	def __repr__(self):
		if self.op.__name__ == "eq":
			infix = "=="
		elif self.op.__name__ == "gt":
			infix = ">"
		elif self.op.__name__ == "lt":
			infix = "<"
		elif self.op.__name__ == "ge":
			infix = ">="
		elif self.op.__name__ == "le":
			infix = "<="
		elif self.op.__name__ == "ne":
			infix = "!="
		else:
			infix = "UNKNOWN_OP"
		return "<%r %s %r>" % (self.left, infix, self.right)


class FilterSelector(Selector):
	def __init__(self, func: Callable[[BaseEntity, BaseEntity], bool]):
		"""
		func(entity, source) returns true iff the entity
		should be selected
		"""
		self.func = func

	def eval(self, entities, source):
		return [e for e in entities if self.func(e, source)]


class FuncSelector(Selector):
	def __init__(self, func: Callable[[List[BaseEntity], BaseEntity], List[BaseEntity]]):
		"""func(entities, source) returns the results"""
		self.func = func

	def eval(self, entities, source):
		return self.func(entities, source)


class SliceSelector(Selector):
	"""Applies a slice to child selector at evaluation time."""
	def __init__(self, child: SelectorLike, slice_val: slice):
		if isinstance(child, LazyValue):
			child = LazyValueSelector(child)
		self.child = child
		self.slice = slice_val

	def eval(self, entities, source):
		return list(self.child.eval(entities, source)[self.slice])

	def __repr__(self):
		return "%r[%r]" % (self.child, self.slice)


class SetOpSelector(Selector):
	def __init__(self, op: Callable, left: Selector, right: SelectorLike):
		if isinstance(right, LazyValue):
			right = LazyValueSelector(right)
		self.op = op
		self.left = left
		self.right = right

	@staticmethod
	def _entity_id_set(entities: Iterable[BaseEntity]) -> Set[BaseEntity]:
		return set(e.entity_id for e in entities if e)

	def eval(self, entities, source):
		left_children = self.left.eval(entities, source)
		right_children = self.right.eval(entities, source)
		result_entity_ids = self.op(self._entity_id_set(left_children),
									self._entity_id_set(right_children))
		# Preserve input ordering and multiplicity
		return [e for e in entities if e.entity_id in result_entity_ids]

	def __repr__(self):
		name = self.op.__name__
		if name == "and_":
			infix = "+"
		elif name == "or_":
			infix = "|"
		elif name == "sub":
			infix = "-"
		else:
			infix = "UNKNOWN_OP"

		return "<%r %s %r>" % (self.left, infix, self.right)


SELF = FuncSelector(lambda _, source: [source])
OWNER = FuncSelector(lambda entities, source: [source.owner] if hasattr(source, "owner") else [])


def LazyValueSelector(value):
	return FuncSelector(lambda entities, source: [value.evaluate(source)])


def ID(id):
	return FilterSelector(lambda entity, source: getattr(entity, "id", None) == id)

TARGET = FuncSelector(lambda entities, source: [source.target])


class BoardPositionSelector(Selector):
	class Direction(IntEnum):
		LEFT = 1
		RIGHT = 2

	def __init__(self, direction: Direction, child: SelectorLike):
		if isinstance(child, LazyValue):
			child = LazyValueSelector(child)
		self.child = child
		self.direction = direction

	def eval(self, entities, source):
		result = []
		for e in self.child.eval(entities, source):
			if getattr(e, "zone", None) == Zone.PLAY:
				field = e.controller.field
				position = e.zone_position - 1
				if self.direction == self.Direction.RIGHT:
					# Swap the list, reverse the position
					field = list(reversed(field))
					position = -(position + 1)

				left = field[:position]
				if left:
					result.append(left[-1])

		return result


LEFT_OF = lambda s: BoardPositionSelector(BoardPositionSelector.Direction.LEFT, s)
RIGHT_OF = lambda s: BoardPositionSelector(BoardPositionSelector.Direction.RIGHT, s)
ADJACENT = lambda s: LEFT_OF(s) | RIGHT_OF(s)
SELF_ADJACENT = ADJACENT(SELF)
TARGET_ADJACENT = ADJACENT(TARGET)


class RandomSelector(Selector):
	"""
	Selects a 1-member random sample of the targets.
	This selector can be multiplied to select more than 1 target.
	"""
	def __init__(self, child: SelectorLike, times=1):
		if isinstance(child, LazyValue):
			child = LazyValueSelector(child)
		self.child = child
		self.times = times

	def eval(self, entities, source):
		child_entities = self.child.eval(entities, source)
		return random.sample(child_entities, min(len(child_entities), self.times))

	def __mul__(self, other):
		return RandomSelector(self.child, self.times * other)


class SelectorOne(Selector):
	"""
	Selects a 1-member of the targets.
	This selector can be multiplied to select more than 1 target.
	"""
	def __init__(self, child: SelectorLike, times=1):
		if isinstance(child, LazyValue):
			child = LazyValueSelector(child)
		self.child = child
		self.times = times

	def eval(self, entities, source):
		child_entities = self.child.eval(entities, source)
		if len(child_entities) == 0:
			return []
		return [child_entities[0]]

	def __mul__(self, other):
		return SelectorOne(self.child, self.times * other)


RANDOM = RandomSelector

MORTALLY_WOUNDED = CURRENT_HEALTH <= 0

# Selects the highest and lowest attack entities, respectively
HIGHEST_ATK = lambda sel: RANDOM(sel + (AttrValue(GameTag.ATK) == OpAttr(sel, GameTag.ATK, max)))
LOWEST_ATK = lambda sel: RANDOM(sel + (AttrValue(GameTag.ATK) == OpAttr(sel, GameTag.ATK, min)))


class Controller(LazyValue):
	def __init__(self, child: Optional[SelectorLike]=None):
		if isinstance(child, LazyValue):
			child = LazyValueSelector(child)
		self.child = child

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, self.child or "<SELF>")

	def _get_entity_attr(self, entity):
		return entity.controller

	def evaluate(self, source):
		if self.child is None:
			# If we don't have an argument, we default to SELF
			# This allows us to skip selector evaluation altogether.
			return self._get_entity_attr(source)
		else:
			entities = self.child.eval(source.game, source)
		assert len(entities) == 1
		return self._get_entity_attr(entities[0])


class Opponent(Controller):
	def _get_entity_attr(self, entity):
		return entity.controller.opponent

FRIENDLY = CONTROLLER == Controller()
ENEMY = CONTROLLER == Opponent()


def CONTROLLED_BY(selector):
	return AttrValue(GameTag.CONTROLLER) == Controller(selector)

CONTROLLED_BY_OWNER_OPPONENT = CONTROLLER == Opponent(OWNER)


# Enum tests
GameTag.test = lambda self, entity, *args: entity is not None and bool(entity.tags.get(self))
CardType.test = lambda self, entity, *args: entity is not None and self == entity.type
Race.test = lambda self, entity, *args: entity is not None and self == getattr(entity, "race", Race.INVALID)
Rarity.test = lambda self, entity, *args: entity is not None and self == getattr(entity, "rarity", Rarity.INVALID)
Zone.test = lambda self, entity, *args: entity is not None and self == entity.zone
CardClass.test = lambda self, entity, *args: entity is not None and self == getattr(entity, "card_class", CardClass.INVALID)

BATTLECRY = EnumSelector(GameTag.BATTLECRY)
CHARGE = EnumSelector(GameTag.CHARGE)
DAMAGED = EnumSelector(GameTag.DAMAGE)
DEATHRATTLE = EnumSelector(GameTag.DEATHRATTLE)
DIVINE_SHIELD = EnumSelector(GameTag.DIVINE_SHIELD)
FROZEN = EnumSelector(GameTag.FROZEN)
OVERLOAD = EnumSelector(GameTag.OVERLOAD)
SPELLPOWER = EnumSelector(GameTag.SPELLPOWER)
STEALTH = EnumSelector(GameTag.STEALTH)
TAUNT = EnumSelector(GameTag.TAUNT)
WINDFURY = EnumSelector(GameTag.WINDFURY)
CLASS_CARD = EnumSelector(GameTag.CLASS)

ALWAYS_WINS_BRAWLS = AttrValue(enums.ALWAYS_WINS_BRAWLS) == True
KILLED_THIS_TURN = AttrValue(enums.KILLED_THIS_TURN) == True

ROGUE = EnumSelector(CardClass.ROGUE)

IN_PLAY = EnumSelector(Zone.PLAY)
IN_DECK = EnumSelector(Zone.DECK)
IN_HAND = EnumSelector(Zone.HAND)
HIDDEN = EnumSelector(Zone.SECRET)
DISCARDED = AttrValue(enums.DISCARDED) == True
KILLED = EnumSelector(Zone.GRAVEYARD) - DISCARDED

GAME = EnumSelector(CardType.GAME)
PLAYER = EnumSelector(CardType.PLAYER)
HERO = EnumSelector(CardType.HERO)
MINION = EnumSelector(CardType.MINION)
CHARACTER = MINION | HERO
WEAPON = EnumSelector(CardType.WEAPON)
SPELL = EnumSelector(CardType.SPELL)
SECRET = EnumSelector(GameTag.SECRET)
HERO_POWER = EnumSelector(CardType.HERO_POWER)

BEAST = EnumSelector(Race.BEAST)
DEMON = EnumSelector(Race.DEMON)
DRAGON = EnumSelector(Race.DRAGON)
MECH = EnumSelector(Race.MECHANICAL)
MURLOC = EnumSelector(Race.MURLOC)
PIRATE = EnumSelector(Race.PIRATE)
TOTEM = EnumSelector(Race.TOTEM)
ELEMENTAL = EnumSelector(Race.ELEMENTAL)

COMMON = EnumSelector(Rarity.COMMON)
RARE = EnumSelector(Rarity.RARE)
EPIC = EnumSelector(Rarity.EPIC)
LEGENDARY = EnumSelector(Rarity.LEGENDARY)

ALL_PLAYERS = IN_PLAY + PLAYER
ALL_HEROES = IN_PLAY + HERO
ALL_MINIONS = IN_PLAY + MINION
ALL_CHARACTERS = IN_PLAY + CHARACTER
ALL_WEAPONS = IN_PLAY + WEAPON
ALL_SECRETS = HIDDEN + SECRET
ALL_HERO_POWERS = IN_PLAY + HERO_POWER

OWNER_CONTROLLER = ALL_PLAYERS + CONTROLLED_BY(OWNER)
OWNER_OPPONENT = ALL_PLAYERS + CONTROLLED_BY_OWNER_OPPONENT
TARGET_PLAYER = ALL_PLAYERS + CONTROLLED_BY(TARGET)
CONTROLLER = ALL_PLAYERS + FRIENDLY
OPPONENT = ALL_PLAYERS + ENEMY
CURRENT_PLAYER = ALL_PLAYERS + EnumSelector(GameTag.CURRENT_PLAYER)

FRIENDLY_HAND = IN_HAND + FRIENDLY
FRIENDLY_DECK = IN_DECK + FRIENDLY
FRIENDLY_HERO = IN_PLAY + FRIENDLY + HERO
FRIENDLY_MINIONS = IN_PLAY + FRIENDLY + MINION
FRIENDLY_CHARACTERS = IN_PLAY + FRIENDLY + CHARACTER
FRIENDLY_WEAPON = IN_PLAY + FRIENDLY + WEAPON
FRIENDLY_SECRETS = HIDDEN + FRIENDLY + SECRET
FRIENDLY_HERO_POWER = IN_PLAY + FRIENDLY + HERO_POWER

ENEMY_HAND = IN_HAND + ENEMY
ENEMY_DECK = IN_DECK + ENEMY
ENEMY_HERO = IN_PLAY + ENEMY + HERO
ENEMY_MINIONS = IN_PLAY + ENEMY + MINION
ENEMY_CHARACTERS = IN_PLAY + ENEMY + CHARACTER
ENEMY_WEAPON = IN_PLAY + ENEMY + WEAPON
ENEMY_SECRETS = HIDDEN + ENEMY + SECRET
ENEMY_HERO_POWER = IN_PLAY + ENEMY + HERO_POWER

RANDOM_MINION = RANDOM(ALL_MINIONS)
RANDOM_CHARACTER = RANDOM(ALL_CHARACTERS)
RANDOM_OTHER_CHARACTER = RANDOM(ALL_CHARACTERS - SELF)
RANDOM_FRIENDLY_MINION = RANDOM(FRIENDLY_MINIONS)
RANDOM_OTHER_FRIENDLY_MINION = RANDOM(FRIENDLY_MINIONS - SELF)
RANDOM_FRIENDLY_CHARACTER = RANDOM(FRIENDLY_CHARACTERS)
RANDOM_ENEMY_MINION = RANDOM(ENEMY_MINIONS - MORTALLY_WOUNDED)
RANDOM_ENEMY_CHARACTER = RANDOM(ENEMY_CHARACTERS - MORTALLY_WOUNDED)

DAMAGED_CHARACTERS = ALL_CHARACTERS + DAMAGED

CTHUN = FRIENDLY + ID("OG_280")
