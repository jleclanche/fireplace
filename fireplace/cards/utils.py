import random

from hearthstone.deckstrings import Deck
from hearthstone.enums import CardClass, CardSet, CardType, GameTag, PlayReq, Race, Rarity
# from hearthstone.utils import LACKEY_CARDS

from ..actions import *
from ..aura import Refresh
from ..cards import db
from ..dsl import *
from ..events import *


# For buffs which are removed when the card is moved to play (eg. cost buffs)
# This needs to be Summon, because of Summon from the hand
REMOVED_IN_PLAY = Summon(ALL_PLAYERS, OWNER).after(Destroy(SELF))

ENEMY_CLASS = Attr(ENEMY_HERO, GameTag.CLASS)
FRIENDLY_CLASS = Attr(FRIENDLY_HERO, GameTag.CLASS)


Freeze = lambda target: SetTag(target, (GameTag.FROZEN, ))
Stealth = lambda target: SetTag(target, (GameTag.STEALTH, ))
Unstealth = lambda target: UnsetTag(target, (GameTag.STEALTH, ))
Taunt = lambda target: SetTag(target, (GameTag.TAUNT, ))
GiveCharge = lambda target: SetTag(target, (GameTag.CHARGE, ))
GiveDivineShield = lambda target: SetTag(target, (GameTag.DIVINE_SHIELD, ))
GiveWindfury = lambda target: SetTag(target, (GameTag.WINDFURY, ))
GivePoisonous = lambda target: SetTag(target, (GameTag.POISONOUS, ))
GiveLifesteal = lambda target: SetTag(target, (GameTag.LIFESTEAL, ))
GiveRush = lambda target: SetTag(target, (GameTag.RUSH, ))


CLEAVE = Hit(TARGET_ADJACENT, ATK(SELF))
COINFLIP = RandomNumber(0, 1) == 1
EMPTY_BOARD = Count(FRIENDLY_MINIONS) == 0
EMPTY_HAND = Count(FRIENDLY_HAND) == 0
FULL_BOARD = Count(FRIENDLY_MINIONS) == 7
FULL_HAND = Count(FRIENDLY_HAND) == 10
HOLDING_DRAGON = Find(FRIENDLY_HAND + DRAGON - SELF)
ELEMENTAL_PLAYED_LAST_TURN = Attr(CONTROLLER, enums.ELEMENTAL_PLAYED_LAST_TURN) > 0
TIMES_SPELL_PLAYED_THIS_GAME = Count(CARDS_PLAYED_THIS_GAME + SPELL)
TIMES_SECRETS_PLAYED_THIS_GAME = Count(CARDS_PLAYED_THIS_GAME + SECRET)

DISCOVER = lambda *args: Discover(CONTROLLER, *args).then(Give(CONTROLLER, Discover.CARD))

BASIC_HERO_POWERS = [
	"CS2_017", "DS1h_292", "CS2_034",
	"CS2_101", "CS1h_001", "CS2_083b",
	"CS2_083b", "CS2_056", "CS2_102",
]

HERO_POWER_MAP = {
	# Druid
	"CS2_017": "AT_132_DRUID",  # Malfurion Stormrage
	"CS2_017_HS1": "AT_132_DRUIDa",  # Lunara
	"CS2_017_HS2": "AT_132_DRUIDb",  # Elise Starseeker
	# Hunter
	"DS1h_292": "AT_132_HUNTER",  # Rexxar
	"DS1h_292_H1": "DS1h_292_H1_AT_132",  # Alleria Windrunner
	# Mage
	"CS2_034": "AT_132_MAGE",  # Jaina Proudmoore
	"CS2_034_H1": "CS2_034_H1_AT_132",  # Medivh
	"CS2_034_H2": "CS2_034_H2_AT_132",  # Khadgar
	# Paladin
	"CS2_101": "AT_132_PALADIN",  # Uther Lightbringer
	"CS2_101_H1": "CS2_101_H1_AT_132",  # Lady Liadrin
	"CS2_101_H2": "CS2_101_H2_AT_132",  # Prince Arthas
	"CS2_101_H3": "CS2_101_H3_AT_132",  # Sir Annoy-O
	# Priest
	"CS1h_001": "AT_132_PRIEST",  # Anduin Wrynn
	"CS1h_001_H1": "CS1h_001_H1_AT_132",  # Tyrande Whisperwind
	"CS1h_001_H2": "CS1h_001_H2_AT_132",  # Madame Lazul
	# Rogue
	"CS2_083b": "AT_132_ROGUE",  # Valeera Sanguinar
	"CS2_083b_H1": "AT_132_ROGUE_H1",  # Maiev Shadowsong
	# Shaman
	"CS2_049": "AT_132_SHAMAN",  # Thrall
	"CS2_049_H1": "CS2_049_H1_AT_132",  # Morgl the Oracle
	"CS2_049_H2": "CS2_049_H2_AT_132",  # King Rastakhan
	"CS2_049_H3": "CS2_049_H3_AT_132",  # The Thunder King
	# Warlock
	"CS2_056": "AT_132_WARLOCK",  # Gul'dan
	"CS2_056_H1": "AT_132_WARLOCKa",  # Nemsy Necrofizzle
	"CS2_056_H2": "AT_132_WARLOCKb",  # Mecha-Jaraxxus
	# Warrior
	"CS2_102": "AT_132_WARRIOR",  # Garrosh Hellscream
	"CS2_102_H1": "CS2_102_H1_AT_132",  # Magni Bronzebeard
}

