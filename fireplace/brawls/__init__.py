import random
from hearthstone.enums import CardClass, CardType, GameTag
from ..cards.brawl.banana_brawl import RandomBanana
from ..cards.utils import *
from ..game import Game


class BlackrockShowdownBrawl(Game):
	"""
	Showdown at Blackrock Mountain

	These two epic bosses of Blackrock Mountain are
	settling things once and for all... with your help!
	"""

	NEFARIAN_DECK = ([
		"BRMA14_3",
		"BRMA14_5",
		"BRMA14_7",
		"BRMA14_9",
		"BRMA10_5H", "BRMA10_5H", "BRMA10_5H",
		"BRMC_83", "BRMC_83",
		"BRMC_84", "BRMC_84",
		"BRMC_86",
		"BRMC_88", "BRMC_88",
		"BRMC_97",
		"BRMC_98",
		"BRM_018", "BRM_018",
		"BRM_029",
		"BRM_031",
		"BRM_033", "BRM_033", "BRM_033",
		"BRM_034", "BRM_034",
		"EX1_303", "EX1_303",
		"EX1_562",
		"EX1_570", "EX1_570",
	], "TBA01_4")

	RAGNAROS_DECK = ([
		"BRMA_01", "BRMA_01",
		"BRMC_85",
		"BRMC_87",
		"BRMC_89", "BRMC_89",
		"BRMC_90", "BRMC_90", "BRMC_90",
		"BRMC_91", "BRMC_91",
		"BRMC_92",
		"BRMC_95",
		"BRMC_95h", "BRMC_95h",
		"BRMC_96",
		"BRMC_99",
		"BRMC_100", "BRMC_100",
		"CS2_032", "CS2_032",
		"CS2_042", "CS2_042",
		"EX1_241", "EX1_241",
		"EX1_249",
		"EX1_319", "EX1_319",
		"EX1_620", "EX1_620",
	], "TBA01_1")

	@classmethod
	def new_game(cls, *players):
		decks = random.sample((cls.NEFARIAN_DECK, cls.RAGNAROS_DECK), 2)
		for player, deck in zip(players, decks):
			player.starting_deck, player.starting_hero = deck
		return cls(players)

	def setup(self):
		super().setup()
		for player in self.players:
			if player.hero.id == self.NEFARIAN_DECK[1]:
				player.max_mana = 4
				player.hero.armor = 30
			else:
				player.summon("BRMC_94")  # Sulfuras


class BananaBrawl(Game):
	"""
	Banana Brawl!

	Mukla is a year older, and he LOVES bananas! Whenever
	one of your minions dies, he gives you a Banana to
	celebrate!
	"""

	def _schedule_death(self, card):
		ret = super()._schedule_death(card)
		if card.type == CardType.MINION:
			ret.append(Give(card.controller, RandomBanana))
		return ret


class SpidersEverywhereBrawl(Game):
	"""
	Spiders, Spiders EVERYWHERE!

	Spiders have overrun everything, including your deck!
	Whatever class you play, your deck will be TEEMING with
	Webspinners.
	"""

	def __init__(self, players):
		from .. import cards
		super().__init__(players)
		for player in players:
			hero = player.starting_hero
			player_class = getattr(cards, hero).card_class
			spells = cards.filter(card_class=player_class, type=CardType.SPELL)
			deck = ["FP1_011"] * 23
			for i in range(7):
				deck.append(random.choice(spells))
			player.starting_deck, player.starting_hero = deck, hero


class GreatSummonerBrawl(Game):
	"""
	The Great Summoner Competition

	Summoners from across the world have come to compete. When
	you cast a spell, a random minion of the same cost is summoned
	for you!
	"""

	base_events = [
		Play(PLAYER, SPELL).on(
			Summon(Play.PLAYER, RandomMinion(cost=COST(Play.CARD)))
		)
	]


class CrossroadsEncounterBrawl(Game):
	"""
	Encounter at the Crossroads

	Encounter at the crossroads! Pick a class.
	Let's see what's in your deck this time!
	"""

	def __init__(self, players):
		from .. import cards
		super().__init__(players)
		for player in players:
			hero = player.starting_hero
			player_class = getattr(cards, hero).card_class
			pool = cards.filter(card_class=player_class, collectible=True)
			deck = [random.choice(pool) for i in range(15)]
			pool = cards.filter(card_class=CardClass.INVALID, collectible=True)
			deck += [random.choice(pool) for i in range(15)]
			player.starting_deck, player.starting_hero = deck, hero


