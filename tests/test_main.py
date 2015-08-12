#!/usr/bin/env python
import sys; sys.path.append("..")
import logging
import random
import fireplace.cards
from fireplace.cards.heroes import *
from fireplace.enums import *
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import random_draft


# Token minions
GOLDSHIRE_FOOTMAN = "CS1_042"
TARGET_DUMMY = "GVG_093"
KOBOLD_GEOMANCER = "CS2_142"
SPELLBENDERT = "tt_010a"
WISP = "CS2_231"
WHELP = "ds1_whelptoken"

# Token spells
MOONFIRE = "CS2_008"
CIRCLE_OF_HEALING = "EX1_621"
DREAM = "DREAM_04"
SILENCE = "EX1_332"
THE_COIN = "GAME_005"
HAND_OF_PROTECTION = "EX1_371"
TIME_REWINDER = "PART_002"

# Debug spells
RESTORE_1 = "XXX_003"
DESTROY_DECK = "XXX_047"


BLACKLIST = (
	"GVG_007",  # Flame Leviathan
)

logging.getLogger().setLevel(logging.DEBUG)


class BaseTestGame(Game):
	def start(self):
		super().start()
		self.player1.max_mana = 10
		self.player2.max_mana = 10


_draftcache = {}
def _draft(hero, exclude):
	# random_draft() is fairly slow, this caches the drafts
	if (hero, exclude) not in _draftcache:
		_draftcache[(hero, exclude)] = random_draft(hero, exclude + BLACKLIST)
	return _draftcache[(hero, exclude)]


_heroes = fireplace.cards.filter(collectible=True, type=CardType.HERO)

def prepare_game(hero1=None, hero2=None, exclude=(), game_class=BaseTestGame):
	print("Initializing a new game")
	if hero1 is None:
		hero1 = random.choice(_heroes)
	if hero2 is None:
		hero2 = random.choice(_heroes)
	deck1 = _draft(hero=hero1, exclude=exclude)
	deck2 = _draft(hero=hero2, exclude=exclude)
	player1 = Player(name="Player1")
	player1.prepare_deck(deck1, hero1)
	player2 = Player(name="Player2")
	player2.prepare_deck(deck2, hero2)
	game = game_class(players=(player1, player2))
	game.start()

	return game


def prepare_empty_game(game_class=BaseTestGame):
	player1 = Player(name="Player1")
	player1.prepare_deck([], random.choice(_heroes))
	player1.cant_fatigue = True
	player2 = Player(name="Player2")
	player2.prepare_deck([], random.choice(_heroes))
	player2.cant_fatigue = True
	game = game_class(players=(player1, player2))
	game.start()

	return game


def test_joust():
	from fireplace.cards.utils import Give, JOUST
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.shuffle_into_deck()
	wisp2 = game.player1.give(WISP)
	wisp2.shuffle_into_deck()
	game.end_turn()

	goldshire = game.player2.give(GOLDSHIRE_FOOTMAN)
	goldshire.shuffle_into_deck()
	game.queue_actions(game.player2, [JOUST & Give(game.player2, TARGET_DUMMY)])
	assert game.player2.hand.filter(id=TARGET_DUMMY)
	game.end_turn()

	game.queue_actions(game.player1, [JOUST & Give(game.player1, TARGET_DUMMY)])
	assert not game.player1.hand.filter(id=TARGET_DUMMY)


def test_cheat_destroy_deck():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	game.player1.give(DESTROY_DECK).play(target=game.player2.hero)
	assert not game.player2.deck
	game.end_turn()

	assert not game.player2.hand
	assert game.player2.hero.health == 29
	game.player2.give(DESTROY_DECK).play(target=game.player1.hero)
	assert not game.player1.deck


def test_positioning():
	game = prepare_game()
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	wisp3 = game.current_player.give(WISP)
	wisp3.play()

	assert wisp1.adjacent_minions == [wisp2]
	assert wisp2.adjacent_minions == [wisp1, wisp3]
	assert wisp3.adjacent_minions == [wisp2]
	game.end_turn(); game.end_turn()
	flametongue = game.current_player.give("EX1_565")
	flametongue.play()
	wisp4 = game.current_player.give(WISP)
	wisp4.play()
	assert flametongue.aura
	assert wisp3.buffs, wisp3.buffs
	assert wisp1.atk == 1, wisp1.atk
	assert wisp2.atk == 1
	assert wisp3.atk == 3, wisp3.atk
	assert flametongue.atk == 0, flametongue.atk
	assert flametongue.adjacent_minions == [wisp3, wisp4]
	assert wisp4.atk == 3, wisp4.atk


def test_armor():
	game = prepare_game(WARRIOR, WARRIOR)
	assert game.current_player.hero.armor == 0
	assert not game.current_player.hero.power.exhausted
	assert game.current_player.hero.power.is_usable()
	game.current_player.hero.power.use()
	assert game.current_player.hero.power.exhausted
	assert not game.current_player.hero.power.is_usable()
	assert game.current_player.hero.armor == 2
	game.end_turn()

	axe = game.current_player.give("CS2_106")
	axe.play()
	assert axe is game.current_player.weapon
	assert axe in game.current_player.hero.slots
	assert game.current_player.hero.atk == 3
	game.current_player.hero.attack(game.current_player.opponent.hero)
	assert game.current_player.opponent.hero.health == 29
	assert game.current_player.opponent.hero.armor == 0


def test_freeze():
	game = prepare_game()
	flameimp = game.current_player.give("EX1_319")
	flameimp.play()
	game.end_turn()

	frostshock = game.current_player.give("CS2_037")
	frostshock.play(target=flameimp)
	assert flameimp.frozen
	game.end_turn()

	assert flameimp.frozen
	assert not flameimp.can_attack()
	game.end_turn()
	assert not flameimp.frozen
	game.end_turn()

	wisp = game.current_player.give(WISP)
	wisp.play()
	wisp.frozen = True
	assert wisp.frozen
	game.end_turn()
	assert not wisp.frozen


def test_spell_power():
	game = prepare_game(HUNTER, HUNTER)

	expected_health = 30
	assert game.player2.hero.health == expected_health
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 1
	assert game.player2.hero.health == expected_health
	# Play a kobold
	assert game.player1.spellpower == 0
	game.player1.give(KOBOLD_GEOMANCER).play()
	assert game.player1.spellpower == 1
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 1 + 1
	assert game.player2.hero.health == expected_health
	# Summon Malygos
	malygos = game.player1.summon("EX1_563")
	assert game.player1.spellpower == 1 + 5
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 1 + 1 + 5
	assert game.player2.hero.health == expected_health
	# Test heals are not affected
	game.player1.give(RESTORE_1).play(target=game.player2.hero)
	expected_health += 1
	assert game.player2.hero.health == expected_health
	game.end_turn(); game.end_turn()

	# Check hero power is unaffected
	game.player1.hero.power.use()
	expected_health -= 2
	assert game.player2.hero.health == expected_health
	# Check battlecries are unaffected
	game.player1.give("CS2_189").play(target=game.player2.hero)
	expected_health -= 1
	assert game.player2.hero.health == expected_health
	game.end_turn(); game.end_turn()

	malygos.destroy()
	# Check arcane missiles doesn't wreck everything
	game.player1.give("EX1_277").play()
	expected_health -= 3 + 1
	assert game.player2.hero.health == expected_health


def test_mage():
	game = prepare_game(MAGE, MAGE)
	assert game.player1.hero.id is MAGE
	assert game.player1.hero.health == 30
	assert game.player1.opponent.hero.health == 30
	assert game.player1.times_hero_power_used_this_game == 0

	# Fireblast the opponent hero
	game.player1.hero.power.use(target=game.player2.hero)
	assert game.player1.hero.health == 30
	assert game.player1.opponent.hero.health == 29
	assert game.player1.times_hero_power_used_this_game == 1
	assert not game.player1.hero.power.is_usable()


def test_priest():
	game = prepare_game(PRIEST, PRIEST)
	assert game.player1.hero.id is PRIEST
	# Heal self
	assert game.player1.hero.health == 30
	game.player1.hero.power.use(target=game.player1.hero)
	assert game.player1.hero.health == 30

	game.end_turn(); game.end_turn()
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 29
	game.player1.hero.power.use(target=game.player1.hero)
	assert game.player1.hero.health == 30
	assert not game.player1.hero.power.is_usable()


def test_shaman():
	game = prepare_game(SHAMAN, SHAMAN)
	assert game.player1.hero.id is SHAMAN
	assert len(game.player1.hero.power.data.entourage) == 4

	# use hero power four times
	for i in range(4):
		assert len(game.player1.field) == i
		assert game.player1.hero.power.is_usable()
		game.player1.hero.power.use()
		assert len(game.player1.field) == i + 1
		assert game.player1.field[-1].id in game.player1.hero.power.data.entourage
		game.end_turn(); game.end_turn()

	# ensure hero power can only be used again after a totem was destroyed
	assert not game.player1.hero.power.is_usable()
	game.player1.field[0].destroy()
	assert game.player1.hero.power.is_usable()

	# ensure that hero power cannot be used on full board
	for i in range(4):
		game.player1.give(WISP).play()
	assert len(game.player1.field) == 7
	assert not game.player1.hero.power.is_usable()


def test_paladin():
	game = prepare_game(PALADIN, PALADIN)
	assert game.current_player.hero.id is PALADIN

	game.current_player.hero.power.use()
	assert len(game.board) == 1
	assert len(game.current_player.field) == 1
	assert game.current_player.field[0].id == "CS2_101t"

	# ensure that hero power cannot be used on full board
	game.end_turn(); game.end_turn()
	assert game.player1.hero.power.is_usable()
	for i in range(6):
		game.player1.give(WISP).play()
	assert len(game.player1.field) == 7
	assert not game.player1.hero.power.is_usable()


def test_deathrattle():
	game = prepare_game()
	loothoarder = game.current_player.give("EX1_096")
	loothoarder.play()
	cardcount = len(game.current_player.hand)
	game.end_turn()

	archer = game.current_player.give("CS2_189")
	archer.play(target=loothoarder)
	assert loothoarder.dead
	assert loothoarder.damage == 0
	assert len(game.current_player.opponent.hand) == cardcount + 1
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()

	# test soul of the forest: deathrattle in slots
	assert not archer.has_deathrattle
	sotf = game.current_player.give("EX1_158")
	sotf.play()
	assert len(archer.buffs) == 1
	assert archer.buffs[0].has_deathrattle
	assert archer.has_deathrattle
	assert len(game.current_player.field) == 1
	game.current_player.give(MOONFIRE).play(target=archer)
	assert archer.dead
	assert len(game.current_player.field) == 1


def test_chromaggus():
	game = prepare_game()
	chromaggus = game.player1.give("BRM_031")
	chromaggus.play()
	game.end_turn(); game.end_turn()

	game.player1.discard_hand()
	arcint = game.player1.give("CS2_023")
	assert len(game.player1.hand) == 1
	arcint.play()
	assert len(game.player1.hand) == 4
	assert game.player1.hand[0] == game.player1.hand[1]
	assert game.player1.hand[2] == game.player1.hand[3]


def test_chromaggus_naturalize():
	game = prepare_game()
	chromaggus = game.player1.give("BRM_031")
	chromaggus.play()
	game.end_turn()
	game.player1.discard_hand()
	naturalize = game.player2.give("EX1_161")
	naturalize.play(target=chromaggus)
	assert len(game.player1.hand) == 4
	assert game.player1.hand[0] == game.player1.hand[1]
	assert game.player1.hand[2] == game.player1.hand[3]


def test_cobalt_guardian():
	game = prepare_game()
	cobalt = game.player1.give("GVG_062")
	cobalt.play()
	assert not cobalt.divine_shield
	game.player1.give(TARGET_DUMMY).play()
	assert cobalt.divine_shield
	game.player1.give(TARGET_DUMMY).play()
	assert cobalt.divine_shield


def test_cogmaster():
	game = prepare_game()
	cogmaster = game.current_player.give("GVG_013")
	cogmaster.play()
	assert cogmaster.atk == 1
	dummy = game.current_player.give(TARGET_DUMMY)
	dummy.play()
	assert cogmaster.atk == 3
	humility = game.current_player.give("EX1_360")
	humility.play(target=cogmaster)
	assert cogmaster.atk == 3
	dummy.destroy()
	assert cogmaster.atk == 1
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()

	game.current_player.give(TARGET_DUMMY).play()
	assert cogmaster.atk == 3
	blessedchamp = game.current_player.give("EX1_355")
	blessedchamp.play(target=cogmaster)
	cogmaster.atk == 6


def test_cogmasters_wrench():
	game = prepare_game()
	wrench = game.current_player.summon("GVG_024")
	assert wrench.atk == game.current_player.hero.atk == 1
	game.end_turn(); game.end_turn()

	dummy = game.current_player.give(TARGET_DUMMY)
	dummy.play()
	assert wrench.atk == game.current_player.hero.atk == 3
	dummy.destroy()
	assert wrench.atk == game.current_player.hero.atk == 1


def test_cult_master():
	game = prepare_game()
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	cultmaster = game.current_player.give("EX1_595")
	cultmaster.play()
	assert len(game.current_player.hand) == 4
	game.current_player.give(MOONFIRE).play(target=wisp1)
	assert len(game.current_player.hand) == 4 + 1

	# Make sure cult master doesn't draw off itself
	game.current_player.give(MOONFIRE).play(target=cultmaster)
	game.current_player.give(MOONFIRE).play(target=cultmaster)
	assert len(game.current_player.hand) == 4 + 1

	game.current_player.give(MOONFIRE).play(target=wisp2)
	assert len(game.current_player.hand) == 4 + 1


def test_cult_master_board_clear():
	game = prepare_game()
	game.player1.discard_hand()
	for i in range(4):
		game.player1.give(WISP).play()
	cultmaster = game.player1.give("EX1_595")
	cultmaster.play()
	game.player1.give(MOONFIRE).play(target=cultmaster)
	assert len(game.player1.field) == 5
	# Whirlwind the board
	game.player1.give("EX1_400").play()
	assert len(game.player1.hand) == 0


def test_mana():
	game = prepare_game(game_class=Game)
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	assert footman.cost == 1
	footman.play()
	assert footman.atk == 1
	assert footman.health == 2
	game.end_turn()

	# Play the coin
	coin = game.player2.hand.filter(id=THE_COIN)[0]
	coin.play()
	assert game.player2.mana == 2
	assert game.player2.temp_mana == 1
	game.end_turn()

	assert game.player2.temp_mana == 0
	assert game.player2.mana == 1
	game.end_turn(); game.end_turn()

	assert game.player1.mana == 3
	assert game.player1.max_mana == 3
	felguard = game.player1.give("EX1_301")
	felguard.play()
	assert game.player1.mana == 0
	assert game.player1.max_mana == 2

	for i in range(10):
		game.end_turn(); game.end_turn()

	assert game.player1.mana == game.player1.max_resources == 10
	assert game.player2.mana == game.player2.max_resources == 10


def test_overload():
	game = prepare_game(game_class=Game)
	dustdevil = game.player1.give("EX1_243")
	dustdevil.play()
	assert game.player1.overloaded == 2
	game.end_turn(); game.end_turn()
	assert game.player1.overloaded == 0
	assert game.player1.overload_locked == 2
	assert game.current_player.mana == 0


def test_charge():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	wisp.play()
	assert not wisp.charge
	assert not wisp.can_attack()
	# play Charge on wisp
	game.current_player.give("CS2_103").play(target=wisp)
	assert wisp.buffs[0].tags[GameTag.CHARGE]
	assert wisp.charge
	assert wisp.can_attack()
	wisp.attack(game.current_player.opponent.hero)
	assert not wisp.can_attack()
	game.end_turn()

	stonetusk = game.current_player.give("CS2_171")
	stonetusk.play()
	assert stonetusk.charge
	assert stonetusk.can_attack()
	game.end_turn()
	assert wisp.can_attack()
	wisp.attack(game.current_player.opponent.hero)
	assert not wisp.can_attack()
	game.end_turn()

	watcher = game.current_player.give("EX1_045")
	watcher.play()
	assert not watcher.can_attack()
	game.current_player.give("CS2_103").play(target=watcher)
	assert not watcher.can_attack()
	game.end_turn(); game.end_turn()

	assert not watcher.can_attack()
	watcher.silence()
	assert watcher.can_attack()


def test_divine_shield():
	game = prepare_game()
	squire = game.current_player.give("EX1_008")
	squire.play()
	assert squire.divine_shield
	game.current_player.give(MOONFIRE).play(target=squire)
	assert len(game.current_player.field) == 1
	assert not squire.divine_shield
	game.current_player.give(MOONFIRE).play(target=squire)
	assert len(game.current_player.field) == 0
	assert not squire.divine_shield
	game.end_turn(); game.end_turn()

	# test damage events with Divine Shield
	gurubashi = game.current_player.summon("EX1_399")
	assert gurubashi.atk == 2
	assert gurubashi.health == 7
	assert not gurubashi.divine_shield
	prot = game.current_player.give(HAND_OF_PROTECTION)
	prot.play(target=gurubashi)
	assert gurubashi.divine_shield
	game.current_player.give(MOONFIRE).play(target=gurubashi)
	assert not gurubashi.divine_shield
	assert gurubashi.atk == 2
	assert gurubashi.health == 7


def test_divine_spirit():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	assert wisp.health == 1
	wisp.play()
	game.end_turn()

	game.current_player.give("CS2_236").play(target=wisp)
	assert wisp.health == 1 * 2
	game.end_turn()

	game.current_player.give("CS2_236").play(target=wisp)
	assert wisp.health == 1 * 2 * 2
	game.end_turn()

	equality = game.current_player.give("EX1_619")
	equality.play()
	assert wisp.health == 1
	game.current_player.give("CS2_236").play(target=wisp)
	assert wisp.health == 1 * 2
	game.end_turn()


def test_savagery():
	game = prepare_game(DRUID, DRUID)
	watcher = game.player1.give("EX1_045")
	watcher.play()
	assert watcher.health == 5
	savagery = game.player1.give("EX1_578")
	savagery.play(watcher)
	assert watcher.health == 5

	game.player1.hero.power.use()
	savagery2 = game.player1.give("EX1_578")
	savagery2.play(watcher)
	assert watcher.health == 5 - 1
	game.end_turn(); game.end_turn()

	# Play a kobold
	game.current_player.give(KOBOLD_GEOMANCER).play()
	savagery3 = game.player1.give("EX1_578")
	savagery3.play(watcher)
	assert watcher.health == 5 - 1 - 1


def test_silence():
	game = prepare_game()
	silence = game.current_player.give(SILENCE)
	thrallmar = game.current_player.give("EX1_021")
	thrallmar.play()
	assert not thrallmar.silenced
	assert thrallmar.windfury
	silence.play(target=thrallmar)
	assert thrallmar.silenced
	assert not thrallmar.windfury


def test_earth_shock():
	game = prepare_game()
	crusader = game.current_player.give("EX1_020")
	crusader.play()
	assert crusader.divine_shield
	game.end_turn()
	earthshock = game.current_player.give("EX1_245")
	earthshock.play(target=crusader)
	assert crusader.dead


