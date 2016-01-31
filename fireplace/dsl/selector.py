import operator
import random
from enum import IntEnum
from hearthstone.enums import CardType, GameTag, Race, Rarity, Zone
from .. import enums
from ..utils import CardList
from .lazynum import LazyValue


class Selector:
	"""
	A Forth-like program consisting of methods of Selector and members of
	IntEnum classes. The IntEnums must have appropriate test(entity)
	methods returning a boolean, true if entity matches the condition.
	"""
	class MergeFilter:
		"""
		Signals the start of a merge: the following commands define the filter
		to be passed after Merge
		"""
		pass

	class Merge:
		"""
		Ops between Merge and Unmerge are classes with merge(selector, entities)
		methods that operate on the full collection specified by the ops between
		MergeFilter and Merge.
		"""
		pass

	class Unmerge:
		pass

	def __init__(self, tag=None):
		self.program = []
		self.slice = None
		if tag is not None:
			self.program.append(tag)

	def __repr__(self):
		prog = []
		for op in self.program:
			name = ""
			if hasattr(op, "__name__"):
				name = op.__name__
				if name == "_and":
					name = "+"
				elif name == "_not":
					name = "-"
				elif name == "_or":
					name = "|"
			elif isinstance(op, IntEnum):
				name = op.name
			else:
				name = repr(op)
			prog.append(name)
		return "<%s>" % (" ".join(prog))

	def __or__(self, other):
		result = Selector()
		if isinstance(other, LazyValue):
			other = LazySelector(other)
		result.program = self.program + other.program
		result.program.append(Selector._or)
		return result

	def __add__(self, other):
		result = Selector()
		if isinstance(other, LazyValue):
			other = LazySelector(other)
		result.program = self.program + other.program
		result.program.append(Selector._and)
		return result

	def __sub__(self, other):
		result = Selector()
		if isinstance(other, LazyValue):
			other = LazySelector(other)
		result.program = self.program + other.program
		result.program += [Selector._not, Selector._and]
		return result

	def __getitem__(self, val):
		ret = Selector()
		ret.program = self.program
		if isinstance(val, int):
			ret.slice = slice(val)
		else:
			ret.slice = val
		return ret

	def eval(self, entities, source):
		if not entities:
			return []
		self.opc = 0  # outer program counter
		result = []
		while self.opc < len(self.program):
			if self.program[self.opc] != Selector.MergeFilter:
				result += [e for e in entities if self.test(e, source)]
				self.opc = self.pc
				if self.opc >= len(self.program):
					break
			else:
				self.opc += 1
			# handle merge step:
			merge_input = CardList([e for e in entities if self.test(e, source)])
			self.opc = self.pc
			merge_output = CardList()
			while self.opc < len(self.program):
				op = self.program[self.opc]
				self.opc += 1
				if op == Selector.Unmerge:
					break
				merge_output += op.merge(self, merge_input)
			negated = False
			combined = False
			while self.opc < len(self.program):
				# special handling for operators on merged collections:
				op = self.program[self.opc]
				if op == Selector._or:
					result += [e for e in merge_output]
					combined = True
				elif op == Selector._and:
					result = [e for e in result if (e in merge_output) != negated]
					combined = True
				elif op == Selector._not:
					negated = not negated
				else:
					break
				self.opc += 1
			if not combined:
				# assume or
				result += merge_output

		if self.slice:
			result = result[self.slice]

		return result

	def test(self, entity, source):
		stack = []
		self.pc = self.opc  # program counter
		while self.pc < len(self.program):
			op = self.program[self.pc]
			self.pc += 1
			if op == Selector.Merge or op == Selector.MergeFilter:
				break
			if callable(op):
				op(self, stack)
			else:
				val = type(op).test(op, entity, source)
				stack.append(val)
		return stack[-1]

	# boolean ops:
	def _and(self, stack):
		a = stack.pop()
		b = stack.pop()
		stack.append(a and b)

	def _or(self, stack):
		a = stack.pop()
		b = stack.pop()
		stack.append(a or b)

	def _not(self, stack):
		stack.append(not stack.pop())


class AttrSelector(Selector):
	"""
	Selects entities with tags matching a comparison.
	"""
	class IsAttrValue:
		def __init__(self, tag, op, value):
			self.tag = tag
			self.op = op
			self.value = value

		def __repr__(self):
			return "Attr(%s(%r, %r))" % (self.op.__name__, self.tag, self.value)

		def test(self, entity, source):
			value = self.value
			if isinstance(value, LazyValue):
				# Support AttrSelector(SELF, GameTag.CONTROLLER) == Controller(...)
				value = self.value.evaluate(source)
			return self.op(entity.tags.get(self.tag, 0), value)

	def __init__(self, tag):
		super().__init__()
		self.tag = tag
		self.program = []

	def __call__(self, selector):
		from .lazynum import Attr

		return Attr(selector, self.tag)

	def _cmp(op):
		def func(self, other):
			sel = self.__class__(self.tag)
			sel.program = [self.IsAttrValue(self.tag, getattr(operator, op), other)]
			return sel
		return func

	__eq__ = _cmp("eq")
	__ge__ = _cmp("ge")
	__gt__ = _cmp("gt")
	__le__ = _cmp("le")
	__lt__ = _cmp("lt")

