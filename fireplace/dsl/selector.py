import operator
import random
from abc import ABCMeta, abstractmethod
from enum import IntEnum
from typing import Any, Callable, Iterable, List, Optional, Set, Union

from hearthstone.enums import CardClass, CardType, GameTag, Race, Rarity, Zone

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
        return Selector() - self

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
MAX_HEALTH = AttrValue(GameTag.HEALTH)
CURRENT_HEALTH = AttrValue("health")
CURRENT_DURABILITY = AttrValue("durability")
MIN_HEALTH = AttrValue(GameTag.HEALTH_MINIMUM)
COST = AttrValue(GameTag.COST)
DAMAGE = AttrValue(GameTag.DAMAGE)
MANA = AttrValue(GameTag.RESOURCES)
MAX_MANA = AttrValue(GameTag.MAXRESOURCES)
USED_MANA = AttrValue(GameTag.RESOURCES_USED)
OVERLOAD_LOCKED = AttrValue(GameTag.OVERLOAD_LOCKED)
OVERLOAD_OWED = AttrValue(GameTag.OVERLOAD_OWED)
CURRENT_MANA = AttrValue("mana")
NUM_ATTACKS_THIS_TURN = AttrValue(GameTag.NUM_ATTACKS_THIS_TURN)
DAMAGED_THIS_TURN = AttrValue(enums.DAMAGED_THIS_TURN)
NUM_ATTACKS = AttrValue("num_attacks")
MAX_HAND_SIZE = AttrValue("max_hand_size")


class ComparisonSelector(Selector):
    """A ComparisonSelector compares values of entities to
    other values. Lazy values are evaluated at selector runtime."""

    def __init__(self, op: BinaryOp, left: SelectorEntityValue, right):
        self.op = op
        self.left = left
        self.right = right

    def eval(self, entities, source):
        right_value = (
            self.right.evaluate(source)
            if isinstance(self.right, LazyValue)
            else self.right
        )
        return [
            e
            for e in entities
            if self.op(
                self.left.value(e, source),
                (
                    right_value.value(e, source)
                    if isinstance(right_value, SelectorEntityValue)
                    else right_value
                ),
            )
        ]

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
    def __init__(
        self, func: Callable[[List[BaseEntity], BaseEntity], List[BaseEntity]]
    ):
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
        return set(e.entity_id for e in entities if hasattr(e, "entity_id"))

    def eval(self, entities, source):
        left_children = self.left.eval(entities, source)
        right_children = self.right.eval(entities, source)
        result_entity_ids = self.op(
            self._entity_id_set(left_children), self._entity_id_set(right_children)
        )
        # Preserve input ordering and multiplicity
        return [
            e
            for e in entities
            if hasattr(e, "entity_id") and e.entity_id in result_entity_ids
        ]

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


class DeDuplicate(Selector):
    def __init__(self, child: SelectorLike):
        if isinstance(child, LazyValue):
            child = LazyValueSelector(child)
        self.child = child

    def eval(self, entities, source):
        entities = self.child.eval(entities, source)
        ret = []
        for entity in entities:
            if entity.id not in ret:
                ret.append(entity)
        return ret

    def __repr__(self):
        return "%s(%r)" % (self.__class__.__name__, self.child)


SELF = FuncSelector(lambda _, source: [source])
OWNER = FuncSelector(
    lambda entities, source: [source.owner] if hasattr(source, "owner") else []
)


def LazyValueSelector(value):
    return FuncSelector(
        lambda entities, source: (
            [value.evaluate(source)] if value.evaluate(source) else []
        )
    )


def ID(id):
    return FilterSelector(lambda entity, source: getattr(entity, "id", None) == id)


def IDS(ids):
    return FilterSelector(lambda entity, source: getattr(entity, "id", None) in ids)


TARGET = FuncSelector(lambda entities, source: [source.target])
ATTACK_TARGET = FuncSelector(lambda entities, source: [source.attack_target])
CREATOR_TARGET = FuncSelector(lambda entities, source: [source.creator.target])


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
                if self.direction == self.Direction.LEFT:
                    result += e.left_minion
                else:
                    result += e.right_minion

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