def test_eaglehorn_bow():
	game = prepare_game()
	bow = game.player1.give("EX1_536")
	icebarrier = game.player1.give("EX1_289")
	wisp = game.player2.give(WISP)
	bow.play()
	assert bow.durability == 2
	game.end_turn()

	wisp.play()
	game.end_turn()

	icebarrier.play()
	assert bow.durability == 2
	game.end_turn()

	assert game.current_player.opponent.secrets
	wisp.attack(target=game.player1.hero)
	assert not game.current_player.opponent.secrets
	assert game.player1.hero.health == 30
	assert game.player1.hero.armor == 7
	assert bow.buffs
	assert bow.durability == 3


def test_echoing_ooze():
	game = prepare_game()
	ooze = game.player1.give("FP1_003")
	ooze.play()
	assert len(game.player1.field) == 1
	game.end_turn()

	assert len(game.player1.field) == 2
	assert game.player1.field[0] is ooze
	assert game.player1.field[1].id == ooze.id
	assert game.player1.field[1].atk == ooze.atk
	assert game.player1.field[1].health == ooze.health


def test_echo_of_medivh():
	game = prepare_game()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give(TARGET_DUMMY).play()
	game.player1.give(GOLDSHIRE_FOOTMAN).play()
	game.end_turn()
	game.player2.give(SPELLBENDERT).play()
	game.end_turn()
	game.player1.discard_hand()
	echo = game.player1.give("GVG_005")
	echo.play()
	assert game.player1.hand == [WISP, WISP, TARGET_DUMMY, GOLDSHIRE_FOOTMAN]
	assert len(game.player1.field) == 4


def test_equality():
	game = prepare_game()
	equality = game.current_player.give("EX1_619")
	# summon a bunch of big dudes
	game.current_player.summon("CS2_186")
	game.current_player.summon("CS2_186")
	game.current_player.opponent.summon("CS2_186")
	game.current_player.opponent.summon("CS2_186")
	# And a violet teacher too, why not
	game.current_player.summon("NEW1_026")

	pyro = game.current_player.give("NEW1_020")
	pyro.play()
	assert len(game.board) == 6
	equality.play()
	assert not game.board


def test_elite_tauren_chieftain():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	assert len(game.player1.hand) == 0
	assert len(game.player2.hand) == 0
	tauren = game.player1.give("PRO_001")
	tauren.play()
	assert len(game.player1.hand) == 1
	assert len(game.player2.hand) == 1
	chords = ("PRO_001a", "PRO_001b", "PRO_001c")
	assert game.player1.hand[0] in chords
	assert game.player2.hand[0] in chords


def test_stealth_windfury():
	game = prepare_game(MAGE, MAGE)
	worgen = game.current_player.give("EX1_010")
	worgen.play()
	assert worgen.stealthed
	assert not worgen.can_attack()
	game.end_turn(); game.end_turn()
	game.end_turn()

	archer = game.current_player.give("CS2_189")
	assert len(archer.targets) == 2  # Only the heroes
	assert len(game.current_player.hero.power.targets) == 2
	game.end_turn()

	worgen.attack(game.current_player.opponent.hero)
	assert not worgen.stealthed
	assert not worgen.can_attack()
	windfury = game.current_player.give("CS2_039")
	windfury.play(target=worgen)
	assert worgen.windfury
	assert worgen.num_attacks == 1
	assert worgen.can_attack()
	worgen.attack(game.current_player.opponent.hero)
	assert not worgen.can_attack()
	game.end_turn()

	assert len(archer.targets) == 3


def test_tags():
	game = prepare_game()
	alakir = game.current_player.give("NEW1_010")
	alakir.play()
	assert alakir.tags[GameTag.CHARGE]
	assert alakir.charge
	assert alakir.tags[GameTag.DIVINE_SHIELD]
	assert alakir.divine_shield
	assert alakir.tags[GameTag.TAUNT]
	assert alakir.taunt
	assert alakir.tags[GameTag.WINDFURY]
	assert alakir.windfury


def test_taunt():
	game = prepare_game()
	goldshire1 = game.player1.give(GOLDSHIRE_FOOTMAN)
	wisp1 = game.player1.summon(WISP)
	goldshire2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	wisp2 = game.player2.summon(WISP)
	game.end_turn(); game.end_turn()

	assert wisp1.can_attack()
	assert wisp1.targets == [wisp2, game.player2.hero]
	game.end_turn()

	goldshire2.play()
	game.end_turn()

	assert wisp1.targets == [goldshire2]
	goldshire1.play()
	game.end_turn()

	assert wisp2.targets == [goldshire1]


def test_card_draw():
	game = prepare_game()
	# pass turn 1
	game.end_turn(); game.end_turn()

	assert game.current_player.cards_drawn_this_turn == 1
	assert len(game.current_player.hand) == 5
	novice = game.current_player.give("EX1_015")
	assert len(game.current_player.hand) == 6
	# novice should draw 1 card
	novice.play()
	# hand should be 1 card played, 1 card drawn; same size
	assert len(game.current_player.hand) == 6
	assert game.current_player.cards_drawn_this_turn == 2
	game.end_turn()

	# succubus should discard 1 card
	card = game.current_player.give("EX1_306")
	handlength = len(game.current_player.hand)
	card.play()
	assert len(game.current_player.hand) == handlength - 2


def test_cant_draw():
	game = prepare_game()
	game.player1.discard_hand()
	game.player1.cant_draw = True
	game.end_turn(); game.end_turn()

	assert len(game.player1.hand) == 0
	game.end_turn(); game.end_turn()

	assert len(game.player1.hand) == 0
	game.player1.cant_draw = False
	game.end_turn(); game.end_turn()

	assert len(game.player1.hand) == 1


def test_deadly_poison():
	game = prepare_game(ROGUE, ROGUE)
	poison = game.current_player.give("CS2_074")
	assert not poison.is_playable()
	game.current_player.hero.power.use()
	assert game.current_player.weapon.atk == 1
	assert game.current_player.hero.atk == 1
	assert poison.is_playable()
	poison.play()
	assert game.current_player.weapon.atk == 3
	assert game.current_player.hero.atk == 3


def test_demonfire():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.player1.give("EX1_596").play(target=wisp)
	assert wisp.dead
	imp = game.player1.give("CS2_059")
	imp.play()
	game.player1.give("EX1_596").play(target=imp)
	assert imp.atk == 0 + 2
	assert imp.health == 1 + 2
	assert imp.buffs
	game.end_turn()

	imp2 = game.player2.give("CS2_059")
	imp2.play()
	game.end_turn()

	game.player1.give("EX1_596").play(target=imp2)
	assert imp2.dead


def test_duplicate():
	game = prepare_game()
	game.player1.discard_hand()
	duplicate = game.player1.give("FP1_018")
	duplicate.play()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	game.player2.give(MOONFIRE).play(target=wisp)
	assert len(game.player1.hand) == 2
	assert game.player1.hand[0] == game.player1.hand[1] == WISP


def test_deathwing():
	game = prepare_game()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	deathwing = game.player1.give("NEW1_030")
	deathwing.play()
	assert not game.current_player.hand
	assert len(game.board) == 1
	assert not deathwing.dead


def test_combo():
	game = prepare_game()
	game.end_turn(); game.end_turn()
	game.end_turn()

	game.current_player.hand.filter(id=THE_COIN)[0].play()
	# SI:7 with combo
	assert game.current_player.combo
	game.current_player.give("EX1_134").play(target=game.current_player.hero)
	assert game.current_player.hero.health == 28
	game.end_turn()

	# Without combo should not have a target
	assert not game.current_player.combo
	game.current_player.give("EX1_134").play()


def test_morph():
	game = prepare_game()
	game.end_turn()

	buzzard = game.player2.give("CS2_237")
	buzzard.play()
	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	game.player1.discard_hand()
	game.player2.discard_hand()
	assert not game.player1.hand
	assert not game.player2.hand
	hex = game.player1.give("EX1_246")
	hex.play(target=wisp)
	assert not game.player2.field.contains(WISP)
	assert game.player2.field.contains("hexfrog")
	# Test that buzzard no longer draws on poly/hex (fixed in GVG)
	assert not game.player2.hand
	game.end_turn(); game.end_turn()

	assert len(game.player2.hand) == 1
	polymorph = game.player1.give("CS2_022")
	polymorph.play(target=game.player2.field[-1])
	assert game.player2.field[-1].id == "CS2_tk1"
	assert len(game.current_player.opponent.hand) == 1


def test_power_word_shield():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	wisp.play()
	assert wisp.health == 1
	assert len(game.current_player.hand) == 4

	pwshield = game.current_player.give("CS2_004")
	pwshield.play(target=wisp)
	assert wisp.health == 3
	assert len(game.current_player.hand) == 5

	wisp.silence()
	assert wisp.health == 1


def test_preparation():
	game = prepare_game()
	game.player1.discard_hand()
	prep1 = game.player1.give("EX1_145")
	prep2 = game.player1.give("EX1_145")
	prep3 = game.player1.give("EX1_145")
	pwshield = game.player1.give("CS2_004")
	fireball = game.player1.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	footman2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	assert prep1.cost == prep2.cost == prep3.cost == 0
	assert pwshield.cost == 1
	assert fireball.cost == fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	game.end_turn(); game.end_turn()

	assert game.player1.used_mana == 0
	prep1.play()
	assert game.player1.used_mana == 0
	assert prep2.cost == prep3.cost == 0
	assert pwshield.cost == 0
	assert fireball.cost == 4 - 3
	assert fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	prep2.play()
	assert game.player1.used_mana == 0
	assert prep2.cost == prep3.cost == 0
	assert pwshield.cost == 0
	assert fireball.cost == 4 - 3
	assert fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	fireball.play(target=game.player2.hero)
	assert game.player1.used_mana == 1
	assert pwshield.cost == 1
	assert fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	prep3.play()
	assert pwshield.cost == 0
	assert footman.cost == footman2.cost == 1
	game.end_turn()
	assert pwshield.cost == 1
	assert footman.cost == footman2.cost == 1


def test_kill_command():
	game = prepare_game(HUNTER, HUNTER)
	kc = game.current_player.give("EX1_539")
	kc.play(target=game.current_player.opponent.hero)
	assert game.current_player.opponent.hero.health == 27
	game.end_turn(); game.end_turn()

	# play a timber wolf before this time
	game.current_player.give("DS1_175").play()
	kc = game.current_player.give("EX1_539")
	kc.play(target=game.current_player.opponent.hero)
	assert game.current_player.opponent.hero.health == 22


def test_abusive_sergeant():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	game.player1.give("CS2_188").play(target=wisp)
	assert wisp.atk == 3
	game.end_turn()
	assert wisp.atk == 1


def test_animal_companion():
	game = prepare_game()
	companion = game.player1.give("NEW1_031")
	companion.play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id in ("NEW1_032", "NEW1_033", "NEW1_034")


def test_ancestors_call():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	novice = game.player1.give("EX1_015")
	wisp = game.player2.give(WISP)
	call = game.current_player.give("GVG_029")
	call.play()
	assert novice in game.player1.field
	assert wisp in game.player2.field
	assert not game.player1.hand
	assert not game.player2.hand


def test_ancestral_healing():
	game = prepare_empty_game()
	watcher = game.current_player.give("EX1_045")
	watcher.play()
	assert not watcher.taunt
	assert watcher.health == 5
	watcher.set_current_health(1)
	assert watcher.health == 1
	game.current_player.give("CS2_041").play(watcher)
	assert watcher.taunt
	assert watcher.health == 5


def test_ancestral_spirit():
	game = prepare_game()
	ancestral = game.player1.give("CS2_038")
	wisp = game.player1.give(WISP)
	wisp.play()
	assert not wisp.has_deathrattle
	ancestral.play(target=wisp)
	assert wisp.has_deathrattle
	wisp.destroy()
	assert len(game.board) == 1
	assert game.player1.field[0].id == WISP


def test_ancient_of_lore():
	game = prepare_game()
	game.current_player.discard_hand()

	# damage the hero with 6 moonfires
	for i in range(6):
		game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.current_player.hero.health == 30 - 6

	ancient1 = game.current_player.give("NEW1_008")
	assert len(game.current_player.hand) == 1
	assert ancient1.cost == 7
	# Play to draw 2 cards
	ancient1.play(choose="NEW1_008a")
	assert len(game.current_player.hand) == 2
	assert game.current_player.hero.health == 30 - 6
	game.end_turn(); game.end_turn()

	game.current_player.discard_hand()
	ancient2 = game.current_player.give("NEW1_008")
	# Play to heal hero by 5
	ancient2.play(target=game.current_player.hero, choose="NEW1_008b")
	assert not game.current_player.hand
	assert game.current_player.hero.health == 30 - 6 + 5


def test_ancient_watcher():
	game = prepare_game()
	watcher = game.player1.give("EX1_045")
	watcher.play()
	game.end_turn(); game.end_turn()
	assert not watcher.can_attack()
	game.player1.give(SILENCE).play(target=watcher)
	assert watcher.can_attack()


def test_alarmobot():
	game = prepare_game()
	bot = game.current_player.give("EX1_006")
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	bot.play()
	game.current_player.discard_hand()
	wisp = game.current_player.give(WISP)
	for i in range(9):
		game.current_player.give(MOONFIRE)
	assert len(game.current_player.hand) == 10
	assert bot.zone == Zone.PLAY
	assert wisp.zone == Zone.HAND
	game.end_turn(); game.end_turn()
	assert bot.zone == Zone.HAND
	assert wisp.zone == Zone.PLAY
	assert len(game.current_player.field) == 1
	assert len(game.current_player.hand) == 10

	# bot should not trigger if hand has no minions
	bot.play()
	game.current_player.give(MOONFIRE)
	assert len(game.current_player.hand) == 10
	game.end_turn(); game.end_turn()
	assert len(game.current_player.hand) == 10
	assert bot.zone == Zone.PLAY
	assert len(game.current_player.field) == 2


def test_alexstrasza():
	game = prepare_game()
	alex1 = game.player1.give("EX1_561")
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	alex1.play(target=game.player1.hero)
	assert game.player1.hero.health == 15
	assert game.player1.hero.max_health == 30
	assert game.player2.hero.health == 30
	game.end_turn(); game.end_turn()

	alex2 = game.player1.give("EX1_561")
	assert game.player2.hero.health == 30
	alex2.play(target=game.player2.hero)
	assert game.player2.hero.health == 15


def test_alexstrasza_ragnaros():
	game = prepare_game()
	majordomo = game.player1.give("BRM_027")
	majordomo.play()
	majordomo.destroy()
	assert game.player1.hero.id == "BRM_027h"
	assert game.player1.hero.health == 8
	assert game.player1.hero.max_health == 8
	game.end_turn(); game.end_turn()

	alex = game.player1.give("EX1_561")
	alex.play(target=game.player1.hero)
	assert game.player1.hero.buffs
	assert game.player1.hero.health == 15
	assert game.player1.hero.max_health == 15


def test_avenging_wrath():
	game = prepare_game()
	game.current_player.give("EX1_384").play()
	assert game.current_player.opponent.hero.health == 30 - 8

	game.end_turn()
	# Summon Malygos and test that spellpower only increases dmg by 5
	game.current_player.summon("EX1_563")
	game.current_player.give("EX1_384").play()
	assert game.current_player.opponent.hero.health == 30 - (8 + 5)


def test_doomhammer():
	game = prepare_game()
	doomhammer = game.current_player.give("EX1_567")
	assert not game.current_player.hero.atk
	assert not game.current_player.hero.windfury
	doomhammer.play()
	assert game.current_player.hero.atk == 2
	assert game.current_player.hero.windfury
	assert game.current_player.weapon.durability == 8
	game.current_player.hero.attack(target=game.current_player.opponent.hero)
	assert game.current_player.hero.can_attack()
	game.current_player.hero.attack(target=game.current_player.opponent.hero)
	assert not game.current_player.hero.can_attack()
	assert game.current_player.weapon.durability == 6


def test_dr_boom():
	game = prepare_game()
	boom = game.player1.give("GVG_110")
	assert len(game.player1.field) == 0
	boom.play()
	assert len(game.player1.field) == 3
	assert len(game.player1.field.filter(id="GVG_110t")) == 2
	# Whirlwind the board
	game.player1.give("EX1_400").play()
	assert (30 - 2) >= game.player2.hero.health >= (30 - 8)


def test_raging_worgen():
	game = prepare_game()
	worgen = game.current_player.summon("EX1_412")
	assert worgen.health == 3
	game.current_player.give(MOONFIRE).play(target=worgen)
	assert worgen.health == 2
	assert worgen.atk == 4
	assert worgen.windfury
	game.current_player.give(CIRCLE_OF_HEALING).play()
	assert worgen.atk == 3
	assert not worgen.windfury


def test_amani_berserker():
	game = prepare_game()
	amani1 = game.player1.give("EX1_393")
	amani1.play()
	game.end_turn()

	amani2 = game.player2.give("EX1_393")
	amani2.play()
	game.end_turn()

	assert amani1.atk == amani2.atk == 2
	amani1.attack(amani2)
	# check both minions are still alive, that the enrage didn't trigger too early
	assert amani1.zone == amani2.zone == Zone.PLAY
	assert amani1 in game.player1.field
	assert amani2 in game.player2.field
	assert amani1.damage == amani2.damage == 2
	assert amani1.atk == amani2.atk == 2 + 3
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert amani1.atk == amani2.atk == 2
	assert amani1.health == amani2.health == 3
	game.player1.give(MOONFIRE).play(target=amani1)
	assert amani1.atk == 2 + 3


def test_secretkeeper():
	game = prepare_game()
	secretkeeper = game.player1.give("EX1_080")
	secretkeeper.play()
	assert secretkeeper.atk == 1
	assert secretkeeper.health == 2
	icebarrier = game.current_player.give("EX1_289")
	icebarrier.play()
	assert secretkeeper.atk == 2
	assert secretkeeper.health == 3
	game.current_player.give(THE_COIN).play()
	game.current_player.give(WISP).play()
	assert secretkeeper.atk == 2
	assert secretkeeper.health == 3


def test_siege_engine():
	game = prepare_game(WARRIOR, WARRIOR)
	engine = game.player1.give("GVG_086")
	engine.play()
	assert engine.atk == 5
	game.player1.hero.power.use()
	assert game.player1.hero.armor == 2
	assert engine.atk == 6
	game.end_turn()
	game.player2.hero.power.use()
	assert engine.atk == 6
	game.end_turn()

	# Shield Block
	game.player1.give("EX1_606").play()
	assert game.player1.hero.armor == 7
	assert engine.atk == 7


def test_siltfin_spiritwalker():
	game = prepare_game()
	game.player1.discard_hand()
	siltfin = game.player1.give("GVG_040")
	siltfin.play()
	murloc = game.player1.give("CS2_168")
	murloc.play()
	game.player1.give(MOONFIRE).play(target=murloc)
	assert len(game.player1.hand) == 1