UPGRADE_HERO_POWER = Switch(FRIENDLY_HERO_POWER, {
	k: Summon(CONTROLLER, v) for k, v in HERO_POWER_MAP.items()
})

BASIC_TOTEMS = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]

POTIONS = [
	"CFM_021",  # Freezing Potion
	"CFM_065",  # Volcanic Potion
	"CFM_620",  # Potion of Polymorph
	"CFM_603",  # Potion of Madness
	"CFM_604",  # Greater Healing Potion
	"CFM_661",  # Pint-Size Potion
	"CFM_662",  # Dragonfire Potion
	"CFM_094",  # Felfire Potion
	"CFM_608",  # Blastcrystal Potion
	"CFM_611",  # Bloodfury Potion
]

LIBRAMS = IDS([
	"BT_011",  # Libram of Justice
	"BT_024",  # Libram of Hope
	"BT_025",  # Libram of Wisdom
])

LICH_KING_CARDS = [
	"ICC_314t1",
	"ICC_314t2",
	"ICC_314t3",
	"ICC_314t4",
	"ICC_314t5",
	"ICC_314t6",
	"ICC_314t7",
	"ICC_314t8",
]

THE_COIN = "GAME_005"

LACKEY_CARDS = [
	"DAL_613",
	"DAL_614",
	"DAL_615",
	"DAL_739",
	"DAL_741",
	# "ULD_616",
	# "DRG_052",
]

RandomBasicTotem = lambda *args, **kw: RandomID(*BASIC_TOTEMS, **kw)
RandomBasicHeroPower = lambda *args, **kw: RandomID(*BASIC_HERO_POWERS, **kw)
RandomPotion = lambda *args, **kw: RandomID(*POTIONS, **kw)
RandomLackey = lambda *args, **kw: RandomID(*LACKEY_CARDS, **kw)

# 50% chance to attack the wrong enemy.
FORGETFUL = Attack(SELF).on(
	COINFLIP & Retarget(SELF, RANDOM(ALL_CHARACTERS - Attack.DEFENDER - CONTROLLED_BY(SELF)))
)

AT_MAX_MANA = lambda s: MANA(s) == 10
OVERLOADED = lambda s: (OVERLOAD_LOCKED(s) > 0) or (OVERLOAD_OWED(s) > 0)
CHECK_CTHUN = ATK(HIGHEST_ATK(CTHUN)) >= 10
CAST_WHEN_DRAWN = Destroy(SELF), Draw(CONTROLLER), Battlecry(SELF, None)


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

JOUST_SPELL = JoustHelper(
	RANDOM(FRIENDLY_DECK + SPELL),
	RANDOM(ENEMY_DECK + SPELL)
)

RECRUIT = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))
Recruit = lambda selector: Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + selector))

MAGNETIC = lambda buff: Find(RIGHT_OF(SELF) + MECH) & (
	Buff(RIGHT_OF(SELF), buff, atk=ATK(SELF), max_health=CURRENT_HEALTH(SELF)), Remove(SELF)
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
	return GainMana(selector, amount).then(SpendMana(selector, GainMana.AMOUNT))


def custom_card(cls):
	from . import CardDB, db
	id = cls.__name__
	if GameTag.CARDNAME not in cls.tags:
		raise ValueError("No name provided for custom card %r" % (cls))
	db[id] = CardDB.merge(id, None, cls)
	# Give the card its fake name
	db[id].strings = {
		GameTag.CARDNAME: {"enUS": cls.tags[GameTag.CARDNAME]},
		GameTag.CARDTEXT_INHAND: {"enUS": ""}
	}
	return cls


def decode_deckstring(deckstring: str):
	deck = Deck.from_deckstring(deckstring)
	hero_id = deck.heroes[0]
	hero_id = db.dbf[hero_id]
	cards = []
	for card_id, num in deck.cards:
		card_id = db.dbf[card_id]
		cards += [card_id] * num
	return hero_id, cards


class JadeGolemCardtextEntity0(LazyNum):
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def evaluate(self, source):
		card = self.get_entities(source)[0]
		jade_golem = card.controller.jade_golem
		return f"{jade_golem}/{jade_golem}"


class JadeGolemCardtextEntity1(LazyNum):
	def __init__(self, selector):
		super().__init__()
		self.selector = selector

	def evaluate(self, source):
		card = self.get_entities(source)[0]
		if card.data.locale == "enUS":
			jade_golem = card.controller.jade_golem
			if jade_golem == 8 or jade_golem == 18:
				return "n"
		return ""


class JadeGolemUtils:
	tags = {
		GameTag.CARDTEXT_ENTITY_0: JadeGolemCardtextEntity0(SELF),
		GameTag.CARDTEXT_ENTITY_1: JadeGolemCardtextEntity1(SELF),
	}