ARMOR = AttrSelector(GameTag.ARMOR)
ATK = AttrSelector(GameTag.ATK)
CONTROLLER = AttrSelector(GameTag.CONTROLLER)
CURRENT_HEALTH = AttrSelector("health")
COST = AttrSelector(GameTag.COST)
DAMAGE = AttrSelector(GameTag.DAMAGE)
MANA = AttrSelector(GameTag.RESOURCES)
USED_MANA = AttrSelector(GameTag.RESOURCES_USED)


class SelfSelector(Selector):
	"""
	Selects the source.
	"""
	class IsSelf:
		def __repr__(self):
			return "SELF"

		def test(self, entity, source):
			return entity is source

	def __init__(self):
		self.program = [self.IsSelf()]

	def __repr__(self):
		return "<SELF>"

	def eval(self, entities, source):
		return [source]

SELF = SelfSelector()


class OwnerSelector(Selector):
	"""
	Selects the source's owner.
	"""
	class IsOwner:
		def test(self, entity, source):
			return entity is source.owner

	def __init__(self):
		self.program = [self.IsOwner()]

	def __repr__(self):
		return "<OWNER>"

	def eval(self, entities, source):
		if source.owner:
			return [source.owner]
		return []

OWNER = OwnerSelector()


class FuncSelector(Selector):
	"""
	Selects cards after applying a filter function to them
	"""
	class MatchesFunc:
		def __init__(self, func):
			self.func = func

		def test(self, entity, source):
			return self.func(entity, source)

	def __init__(self, func):
		self.program = [self.MatchesFunc(func)]
		self.slice = None


def ID(id):
	return FuncSelector(lambda entity, source: getattr(entity, "id", None) == id)


def LazySelector(value):
	"""
	Returns a selector that evaluates the value at selection time
	Useful for eg. `ALL_CHARACTERS - Attack.TARGET`
	"""
	return FuncSelector(lambda entity, source: entity is value.evaluate(source))


TARGET = FuncSelector(lambda entity, source: entity is source.target)
TARGET.eval = lambda entity, source: [source.target]


class MinMaxSelector(Selector):
	"""
	Selects the entities in \a selector whose \a tag match \a func comparison
	"""
	class SelectFunc:
		def __init__(self, tag, func):
			self.tag = tag
			self.func = func

		def __repr__(self):
			return "<%s(%s)>" % (self.func.__name__, self.tag)

		def merge(self, selector, entities):
			key = lambda x: x.tags.get(self.tag, 0)
			highest = self.func(entities, key=key).tags.get(self.tag, 0)
			ret = [e for e in entities if e.tags.get(self.tag) == highest]
			return random.sample(ret, min(len(ret), 1))

	def __init__(self, selector, tag, func):
		self.slice = None
		self.select = self.SelectFunc(tag, func)
		self.selector = selector
		self.program = [Selector.MergeFilter]
		self.program.extend(selector.program)
		self.program.append(Selector.Merge)
		self.program.append(self.select)
		self.program.append(Selector.Unmerge)

	def __repr__(self):
		return "%s(%r)" % (self.__class__.__name__, self.selector)


HIGHEST_ATK = lambda sel: MinMaxSelector(sel, GameTag.ATK, max)
LOWEST_ATK = lambda sel: MinMaxSelector(sel, GameTag.ATK, min)


class LeftOfSelector(Selector):
	"""
	Selects the entities to the left of the targets.
	"""
	class SelectAdjacent:
		def merge(self, selector, entities):
			result = []
			for e in entities:
				if e.zone == Zone.PLAY:
					left = e.controller.field[:e.zone_position]
					if left:
						result.append(left[-1])
			return result

	def __init__(self, selector):
		self.slice = None
		self.program = [Selector.MergeFilter]
		self.program.extend(selector.program)
		self.program.append(Selector.Merge)
		self.program.append(self.SelectAdjacent())
		self.program.append(Selector.Unmerge)

	def __repr__(self):
		return "<LEFT OF>"

LEFT_OF = LeftOfSelector


class RightOfSelector(Selector):
	"""
	Selects the entities to the right of the targets.
	"""
	class SelectAdjacent:
		def merge(self, selector, entities):
			result = []
			for e in entities:
				if e.zone == Zone.PLAY:
					right = e.controller.field[e.zone_position + 1:]
					if right:
						result.append(right[0])
			return result

	def __init__(self, selector):
		self.slice = None
		self.program = [Selector.MergeFilter]
		self.program.extend(selector.program)
		self.program.append(Selector.Merge)
		self.program.append(self.SelectAdjacent())
		self.program.append(Selector.Unmerge)

	def __repr__(self):
		return "<RIGHT OF>"

RIGHT_OF = RightOfSelector

ADJACENT = lambda s: LEFT_OF(s) | RIGHT_OF(s)
SELF_ADJACENT = ADJACENT(SELF)
TARGET_ADJACENT = ADJACENT(TARGET)