def test_solemn_vigil():
	game = prepare_game()
	game.player1.discard_hand()
	vigil = game.player1.give("BRM_001")
	assert vigil.cost == 5
	game.player1.summon(WISP).destroy()
	assert vigil.cost == 4
	game.player2.summon(WISP).destroy()
	assert vigil.cost == 3
	wisp1 = game.player1.summon(WISP)
	game.player1.give(MOONFIRE).play(target=wisp1)
	assert vigil.cost == 2
	wisp2 = game.player1.summon(WISP)
	game.player1.give(MOONFIRE).play(target=wisp2)
	assert vigil.cost == 1
	game.player1.summon(WISP).destroy()
	assert vigil.cost == 0
	game.player1.summon(WISP).destroy()
	assert vigil.cost == 0
	vigil.play()
	assert len(game.player1.hand) == 2
	assert game.player1.used_mana == 0


def test_southsea_deckhand():
	game = prepare_game(ROGUE, ROGUE)
	deckhand = game.current_player.give("CS2_146")
	deckhand.play()
	assert not deckhand.charge
	# Play rogue hero power (gives a weapon)
	game.current_player.hero.power.use()
	assert deckhand.charge
	game.end_turn(); game.end_turn()

	assert deckhand.charge
	axe = game.current_player.give("CS2_106")
	axe.play()
	assert deckhand.charge
	axe.destroy()
	assert not deckhand.charge

	game.end_turn(); game.end_turn()
	# play charge
	game.current_player.give("CS2_103").play(target=deckhand)
	assert deckhand.charge
	game.end_turn(); game.end_turn()

	assert deckhand.charge
	game.current_player.hero.power.use()
	assert deckhand.charge
	game.current_player.weapon.destroy()
	# No longer have weapon, but still have the charge buff from earlier
	assert deckhand.charge


def test_spiteful_smith():
	game = prepare_game()
	assert not game.current_player.hero.atk
	smith = game.current_player.summon("CS2_221")
	assert smith.health == 6
	assert not game.current_player.hero.atk
	axe = game.current_player.give("CS2_106")
	axe.play()
	assert axe.atk == 3
	assert game.current_player.hero.atk == 3
	assert not game.current_player.opponent.hero.atk
	game.current_player.give(MOONFIRE).play(target=smith)
	assert smith.health == 5
	assert axe.atk == 5
	assert axe.buffs
	assert game.current_player.hero.atk == 5
	assert not game.current_player.opponent.hero.atk
	game.current_player.give(CIRCLE_OF_HEALING).play()
	assert axe.atk == 3
	assert game.current_player.hero.atk == 3
	game.current_player.give(MOONFIRE).play(target=smith)
	assert smith.health == 5
	assert axe.atk == 5
	assert game.current_player.hero.atk == 5


def test_sword_of_justice():
	game = prepare_game(PALADIN, PALADIN)
	sword = game.current_player.give("EX1_366")
	sword.play()
	assert sword.durability == 5
	wisp = game.current_player.give(WISP)
	wisp.play()
	assert wisp.atk == 2
	assert wisp.health == 2
	assert wisp.buffs
	assert sword.durability == 4
	game.end_turn()

	game.current_player.give(WISP).play()
	assert sword.durability == 4
	game.end_turn()

	game.current_player.hero.power.use()
	assert sword.durability == 3

	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	assert not game.current_player.weapon
	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	assert wisp2.health == 1
	assert wisp2.atk == 1
	assert not wisp2.buffs


def test_emperor_thaurissan():
	game = prepare_game()
	thaurissan = game.player1.give("BRM_028")
	fireball = game.player1.give("CS2_029")
	wisp = game.player1.give(WISP)
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	deathwing = game.player1.give("NEW1_030")
	thaurissan.play()
	assert fireball.cost == 4
	assert wisp.cost == 0
	assert footman.cost == 1
	assert deathwing.cost == 10
	game.end_turn()

	assert fireball.cost == 4 - 1
	assert wisp.cost == 0
	assert footman.cost == 1 - 1
	assert deathwing.cost == 10 - 1
	game.end_turn()

	assert fireball.cost == 4 - 1
	assert wisp.cost == 0
	assert footman.cost == 1 - 1
	assert deathwing.cost == 10 - 1
	game.end_turn()

	assert fireball.cost == 4 - 2
	assert wisp.cost == 0
	assert footman.cost == 0
	assert deathwing.cost == 10 - 2
	game.end_turn()

	thaurissan.destroy()
	game.end_turn()

	assert fireball.cost == 4 - 2
	assert wisp.cost == 0
	assert footman.cost == 0
	assert deathwing.cost == 10 - 2
	game.end_turn()

	assert fireball.cost == 4 - 2
	assert wisp.cost == 0
	assert footman.cost == 0
	assert deathwing.cost == 10 - 2


def test_ethereal_arcanist():
	game = prepare_game()
	arcanist = game.player1.give("EX1_274")
	arcanist.play()
	assert arcanist.atk == arcanist.health == 3
	game.end_turn(); game.end_turn()

	assert arcanist.atk == arcanist.health == 3
	icebarrier = game.player1.give("EX1_289")
	icebarrier.play()
	assert arcanist.atk == arcanist.health == 3
	game.end_turn()

	assert arcanist.atk == arcanist.health == 3 + 2
	game.end_turn()

	assert arcanist.atk == arcanist.health == 3 + 2
	icebarrier.destroy()
	game.end_turn()

	assert arcanist.atk == arcanist.health == 3 + 2


def test_healing_totem():
	game = prepare_game()
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	footman.play()
	game.player1.give(MOONFIRE).play(target=footman)
	healtotem = game.player1.give("NEW1_009")
	healtotem.play()
	assert footman.health == 1
	game.end_turn()

	assert footman.health == 2
	game.end_turn()

	assert footman.health == 2


def test_crazed_alchemist():
	game = prepare_game()
	alchemist = game.current_player.give("EX1_059")
	warden = game.current_player.summon("EX1_396")
	assert warden.atk == 1
	assert not warden.damage
	assert warden.max_health == 7
	assert warden.health == 7
	alchemist.play(target=warden)
	assert warden.atk == 7
	assert warden.health == 1


def test_crazed_alchemist_damage_silence():
	# Test for bug #9
	game = prepare_game()
	snapjaw = game.player1.give("CS2_119")
	snapjaw.play()
	assert snapjaw.atk == 2
	assert snapjaw.health == 7
	game.player1.give("EX1_059").play(target=snapjaw)
	assert snapjaw.atk == 7
	assert snapjaw.health == 2
	game.player1.give(MOONFIRE).play(target=snapjaw)
	assert snapjaw.atk == 7
	assert snapjaw.health == 1
	game.player1.give(SILENCE).play(target=snapjaw)
	assert snapjaw.atk == 2
	assert snapjaw.health == 6


def test_reversing_switch():
	game = prepare_game()
	switch = game.player1.give("PART_006")
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	game.end_turn(); game.end_turn()

	switch.play(goldshire)
	assert goldshire.atk == 2


def test_commanding_shout():
	game = prepare_game()
	shout = game.current_player.give("NEW1_036")
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	bender = game.current_player.give(SPELLBENDERT)
	bender.play()
	giant = game.current_player.opponent.summon("EX1_620")
	assert wisp1.health == 1
	assert bender.health == 3
	assert not wisp1.min_health
	assert not bender.min_health
	shout.play()
	assert wisp1.min_health == 1
	assert bender.min_health == 1
	wisp1.attack(target=giant)
	assert giant.health == 7
	assert wisp1.health == 1
	assert not wisp1.damage
	assert wisp1.zone == Zone.PLAY
	game.current_player.give(MOONFIRE).play(target=bender)
	assert bender.health == 2
	assert bender.damage == 1
	bender.attack(target=giant)
	assert bender.health == 1
	assert bender.damage == 2
	assert bender.zone == Zone.PLAY

	# TODO test that minions played afterwards still get commanding shout buff


def test_conceal():
	game = prepare_game()
	conceal = game.current_player.give("EX1_128")
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	conceal.play()
	assert wisp1.stealthed
	assert wisp2.stealthed
	game.end_turn()
	assert wisp1.stealthed
	assert wisp2.stealthed
	game.end_turn()
	assert not wisp1.stealthed
	assert not wisp2.stealthed


def test_counterspell():
	game = prepare_game()
	counterspell = game.player1.give("EX1_287")
	counterspell.play()
	game.end_turn()

	game.player2.give(WISP).play()
	assert counterspell in game.player1.secrets
	bolt = game.player2.give("EX1_238")
	bolt.play(target=game.player1.hero)
	assert not game.player1.secrets
	assert game.player2.used_mana == 1
	assert game.player2.overloaded == 0
	assert game.player1.hero.health == 30


def test_cruel_taskmaster():
	game = prepare_game()
	taskmaster1 = game.current_player.give("EX1_603")
	taskmaster2 = game.current_player.give("EX1_603")
	game.end_turn(); game.end_turn()

	wisp = game.current_player.give(WISP)
	wisp.play()
	taskmaster1.play(target=wisp)
	assert wisp.dead
	game.end_turn(); game.end_turn()

	assert taskmaster1.health == 2
	assert taskmaster1.atk == 2
	taskmaster2.play(target=taskmaster1)
	assert taskmaster1.health == 1
	assert taskmaster1.atk == 4


def test_demolisher():
	game = prepare_game()
	demolisher = game.current_player.give("EX1_102")
	demolisher.play()
	assert game.current_player.opponent.hero.health == 30
	game.end_turn()
	assert game.current_player.opponent.hero.health == 30
	game.end_turn()
	assert game.current_player.opponent.hero.health == 28


def test_dire_wolf_alpha():
	game = prepare_game()
	direwolf1 = game.player2.summon("EX1_162")
	assert direwolf1.atk == 2
	direwolf2 = game.player2.summon("EX1_162")
	assert direwolf1.atk == 3
	assert direwolf2.atk == 3
	frostwolf = game.current_player.summon("CS2_121")
	game.end_turn(); game.end_turn()
	frostwolf.attack(direwolf2)


def test_dragonkin_sorcerer():
	game = prepare_game()
	dragonkin = game.player1.give("BRM_020")
	dragonkin.play()
	assert dragonkin.health == 5
	pwshield = game.player1.give("CS2_004")
	pwshield.play(target=dragonkin)
	assert dragonkin.health == 5 + 2 + 1
	assert dragonkin.max_health == 5 + 2 + 1
	game.player1.give(MOONFIRE).play(target=dragonkin)
	assert dragonkin.health == 5 + 2 + 1 + 1 - 1
	assert dragonkin.max_health == 5 + 2 + 1 + 1


def test_dread_infernal():
	game = prepare_game()
	infernal = game.current_player.give("CS2_064")
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	game.end_turn()

	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	game.end_turn()

	assert len(game.board) == 6
	infernal.play()
	assert len(game.board) == 1
	assert game.current_player.hero.health == 29
	assert game.current_player.opponent.hero.health == 29
	assert infernal.health == 6


def test_dread_corsair():
	game = prepare_game()
	corsair = game.player1.give("NEW1_022")
	assert corsair.cost == 4
	axe = game.player1.give("CS2_106")
	axe.play()
	assert corsair.cost == 4 - 3
	axe.destroy()
	assert corsair.cost == 4


def test_druid_of_the_flame():
	game = prepare_game()
	flame1 = game.player1.give("BRM_010")
	flame1.play(choose="BRM_010a")
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "BRM_010t"
	assert game.player1.field[0].atk == 5
	assert game.player1.field[0].health == 2

	flame2 = game.player1.give("BRM_010")
	flame2.play(choose="BRM_010b")
	assert len(game.player1.field) == 2
	assert game.player1.field[1].id == "BRM_010t2"
	assert game.player1.field[1].atk == 2
	assert game.player1.field[1].health == 5


def test_druid_of_the_fang():
	game = prepare_game()
	fang = game.current_player.give("GVG_080")
	fang.play()
	assert not fang.powered_up
	druid = game.current_player.field[0]
	assert druid.id == "GVG_080"
	assert druid.atk == 4
	assert druid.health == 4

	game.end_turn(); game.end_turn()
	fang2 = game.current_player.give("GVG_080")
	assert not fang2.powered_up
	webspinner = game.current_player.give("FP1_011")
	webspinner.play()
	assert fang2.powered_up
	fang2.play()
	druid2 = game.current_player.field[-1]
	assert druid2.id == "GVG_080t"
	assert druid2.atk == 7
	assert druid2.health == 7
	assert druid2.race == Race.BEAST


def test_imp_gang_boss():
	game = prepare_game()
	igb = game.player1.give("BRM_006")
	igb.play()
	game.player1.give(MOONFIRE).play(target=igb)
	assert len(game.player1.field) == 2
	assert game.player1.field[1].id == "BRM_006t"

	igb2 = game.player1.give("BRM_006")
	igb2.play()
	game.player1.give(MOONFIRE).play(target=igb2)
	assert len(game.player1.field) == 4


def test_imp_master():
	game = prepare_game()
	impmaster = game.current_player.give("EX1_597")
	impmaster.play()
	assert impmaster.health == 5
	assert len(impmaster.controller.field) == 1
	game.end_turn()

	assert impmaster.health == 4
	assert len(impmaster.controller.field) == 2
	assert impmaster.controller.field.contains("EX1_598")


def test_auras():
	game = prepare_game()
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	assert wisp1.atk == 1
	game.end_turn()

	webspinner = game.current_player.give("FP1_011")
	webspinner.play()
	raidleader = game.current_player.give("CS2_122")
	raidleader.play()
	assert raidleader.aura
	assert raidleader.atk == 2
	assert wisp1.atk == 1
	assert webspinner.atk == 2
	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	assert webspinner.atk == 2

	# Test the timber wolf (beast-only) too
	timberwolf = game.current_player.give("DS1_175")
	timberwolf.play()
	assert timberwolf.atk == 1 + 1
	assert raidleader.atk == 2
	assert len(webspinner.buffs) == 2
	assert webspinner.atk == 1 + 1 + 1
	assert wisp2.atk == 1 + 1

	timberwolf2 = game.current_player.give("DS1_175")
	timberwolf2.play()
	assert timberwolf.atk == 3
	assert timberwolf2.atk == 3
	game.current_player.give(MOONFIRE).play(target=timberwolf)
	timberwolf2.atk == 2
	game.current_player.give(MOONFIRE).play(target=timberwolf2)


def test_bounce():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	wisp.play()
	assert game.current_player.field == [wisp]
	brewmaster = game.current_player.give("EX1_049")
	brewmaster.play(target=wisp)
	assert game.current_player.field == [brewmaster]
	assert wisp in game.current_player.hand
	assert wisp.zone == Zone.HAND
	wisp.play()

	# test for damage reset on bounce
	brewmaster2 = game.current_player.give("EX1_049")
	moonfire = game.current_player.give(MOONFIRE)
	moonfire.play(target=brewmaster)
	assert brewmaster.health == 1
	brewmaster2.play(target=brewmaster)
	assert brewmaster.health == 2
	assert brewmaster2.health == 2

	game.end_turn()
	# fill the hand with some bananas
	game.current_player.give("EX1_014t")
	game.current_player.give("EX1_014t")
	game.end_turn()
	vanish = game.current_player.give("NEW1_004")
	vanish.play()
	assert brewmaster not in game.current_player.opponent.hand


def test_bouncing_blade():
	game = prepare_game()
	acolyte = game.player1.give("EX1_007")
	acolyte.play()
	game.player1.discard_hand()
	blade = game.player1.give("GVG_050")
	blade.play()
	assert acolyte.dead
	assert len(game.player1.hand) == 3


def test_bouncing_blade_commanding_shout():
	game = prepare_game()
	acolyte = game.player1.give("EX1_007")
	acolyte.play()
	shout = game.current_player.give("NEW1_036")
	shout.play()
	game.player1.discard_hand()
	assert acolyte.min_health == 1
	blade = game.player1.give("GVG_050")
	blade.play()
	assert acolyte.health == 1
	assert acolyte.zone == Zone.PLAY
	assert len(game.player1.hand) == 2


def test_deaths_bite():
	game = prepare_game()
	deathsbite = game.player1.give("FP1_021")
	deathsbite.play()
	assert game.player1.weapon is deathsbite
	game.player1.hero.attack(game.player2.hero)
	assert game.player2.hero.health == 26
	assert deathsbite.durability == 1
	game.end_turn()

	token = game.player2.give(SPELLBENDERT)
	token.play()
	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	wisp2 = game.player1.give(WISP)
	wisp2.play()
	game.player1.hero.attack(game.player2.hero)
	assert game.player2.hero.health == 22
	assert wisp.dead
	assert wisp2.dead
	assert token.health == 2


def test_weapon_sheathing():
	game = prepare_game()
	axe = game.player1.give("CS2_106")
	game.end_turn(); game.end_turn()

	axe.play()
	assert not axe.exhausted
	assert game.player1.hero.atk == 3
	assert game.player1.hero.can_attack()
	game.player1.hero.attack(target=game.player2.hero)
	assert not axe.exhausted
	assert game.player1.hero.atk == 3
	game.end_turn()

	assert axe.exhausted
	assert game.player1.hero.atk == 0
	assert game.player2.hero.health == 27
	game.player2.give("CS2_106").play()
	game.player2.hero.attack(target=game.player1.hero)
	assert game.player1.hero.health == 27
	assert game.player2.hero.health == 27
	game.end_turn()

	assert not axe.exhausted


def test_arcane_explosion():
	game = prepare_game(MAGE, MAGE)
	# play some wisps
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	game.end_turn()

	arcanex = game.current_player.give("CS2_025")
	assert len(game.current_player.opponent.field) == 3
	arcanex.play()
	assert len(game.current_player.opponent.field) == 0


def test_arcane_missiles():
	game = prepare_game()
	missiles = game.current_player.give("EX1_277")
	missiles.play()
	assert game.current_player.opponent.hero.health == 27


def test_power_overwhelming():
	game = prepare_game()
	power = game.current_player.give("EX1_316")
	wisp = game.current_player.give(WISP)
	wisp.play()
	power.play(target=wisp)
	assert wisp.atk == 5
	assert wisp.health == 5
	game.end_turn()
	assert wisp not in game.board


def test_questing_adventurer():
	game = prepare_game()
	adventurer = game.current_player.give("EX1_044")
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	adventurer.play()
	assert adventurer.atk == 2
	assert adventurer.health == 2
	game.current_player.give(THE_COIN).play()
	assert adventurer.atk == 3
	assert adventurer.health == 3
	game.current_player.give(THE_COIN).play()
	game.current_player.give(THE_COIN).play()
	game.current_player.give(THE_COIN).play()
	assert adventurer.atk == 6
	assert adventurer.health == 6