class RandomShuffle(RandomSelector):
    def eval(self, entities, source):
        child_entities = self.child.eval(entities, source)
        return random.sample(child_entities, len(child_entities))


RANDOM = RandomSelector
SHUFFLE = RandomShuffle

DEAD = FuncSelector(
    lambda entities, source: [e for e in entities if hasattr(e, "dead") and e.dead]
)

# Selects the highest and lowest attack entities, respectively
HIGHEST_ATK = lambda sel: (
    RANDOM(sel + (AttrValue(GameTag.ATK) == OpAttr(sel, GameTag.ATK, max)))
)
LOWEST_ATK = lambda sel: (
    RANDOM(sel + (AttrValue(GameTag.ATK) == OpAttr(sel, GameTag.ATK, min)))
)

HIGHEST_COST = lambda sel: (
    RANDOM(sel + (AttrValue(GameTag.COST) == OpAttr(sel, GameTag.COST, max)))
)
LOWEST_COST = lambda sel: (
    RANDOM(sel + (AttrValue(GameTag.COST) == OpAttr(sel, GameTag.COST, min)))
)


class Controller(LazyValue):
    def __init__(self, child: Optional[SelectorLike] = None):
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


def SAME_RACE(entity1, entity2):
    races1 = getattr(entity1, "races", [])
    races2 = getattr(entity2, "races", [])
    for race in races1:
        if race in races2:
            return True
    return False


FRIENDLY = CONTROLLER == Controller()
ENEMY = CONTROLLER == Opponent()


def CONTROLLED_BY(selector):
    return AttrValue(GameTag.CONTROLLER) == Controller(selector)


CONTROLLED_BY_OWNER_OPPONENT = CONTROLLER == Opponent(OWNER)


# Enum tests
GameTag.test = lambda self, entity, *args: (
    entity is not None and bool(entity.tags.get(self))
)
CardType.test = lambda self, entity, *args: (entity is not None and self == entity.type)
Race.test = lambda self, entity, *args: (
    entity is not None and self in getattr(entity, "races", [])
)
Rarity.test = lambda self, entity, *args: (
    entity is not None and self == getattr(entity, "rarity", Rarity.INVALID)
)
Zone.test = lambda self, entity, *args: (entity is not None and self == entity.zone)
CardClass.test = lambda self, entity, *args: (
    entity is not None and self == getattr(entity, "card_class", CardClass.INVALID)
)

BATTLECRY = EnumSelector(GameTag.BATTLECRY)
CHARGE = EnumSelector(GameTag.CHARGE)
COMBO = EnumSelector(GameTag.COMBO)
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
DORMANT = EnumSelector(GameTag.DORMANT)
LIFESTEAL = EnumSelector(GameTag.LIFESTEAL)
IMMUNE = EnumSelector(GameTag.IMMUNE)
RUSH = EnumSelector(GameTag.RUSH)
ECHO = EnumSelector(GameTag.ECHO)
REBORN = EnumSelector(GameTag.REBORN)
CHOOSE_ONE = EnumSelector(GameTag.CHOOSE_ONE)
HAS_DISCOVER = EnumSelector(GameTag.DISCOVER)
LACKEY = EnumSelector(GameTag.MARK_OF_EVIL)
LIBRAM = EnumSelector(GameTag.LIBRAM)

ALWAYS_WINS_BRAWLS = AttrValue(enums.ALWAYS_WINS_BRAWLS) == True
KILLED_THIS_TURN = AttrValue(enums.KILLED_THIS_TURN) == True
CAST_ON_FRIENDLY_MINIONS = AttrValue(enums.CAST_ON_FRIENDLY_MINIONS) == True
CAST_ON_FRIENDLY_CHARACTERS = AttrValue(enums.CAST_ON_FRIENDLY_CHARACTERS) == True
EXHAUSTED = AttrValue(GameTag.EXHAUSTED) == True
THE_TURN_SUMMONED = AttrValue(GameTag.NUM_TURNS_IN_PLAY) == 0
TO_BE_DESTROYED = AttrValue("to_be_destroyed") == True

ROGUE = EnumSelector(CardClass.ROGUE)
WARLOCK = EnumSelector(CardClass.WARLOCK)