class HeartOfTheSunwellBrawl(Game):
	"""
	Heart of the Sunwell

	In the Sunwell lies unlimited power, and that power is
	yours! Start each game with 10 mana and see what you
	can do with it!
	"""

	def setup(self):
		super().setup()
		for player in self.players:
			player.max_mana = 10


class TooManyPortalsBrawl(Game):
	"""
	Too Many Portals!

	The master mages of Dalaran have gone too far this time,
	opening up hundreds of portals!  Choose a class and use a
	few spells and a WHOLE lot of portals to defeat your rivals!
	"""
	UNSTABLE_PORTAL = "GVG_003"

	def __init__(self, players):
		from .. import cards
		super().__init__(players)
		for player in players:
			hero = player.starting_hero
			player_class = getattr(cards, hero).card_class
			spells = cards.filter(card_class=player_class, type=CardType.SPELL)
			deck = [self.UNSTABLE_PORTAL] * 23
			for i in range(7):
				deck.append(random.choice(spells))
			player.starting_deck, player.starting_hero = deck, hero


class MaskedBallBrawl(Game):
	"""
	The Masked Ball

	At the SI:7 mansion in Stormwind they have a grand masked ball every year.
	Everyone is in disguise! When a minion dies, its disguise is revealed, showing the
	minion to actually be a different random minion that costs (2) less and ready for
	another fight!
	"""

	base_events = [
		Play(PLAYER, MINION + (COST >= 2)).on(
			Buff(Play.CARD, "TB_Pilot1")
		)
	]


class GrandTournamentBrawl(Game):
	"""
	Grand Tournament Match

	On the road to The Grand Tournament, two knights face off!
	One relies on jousting skill, while the other inspires troops to
	great deeds. Who will win?
	"""

	ALLERIA_DECK = ([
		"AT_010",
		"AT_058", "AT_058",
		"AT_060",
		"AT_061", "AT_061",
		"AT_063",
		"AT_102", "AT_102",
		"AT_103"
		"AT_108", "AT_108",
		"AT_111",
		"AT_112", "AT_112",
		"AT_128",
		"CS2_084", "CS2_084",
		"DS1_178",
		"DS1_184", "DS1_184",
		"DS1_185", "DS1_185",
		"EX1_538", "EX1_538",
		"EX1_609",
		"EX1_611",
		"GVG_073",
		"NEW1_031", "NEW1_031",
	], "HERO_05a")

	MEDIVH_DECK = ([
		"AT_001", "AT_001",
		"AT_003", "AT_003",
		"AT_005", "AT_005",
		"AT_007", "AT_007",
		"AT_008", "AT_008",
		"AT_009",
		"AT_080", "AT_080",
		"AT_082", "AT_082",
		"AT_083",
		"AT_085", "AT_085",
		"AT_087",
		"AT_089", "AT_089",
		"AT_097",
		"AT_099",
		"AT_114", "AT_114",
		"AT_119",
		"AT_127",
		"AT_120", "AT_120",
		"CS2_028",
	], "HERO_08a")

	@classmethod
	def new_game(cls, *players):
		decks = random.sample((cls.ALLERIA_DECK, cls.MEDIVH_DECK), 2)
		for player, deck in zip(players, decks):
			player.starting_deck, player.starting_hero = deck
		return cls(players)


class RainingManaBrawl(Game):
	"""
	It's Raining Mana!

	Dalaran floats overhead, it's soaking your deck with mana! On
	your first turn you get 1 like normal, but then you get 3, then
	5, then 7, etc
	"""
	def begin_turn(self, player):
		super().begin_turn(player)
		if self.turn > 2:
			player.max_mana += 1


class DoubleDeathrattlerBattler(Game):
	"""
	Double Deathrattler Battler

	Death is not quiet the end... because minions
	with Deathrattle now rattle twice.
	"""
	class Data:
		class scripts:
			update = Refresh(ALL_PLAYERS, {GameTag.EXTRA_DEATHRATTLES: True})

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.data = self.Data()