def test_venture_co():
	game = prepare_game()
	fireball = game.player1.give("CS2_029")
	wisp = game.player1.give(WISP)
	assert wisp.cost == 0
	assert fireball.cost == 4
	ventureco = game.player1.give("CS2_227")
	ventureco.play()
	assert wisp.cost == 0 + 3
	assert fireball.cost == 4
	game.end_turn(); game.end_turn()

	ventureco2 = game.player1.give("CS2_227")
	assert ventureco2.cost == 5 + 3
	ventureco2.play()
	assert wisp.cost == 0 + 3 + 3
	assert fireball.cost == 4
	game.player1.give(SILENCE).play(target=ventureco)
	assert wisp.cost == 0 + 3
	assert fireball.cost == 4


def test_violet_teacher():
	game = prepare_game()
	teacher = game.player1.give("NEW1_026")
	teacher.play()
	assert len(game.player1.field) == 1
	game.player1.give(THE_COIN).play()
	assert len(game.player1.field) == 2
	assert len(game.player1.field.filter(id="NEW1_026t")) == 1
	game.end_turn()
	game.player2.give(THE_COIN).play()
	assert len(game.player1.field) == 2


def test_voidcaller():
	game = prepare_game()
	game.current_player.discard_hand()
	voidcaller = game.current_player.give("FP1_022")
	voidcaller.play()

	# give the player a Doomguard and a couple of wisps
	doomguard = game.current_player.give("EX1_310")
	game.current_player.give(WISP)
	game.current_player.give(WISP)
	game.current_player.give(WISP)
	assert len(game.current_player.hand) == 4

	# sacrificial pact on the voidcaller, should summon the Doomguard w/o discards
	game.current_player.give("NEW1_003").play(target=voidcaller)
	assert voidcaller.dead
	assert doomguard.zone == Zone.PLAY
	assert doomguard.can_attack()
	assert len(game.current_player.hand) == 3


def test_void_terror():
	game = prepare_game()
	terror1 = game.current_player.give("EX1_304")
	terror2 = game.current_player.give("EX1_304")
	terror3 = game.current_player.give("EX1_304")
	power = game.current_player.give("EX1_316")
	terror1.play()
	assert terror1.atk == 3
	assert terror1.health == 3

	terror2.play()
	assert terror1.dead
	assert terror2.atk == 3 + 3
	assert terror2.health == 3 + 3

	power.play(target=terror2)
	assert terror2.health == 3 + 3 + 4
	assert terror2.atk == 3 + 3 + 4
	terror3.play()
	assert terror2.dead
	assert terror3.atk == 3 + 3 + 3 + 4
	assert terror3.health == 3 + 3 + 3 + 4
	game.end_turn(); game.end_turn()
	assert terror3.zone == Zone.PLAY


def test_voljin():
	game = prepare_game()
	voljin = game.player1.give("GVG_014")
	deathwing = game.player1.summon("NEW1_030")
	assert voljin.health == 2
	assert deathwing.health == 12
	voljin.play(target=deathwing)
	assert voljin.health == 12
	assert deathwing.health == 2


def test_voljin_stealth():
	game = prepare_game()
	tiger = game.player1.give("EX1_028")
	tiger.play()
	game.end_turn()

	voljin = game.player2.give("GVG_014")
	assert not voljin.targets
	voljin.play()
	assert not voljin.dead
	assert voljin.health == 2
	assert tiger.health == 5


def test_malorne():
	game = prepare_empty_game()
	assert len(game.player1.deck) == 0
	malorne = game.player1.give("GVG_035")
	malorne.play()
	malorne.destroy()
	assert len(game.player1.deck) == 1
	game.player1.draw()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == "GVG_035"


def test_mana_addict():
	game = prepare_game()
	manaaddict = game.current_player.give("EX1_055")
	manaaddict.play()
	assert manaaddict.atk == 1
	game.end_turn()

	assert manaaddict.atk == 1
	game.current_player.give(THE_COIN).play()
	assert manaaddict.atk == 1
	game.end_turn()

	game.current_player.give(THE_COIN).play()
	assert manaaddict.atk == 3
	game.current_player.give(THE_COIN).play()
	assert manaaddict.atk == 5
	game.end_turn()
	assert manaaddict.atk == 1


def test_mana_wyrm():
	game = prepare_game()
	wyrm = game.player1.give("NEW1_012")
	wyrm.play()
	assert wyrm.atk == 1
	game.player1.give(THE_COIN).play()
	assert wyrm.atk == 2

	game.end_turn()
	assert wyrm.atk == 2
	game.player2.give(THE_COIN).play()
	assert wyrm.atk == 2

	game.end_turn()
	assert wyrm.atk == 2
	game.player1.give(THE_COIN).play()
	assert wyrm.atk == 3


def test_old_murkeye():
	game = prepare_game()
	murkeye = game.player1.give("EX1_062")
	murloc = game.player1.summon("CS2_168")
	murkeye.play()
	assert murkeye.charge
	assert murkeye.can_attack()
	assert murkeye.atk == 2 + 1
	game.player2.summon("CS2_168")
	assert murkeye.atk == 2 + 2
	game.player2.summon("CS2_168")
	assert murkeye.atk == 2 + 3
	murloc.destroy()
	assert murkeye.atk == 2 + 2
	murkeye2 = game.player2.summon("EX1_062")
	assert murkeye.atk == murkeye2.atk == 2 + 3


def test_pint_sized_summoner():
	game = prepare_game()
	goldshire1 = game.current_player.give(GOLDSHIRE_FOOTMAN)
	goldshire2 = game.current_player.give(GOLDSHIRE_FOOTMAN)
	moonfire = game.current_player.give(MOONFIRE)
	frostwolf = game.current_player.give("CS2_121")
	wisp = game.current_player.give(WISP)
	assert goldshire1.cost == 1
	assert goldshire2.cost == 1
	assert frostwolf.cost == 2
	assert wisp.cost == 0

	# summon it directly, minions played still at 0
	summoner = game.current_player.summon("EX1_076")
	assert game.current_player.minions_played_this_turn == 0
	assert goldshire1.cost == 1 - 1
	assert goldshire2.cost == 1 - 1
	assert not moonfire.buffs
	assert moonfire.cost == 0
	assert frostwolf.cost == 2 - 1
	assert wisp.cost == 0

	goldshire1.play()
	assert game.current_player.minions_played_this_turn == 1
	assert goldshire2.cost == 1
	assert frostwolf.cost == 2
	assert wisp.cost == 0
	game.end_turn()

	assert game.current_player.minions_played_this_turn == 0
	assert goldshire1.cost == 1
	assert goldshire2.cost == 1
	assert frostwolf.cost == 2
	assert wisp.cost == 0

	game.end_turn()
	summoner2 = game.current_player.summon("EX1_076")
	assert frostwolf.cost == 2 - 2
	summoner.destroy()
	assert frostwolf.cost == 2 - 1
	summoner2.destroy()
	assert frostwolf.cost == 2


def test_prophet_velen():
	game = prepare_game(PRIEST, PRIEST)

	expected_health = 30
	assert game.player2.hero.health == expected_health
	assert game.player1.healing_double == 0
	assert game.player1.hero_power_double == 0
	assert game.player1.spellpower_double == 0
	velen = game.player1.give("EX1_350")
	velen.play()
	assert game.player1.healing_double == 1
	assert game.player1.hero_power_double == 1
	assert game.player1.spellpower_double == 1

	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 2 * 1
	assert game.player2.hero.health == expected_health

	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 2 * 1
	assert game.player2.hero.health == expected_health

	game.player1.hero.power.use(target=game.player2.hero)
	expected_health += 2 * 2
	assert game.player2.hero.health == expected_health
	game.end_turn(); game.end_turn()

	kobold = game.current_player.give(KOBOLD_GEOMANCER)
	kobold.play()
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 2 * (1 + 1)
	assert game.player2.hero.health == expected_health


def test_mana_wraith():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	goldshire1 = game.player1.give(GOLDSHIRE_FOOTMAN)
	wisp2 = game.player2.give(WISP)
	goldshire2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	fireball1 = game.player1.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	axe1 = game.player1.give("CS2_106")
	axe2 = game.player2.give("CS2_106")
	assert wisp1.cost == wisp2.cost == 0
	assert goldshire1.cost == goldshire2.cost == 1
	assert fireball1.cost == fireball2.cost == 4
	assert axe1.cost == axe2.cost == 2
	assert game.player1.hero.power.cost == game.player2.hero.power.cost == 2

	wraith = game.current_player.give("EX1_616")
	wraith.play()
	assert wisp1.cost == wisp2.cost == 0 + 1
	assert goldshire1.cost == goldshire2.cost == 1 + 1
	assert fireball1.cost == fireball2.cost == 4
	assert axe1.cost == axe2.cost == 2
	assert game.player1.hero.power.cost == game.player2.hero.power.cost == 2

	wraith.destroy()
	assert wisp1.cost == wisp2.cost == 0
	assert goldshire1.cost == goldshire2.cost == 1
	assert fireball1.cost == fireball2.cost == 4
	assert axe1.cost == axe2.cost == 2
	assert game.player1.hero.power.cost == game.player2.hero.power.cost == 2


def test_mechwarper():
	game = prepare_game()
	mechwarper = game.player1.give("GVG_006")
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	harvest = game.player1.give("EX1_556")
	clockwork = game.player1.give("GVG_082")
	clockwork2 = game.player1.give("GVG_082")
	assert harvest.cost == 3
	assert goldshire.cost == 1
	assert clockwork.cost == clockwork2.cost == 1

	mechwarper.play()
	assert harvest.cost == 3 - 1
	assert goldshire.cost == 1
	assert clockwork.cost == clockwork2.cost == 0

	clockwork.play()
	assert clockwork.cost == 1

	game.current_player.give(SILENCE).play(target=mechwarper)
	assert harvest.cost == 3
	assert goldshire.cost == 1
	assert clockwork.cost == clockwork2.cost == 1

	mechwarper.destroy()
	assert harvest.cost == 3
	assert goldshire.cost == 1
	assert clockwork.cost == clockwork2.cost == 1


def test_mekgineer_thermaplugg():
	game = prepare_game()
	mekgineer = game.player1.give("GVG_116")
	mekgineer.play()

	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	game.player1.give(MOONFIRE).play(target=wisp1)
	assert wisp1.dead
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	game.end_turn()

	wisp2 = game.player2.give(WISP)
	wisp2.play()
	game.player2.give(MOONFIRE).play(target=wisp2)
	assert wisp2.dead
	assert len(game.player1.field) == 2
	assert len(game.player1.field.filter(id="EX1_029")) == 1
	assert len(game.player2.field) == 0


def test_metaltooth_leaper():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	wisp.play()
	dummy = game.current_player.give(TARGET_DUMMY)
	dummy.play()
	metaltooth = game.current_player.give("GVG_048")
	metaltooth.play()
	assert metaltooth.atk == 3
	assert metaltooth.health == 3
	assert wisp.atk == 1
	assert dummy.atk == 0 + 2


def test_bestial_wrath():
	game = prepare_game()
	wolf = game.current_player.give("DS1_175")
	wolf.play()
	bestial = game.current_player.give("EX1_549")
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	game.end_turn()

	wisp2 = game.current_player.summon(WISP)
	game.end_turn()

	assert wolf.atk == 1
	assert not wolf.immune
	assert wolf in bestial.targets
	assert wisp1 not in bestial.targets
	assert wisp2 not in bestial.targets
	bestial.play(target=wolf)
	assert wolf.atk == 3
	assert wolf.immune
	wolf.attack(target=wisp2)
	assert wolf.health == 1
	assert wolf.zone == Zone.PLAY
	assert wisp2.dead
	game.end_turn()

	assert wolf.atk == 1
	assert not wolf.immune


def test_betrayal():
	game = prepare_game()
	wisp1 = game.player1.give(WISP).play()
	wisp2 = game.player1.give(WISP).play()
	wisp3 = game.player1.give(WISP).play()
	assert len(game.current_player.field) == 3
	game.end_turn()

	betrayal = game.player2.give("EX1_126")
	betrayal.play(target=wisp2)
	assert len(game.player1.field) == 1
	assert wisp1.dead
	assert not wisp2.dead
	assert wisp3.dead
	game.end_turn()

	bender = game.player1.give(SPELLBENDERT).play()
	game.end_turn()

	game.player2.give("EX1_126").play(target=wisp2)
	assert not wisp2.dead
	assert not bender.dead
	assert bender.health == 2


def test_betrayal_poisonous():
	game = prepare_game()
	watcher1 = game.player1.give("EX1_045").play()
	cobra = game.player1.give("EX1_170").play()
	watcher2 = game.player1.give("EX1_045").play()
	game.end_turn()

	game.player2.give("EX1_126").play(target=cobra)
	assert watcher1.dead
	assert not cobra.dead
	assert watcher2.dead


def test_cold_blood():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	game.end_turn(); game.end_turn()

	cb1 = game.current_player.give("CS2_073")
	cb1.play(target=wisp)
	assert wisp.atk == 1 + 2

	cb2 = game.current_player.give("CS2_073")
	cb2.play(target=wisp)
	assert wisp.atk == 1 + 2 + 4


def test_corruption():
	game = prepare_game()
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	corruption1 = game.player1.give("CS2_063")
	corruption1.play(target=wisp)
	assert wisp.buffs
	assert wisp.buffs[0].controller == game.player1
	game.end_turn()

	assert not wisp.dead
	game.end_turn()

	assert wisp.dead
	game.end_turn()

	# corrupt our own wisp. next turn opponent MCs it.
	wisp2 = game.player2.give(WISP)
	wisp2.play()
	lucifron = game.player2.give("BRMC_85")
	lucifron.play()
	assert not wisp2.dead
	game.end_turn()

	assert not wisp2.dead
	cabal = game.player1.give("EX1_091")
	cabal.play(target=wisp2)
	assert not wisp2.dead
	game.end_turn()

	assert wisp2.dead


def test_harrison_jones():
	game = prepare_game()
	game.end_turn()

	lightsjustice = game.player2.give("CS2_091")
	lightsjustice.play()
	game.end_turn()

	game.player1.discard_hand()
	assert not game.player1.hand
	assert lightsjustice.durability == 4
	jones = game.player1.give("EX1_558")
	jones.play()
	assert len(game.player1.hand) == 4
	assert lightsjustice.dead
	game.end_turn()

	game.player2.discard_hand()
	jones2 = game.player2.give("EX1_558")
	jones2.play()
	assert not game.player2.hand


def test_headcrack():
	game = prepare_game(exclude=("EX1_137", ))
	headcrack1 = game.player1.give("EX1_137")
	assert game.player1.hand.contains("EX1_137")
	headcrack1.play()
	assert not game.player1.hand.contains("EX1_137")
	game.end_turn(); game.end_turn()

	assert not game.player1.hand.contains("EX1_137")
	headcrack2 = game.player1.give("EX1_137")
	game.player1.give(THE_COIN).play()
	headcrack2.play()
	assert not game.player1.hand.contains("EX1_137")
	game.end_turn()
	assert game.player1.hand.contains("EX1_137")
	game.player1.discard_hand()
	game.end_turn(); game.end_turn()
	assert not game.player1.hand.contains("EX1_137")


def test_heroic_strike():
	game = prepare_game()
	strike = game.current_player.give("CS2_105")
	assert game.current_player.hero.atk == 0
	strike.play()
	assert game.current_player.hero.atk == 4
	game.end_turn()
	assert game.current_player.hero.atk == 0
	game.end_turn()
	assert game.current_player.hero.atk == 0

	game.current_player.give("CS2_105").play()
	game.current_player.give("CS2_106").play()
	assert game.current_player.hero.atk == 7


def test_humility():
	game = prepare_game()
	humility = game.current_player.give("EX1_360")
	humility2 = game.current_player.give("EX1_360")
	seargent = game.current_player.give("CS2_188")
	seargent2 = game.current_player.give("CS2_188")
	golem = game.current_player.summon("CS2_186")
	game.end_turn(); game.end_turn()

	assert golem.atk == 7
	humility.play(target=golem)
	assert golem.atk == 1
	seargent.play(target=golem)
	assert golem.atk == 3
	game.end_turn()
	assert golem.atk == 1
	game.end_turn()

	seargent2.play(target=golem)
	assert golem.atk == 3
	humility2.play(target=golem)
	assert golem.atk == 1
	game.end_turn()
	assert golem.atk == 1


def test_hunters_mark():
	game = prepare_game()
	token = game.current_player.give(SPELLBENDERT)
	token.play()
	assert token.health == 3
	game.current_player.give(MOONFIRE).play(target=token)
	assert token.health == 2
	mark = game.current_player.give("CS2_084")
	mark.play(target=token)
	assert token.health == 1
	game.current_player.give(SILENCE).play(target=token)
	assert token.health == 3


def test_kezan_mystic():
	game = prepare_game()
	kezan = game.player1.give("GVG_074")
	snipe = game.player2.give("EX1_609")
	game.end_turn()

	snipe.play()
	assert snipe in game.player2.secrets
	game.end_turn()

	kezan.play()
	assert not kezan.dead
	assert snipe in game.player1.secrets
	game.end_turn(); game.end_turn()

	kezan2 = game.player1.give("GVG_074")
	kezan2.play()
	assert not kezan2.dead
	assert snipe in game.player1.secrets


def test_kel_thuzad():
	game = prepare_game()
	kt = game.player1.summon("FP1_013")
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	game.end_turn()

	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	wisp = game.player2.give(WISP)
	wisp.play()
	game.player2.give(MOONFIRE).play(target=wisp)
	game.end_turn()

	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	assert len(game.player1.field) == 2
	assert len(game.player2.field) == 0
	game.end_turn()

	assert len(game.player1.field) == 2
	assert len(game.player2.field) == 0
	game.player2.give(MOONFIRE).play(target=wisp2)
	assert wisp2.dead
	assert len(game.player1.field) == 1
	game.end_turn()

	assert wisp2.dead
	assert len(game.player1.field) == 2
	assert game.player1.field[1] == WISP
	game.end_turn()

	# ensure the effect is gone when Kel'Thuzad dies
	game.player2.give(MOONFIRE).play(target=game.player1.field[1])
	kt.destroy()
	assert len(game.player1.field) == 0
	game.end_turn()

	assert len(game.player1.field) == 0


def test_king_mukla():
	game = prepare_game()
	mukla = game.player1.give("EX1_014")
	game.player2.discard_hand()
	assert len(game.player2.hand) == 0
	mukla.play()
	assert len(game.player2.hand) == 2
	for i in range(2):
		assert game.player2.hand[i].id == "EX1_014t"
	game.end_turn()
	wisp = game.player2.give(WISP)
	wisp.play()
	assert wisp.health == 1
	assert wisp.atk == 1
	assert game.player2.hand[0].id == "EX1_014t"
	game.player2.hand[0].play(target=wisp)
	assert wisp.health == 2
	assert wisp.atk == 2


def test_knife_juggler():
	game = prepare_game()
	juggler = game.player1.give("NEW1_019")
	juggler.play()
	assert game.player2.hero.health == 30
	game.player1.give(WISP).play()
	assert game.player2.hero.health == 29
	game.player1.give(MOONFIRE).play(target=juggler)
	# kill juggler with archer, shouldnt juggle
	archer = game.current_player.give("CS2_189")
	archer.play(target=juggler)
	assert juggler.dead
	assert game.player2.hero.health == 29