IN_PLAY = EnumSelector(Zone.PLAY)
IN_DECK = EnumSelector(Zone.DECK)
IN_HAND = EnumSelector(Zone.HAND)
IN_SECRET = EnumSelector(Zone.SECRET)
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
QUEST = EnumSelector(GameTag.QUEST)
HERO_POWER = EnumSelector(CardType.HERO_POWER)

BEAST = EnumSelector(Race.BEAST)
DEMON = EnumSelector(Race.DEMON)
DRAGON = EnumSelector(Race.DRAGON)
MECH = EnumSelector(Race.MECHANICAL)
MURLOC = EnumSelector(Race.MURLOC)
PIRATE = EnumSelector(Race.PIRATE)
TOTEM = EnumSelector(Race.TOTEM)
ELEMENTAL = EnumSelector(Race.ELEMENTAL)
TREANT = FuncSelector(
    lambda entities, src: [
        e for e in entities if getattr(e, "name_enUS", "").endswith("Treant")
    ]
)  # Race.`TREANT` is not defined yet.

COMMON = EnumSelector(Rarity.COMMON)
RARE = EnumSelector(Rarity.RARE)
EPIC = EnumSelector(Rarity.EPIC)
LEGENDARY = EnumSelector(Rarity.LEGENDARY)

ALL_PLAYERS = IN_PLAY + PLAYER
ALL_HEROES = IN_PLAY + HERO
ALL_MINIONS = IN_PLAY + MINION - DORMANT
ALL_CHARACTERS = IN_PLAY + CHARACTER - DORMANT
ALL_WEAPONS = IN_PLAY + WEAPON
ALL_SECRETS = IN_SECRET + SECRET
ALL_QUESTS = IN_SECRET + QUEST
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
FRIENDLY_MINIONS = ALL_MINIONS + FRIENDLY
FRIENDLY_CHARACTERS = ALL_CHARACTERS + FRIENDLY
FRIENDLY_WEAPON = ALL_WEAPONS + FRIENDLY
FRIENDLY_SECRETS = ALL_SECRETS + FRIENDLY
FRIENDLY_QUEST = ALL_QUESTS + FRIENDLY
FRIENDLY_HERO_POWER = ALL_HERO_POWERS + FRIENDLY

ENEMY_HAND = IN_HAND + ENEMY
ENEMY_DECK = IN_DECK + ENEMY
ENEMY_HERO = ALL_HEROES + ENEMY
ENEMY_MINIONS = ALL_MINIONS + ENEMY
ENEMY_CHARACTERS = ALL_CHARACTERS + ENEMY
ENEMY_WEAPON = ALL_WEAPONS + ENEMY
ENEMY_SECRETS = ALL_SECRETS + ENEMY
ENEMY_QUEST = ALL_QUESTS + ENEMY
ENEMY_HERO_POWER = ALL_HERO_POWERS + ENEMY

RANDOM_MINION = RANDOM(ALL_MINIONS - DEAD)
RANDOM_CHARACTER = RANDOM(ALL_CHARACTERS - DEAD)
RANDOM_OTHER_CHARACTER = RANDOM(ALL_CHARACTERS - DEAD - SELF)
RANDOM_FRIENDLY_MINION = RANDOM(FRIENDLY_MINIONS)
RANDOM_OTHER_MINION = RANDOM(ALL_MINIONS - SELF)
RANDOM_OTHER_FRIENDLY_MINION = RANDOM(FRIENDLY_MINIONS - SELF)
RANDOM_FRIENDLY_CHARACTER = RANDOM(FRIENDLY_CHARACTERS)
RANDOM_ENEMY_MINION = RANDOM(ENEMY_MINIONS - DEAD)
RANDOM_ENEMY_CHARACTER = RANDOM(ENEMY_CHARACTERS - DEAD)

DAMAGED_CHARACTERS = ALL_CHARACTERS + DAMAGED
CTHUN = FRIENDLY + ID("OG_280")

FRIENDLY_CLASS_CHARACTER = FuncSelector(
    lambda entities, src: [
        e
        for e in entities
        if hasattr(e, "card_class")
        and hasattr(e, "controller")
        and e.card_class == e.controller.hero.card_class
    ]
)
OTHER_CLASS_CHARACTER = FuncSelector(
    lambda entities, src: [
        e
        for e in entities
        if hasattr(e, "card_class")
        and hasattr(e, "controller")
        and e.card_class != CardClass.NEUTRAL
        and e.card_class != CardClass.DREAM
        and e.card_class != e.controller.hero.card_class
    ]
)