class RandomSelector(Selector):
	"""
	Selects a 1-member random sample of the targets.
	This selector can be multiplied to select more than 1 target.
	"""
	class SelectRandom:
		def __init__(self, times):
			self.times = times

		def __repr__(self):
			return "<RANDOM(%s)>" % (self.times)

		def merge(self, selector, entities):
			return random.sample(entities, min(len(entities), self.times))

	def __init__(self, selector):
		self.slice = None
		self.random = self.SelectRandom(1)
		self.selector = selector
		self.program = [Selector.MergeFilter]
		self.program.extend(selector.program)
		self.program.append(Selector.Merge)
		self.program.append(self.random)
		self.program.append(Selector.Unmerge)

	def __repr__(self):
		return "RANDOM(%r)" % (self.selector)

	def __mul__(self, other):
		result = RandomSelector(self.selector)
		result.random.times = self.random.times * other
		return result

RANDOM = RandomSelector


class Controller(LazyValue):
	def __init__(self, selector=None):
		self.selector = selector

	def __repr__(self):
		return "%s(%s)" % (self.__class__.__name__, self.selector or "<SELF>")

	def _get_entity_attr(self, entity):
		return entity.controller

	def evaluate(self, source):
		if self.selector is None:
			# If we don't have an argument, we default to SELF
			# This allows us to skip selector evaluation altogether.
			return self._get_entity_attr(source)
		if isinstance(self.selector, LazyValue):
			entities = [self.selector.evaluate(source)]
		else:
			entities = self.selector.eval(source.game, source)
		assert len(entities) == 1
		return self._get_entity_attr(entities[0])


class Opponent(Controller):
	def _get_entity_attr(self, entity):
		return entity.controller.opponent

FRIENDLY = CONTROLLER == Controller()
ENEMY = CONTROLLER == Opponent()

def CONTROLLED_BY(selector):
	return AttrSelector(GameTag.CONTROLLER) == Controller(selector)

CONTROLLED_BY_OWNER_OPPONENT = CONTROLLER == Opponent(OWNER)


# Enum tests
GameTag.test = lambda self, entity, *args: entity is not None and bool(entity.tags.get(self))
CardType.test = lambda self, entity, *args: entity is not None and self == entity.type
Race.test = lambda self, entity, *args: entity is not None and self == getattr(entity, "race", Race.INVALID)
Rarity.test = lambda self, entity, *args: entity is not None and self == getattr(entity, "rarity", Rarity.INVALID)
Zone.test = lambda self, entity, *args: entity is not None and self == entity.zone


BATTLECRY = Selector(GameTag.BATTLECRY)
CHARGE = Selector(GameTag.CHARGE)
DAMAGED = Selector(GameTag.DAMAGE)
DEATHRATTLE = Selector(GameTag.DEATHRATTLE)
DIVINE_SHIELD = Selector(GameTag.DIVINE_SHIELD)
FROZEN = Selector(GameTag.FROZEN)
OVERLOAD = Selector(GameTag.OVERLOAD)
SPELLPOWER = Selector(GameTag.SPELLPOWER)
STEALTH = Selector(GameTag.STEALTH)
TAUNT = Selector(GameTag.TAUNT)
WINDFURY = Selector(GameTag.WINDFURY)
CLASS_CARD = Selector(GameTag.CLASS)

ALWAYS_WINS_BRAWLS = AttrSelector(enums.ALWAYS_WINS_BRAWLS) == True
KILLED_THIS_TURN = AttrSelector(enums.KILLED_THIS_TURN) == True


IN_PLAY = Selector(Zone.PLAY)
IN_DECK = Selector(Zone.DECK)
IN_HAND = Selector(Zone.HAND)
HIDDEN = Selector(Zone.SECRET)
KILLED = Selector(Zone.GRAVEYARD)

GAME = Selector(CardType.GAME)
PLAYER = Selector(CardType.PLAYER)
HERO = Selector(CardType.HERO)
MINION = Selector(CardType.MINION)
CHARACTER = MINION | HERO
WEAPON = Selector(CardType.WEAPON)
SPELL = Selector(CardType.SPELL)
SECRET = Selector(GameTag.SECRET)
HERO_POWER = Selector(CardType.HERO_POWER)

BEAST = Selector(Race.BEAST)
DEMON = Selector(Race.DEMON)
DRAGON = Selector(Race.DRAGON)
MECH = Selector(Race.MECHANICAL)
MURLOC = Selector(Race.MURLOC)
PIRATE = Selector(Race.PIRATE)
TOTEM = Selector(Race.TOTEM)

COMMON = Selector(Rarity.COMMON)
RARE = Selector(Rarity.RARE)
EPIC = Selector(Rarity.EPIC)
LEGENDARY = Selector(Rarity.LEGENDARY)

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
CURRENT_PLAYER = ALL_PLAYERS + Selector(GameTag.CURRENT_PLAYER)

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
RANDOM_ENEMY_MINION = RANDOM(ENEMY_MINIONS)
RANDOM_ENEMY_CHARACTER = RANDOM(ENEMY_CHARACTERS)

DAMAGED_CHARACTERS = ALL_CHARACTERS + DAMAGED