def test_knife_juggler_swipe():
	"""
	Test that a Swipe on Knife Juggler that kills a Haunted Creeper
	does not trigger the Knife Juggler by the time the spiders spawn
	"""
	game = prepare_game()
	creeper = game.player2.summon("FP1_002")
	juggler = game.player2.summon("NEW1_019")
	game.current_player.give(MOONFIRE).play(target=creeper)
	swipe = game.player1.give("CS2_012")
	swipe.play(target=juggler)
	assert juggler.dead
	assert creeper.dead
	assert len(game.player2.field) == 2
	assert game.player1.hero.health == 30


def test_mark_of_nature():
	game = prepare_game()
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	assert wisp1.atk == 1
	assert wisp1.health == 1
	assert not wisp1.taunt

	mark1 = game.current_player.give("EX1_155")
	mark1.play(target=wisp1, choose="EX1_155a")
	assert wisp1.atk == 1 + 4
	assert wisp1.health == 1
	assert not wisp1.taunt

	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	assert wisp2.atk == 1
	assert wisp2.health == 1
	assert not wisp2.taunt

	mark2 = game.current_player.give("EX1_155")
	mark2.play(target=wisp2, choose="EX1_155b")
	assert wisp2.atk == 1
	assert wisp2.health == 1 + 4
	assert wisp2.taunt


def test_mindgames():
	game = prepare_game(PRIEST, PRIEST)
	mindgames = game.player1.give("EX1_345")
	mindgames.play()
	assert len(game.player1.field) == 1
	assert game.player2.deck.contains(game.player1.field[0])


def test_mind_vision():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()

	# play mind vision, should give nothing
	assert len(game.current_player.hand) == 0
	game.current_player.give("CS2_003").play()
	assert len(game.current_player.hand) == 0

	# opponent draws a card, mind vision should get that one card
	card = game.current_player.opponent.draw()
	game.current_player.give("CS2_003").play()
	assert game.current_player.hand[-1] == card


def test_mirror_image():
	game = prepare_game()
	mirror = game.current_player.give("CS2_027")
	mirror.play()
	assert len(game.current_player.field) == 2
	assert game.current_player.field[0].id == "CS2_mirror"
	assert game.current_player.field[1].id == "CS2_mirror"


def test_mortal_strike():
	game = prepare_game()
	game.player1.discard_hand()
	expected_health = 30
	for i in range(5):
		ms = game.player1.give("EX1_408")
		assert not ms.powered_up
		ms.play(target=game.player1.hero)
		expected_health -= 4
		assert game.player1.hero.health == expected_health
		if i % 2:
			game.end_turn(); game.end_turn()

	ms = game.player1.give("EX1_408")
	# assert ms.powered_up  # TODO
	ms.play(target=game.player1.hero)
	expected_health -= 6
	assert game.player1.hero.health == expected_health


def test_mortal_coil():
	game = prepare_game()
	dummy = game.player1.summon(TARGET_DUMMY)
	assert dummy.health == 2
	game.end_turn()
	game.player2.discard_hand()
	assert len(game.player2.hand) == 0
	coil1 = game.player2.give("EX1_302")
	assert len(game.player2.hand) == 1
	coil1.play(target=dummy)
	assert len(game.player2.hand) == 0
	coil2 = game.player2.give("EX1_302")
	coil2.play(target=dummy)
	assert len(game.player2.hand) == 1


def test_archmage_antonidas():
	game = prepare_game()
	antonidas = game.player1.give("EX1_559")
	antonidas.play()
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == "CS2_029"
	game.player1.give(THE_COIN).play()
	assert len(game.player1.hand) == 2
	assert game.player1.hand[1].id == "CS2_029"


def test_armorsmith():
	game = prepare_game()
	armorsmith1 = game.player1.give("EX1_402")
	armorsmith1.play()
	game.end_turn()

	armorsmith2 = game.player2.give("EX1_402")
	armorsmith2.play()
	game.end_turn()

	assert game.player1.hero.armor == game.player2.hero.armor == 0
	armorsmith1.attack(target=armorsmith2)
	assert game.player1.hero.armor == game.player2.hero.armor == 1
	game.end_turn()

	game.player2.give("EX1_402").play()
	game.player2.give(WISP).play()

	# Whirlwind
	# 1 armor on each hero, 2 smiths in play for current player, 1 for opponent
	game.player2.give("EX1_400").play()
	assert game.player2.hero.armor == 1 + (2 * 3)
	assert game.current_player.hero.health == 30
	assert game.player1.hero.armor == 1 + 1


def test_auchenai_soulpriest():
	game = prepare_game(PRIEST, PRIEST)
	auchenai = game.player1.give("EX1_591")
	auchenai.play()
	game.player1.hero.power.use(target=game.player2.hero)
	assert game.player2.hero.health == 28
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert auchenai.health == 1


def test_blessing_of_wisdom():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	blessing = game.player1.give("EX1_363")
	blessing.play(target=wisp)
	game.player1.discard_hand()
	wisp.attack(target=game.current_player.opponent.hero)
	assert len(game.current_player.hand) == 1
	game.end_turn()

	# Shadow Madness should draw for the original caster
	game.player2.discard_hand()
	shadowmadness = game.player2.give("EX1_334")
	shadowmadness.play(target=wisp)
	assert len(game.player1.hand) == 1
	wisp.attack(target=game.player1.hero)
	assert len(game.player1.hand) == 2
	assert not game.player2.hand


def test_blizzard():
	game = prepare_game()
	for i in range(6):
		game.player1.give(SPELLBENDERT).play()
	game.end_turn()

	blizzard = game.player2.give("CS2_028")
	blizzard.play()
	for spellbendert in game.current_player.opponent.field:
		assert spellbendert.health == 1
		assert spellbendert.frozen


def test_brawl():
	game = prepare_game()
	brawl = game.player1.give("EX1_407")
	game.player1.give(GOLDSHIRE_FOOTMAN).play()
	game.player1.give(WISP).play()
	game.end_turn()

	game.player2.give(GOLDSHIRE_FOOTMAN).play()
	game.player2.give(WISP).play()
	game.end_turn()

	assert len(game.board) == 4
	brawl.play()
	assert len(game.board) == 1
	assert game.board[0].id in (WISP, GOLDSHIRE_FOOTMAN)


def test_dark_iron_bouncer_brawl():
	game = prepare_game()
	bouncer = game.player1.give("BRMA01_3")
	bouncer.play()
	for i in range(6):
		game.player1.give(WISP).play()
	game.end_turn()

	for i in range(7):
		game.player2.give(WISP).play()
	brawl = game.player2.give("EX1_407")
	brawl.play()
	assert len(game.board) == 1
	assert not bouncer.dead


def test_bane_of_doom():
	game = prepare_game()
	doom = game.current_player.give("EX1_320")
	token = game.player2.summon(SPELLBENDERT)
	assert not game.player1.field
	doom.play(target=token)
	assert not game.player1.field
	game.end_turn(); game.end_turn()

	doom2 = game.current_player.give("EX1_320")
	doom2.play(target=token)
	assert len(game.player1.field) == 1
	assert game.player1.field[0].race == Race.DEMON
	assert game.player1.field[0].data.collectible


def test_baron_geddon():
	game = prepare_game()

	geddon1 = game.player1.give("EX1_249")
	wisp = game.player1.give(WISP)
	geddon1.play()
	wisp.play()
	assert geddon1.health == 5
	assert not wisp.dead
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	game.end_turn()
	assert geddon1.health == 5
	assert wisp.dead
	assert game.player1.hero.health == 28
	assert game.player2.hero.health == 28

	geddon2 = game.player2.give("EX1_249")
	geddon2.play()
	assert geddon1.health == 5
	assert geddon2.health == 5
	game.end_turn()
	assert geddon1.health == 3
	assert geddon2.health == 5


def test_baron_rivendare():
	game = prepare_game()
	gnome = game.current_player.give("EX1_029")
	gnome.play()
	assert not game.current_player.extra_deathrattles
	rivendare = game.current_player.summon("FP1_031")
	assert game.current_player.extra_deathrattles
	game.current_player.give(MOONFIRE).play(target=gnome)
	assert game.current_player.opponent.hero.health == 26
	wisp = game.current_player.give(WISP)
	wisp.play()
	assert not wisp.has_deathrattle
	sotf = game.current_player.give("EX1_158")
	sotf.play()
	assert len(game.current_player.field) == 2
	game.current_player.give(MOONFIRE).play(target=wisp)
	assert wisp.dead
	assert rivendare.zone == Zone.PLAY
	assert len(game.current_player.field) == 3  # Rivendare and two treants
	rivendare.destroy()
	assert len(game.current_player.field) == 3  # Only one treant spawns


def test_blingtron_3000():
	game = prepare_game()
	blingtron = game.player1.give("GVG_119")
	blingtron.play()
	assert game.player1.weapon
	assert game.player2.weapon


def test_blood_imp():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	imp = game.current_player.give("CS2_059")
	imp.play()
	assert imp.health == 1
	game.end_turn(); game.end_turn()

	assert imp.health == 1
	wisp.play()
	assert wisp.health == 1
	game.end_turn()

	assert imp.health == 1
	assert wisp.atk == 1
	assert wisp.health == 2


def test_blood_knight():
	game = prepare_game()
	game.end_turn()

	squire = game.current_player.give("EX1_008")
	squire.play()
	assert squire.divine_shield
	game.end_turn()

	bloodknight1 = game.current_player.give("EX1_590")
	bloodknight1.play()
	assert not squire.divine_shield
	assert bloodknight1.atk == 6
	assert bloodknight1.health == 6
	game.end_turn()

	game.current_player.give("EX1_008").play()
	game.current_player.give("EX1_008").play()
	# Play an argent protector on the squire
	game.current_player.give("EX1_362").play(target=squire)
	assert squire.divine_shield
	game.end_turn()

	bloodknight2 = game.current_player.give("EX1_590")
	bloodknight2.play()
	assert not squire.divine_shield
	assert bloodknight2.atk == 12
	assert bloodknight2.health == 12
	game.end_turn(); game.end_turn()

	bloodknight3 = game.current_player.give("EX1_590")
	bloodknight3.play()
	assert bloodknight3.atk == 3
	assert bloodknight3.health == 3


def test_bolvar_fordragon():
	game = prepare_game()
	bolvar = game.current_player.give("GVG_063")
	assert bolvar.atk == 1
	wisp = game.current_player.give(WISP)
	wisp.play()
	game.current_player.give(MOONFIRE).play(target=wisp)
	assert bolvar.atk == 2
	assert bolvar.buffs
	wisp = game.current_player.give(WISP)
	wisp.play()
	game.current_player.give(MOONFIRE).play(target=wisp)
	assert bolvar.atk == 3
	game.end_turn(); game.end_turn()

	assert bolvar.atk == 3
	assert bolvar.buffs
	bolvar.play()
	assert bolvar.atk == 3
	assert bolvar.buffs
	# game.current_player.give(DREAM).play(target=bolvar)
	# assert bolvar.atk == 1
	# assert not bolvar.buffs


def test_bomb_lobber():
	game = prepare_game()
	lobber1 = game.current_player.give("GVG_099")
	lobber2 = game.current_player.give("GVG_099")
	game.end_turn()

	wisp = game.current_player.give(WISP)
	warden = game.current_player.give("EX1_396")
	game.end_turn()

	lobber1.play()
	assert game.current_player.opponent.hero.health == 30
	game.end_turn()

	wisp.play()
	warden.play()
	game.end_turn()

	lobber2.play()
	assert wisp.dead or warden.health == 7 - 4


def test_defias():
	game = prepare_game()
	defias1 = game.current_player.give("EX1_131")
	defias1.play()
	assert len(game.current_player.field) == 1
	game.end_turn()

	# Coin-defias
	game.current_player.hand.filter(id=THE_COIN)[0].play()
	defias2 = game.current_player.give("EX1_131")
	defias2.play()
	assert len(game.current_player.field) == 2


def test_doomsayer():
	game = prepare_game()
	# play some wisps
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()

	game.end_turn()
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()

	assert len(game.board) == 4
	doomsayer = game.current_player.give("NEW1_021")
	doomsayer.play()
	assert len(game.board) == 5
	game.end_turn()

	assert len(game.board) == 5
	game.end_turn()

	assert len(game.board) == 0


def test_gadgetzan_auctioneer():
	game = prepare_game()
	game.player1.discard_hand()
	auctioneer = game.player1.give("EX1_095")
	auctioneer.play()
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert len(game.player1.hand) == 1
	game.player1.give(WISP).play()
	assert len(game.player1.hand) == 1


def test_gallywix():
	game = prepare_game()
	gallywix = game.player1.give("GVG_028")
	gallywix.play()
	game.end_turn()

	game.player1.discard_hand()
	game.player2.discard_hand()
	game.player2.give("CS2_029").play(target=game.player1.hero)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == "CS2_029"
	assert len(game.player2.hand) == 1
	assert game.player2.hand[0].id == "GVG_028t"
	game.player2.hand[0].play()
	assert game.player2.temp_mana == 1
	assert len(game.player2.hand) == 0


def test_gang_up():
	game = prepare_empty_game()
	wisp = game.player1.summon(WISP)
	assert len(game.player1.deck) == 0
	assert len(game.player2.deck) == 0
	game.player1.give("BRM_007").play(target=wisp)
	assert len(game.player1.deck) == 3
	assert len(game.player2.deck) == 0
	game.end_turn()

	game.player2.give("BRM_007").play(target=wisp)
	assert len(game.player1.deck) == 3
	assert len(game.player2.deck) == 3
	assert len(game.player1.deck.filter(id=WISP)) == 3
	assert len(game.player2.deck.filter(id=WISP)) == 3


def test_gazlowe():
	game = prepare_empty_game()
	game.player1.discard_hand()
	game.player1.give("GVG_117").play()
	assert len(game.player1.hand) == 0
	smite = game.player1.give("CS1_130")
	assert smite.cost == 1
	smite.play(target=game.player2.hero)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.MECHANICAL


def test_goblin_blastmage():
	game = prepare_game()
	blastmage1 = game.current_player.give("GVG_004")
	assert not blastmage1.powered_up
	assert game.current_player.hero.health == 30
	blastmage1.play()
	assert game.current_player.hero.health == 30
	game.end_turn(); game.end_turn()

	blastmage2 = game.current_player.give("GVG_004")
	assert not blastmage2.powered_up
	clockwork = game.current_player.give("GVG_082")
	clockwork.play()
	assert clockwork.race == Race.MECHANICAL
	assert blastmage2.powered_up
	blastmage2.play()
	assert game.current_player.opponent.hero.health == 30 - 4
	game.end_turn(); game.end_turn()


def test_gahzrilla():
	game = prepare_game()
	gahz = game.current_player.summon("GVG_049")
	assert gahz.atk == 6
	game.current_player.give(MOONFIRE).play(target=gahz)
	assert gahz.atk == 6 * 2
	timberwolf = game.current_player.give("DS1_175")
	timberwolf.play()
	assert gahz.atk == (6 * 2) + 1
	# TODO: Buffs are always taken into account at the end
	# game.current_player.give(MOONFIRE).play(target=gahz)
	# assert gahz.atk == (6*2*2) + 1


def test_grimscale_oracle():
	game = prepare_game()
	grimscale = game.player1.give("EX1_508")
	murloc1 = game.player1.summon("CS2_168")
	murloc2 = game.player2.summon("CS2_168")
	assert murloc1.atk == 2
	assert murloc2.atk == 2
	grimscale.play()
	assert murloc1.atk == 2 + 1
	assert murloc2.atk == 2 + 1
	assert grimscale.atk == 1

	game.player1.give(TIME_REWINDER).play(target=grimscale)
	assert murloc1.atk == 2
	assert murloc2.atk == 2


def test_gruul():
	game = prepare_game()
	gruul = game.current_player.give("NEW1_038")
	gruul.play()
	assert gruul.atk == 7
	assert gruul.health == 7
	assert not gruul.buffs
	game.end_turn()

	assert gruul.buffs
	assert gruul.atk == 8
	assert gruul.health == 8
	game.end_turn()

	assert gruul.atk == 9
	assert gruul.health == 9


def test_hobgoblin():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	assert wisp.health == 1
	hobgoblin = game.current_player.give("GVG_104")
	hobgoblin.play()

	wolf1 = game.current_player.give("DS1_175")
	wolf1.play()
	assert wolf1.atk == 3
	assert wolf1.health == 3

	wolf2 = game.current_player.give("DS1_175")
	wolf2.play()
	assert wolf1.atk == 4
	assert wolf1.health == 3
	assert wolf2.atk == 4
	assert wolf2.health == 3

	loothoarder = game.current_player.give("EX1_096")
	loothoarder.play()
	assert not loothoarder.buffs
	assert loothoarder.atk == 2
	assert loothoarder.health == 1

	# TODO: Test faceless-hobgoblin interaction
	# assert wisp.health == 1
	# assert wisp.atk == 1
	# faceless = game.current_player.give("EX1_564")
	# faceless.play(target=wisp)
	# assert not faceless.buffs
	# assert faceless.atk == 1
	# assert faceless.health == 1


def test_hogger():
	game = prepare_game()
	hogger = game.current_player.give("NEW1_040")
	hogger.play()
	assert len(game.current_player.field) == 1
	game.end_turn()
	assert len(game.current_player.opponent.field) == 2
	assert game.current_player.opponent.field[1].id == "NEW1_040t"
	game.end_turn()
	assert len(game.current_player.field) == 2
	game.end_turn()
	assert len(game.current_player.opponent.field) == 3


def test_houndmaster():
	game = prepare_game()
	houndmaster = game.current_player.give("DS1_070")
	assert not houndmaster.targets
	assert not houndmaster.powered_up
	hound = game.current_player.give("EX1_538t")
	hound.play()
	assert houndmaster.targets == [hound]
	assert houndmaster.powered_up
	assert hound.atk == 1
	assert hound.health == 1
	assert not hound.taunt
	houndmaster.play(target=hound)
	assert hound.atk == 3
	assert hound.health == 3
	assert hound.taunt


def test_illidan():
	game = prepare_game()
	illidan = game.current_player.give("EX1_614")
	assert len(game.board) == 0
	illidan.play()
	assert len(game.board) == 1
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 2
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 3
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 4
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 5

	# 5th moonfire kills illidan, but spawns another token before
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 5
	assert illidan.dead


def test_illidan_knife_juggler():
	game = prepare_game()
	illidan = game.player1.give("EX1_614")
	illidan.play()
	juggler = game.player1.give("NEW1_019")
	juggler.play()
	assert len(game.player1.field) == 3
	assert game.player2.hero.health == 30 - 1