NEUTRAL = AttrValue(GameTag.CLASS) == CardClass.NEUTRAL

LEFTMOST_FIELD = FuncSelector(
    lambda entities, source: (
        source.game.player1.field.filter(dormant=False)[:1]
        + source.game.player2.field.filter(dormant=False)[:1]
    )
)
RIGTHMOST_FIELD = FuncSelector(
    lambda entities, source: (
        source.game.player1.field.filter(dormant=False)[-1:]
        + source.game.player2.field.filter(dormant=False)[-1:]
    )
)
LEFTMOST_HAND = FuncSelector(
    lambda entities, source: source.game.player1.hand[:1]
    + source.game.player2.hand[-1:]
)
RIGTHMOST_HAND = FuncSelector(
    lambda entities, source: source.game.player1.hand[:1]
    + source.game.player2.hand[-1:]
)
OUTERMOST_HAND = LEFTMOST_HAND + RIGTHMOST_HAND

NUM_CARDS_PLAYED_THIS_TURN = Attr(CONTROLLER, GameTag.NUM_CARDS_PLAYED_THIS_TURN)
CARDS_PLAYED_THIS_TURN = AttrValue("played_this_turn") == True

CARDS_PLAYED_THIS_GAME = FuncSelector(
    lambda entities, source: source.controller.cards_played_this_game
)

STARTING_DECK = FuncSelector(lambda entities, source: source.controller.starting_deck)
STARTING_HAND = FuncSelector(lambda entities, source: source.controller.starting_hand)

SPELL_DAMAGE = lambda amount: FuncSelector(
    lambda entities, source: source.controller.get_spell_damage(amount)
)
SPELL_HEAL = lambda amount: FuncSelector(
    lambda entities, source: source.controller.get_spell_heal(amount)
)

PLAY_RIGHT_MOST = FuncSelector(
    lambda entities, source: [
        e for e in entities if getattr(e, "play_right_most", False)
    ]
)

PLAY_LEFT_MOST = FuncSelector(
    lambda entities, source: [
        e for e in entities if getattr(e, "play_left_most", False)
    ]
)

PLAY_OUTCAST = FuncSelector(
    lambda entities, source: [e for e in entities if getattr(e, "play_outcast", False)]
)

ENTOURAGE = FuncSelector(lambda entities, source: source.entourage)

ANOTHER_CLASS = FuncSelector(
    lambda entities, source: [
        card_class for card_class in CardClass if source.card_class != card_class
    ]
)

CHOOSE_CARDS = lambda sel: (
    FuncSelector(lambda entities, source: sel.evaluate(source).choose_cards)
)

CARDS_PLAYED_LAST_TURN = FuncSelector(
    lambda entities, source: [
        e
        for e in entities
        if getattr(e, "turn_played", -1) == source.controller.last_turn
    ]
)

CARDS_OPPONENT_PLAYED_LAST_TURN = FuncSelector(
    lambda entities, source: [
        e
        for e in entities
        if getattr(e, "turn_played", -1) == source.controller.opponent.turn
    ]
)

GALAKROND = FuncSelector(
    lambda entities, source: (
        [source.controller.galakrond] if source.controller.galakrond else []
    )
)

STORE_CARD = FuncSelector(lambda entities, source: [source.store_card])

UPGRADED_HERO_POWER = FuncSelector(
    lambda entities, source: (
        [
            source.controller.card(
                source.controller.hero.power.upgraded_hero_power, source=source
            )
        ]
        if source.controller.hero.power.upgraded_hero_power
        else []
    )
)

GAME_SKIN = FuncSelector(lambda entites, source: [source.game.skin])

DRAWN_THIS_TURN = FuncSelector(
    lambda entites, source: [e for e in entites if getattr(e, "drawn_this_turn", False)]
)

SAME_RACE_TARGET = FuncSelector(
    lambda entites, source: [e for e in entites if SAME_RACE(e, source.target)]
)