def test_illidan_full_board():
	game = prepare_game()
	illidan = game.player1.give("EX1_614")
	illidan.play()
	game.player1.give(THE_COIN).play()
	game.player1.give(THE_COIN).play()
	game.player1.give(THE_COIN).play()
	game.player1.give(THE_COIN).play()
	game.player1.give(THE_COIN).play()
	assert len(game.player1.field) == 6
	juggler = game.player1.give("NEW1_019")
	juggler.play()
	assert len(game.player1.field) == 7
	assert game.player2.hero.health == 30


def test_iron_juggernaut():
	game = prepare_empty_game()
	juggernaut = game.player1.give("GVG_056")
	assert len(game.player2.deck) == 0
	juggernaut.play()

	assert game.player2.hero.health == 30
	assert len(game.player2.deck) == 1
	game.end_turn()
	assert game.player2.hero.health == 20
	assert len(game.player2.deck) == 0


def test_leeroy():
	game = prepare_game()
	leeroy = game.player1.give("EX1_116")
	leeroy.play()
	assert leeroy.can_attack()
	assert len(game.player2.field) == 2
	assert game.player2.field[0].id == game.player2.field[1].id == "EX1_116t"


def test_jaraxxus():
	game = prepare_game(WARRIOR, WARRIOR)
	game.player1.hero.power.use()
	game.player1.give("CS2_106").play()
	assert game.player1.weapon.id == "CS2_106"
	game.end_turn(); game.end_turn()

	assert game.player1.hero.health == 30
	assert game.player1.hero.armor == 2
	game.player1.give("EX1_323").play()
	assert game.player1.weapon.id == "EX1_323w"
	assert game.player1.hero.health == 15
	assert game.player1.hero.armor == 0
	assert game.player1.hero.power.id == "EX1_tk33"
	assert len(game.player1.field) == 0
	game.end_turn(); game.end_turn()

	game.player1.hero.power.use()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "EX1_tk34"


def test_lorewalker_cho():
	game = prepare_game()
	cho = game.current_player.give("EX1_100")
	cho.play()
	game.current_player.discard_hand()
	game.current_player.opponent.discard_hand()
	assert len(game.current_player.hand) == 0
	assert len(game.current_player.opponent.hand) == 0
	game.current_player.give(THE_COIN).play()
	assert len(game.current_player.hand) == 0
	assert len(game.current_player.opponent.hand) == 1
	assert game.current_player.opponent.hand[0].id == THE_COIN

	game.end_turn()
	game.current_player.discard_hand()
	game.current_player.give(THE_COIN).play()
	assert len(game.current_player.hand) == 0
	assert len(game.current_player.opponent.hand) == 1
	assert game.current_player.opponent.hand[0].id == THE_COIN
	game.current_player.give(THE_COIN).play()


def test_lava_shock():
	game = prepare_game()
	game.player1.give("EX1_243").play()
	assert game.player1.overloaded == 2
	lava = game.player1.give("BRM_011")
	lava.play(target=game.player2.hero)
	assert game.player2.hero.health == 28
	assert game.player1.overloaded == 0
	game.end_turn(); game.end_turn()

	game.player1.give("EX1_243").play()
	game.end_turn(); game.end_turn()

	game.player1.give("EX1_243").play()
	assert game.player1.overloaded == 2
	assert game.player1.overload_locked == 2
	lava = game.player1.give("BRM_011")
	lava.play(target=game.player2.hero)
	assert game.player1.overloaded == 0
	assert game.player1.overload_locked == 0


def test_light_of_the_naaru():
	game = prepare_game()
	naaru1 = game.player1.give("GVG_012")
	naaru2 = game.player1.give("GVG_012")
	naaru3 = game.player1.give("GVG_012")
	assert game.player1.hero.health == 30
	naaru1.play(target=game.player1.hero)
	assert not game.player1.field
	assert game.player1.hero.health == 30

	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 29
	naaru2.play(target=game.player1.hero)
	assert not game.player1.field
	assert game.player1.hero.health == 30

	for i in range(5):
		game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 25
	naaru3.play(target=game.player1.hero)
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "EX1_001"
	assert game.player1.hero.health == 28


def test_auchenai_light_of_the_naaru():
	game = prepare_game()
	soulpriest = game.current_player.give("EX1_591")
	soulpriest.play()
	assert len(game.player1.field) == 1
	naaru = game.player1.give("GVG_012")
	naaru.play(target=game.player2.hero)
	assert len(game.player1.field) == 2
	lightwarden = game.player1.field[1]
	assert lightwarden.id == "EX1_001"
	assert game.player2.hero.health == 30 - 3

	naaru2 = game.player1.give("GVG_012")
	naaru2.play(target=lightwarden)
	assert lightwarden.dead
	assert len(game.player1.field) == 2
	lightwarden2 = game.player1.field[1]
	assert lightwarden2.id == "EX1_001"

	# test on full board
	for i in range(5):
		game.player1.give(WISP).play()
	assert len(game.player1.field) == 7
	naaru3 = game.player1.give("GVG_012")
	naaru3.play(target=lightwarden2)

	assert lightwarden2.dead
	assert len(game.player1.field) == 6


def test_lightspawn():
	game = prepare_game()
	lightspawn = game.player1.give("EX1_335")
	lightspawn.play()
	assert lightspawn.health == 5
	assert lightspawn.atk == 5

	# moonfire the lightspawn, goes to 4 health
	game.player1.give(MOONFIRE).play(target=lightspawn)
	assert lightspawn.health == 4
	assert lightspawn.atk == 4
	assert not lightspawn.buffs

	flametongue = game.player1.give("EX1_565")
	flametongue.play()
	assert lightspawn.health == 4
	assert lightspawn.buffs
	assert lightspawn.atk == 4

	game.player1.give(SILENCE).play(target=lightspawn)
	assert lightspawn.buffs
	# 2 attack from the flametongue
	assert lightspawn.atk == 2


def test_lightwarden():
	game = prepare_game(PRIEST, PRIEST)
	lightwarden = game.current_player.give("EX1_001")
	lightwarden.play()
	assert lightwarden.atk == 1
	game.end_turn(); game.end_turn()

	# No-op heal should not do anything.
	assert game.current_player.hero.health == 30
	game.current_player.hero.power.use(target=game.current_player.hero)
	assert game.current_player.hero.health == 30
	assert lightwarden.atk == 1
	lightwarden.attack(target=game.current_player.opponent.hero)
	game.end_turn()
	game.current_player.hero.power.use(target=game.current_player.hero)
	assert lightwarden.atk == 3


def test_lightwell():
	game = prepare_game()
	lightwell = game.player1.give("EX1_341")
	lightwell.play()
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert game.player1.hero.health == 29
	assert game.player2.hero.health == 29
	game.end_turn()

	assert game.player1.hero.health == 29
	assert game.player2.hero.health == 29
	game.end_turn()

	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 29


def test_lil_exorcist():
	game = prepare_game()
	exorcist1 = game.player1.give("GVG_097")
	exorcist1.play()
	assert exorcist1.atk == 2
	assert exorcist1.health == 3
	assert not exorcist1.buffs
	game.end_turn()

	game.player2.give("FP1_001").play()
	game.player2.give("FP1_001").play()
	game.end_turn()

	exorcist2 = game.player1.give("GVG_097")
	exorcist2.play()
	assert exorcist2.atk == 2 + 2
	assert exorcist2.health == 3 + 2
	assert exorcist2.buffs


def test_loatheb():
	game = prepare_game(WARRIOR, MAGE)
	game.player1.discard_hand()
	game.player2.discard_hand()
	loatheb = game.player1.give("FP1_030")
	fireballp1 = game.player1.give("CS2_029")
	fireball1 = game.player2.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	moonfire = game.player2.give(MOONFIRE)

	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballp1.cost == 4
	loatheb.play()
	# costs do not change right away
	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballp1.cost == 4
	game.end_turn()

	assert fireball1.cost == 4 + 5
	assert fireball2.cost == 4 + 5
	assert moonfire.cost == 0 + 5
	assert fireballp1.cost == 4
	game.end_turn()

	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballp1.cost == 4


def test_micro_machine():
	game = prepare_game()
	micro = game.player1.give("GVG_103")
	micro.play()
	assert micro.atk == 1
	game.end_turn()

	assert micro.atk == 2
	game.end_turn()

	assert micro.atk == 3
	game.end_turn()

	assert micro.atk == 4


def test_millhouse_manastorm():
	game = prepare_game(WARRIOR, MAGE)
	game.player1.discard_hand()
	game.player2.discard_hand()
	millhouse = game.player1.give("NEW1_029")
	fireballp1 = game.player1.give("CS2_029")
	fireball1 = game.player2.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	moonfire = game.player2.give(MOONFIRE)

	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballp1.cost == 4
	millhouse.play()
	# costs change as soon as millhouse is played
	assert game.player2.hero.buffs
	assert fireball1.buffs
	assert fireball1.cost == 0
	assert fireball2.cost == 0
	assert moonfire.cost == 0
	assert fireballp1.cost == 4
	game.end_turn()

	assert fireball1.cost == 0
	assert fireball2.cost == 0
	assert moonfire.cost == 0
	assert fireballp1.cost == 4
	game.end_turn()

	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballp1.cost == 4


def test_molten_giant():
	game = prepare_game()
	molten = game.current_player.give("EX1_620")
	assert molten.cost == 20
	game.current_player.give(MOONFIRE).play(target=game.current_player.hero)
	assert molten.cost == 19
	game.current_player.give(MOONFIRE).play(target=game.current_player.hero)
	assert molten.cost == 18
	game.current_player.give(MOONFIRE).play(target=game.current_player.hero)
	assert molten.cost == 17
	game.end_turn()

	assert molten.cost == 17
	molten2 = game.current_player.give("EX1_620")
	assert molten2.cost == 20


def test_mountain_giant():
	game = prepare_game()
	mountain = game.current_player.give("EX1_105")
	assert mountain.cost == 12 - len(game.current_player.hand) + 1
	game.end_turn(); game.end_turn()

	assert mountain.cost == 12 - len(game.current_player.hand) + 1
	game.end_turn(); game.end_turn()

	assert mountain.cost == 12 - len(game.current_player.hand) + 1


def test_sea_giant():
	game = prepare_game()
	seagiant = game.current_player.give("EX1_586")
	assert seagiant.cost == 10
	game.current_player.give(WISP).play()
	assert seagiant.cost == 9
	game.current_player.give(WISP).play()
	assert seagiant.cost == 8
	for i in range(5):
		game.player1.give(WISP).play()
	assert seagiant.cost == 3
	game.end_turn()

	for i in range(7):
		game.player2.give(WISP).play()
	assert seagiant.cost == 0


def test_murloc_tidecaller():
	game = prepare_game()
	tidecaller = game.current_player.give("EX1_509")
	tidecaller.play()
	assert tidecaller.atk == 1
	game.end_turn()

	game.current_player.give("CS2_168").play()
	assert tidecaller.atk == 2
	game.end_turn()

	# Play a tidehunter. Summons two murlocs.
	game.current_player.give("EX1_506").play()
	assert tidecaller.atk == 4


def test_neptulon():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	assert len(game.player1.hand) == 0
	assert len(game.player2.hand) == 0
	game.player1.give("GVG_042").play()
	assert len(game.player1.hand) == 4
	assert len(game.player2.hand) == 0
	for i in range(4):
		assert game.player1.hand[i].race == Race.MURLOC
	assert game.player1.overloaded == 3


def test_nerubar_weblord():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	moonfire1 = game.player1.give(MOONFIRE)
	moonfire2 = game.player2.give(MOONFIRE)
	footman1 = game.player1.give(GOLDSHIRE_FOOTMAN)
	footman2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	archer1 = game.player1.give("CS2_189")
	archer2 = game.player2.give("CS2_189")
	perdition1 = game.player1.give("EX1_133")
	perdition2 = game.player2.give("EX1_133")
	assert moonfire1.cost == moonfire2.cost == 0
	assert footman1.cost == footman2.cost == 1
	assert archer1.cost == archer2.cost == 1
	assert perdition1.cost == perdition2.cost == 3
	nerubar = game.player1.give("FP1_017")
	nerubar.play()
	assert moonfire1.cost == moonfire2.cost == 0
	assert footman1.cost == footman2.cost == 1
	assert archer1.cost == archer2.cost == 1 + 2
	assert perdition1.cost == perdition2.cost == 3


def test_northshire_cleric():
	game = prepare_game(PRIEST, PRIEST)
	game.player1.discard_hand()
	game.player2.discard_hand()
	cleric = game.player1.give("CS2_235")
	cleric.play()
	game.player1.hero.power.use(target=game.current_player.hero)
	assert not game.player1.hand

	pyromancer = game.player1.give("NEW1_020")
	pyromancer.play()
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert not game.player1.hand

	game.player2.summon(SPELLBENDERT)
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert len(game.player1.hand) == 2

	game.player1.give(CIRCLE_OF_HEALING).play()
	assert len(game.player1.hand) == 5
	assert not game.player2.hand


def test_ragnaros():
	game = prepare_game()
	ragnaros = game.current_player.give("EX1_298")
	ragnaros.play()
	assert not ragnaros.can_attack()
	assert game.current_player.opponent.hero.health == 30
	game.end_turn()

	assert game.current_player.hero.health == 22
	game.end_turn()

	assert game.current_player.opponent.hero.health == 22
	assert not ragnaros.can_attack()


def test_raid_leader():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	wisp3 = game.player2.summon(WISP)
	raidleader = game.player1.summon("CS2_122")
	assert wisp1.atk == wisp2.atk == 2
	assert wisp3.atk == 1

	raidleader.destroy()

	assert wisp1.atk == wisp2.atk == 1


def test_recombobulator():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	recom = game.player1.give("GVG_108")
	recom.play(target=wisp)
	recom.destroy()

	assert wisp not in game.player1.field
	assert game.player1.field[0].cost == 0


def test_reincarnate():
	game = prepare_game()

	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	assert goldshire.health == 2
	game.player1.give(MOONFIRE).play(target=goldshire)
	assert goldshire.health == 1
	assert len(game.player1.field) == 1
	game.player1.give("FP1_025").play(target=goldshire)
	assert len(game.player1.field) == 1
	assert game.player1.field[0].health == 2
	game.player1.field[0].destroy()

	# Ensure charge refresh
	leeroy1 = game.current_player.give("EX1_116")
	leeroy1.play()
	assert leeroy1.can_attack()
	leeroy1.attack(target=game.player2.hero)
	assert not leeroy1.can_attack()
	game.player1.give("FP1_025").play(target=leeroy1)
	leeroy2 = game.player1.field[0]
	assert leeroy2.can_attack()
	leeroy1.attack(target=game.player2.hero)
	assert not leeroy1.can_attack()


def test_reincarnate_kel_thuzad():
	game = prepare_game()
	kelthuzad = game.player1.give("FP1_013")
	kelthuzad.play()
	assert len(game.player1.field) == 1
	game.player1.give("FP1_025").play(target=kelthuzad)
	assert len(game.player1.field) == 1
	game.end_turn()
	assert len(game.player1.field) == 2
	assert len(game.player1.field.filter(id="FP1_013")) == 2


def test_tree_of_life():
	game = prepare_game()
	token1 = game.player1.give(SPELLBENDERT)
	token1.play()
	tree = game.player1.give("GVG_033")
	game.end_turn()

	token2 = game.player2.give(SPELLBENDERT)
	token2.play()
	game.end_turn()

	targets = (game.player1.hero, game.player2.hero, token1, token2)
	for target in targets:
		game.player1.give(MOONFIRE).play(target=target)

	assert token1.health == token2.health == 3 - 1
	assert game.player1.hero.health == game.player2.hero.health == 30 - 1
	tree.play()
	assert token1.health == token2.health == 3
	assert game.player1.hero.health == game.player2.hero.health == 30


def test_truesilver_champion():
	game = prepare_game()
	truesilver = game.current_player.give("CS2_097")
	truesilver.play()
	lightwarden = game.current_player.give("EX1_001")
	lightwarden.play()
	assert game.player1.weapon is truesilver
	assert game.player1.hero.atk == 4
	assert game.player1.hero.health == 30
	game.current_player.hero.attack(target=game.player2.hero)
	assert game.player2.hero.health == 26
	assert game.player1.hero.health == 30
	assert lightwarden.atk == 1
	game.end_turn(); game.end_turn()

	for i in range(3):
		game.player1.give(MOONFIRE).play(target=game.player1.hero)
	game.player1.hero.attack(target=game.player2.hero)
	assert game.current_player.hero.health == 29
	assert lightwarden.atk == 3


def test_truesilver_champion_explosive_trap():
	game = prepare_game()
	explosivetrap = game.player1.give("EX1_610")
	explosivetrap.play()
	game.end_turn()
	game.player2.hero.set_current_health(2)
	assert game.player2.hero.health == 2
	truesilver = game.player2.give("CS2_097")
	truesilver.play()
	game.player2.hero.attack(game.player1.hero)
	assert explosivetrap.dead
	assert game.player2.hero.health == 2
	assert game.player1.hero.health == 26


def test_tinkertown_technician():
	game = prepare_game()
	game.player1.discard_hand()
	game.player1.give(WISP).play()
	tech = game.player1.give("GVG_102")
	tech.play()
	assert tech.atk == tech.health == 3
	assert len(game.player1.hand) == 0

	dummy = game.player1.give(TARGET_DUMMY)
	dummy.play()
	tech2 = game.player1.give("GVG_102")
	tech2.play()
	assert tech2.atk == tech2.health == 4
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].type == CardType.SPELL


def test_totemic_might():
	game = prepare_game()
	searing = game.player1.give("CS2_050")
	searing.play()
	assert searing.atk == 1
	assert searing.health == 1
	game.player1.give("EX1_244").play()
	assert searing.atk == 1
	assert searing.health == 3


def test_twilight_drake():
	game = prepare_game()
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	assert len(game.current_player.hand) == 7
	drake = game.current_player.give("EX1_043")
	drake.play()
	assert len(game.current_player.hand) == 7
	assert drake.health == 1 + 7
	assert drake.buffs

	game.end_turn()
	game.current_player.discard_hand()
	drake2 = game.current_player.give("EX1_043")
	assert len(game.current_player.hand) == 1
	drake2.play()
	assert not game.current_player.hand
	assert drake2.health == 1
	assert not drake2.buffs


def test_unbound_elemental():
	game = prepare_game()
	unbound = game.player1.give("EX1_258")
	unbound.play()
	assert unbound.atk == 2
	assert unbound.health == 4
	game.player1.give(THE_COIN).play()
	assert unbound.atk == 2
	assert unbound.health == 4
	# Lightning Bolt should trigger it
	game.player1.give("EX1_238").play(target=game.player2.hero)
	assert unbound.atk == 3
	assert unbound.health == 5
	game.end_turn()

	game.player2.give("EX1_238").play(target=game.player2.hero)
	assert unbound.atk == 3
	assert unbound.health == 5


def test_undertaker():
	game = prepare_game()
	undertaker = game.current_player.give("FP1_028")
	undertaker.play()
	game.current_player.give(WISP).play()
	assert not undertaker.buffs
	assert undertaker.atk == 1
	assert undertaker.health == 2
	game.end_turn()

	# Play a leper gnome, should not trigger undertaker
	game.current_player.give("EX1_029").play()
	assert undertaker.atk == 1
	assert undertaker.health == 2
	game.end_turn()

	game.current_player.give("EX1_029").play()
	assert undertaker.atk == 2
	assert undertaker.health == 2

	game.current_player.give("EX1_029").play()
	assert undertaker.atk == 3
	assert undertaker.health == 2


def test_vancleef():
	game = prepare_game()
	vancleef1 = game.current_player.give("EX1_613")
	vancleef2 = game.current_player.give("EX1_613")

	assert not game.current_player.cards_played_this_turn
	for i in range(5):
		game.player1.give(THE_COIN).play()
	assert game.current_player.cards_played_this_turn == 5
	vancleef1.play()
	assert game.current_player.cards_played_this_turn == 6
	assert vancleef1.atk == 12
	assert vancleef1.health == 12
	game.end_turn(); game.end_turn()

	assert not game.current_player.cards_played_this_turn
	vancleef2.play()
	assert game.current_player.cards_played_this_turn == 1
	assert vancleef2.atk == 2
	assert vancleef2.health == 2


def test_water_elemental():
	game = prepare_game()
	elem = game.player1.give("CS2_033")
	elem.play()
	game.end_turn(); game.end_turn()

	assert not game.player2.hero.frozen
	elem.attack(target=game.player2.hero)
	assert game.player2.hero.frozen
	game.end_turn()

	assert game.player2.hero.frozen
	game.end_turn()

	assert not game.player2.hero.frozen
	game.end_turn()

	axe = game.player2.give("CS2_106")
	axe.play()
	game.player2.hero.attack(target=elem)
	assert game.player2.hero.frozen
	game.end_turn()

	assert game.player2.hero.frozen
	game.end_turn()

	assert game.player2.hero.frozen
	game.end_turn()

	assert not game.player2.hero.frozen
	game.end_turn()


def test_whirlwind():
	game = prepare_game()
	token = game.player1.give(SPELLBENDERT)
	token.play()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()
	wisp2 = game.player2.give(WISP)
	wisp2.play()

	game.player2.give("EX1_400").play()
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	assert wisp.dead
	assert wisp2.dead
	assert token.health == 2


def test_webspinner():
	game = prepare_game()
	game.player1.discard_hand()
	webspinner = game.player1.give("FP1_011")
	webspinner.play()
	game.player1.give(MOONFIRE).play(target=webspinner)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.BEAST
	assert game.player1.hand[0].type == CardType.MINION


def test_wild_pyromancer():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	pyro = game.player1.give("NEW1_020")
	game.end_turn(); game.end_turn()

	pyro.play()
	assert pyro.health == 2
	assert wisp.zone == Zone.PLAY

	# play moonfire. wisp should die.
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert wisp.dead
	assert pyro.health == 1

	# play circle of healing. pyro should go up to 2hp then back to 1.
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert pyro.health == 1
	assert pyro.zone == Zone.PLAY

	# Silence the pyromancer. It should not trigger.
	game.player1.give(SILENCE).play(target=pyro)
	assert pyro.health == 1
	assert pyro.zone == Zone.PLAY


def test_young_priestess():
	game = prepare_game()
	priestess = game.player1.give("EX1_004")
	game.end_turn(); game.end_turn()

	priestess.play()
	assert priestess.health == 1
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	assert priestess.health == 1
	assert wisp.health == 1
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	assert wisp1.health == 1

	game.end_turn()
	assert wisp1.health == 2


def test_ysera():
	game = prepare_game()
	ysera = game.player1.give("EX1_572")
	ysera.play()
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	game.end_turn()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].card_class == CardClass.DREAM


def test_ysera_awakens():
	game = prepare_game()
	game.player1.give(WISP).play()
	ysera = game.player1.give("EX1_572")
	ysera.play()
	game.end_turn()

	game.player2.give(WISP).play()
	game.player2.give("DREAM_02").play()
	assert game.player1.hero.health == game.player2.hero.health == 30 - 5
	assert len(game.board) == 1
	assert ysera.health == 12


def test_sabotage():
	game = prepare_game()
	sabotage = game.player1.give("GVG_047")
	sabotage.play()

	sabotage2 = game.player1.give("GVG_047")
	sabotage2.play()
	game.end_turn()

	axe = game.player2.give("CS2_106")
	axe.play()
	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	sabotage3 = game.player1.give("GVG_047")
	sabotage3.play()
	assert not axe.dead
	assert wisp.dead

	sabotage4 = game.player1.give("GVG_047")
	sabotage4.play()
	assert axe.dead


def test_savage_roar():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	game.end_turn()
	wisp2 = game.player2.give(WISP)
	wisp2.play()
	game.end_turn()

	assert wisp1.atk == 1
	assert wisp2.atk == 1
	assert game.player1.hero.atk == 0
	assert game.player2.hero.atk == 0
	game.player1.give("CS2_011").play()
	assert wisp1.atk == 1 + 2
	assert wisp2.atk == 1
	assert game.player1.hero.atk == 2
	assert game.player2.hero.atk == 0
	game.end_turn()
	assert wisp1.atk == 1
	assert wisp2.atk == 1
	assert game.player1.hero.atk == 0
	assert game.player2.hero.atk == 0


def test_shadowflame():
	game = prepare_game()
	dummy1 = game.player1.give(TARGET_DUMMY)
	dummy1.play()
	game.end_turn()
	goldshire = game.player2.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	dummy2 = game.player2.give(TARGET_DUMMY)
	dummy2.play()

	assert dummy1.health == 2
	assert goldshire.health == 2
	assert not dummy2.dead
	game.player2.give("EX1_303").play(target=dummy2)
	assert dummy1.health == 2
	assert goldshire.health == 2
	assert dummy2.dead
	game.player2.give("EX1_303").play(target=goldshire)
	assert dummy1.health == 1


def test_shadow_madness_wild_pyro():
	game = prepare_game()
	pyromancer = game.current_player.give("NEW1_020")
	pyromancer.play()
	game.end_turn()

	assert pyromancer.controller == game.player1
	assert pyromancer in game.player1.field
	assert pyromancer.health == 2
	shadowmadness = game.player2.give("EX1_334")
	shadowmadness.play(target=pyromancer)
	assert pyromancer.controller == game.player2
	assert pyromancer in game.player2.field
	assert pyromancer.health == 1
	game.end_turn()

	assert pyromancer.controller == game.player1
	assert pyromancer in game.player1.field


def test_shadow_madness_silence():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	wisp.play()
	game.end_turn()

	assert wisp.controller == game.player1
	shadowmadness = game.current_player.give("EX1_334")
	shadowmadness.play(target=wisp)
	assert wisp.controller == game.player2
	game.current_player.give(SILENCE).play(target=wisp)
	assert wisp.controller == game.player1
	game.end_turn()

	assert wisp.controller == game.player1


def test_shadowform():
	game = prepare_game(PRIEST, PRIEST)
	# Hero Power should reset
	shadowform1 = game.current_player.give("EX1_625")
	assert game.current_player.hero.power.id == "CS1h_001"
	assert game.current_player.hero.power.is_usable()
	game.current_player.hero.power.use(target=game.current_player.hero)
	assert not game.current_player.hero.power.is_usable()
	assert shadowform1.is_playable()
	shadowform1.play()
	assert game.current_player.hero.power.id == "EX1_625t"
	assert game.current_player.hero.power.is_usable()
	game.current_player.hero.power.use(target=game.current_player.opponent.hero)
	assert not game.current_player.hero.power.is_usable()
	assert game.current_player.opponent.hero.health == 28
	game.end_turn(); game.end_turn()

	shadowform2 = game.current_player.give("EX1_625")
	shadowform2.play()
	assert game.current_player.hero.power.id == "EX1_625t2"
	assert game.current_player.hero.power.is_usable()
	game.current_player.hero.power.use(target=game.current_player.opponent.hero)
	assert not game.current_player.hero.power.is_usable()
	assert game.current_player.opponent.hero.health == 25

	shadowform3 = game.current_player.give("EX1_625")
	shadowform3.play()
	assert game.current_player.hero.power.id == "EX1_625t2"
	assert not game.current_player.hero.power.is_usable()


def test_shadowstep():
	game = prepare_game()
	shadowstep = game.current_player.give("EX1_144")
	deathwing = game.current_player.summon("NEW1_030")
	assert deathwing.zone == Zone.PLAY
	assert deathwing.cost == 10
	shadowstep.play(target=deathwing)
	assert deathwing.zone == Zone.HAND
	assert deathwing in game.current_player.hand
	assert deathwing.cost == 8


def test_shattered_sun_cleric():
	game = prepare_game()
	cleric = game.player1.give("EX1_019")
	assert not cleric.targets
	cleric.play()
	assert cleric.atk == 3
	assert cleric.health == 2
	game.end_turn(); game.end_turn()

	cleric2 = game.player1.give("EX1_019")
	assert cleric in cleric2.targets
	cleric2.play(target=cleric)
	assert cleric.atk == 3 + 1
	assert cleric.health == 2 + 1


def test_acolyte_of_pain():
	game = prepare_game()
	acolyte = game.player1.give("EX1_007")
	acolyte.play()
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	game.current_player.give(MOONFIRE).play(target=acolyte)
	assert len(game.player1.hand) == 1
	game.current_player.give(MOONFIRE).play(target=acolyte)
	assert len(game.player1.hand) == 2
	game.current_player.give(MOONFIRE).play(target=acolyte)
	assert len(game.player1.hand) == 3
	assert acolyte.dead


def test_poisonous():
	game = prepare_game()
	game.end_turn()

	cobra = game.current_player.give("EX1_170")
	cobra.play()
	assert cobra.poisonous
	game.end_turn()
	zchow = game.current_player.give("FP1_001")
	zchow.play()
	zchow2 = game.current_player.give("FP1_001")
	zchow2.play()
	game.end_turn()
	cobra.attack(target=zchow)
	assert zchow not in game.current_player.opponent.field
	assert zchow.dead
	game.end_turn()
	zchow2.attack(target=cobra)
	assert zchow2.dead

	# test silencing the cobra
	zchow3 = game.current_player.give("FP1_001")
	zchow3.play()
	game.end_turn()
	cobra = game.current_player.give("EX1_170")
	cobra.play()
	cobra.silence()
	game.end_turn()
	zchow3.attack(cobra)
	assert zchow3 in game.current_player.field
	assert cobra in game.current_player.opponent.field


def test_cleave():
	game = prepare_game()
	# play some wisps
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	game.end_turn()

	cleave = game.current_player.give("CS2_114")
	assert cleave.is_playable()
	cleave.play()
	assert len(game.current_player.opponent.field) == 0
	game.current_player.give(WISP).play()
	game.end_turn()

	cleave2 = game.current_player.give("CS2_114")
	assert not cleave2.is_playable()


def test_upgrade():
	game = prepare_game()
	axe = game.current_player.give("CS2_106")
	axe.play()
	assert game.current_player.weapon.atk == 3
	assert game.current_player.weapon.durability == 2
	game.current_player.hero.attack(game.current_player.opponent.hero)
	assert game.current_player.weapon.atk == 3
	assert game.current_player.weapon.durability == 1
	assert game.current_player.opponent.hero.health == 27

	game.end_turn()
	upgrade = game.current_player.give("EX1_409")
	upgrade.play()
	assert game.current_player.hero.atk == 1
	assert game.current_player.weapon.atk == 1
	game.end_turn()

	assert game.current_player.weapon.atk == 3
	assert game.current_player.weapon.durability == 1
	upgrade2 = game.current_player.give("EX1_409")
	upgrade2.play()
	assert game.current_player.weapon.atk == 4
	assert game.current_player.weapon.durability == 2
	game.current_player.hero.attack(game.current_player.opponent.hero)
	assert game.current_player.opponent.hero.health == 23
	assert game.current_player.weapon.durability == 1

	# test Bloodsail Corsair
	game.end_turn()
	corsair = game.current_player.give("NEW1_025")
	corsair.play()
	assert axe.dead
	assert not game.current_player.opponent.weapon


def test_unstable_portal():
	game = prepare_game()
	game.player1.discard_hand()
	portal = game.player1.give("GVG_003")
	portal.play()
	assert len(game.player1.hand) == 1
	minion = game.player1.hand[0]
	assert minion.type == CardType.MINION
	assert minion.buffs


CHEAT_MIRROR_ENTITY = True
def test_mctech():
	game = prepare_game()
	game.end_turn()
	# play some wisps
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()
	if CHEAT_MIRROR_ENTITY:
		# TODO secrets
		game.current_player.give("EX1_294").play()
	game.end_turn()

	assert len(game.current_player.opponent.field) == 3
	# play an mctech. nothing should be controlled.
	game.current_player.give("EX1_085").play()
	assert len(game.current_player.field) == 1
	game.end_turn()
	if CHEAT_MIRROR_ENTITY:
		# mc tech gets copied, board now at 4
		game.current_player.give("EX1_085").play()
	assert len(game.current_player.field) == 4
	game.end_turn()
	game.current_player.give("EX1_085").play()
	assert len(game.current_player.field) == 3
	assert len(game.current_player.opponent.field) == 3


def test_inner_fire():
	game = prepare_game()
	gurubashi = game.player1.give("EX1_399")
	gurubashi.play()
	assert gurubashi.atk == 2

	seargent = game.player1.give("CS2_188")
	seargent.play(target=gurubashi)
	assert gurubashi.atk == 4

	innerfire = game.player1.give("CS1_129")
	innerfire.play(target=gurubashi)
	assert gurubashi.atk == 7
	game.end_turn()

	assert gurubashi.atk == 7
	equality = game.player2.give("EX1_619")
	equality.play()
	assert gurubashi.health == 1
	assert gurubashi.atk == 7


def test_innervate():
    game = prepare_game()
    assert game.player1.mana == 10
    assert game.player1.temp_mana == 0
    assert game.player1.max_mana == 10
    assert game.player1.max_resources == 10
    game.player1.give("EX1_169").play()
    assert game.player1.mana == 10
    assert game.player1.temp_mana == 0
    game.player1.give(GOLDSHIRE_FOOTMAN).play()
    assert game.player1.mana == 9
    game.player1.give("EX1_169").play()
    assert game.player1.mana == 10
    assert game.player1.temp_mana == 1
    game.player1.give(GOLDSHIRE_FOOTMAN).play()
    assert game.player1.mana == 9
    assert game.player1.temp_mana == 0


def test_ice_barrier():
	game = prepare_game(MAGE, MAGE)
	icebarrier = game.current_player.give("EX1_289")
	icebarrier2 = game.current_player.give("EX1_289")
	friendlywisp = game.current_player.give(WISP)
	friendlywisp.play()
	game.end_turn()
	wisp = game.current_player.give(WISP)
	wisp.play()
	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	game.end_turn()

	assert icebarrier.is_playable()
	icebarrier.play()
	assert not icebarrier2.is_playable()
	assert game.current_player.secrets
	assert icebarrier in game.current_player.secrets
	assert not game.current_player.hero.armor
	game.end_turn(); game.end_turn()

	assert not icebarrier2.is_playable()
	friendlywisp.attack(target=game.current_player.opponent.hero)
	assert not game.current_player.hero.armor
	assert not game.current_player.opponent.hero.armor
	game.end_turn(); game.end_turn()

	friendlywisp.attack(target=wisp2)
	assert not game.current_player.hero.armor
	assert not game.current_player.opponent.hero.armor
	assert friendlywisp.dead
	assert wisp2.dead
	game.end_turn()

	assert len(game.current_player.opponent.secrets) == 1
	wisp.attack(target=game.current_player.opponent.hero)
	assert not game.current_player.opponent.secrets
	assert game.current_player.opponent.hero.armor == 7


def test_vaporize():
	game = prepare_game()
	vaporize = game.current_player.give("EX1_594")
	game.end_turn()

	wisp = game.current_player.give(WISP)
	wisp.play()
	game.end_turn()

	vaporize.play()
	assert game.current_player.secrets[0] == vaporize
	game.end_turn()

	assert len(game.current_player.opponent.secrets) == 1
	# Play an axe and hit the hero ourselves
	game.current_player.give("CS2_106").play()
	game.current_player.hero.attack(target=game.current_player.opponent.hero)
	assert len(game.current_player.opponent.secrets) == 1
	assert game.current_player.opponent.hero.health == 27
	wisp.attack(target=game.current_player.opponent.hero)
	assert not game.current_player.opponent.secrets
	assert vaporize.dead
	assert wisp.dead
	assert game.current_player.opponent.hero.health == 27


def test_slam():
	game = prepare_game()
	wisp = game.player1.summon(WISP)
	mogushan = game.player1.summon("EX1_396")
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	game.player1.give("EX1_391").play(target=wisp)
	assert wisp.dead
	assert len(game.player1.hand) == 0
	game.player1.give("EX1_391").play(target=mogushan)
	assert not mogushan.dead
	assert len(game.player1.hand) == 1


def test_stampeding_kodo():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	watcher = game.player1.give("EX1_045")
	watcher.play()
	game.end_turn()

	kodo = game.player2.give("NEW1_041")
	kodo.play()
	assert wisp.dead
	assert not watcher.dead
	kodo2 = game.player2.give("NEW1_041")
	kodo2.play()
	assert not watcher.dead


def test_stoneskin_gargoyle():
	game = prepare_game()
	gargoyle = game.current_player.give("FP1_027")
	gargoyle.play()
	assert gargoyle.health == 4
	# damage the gargoyle by 1
	game.current_player.give(MOONFIRE).play(target=gargoyle)
	assert gargoyle.health == 3
	game.end_turn(); game.end_turn()

	assert gargoyle.health == 4
	# Test auchenai interaction
	soulpriest = game.current_player.give("EX1_591")
	soulpriest.play()
	game.end_turn(); game.end_turn()

	assert gargoyle.health == 4
	game.current_player.give(MOONFIRE).play(target=gargoyle)
	assert gargoyle.health == 3
	game.end_turn(); game.end_turn()

	assert gargoyle.health == 2
	game.end_turn(); game.end_turn()

	assert gargoyle.dead


def test_summoning_portal():
	game = prepare_game()
	game.player1.discard_hand()
	wisp = game.player1.give(WISP)
	assert wisp.cost == 0
	axe = game.player1.give("CS2_106")
	assert axe.cost == 2
	molten = game.player1.give("EX1_620")
	assert molten.cost == 20
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	assert goldshire.cost == 1
	frostwolf = game.player1.give("CS2_121")
	assert frostwolf.cost == 2

	portal = game.player1.give("EX1_315")
	portal.play()
	assert wisp.cost == 0
	assert axe.cost == 2
	assert molten.cost == 18
	assert goldshire.cost == 1
	assert frostwolf.cost == 1
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert molten.cost == 17
	portal2 = game.player1.give("EX1_315")
	portal2.play()
	assert wisp.cost == 0
	assert molten.cost == 20 - 2 - 1 - 2
	assert goldshire.cost == 1
	assert frostwolf.cost == 1


def test_sunfury_protector():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	sunfury = game.player1.give("EX1_058")
	sunfury.play()
	assert not wisp1.taunt
	assert wisp2.taunt


def test_faerie_dragon():
	game = prepare_game(MAGE, MAGE)
	dragon = game.current_player.give("NEW1_023")
	dragon.play()
	moonfire = game.current_player.give(MOONFIRE)
	assert dragon not in moonfire.targets
	assert dragon not in game.current_player.hero.power.targets
	game.end_turn()

	assert dragon not in game.current_player.hero.power.targets
	archer = game.current_player.give("CS2_189")
	assert dragon in archer.targets


def test_fel_cannon():
	game = prepare_game()
	cannon = game.player1.give("GVG_020")
	cannon.play()
	game.end_turn(); game.end_turn()

	assert game.player1.hero.health == game.player2.hero.health == 30
	assert cannon.health == 5

	dummy1 = game.player1.give(TARGET_DUMMY)
	dummy1.play()
	game.end_turn()

	dummy2 = game.player2.give(TARGET_DUMMY)
	dummy2.play()
	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	assert not wisp.dead
	game.end_turn()

	assert dummy1.health == dummy2.health == 2
	assert not dummy1.dead
	assert not dummy2.dead
	assert wisp.dead


def test_fireguard_destroyer():
	game = prepare_game()
	fireguard = game.player1.give("BRM_012")
	fireguard.play()
	assert fireguard.atk in (4, 5, 6, 7)


def test_far_sight():
	game = prepare_game()
	game.player1.discard_hand()
	farsight = game.current_player.give("CS2_053")
	farsight.play()
	assert len(game.current_player.hand) == 1
	assert game.current_player.hand[0].buffs
	assert game.current_player.hand[0].cost >= 0


def test_fatigue():
	game = prepare_game()
	game.player1.fatigue()
	assert game.player1.hero.health == 30 - 1
	game.player1.fatigue()
	assert game.player1.hero.health == 30 - 1 - 2
	game.player1.fatigue()
	assert game.player1.hero.health == 30 - 1 - 2 - 3
	assert game.player2.hero.health == 30

	# Draw the deck
	game.player1.draw(26)
	assert game.player1.hero.health == 30 - 1 - 2 - 3
	game.player1.draw(1)
	assert game.player1.hero.health == 30 - 1 - 2 - 3 - 4
	game.end_turn(); game.end_turn()
	assert game.player1.hero.health == 30 - 1 - 2 - 3 - 4 - 5


def test_flare():
	game = prepare_game(HUNTER, HUNTER)
	flare = game.current_player.give("EX1_544")
	worgen = game.current_player.give("EX1_010")
	worgen.play()
	game.end_turn()

	avenge = game.current_player.give("FP1_020")
	avenge.play()
	game.end_turn()

	flare.play()
	assert not game.current_player.opponent.secrets
	assert not worgen.stealthed


def test_freezing_trap():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	trap = game.player2.give("EX1_611")
	trap.play()
	assert game.player2.secrets
	game.end_turn()

	assert wisp.cost == 0
	assert not wisp.buffs
	assert wisp.zone == Zone.PLAY
	assert game.player2.hero.health == 30
	wisp.attack(target=game.player2.hero)
	assert not game.player2.secrets
	assert trap.dead
	assert game.player2.hero.health == 30
	assert wisp.zone == Zone.HAND
	assert wisp in game.player1.hand
	assert wisp.buffs
	assert wisp.cost == 2
	assert wisp.zone == Zone.HAND
	wisp.play()
	assert game.player1.used_mana == 2
	assert not wisp.buffs
	assert wisp.cost == 0


def test_flame_leviathan():
	game = prepare_empty_game()
	assert len(game.player1.deck) == 0
	leviathan = game.player1.give("GVG_007")
	leviathan.shuffle_into_deck()
	assert len(game.player1.deck) == 1
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()

	# draw the flame leviathan
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	assert not wisp.dead
	game.end_turn()
	assert game.player1.hero.health == 28
	assert game.player2.hero.health == 28
	assert wisp.dead


def test_floating_watcher():
	game = prepare_game()
	game = prepare_game(WARLOCK, WARLOCK)
	watcher = game.player1.give("GVG_100")
	watcher.play()
	assert watcher.atk == watcher.health == 4
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert watcher.atk == watcher.health == 4
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert watcher.atk == watcher.health == 4 + 2
	game.player1.hero.power.use()
	assert watcher.atk == watcher.health == 4 + 4


def test_force_of_nature():
	game = prepare_game()
	game.player1.give("EX1_571").play()
	assert len(game.player1.field) == 3
	assert len(game.player1.field.filter(id="EX1_tk9")) == 3
	game.player1.field[0].attack(game.player2.hero)
	assert game.player2.hero.health == 30 - 2
	game.end_turn()
	assert len(game.player1.field) == 0


def test_warlock():
	game = prepare_game(WARLOCK, WARLOCK)
	sacpact = game.current_player.give("NEW1_003")
	assert not sacpact.is_playable()
	flameimp = game.current_player.give("EX1_319")
	flameimp.play()
	assert game.current_player.hero.health == 27
	assert sacpact.is_playable()
	sacpact.play(target=flameimp)
	assert game.current_player.hero.health == 30
	game.end_turn()


def test_discard_enchanted_cards():
	# Test for bug #58
	game = prepare_game()
	deathwing = game.player1.give("NEW1_030")
	thaurissan = game.player1.give("BRM_028")
	thaurissan.play()
	for i in range(10):
		game.end_turn(); game.end_turn()

	deathwing.play()
	assert not game.player1.hand


def test_resurrect():
	# Doesn't summon if nothing died
	game = prepare_game()
	game.player1.give("BRM_017").play()
	assert len(game.player1.field) == 0

	# Summons something
	wisp = game.player1.give(WISP)
	wisp.play()
	game.player1.give(MOONFIRE).play(target=wisp)
	assert len(game.player1.field) == 0
	game.player1.give("BRM_017").play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0] == wisp


def test_resurrect_wild_pyro():
	"""
	Test that Wild Pyromancer triggers if summoned from Resurrect
	"""
	game = prepare_game()
	resurrect = game.player1.give("BRM_017")
	pyromancer = game.player1.give("NEW1_020")
	pyromancer.play()
	game.player1.give(MOONFIRE).play(target=pyromancer)
	assert pyromancer.dead

	game.player1.give(WISP).play()
	assert len(game.player1.field) == 1

	resurrect.play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == pyromancer.id
	assert game.player1.field[0].health == 1


def test_majordomo_executus():
	game = prepare_game(WARRIOR, WARRIOR)
	game.end_turn(); game.end_turn()

	majordomo = game.player1.give("BRM_027")
	majordomo.play()
	game.end_turn(); game.end_turn()

	game.player1.hero.power.use()
	assert game.player1.hero.power.exhausted
	assert game.player1.hero.armor == 2
	assert game.player1.hero.health == 30
	majordomo.destroy()
	assert game.player1.hero.armor == 0
	assert game.player1.hero.health == 8
	assert game.player1.hero.power.id == "BRM_027p"
	assert not game.player1.hero.power.exhausted
	game.current_player.hero.power.use()
	assert game.player1.hero.power.exhausted
	assert game.player2.hero.health == 22


def test_quick_shot():
	game = prepare_game(HUNTER, HUNTER)
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	quickshot1 = game.player1.give("BRM_013")
	wisp = game.player1.give("CS2_231")
	wisp.play()
	quickshot1.play(target=wisp)
	assert wisp.dead
	assert len(game.player1.hand) == 1
	quickshot2 = game.player1.give("BRM_013")
	quickshot2.play(target=game.current_player.opponent.hero)
	assert game.current_player.opponent.hero.health == 27
	assert len(game.player1.hand) == 1


def test_quick_shot_acolyte():
	game = prepare_game(HUNTER, HUNTER)
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	quickshot = game.player1.give("BRM_013")
	acolyte = game.player1.give("EX1_007")
	acolyte.play()
	assert len(game.player1.hand) == 1
	quickshot.play(target=acolyte)
	assert len(game.player1.hand) == 1
	assert acolyte.dead


def test_quick_shot_gallywix():
	game = prepare_game()
	gallywix = game.player1.give("GVG_028")
	gallywix.play()
	game.end_turn()

	game.player2.discard_hand()
	assert len(game.player2.hand) == 0
	quickshot = game.player2.give("BRM_013")
	assert len(game.player2.hand) == 1
	quickshot.play(target=game.current_player.opponent.hero)
	assert len(game.player2.hand) == 1
	assert game.player2.hand[0].id == "GVG_028t"


def test_avenge():
	game = prepare_game()
	avenge = game.player1.give("FP1_020")
	wisp1 = game.player1.give(WISP)
	avenge.play()
	wisp1.play()
	game.end_turn()

	stonetusk1 = game.player2.give("CS2_171")
	stonetusk1.play()
	stonetusk1.attack(wisp1)
	assert avenge in game.player1.secrets
	game.end_turn()

	wisp2 = game.player1.give(WISP)
	wisp3 = game.player1.give(WISP)
	wisp2.play()
	wisp3.play()
	game.end_turn()

	stonetusk2 = game.player2.give("CS2_171")
	stonetusk2.play()
	stonetusk2.attack(wisp3)
	assert avenge not in game.player1.secrets
	assert wisp2.atk == 4
	assert wisp2.health == 3


def test_avenge_board_clear():
	game = prepare_game()
	avenge = game.player1.give("FP1_020")
	wisp1 = game.player1.give(WISP)
	wisp2 = game.player1.give(WISP)
	avenge.play()
	wisp1.play()
	wisp2.play()
	game.end_turn()

	arcane = game.player2.give("CS2_025")
	arcane.play()
	assert avenge in game.player1.secrets


def test_eye_for_eye():
	game = prepare_game()
	eye_for_eye1 = game.player1.give("EX1_132")
	eye_for_eye1.play()
	game.end_turn()

	stonetusk = game.player2.give("CS2_171")
	eye_for_eye2 = game.player2.give("EX1_132")
	stonetusk.play()
	stonetusk.attack(game.player1.hero)
	assert game.player1.hero.health == 29
	assert game.player2.hero.health == 29
	eye_for_eye2.play()
	game.end_turn()

	hammer = game.player1.give("CS2_094")
	hammer.play(target=game.player2.hero)
	assert game.player2.hero.health == 26
	assert game.player1.hero.health == 26


def test_repentance():
	game = prepare_game()
	repentance = game.player1.give("EX1_379")
	repentance.play()
	game.end_turn()

	spellbendert1 = game.player2.summon(SPELLBENDERT)
	assert repentance in game.player1.secrets
	assert spellbendert1.health == 3
	assert spellbendert1.max_health == 3

	spellbendert2 = game.player2.give(SPELLBENDERT)
	spellbendert2.play()
	assert repentance not in game.player1.secrets
	assert spellbendert2.health == 1
	assert spellbendert2.max_health == 1


def test_revenge():
	game = prepare_game()
	dummy1 = game.player1.summon(TARGET_DUMMY)
	assert dummy1.health == 2
	assert game.player1.hero.health == 30
	game.player1.give("BRM_015").play()
	assert dummy1.health == 1
	assert game.player1.hero.health == 30
	dummy2 = game.player1.summon(TARGET_DUMMY)
	game.player1.hero.set_current_health(12)
	assert dummy2.health == 2
	game.player1.give("BRM_015").play()
	assert dummy1.dead
	assert dummy2.dead


def test_faceless_manipulator():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	motw = game.player1.give("CS2_009")
	motw.play(target=wisp)
	assert wisp.atk == 1 + 2
	assert wisp.health == 1 + 2
	assert wisp.taunt
	game.player1.give(MOONFIRE).play(target=wisp)
	assert wisp.health == 1 + 2 - 1
	game.end_turn()

	faceless = game.player2.give("EX1_564")
	faceless.play(target=wisp)
	morphed = game.player2.field[0]
	assert morphed.id == WISP
	assert morphed.buffs
	assert wisp.atk == morphed.atk
	assert wisp.health == morphed.health
	assert wisp.max_health == morphed.max_health
	assert morphed.buffs


def test_fel_reaver():
	game = prepare_game()
	expected_size = len(game.player1.deck)
	felreaver = game.player1.give("GVG_016")
	felreaver.play()
	game.end_turn()

	for i in range(5):
		game.player2.give(WISP).play()
		expected_size -= 3
		assert len(game.player1.deck) == expected_size
		assert len(game.player2.deck) == 25


def test_snipe():
	game = prepare_game(HUNTER, HUNTER)
	snipe1 = game.player1.give("EX1_609")
	snipe1.play()
	game.end_turn()

	tidehunter = game.player2.give("EX1_506")
	tidehunter.play()
	assert tidehunter.dead
	assert len(game.player2.field) == 1
	snipe2 = game.player2.give("EX1_609")
	snipe2.play()
	game.end_turn()

	watcher = game.player1.give("EX1_045")
	watcher.play()
	assert not watcher.can_attack()
	assert not watcher.dead
	assert watcher.health == 1


def test_snake_trap():
	game = prepare_game(HUNTER, HUNTER)
	snaketrap = game.player1.give("EX1_554")
	wisp = game.player1.give(WISP)
	snaketrap.play()
	wisp.play()
	game.end_turn()

	stonetusk = game.player2.give("CS2_171")
	stonetusk.play().attack(wisp)
	assert len(game.player2.field) == 0
	assert game.player1.field.contains("EX1_554t")
	assert len(game.player1.field) == 3
	assert stonetusk.health == 1
	assert wisp.dead


def test_feign_death():
	game = prepare_game(HUNTER, HUNTER)
	game.player1.discard_hand()
	feigndeath = game.player1.give("GVG_026")
	hauntedcreeper = game.player1.give("FP1_002")
	webspinner = game.player1.give("FP1_011")
	hauntedcreeper.play()
	webspinner.play()
	feigndeath.play()
	assert not hauntedcreeper.dead
	assert not webspinner.dead
	assert len(game.player1.field) == 4
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.BEAST


def test_feign_death_baron_rivendare():
	game = prepare_game(HUNTER, HUNTER)
	feigndeath = game.player1.give("GVG_026")
	rivendare = game.player1.give("FP1_031")
	rivendare.play()
	hauntedcreeper = game.player1.give("FP1_002")
	hauntedcreeper.play()
	feigndeath.play()
	assert not hauntedcreeper.dead
	assert len(game.player1.field) == 6


def test_explosive_trap():
	game = prepare_game(HUNTER, HUNTER)
	explosivetrap = game.player1.give("EX1_610")
	explosivetrap.play()
	huffer = game.player1.give("NEW1_034")
	huffer.play()
	huffer.attack(game.player2.hero)
	assert game.player2.hero.health == 26
	assert game.player1.hero.health == 30
	assert not huffer.dead
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.end_turn(); game.end_turn()

	assert len(game.player2.field) == 4
	wisp.attack(game.player1.hero)
	assert explosivetrap.dead
	assert len(game.player2.field) == 0
	assert game.player2.hero.health == 24
	assert game.player1.hero.health == 30


def test_explosive_trap_weapon():
	game = prepare_game()
	explosivetrap = game.player1.give("EX1_610")
	explosivetrap.play()
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	# Fiery War Axe
	game.player2.give("CS2_106").play()
	assert not wisp.dead
	game.player2.hero.attack(game.player1.hero)
	assert wisp.dead


def test_stalagg_feugen():
	game = prepare_game()
	stalagg1 = game.player1.give("FP1_014")
	stalagg2 = game.player1.give("FP1_014")
	feugen = game.player1.give("FP1_015")
	stalagg1.play()
	stalagg2.play()

	stalagg1.destroy()
	assert stalagg1.dead
	stalagg2.destroy()
	assert stalagg2.dead
	assert len(game.player1.field) == 0
	game.end_turn(); game.end_turn()

	feugen.play()
	feugen.destroy()
	assert feugen.dead
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "FP1_014t"


def test_stalagg_feugen_both_killed():
	game = prepare_game()
	stalagg = game.player1.give("FP1_014")
	stalagg.play()
	game.end_turn()

	feugen = game.player2.give("FP1_015")
	feugen.play()
	game.end_turn()

	stalagg.attack(feugen)
	assert stalagg.dead
	assert feugen.dead
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 1
	assert game.player1.field[0].id == "FP1_014t"
	assert game.player2.field[0].id == "FP1_014t"


def test_blackwing_corruptor():
	game = prepare_game()
	game.player1.discard_hand()
	blackwing1 = game.player1.give("BRM_034")
	blackwing1.play()
	assert blackwing1.health == 4
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	assert len(game.player1.hand) == 0
	game.end_turn()

	game.player2.discard_hand()
	game.player2.give(WHELP)
	blackwing2 = game.player2.give("BRM_034")
	blackwing2.play(target=game.player1.hero)
	assert game.player1.hero.health == 27


def test_blackwing_technician():
	game = prepare_game()
	game.player1.discard_hand()
	blackwing1 = game.player1.give("BRM_033")
	blackwing1.play()
	assert not blackwing1.buffs
	assert blackwing1.atk == 2
	assert blackwing1.health == 4

	game.player1.give(WHELP)
	blackwing2 = game.player1.give("BRM_033")
	blackwing2.play()
	assert blackwing2.buffs
	assert blackwing2.atk == 3
	assert blackwing2.health == 5


def test_crackle():
	game = prepare_game(SHAMAN, SHAMAN)
	crackle = game.player1.give("GVG_038")
	crackle.play(target=game.player2.hero)
	assert game.player2.hero.health in (24, 25, 26, 27)
	assert game.player1.overloaded == 1


def test_crackle_malygos():
	game = prepare_game(SHAMAN, SHAMAN)
	malygos = game.player1.give("EX1_563")
	malygos.play()
	game.end_turn(); game.end_turn()

	crackle = game.player1.give("GVG_038")
	crackle.play(target=game.player2.hero)
	assert game.player2.hero.health in (19, 20, 21, 22)
	assert game.player1.overloaded == 1


def test_i_am_murloc():
	game = prepare_game()
	iammurloc = game.player1.give("PRO_001a")
	iammurloc.play()
	assert len(game.player1.field) in (3, 4, 5)
	assert game.player1.field[0].id == "PRO_001at"


def test_powermace():
	game = prepare_game()

	wisp = game.player1.give(WISP)
	wisp.play()
	powermace1 = game.player1.give("GVG_036")
	powermace1.play()
	assert wisp.atk == 1
	assert wisp.health == 1
	powermace1.destroy()
	assert wisp.atk == 1
	assert wisp.health == 1

	dummy = game.player1.give(TARGET_DUMMY)
	dummy.play()
	powermace2 = game.player1.give("GVG_036")
	powermace2.play()
	assert dummy.atk == 0
	assert dummy.health == 2
	powermace2.destroy()
	assert dummy.atk == 0 + 2
	assert dummy.health == 2 + 2


def main():
	for name, f in globals().items():
		if name.startswith("test_") and callable(f):
			f()
	print("All tests ran OK")


if __name__ == "__main__":
	main()
