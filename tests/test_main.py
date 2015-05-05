#!/usr/bin/env python
import sys; sys.path.append("..")
import logging
import random
from fireplace.heroes import *
from fireplace.enums import *
from fireplace.game import Game
from fireplace.player import Player
from fireplace.utils import randomDraft


GOLDSHIRE_FOOTMAN = "CS1_042"
TARGET_DUMMY = "GVG_093"
MOONFIRE = "CS2_008"
WISP = "CS2_231"
CIRCLE_OF_HEALING = "EX1_621"
DREAM = "DREAM_04"
SILENCE = "EX1_332"
SPELLBENDERT = "tt_010a"
THE_COIN = "GAME_005"
TIME_REWINDER = "PART_002"
RESTORE_1 = "XXX_003"

logging.getLogger().setLevel(logging.DEBUG)


_draftcache = {}
def _draft(hero, exclude):
	# randomDraft() is fairly slow, this caches the drafts
	if (hero, exclude) not in _draftcache:
		_draftcache[(hero, exclude)] = randomDraft(hero, exclude)
	return _draftcache[(hero, exclude)]


def prepare_game(hero1=MAGE, hero2=WARRIOR, exclude=()):
	print("Initializing a new game")
	deck1 = _draft(hero=hero1, exclude=exclude)
	deck2 = _draft(hero=hero2, exclude=exclude)
	player1 = Player(name="Player1")
	player1.prepareDeck(deck1, hero1)
	player2 = Player(name="Player2")
	player2.prepareDeck(deck2, hero2)
	game = Game(players=(player1, player2))
	game.start()

	return game


def test_positioning():
	game = prepare_game()
	wisp1 = game.currentPlayer.give(WISP)
	wisp1.play()
	wisp2 = game.currentPlayer.give(WISP)
	wisp2.play()
	wisp3 = game.currentPlayer.give(WISP)
	wisp3.play()

	assert wisp1.adjacentMinions == [wisp2]
	assert wisp2.adjacentMinions == [wisp1, wisp3]
	assert wisp3.adjacentMinions == [wisp2]
	game.endTurn(); game.endTurn()
	flametongue = game.currentPlayer.give("EX1_565")
	flametongue.play()
	wisp4 = game.currentPlayer.give(WISP)
	wisp4.play()
	assert flametongue.aura
	assert wisp3.buffs, wisp3.buffs
	assert wisp1.atk == 1, wisp1.atk
	assert wisp2.atk == 1
	assert wisp3.atk == 3, wisp3.atk
	assert flametongue.atk == 0, flametongue.atk
	assert flametongue.adjacentMinions == [wisp3, wisp4]
	assert wisp4.atk == 3, wisp4.atk


def test_armor():
	game = prepare_game(WARRIOR, WARRIOR)
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	assert game.currentPlayer.hero.armor == 0
	assert not game.currentPlayer.hero.power.exhausted
	assert game.currentPlayer.hero.power.isPlayable()
	game.currentPlayer.hero.power.play()
	assert game.currentPlayer.hero.power.exhausted
	assert not game.currentPlayer.hero.power.isPlayable()
	assert game.currentPlayer.hero.armor == 2
	assert game.currentPlayer.mana == 2
	game.endTurn()
	axe = game.currentPlayer.give("CS2_106")
	axe.play()
	assert axe is game.currentPlayer.weapon
	assert axe in game.currentPlayer.hero.slots
	assert game.currentPlayer.hero.atk == 3
	game.currentPlayer.hero.attack(game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 29
	assert game.currentPlayer.opponent.hero.armor == 0


def test_freeze():
	game = prepare_game()
	flameimp = game.currentPlayer.give("EX1_319")
	flameimp.play()
	game.endTurn()

	frostshock = game.currentPlayer.give("CS2_037")
	frostshock.play(target=flameimp)
	assert flameimp.frozen
	game.endTurn()

	assert flameimp.frozen
	assert not flameimp.canAttack()
	game.endTurn()
	assert not flameimp.frozen
	game.endTurn()

	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	wisp.frozen = True
	assert wisp.frozen
	game.endTurn()
	assert not wisp.frozen


def test_spell_power():
	game = prepare_game(HUNTER, HUNTER)
	game.endTurn(); game.endTurn()

	expectedHealth = 30
	assert game.player2.hero.health == expectedHealth
	game.currentPlayer.give(MOONFIRE).play(target=game.player2.hero); expectedHealth -= 1
	assert game.player2.hero.health == expectedHealth
	# Play a kobold
	assert game.currentPlayer.spellpower == 0
	game.currentPlayer.give("CS2_142").play()
	assert game.currentPlayer.spellpower == 1
	game.currentPlayer.give(MOONFIRE).play(target=game.player2.hero); expectedHealth -= 1+1
	assert game.player2.hero.health == expectedHealth
	# Summon Malygos
	malygos = game.currentPlayer.summon("EX1_563")
	assert game.currentPlayer.spellpower == 1 + 5
	game.currentPlayer.give(MOONFIRE).play(target=game.player2.hero); expectedHealth -= 1+1+5
	assert game.player2.hero.health == expectedHealth
	# Test heals are not affected
	game.currentPlayer.give(RESTORE_1).play(target=game.player2.hero); expectedHealth += 1
	assert game.player2.hero.health == expectedHealth
	game.endTurn(); game.endTurn()

	# Check hero power is unaffected
	game.currentPlayer.hero.power.play(); expectedHealth -= 2
	assert game.player2.hero.health == expectedHealth
	# Check battlecries are unaffected
	game.currentPlayer.give("CS2_189").play(target=game.player2.hero); expectedHealth -= 1
	assert game.player2.hero.health == expectedHealth

	game.endTurn(); game.endTurn()
	malygos.destroy()
	# Check arcane missiles doesn't wreck everything
	game.currentPlayer.give("EX1_277").play(); expectedHealth -= 3+1
	assert game.player2.hero.health == expectedHealth


def test_mage():
	game = prepare_game(MAGE, MAGE)
	assert game.currentPlayer.hero.id is MAGE
	game.endTurn(); game.endTurn()

	assert game.currentPlayer.hero.health == 30
	assert game.currentPlayer.opponent.hero.health == 30
	assert game.currentPlayer.timesHeroPowerUsedThisGame == 0

	# Fireblast the opponent hero
	game.currentPlayer.hero.power.play(target=game.currentPlayer.opponent.hero)
	assert game.currentPlayer.hero.health == 30
	assert game.currentPlayer.opponent.hero.health == 29
	assert game.currentPlayer.timesHeroPowerUsedThisGame == 1
	assert not game.currentPlayer.hero.power.isPlayable()


def test_priest():
	game = prepare_game(PRIEST, PRIEST)
	assert game.currentPlayer.hero.id is PRIEST
	game.endTurn(); game.endTurn()
	# Heal self
	assert game.currentPlayer.hero.health == 30
	game.currentPlayer.hero.power.play(target=game.currentPlayer.hero)
	assert game.currentPlayer.hero.health == 30

	game.endTurn(); game.endTurn()
	# moonfire self
	moonfire = game.currentPlayer.give(MOONFIRE)
	moonfire.play(target=game.currentPlayer.hero)
	assert game.currentPlayer.lastCardPlayed == moonfire
	assert game.currentPlayer.hero.health == 29
	game.currentPlayer.hero.power.play(target=game.currentPlayer.hero)
	assert game.currentPlayer.hero.health == 30
	assert not game.currentPlayer.hero.power.isPlayable()


def test_shaman():
	game = prepare_game(SHAMAN, SHAMAN)
	assert game.currentPlayer.hero.id is SHAMAN
	game.endTurn(); game.endTurn()
	assert len(game.currentPlayer.hero.power.data.entourage) == 4
	game.currentPlayer.hero.power.play()
	assert game.currentPlayer.field[0].id in ("CS2_050", "CS2_051", "CS2_052", "NEW1_009")


def test_paladin():
	game = prepare_game(PALADIN, PALADIN)
	assert game.currentPlayer.hero.id is PALADIN
	game.endTurn(); game.endTurn()
	game.currentPlayer.hero.power.play()
	assert len(game.board) == 1
	assert len(game.currentPlayer.field) == 1
	assert game.currentPlayer.field[0].id == "CS2_101t"


def test_deathrattle():
	game = prepare_game()
	game.endTurn(); game.endTurn()

	loothoarder = game.currentPlayer.give("EX1_096")
	loothoarder.play()
	cardcount = len(game.currentPlayer.hand)
	game.endTurn()

	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=loothoarder)
	assert loothoarder.dead
	assert loothoarder.damage == 0
	assert len(game.currentPlayer.opponent.hand) == cardcount + 1
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	# test soul of the forest: deathrattle in slots
	assert not archer.hasDeathrattle
	sotf = game.currentPlayer.give("EX1_158")
	sotf.play()
	assert len(archer.buffs) == 1
	assert archer.buffs[0].hasDeathrattle
	assert archer.hasDeathrattle
	assert len(game.currentPlayer.field) == 1
	game.currentPlayer.give(MOONFIRE).play(target=archer)
	assert archer.dead
	assert len(game.currentPlayer.field) == 1


def test_cogmaster():
	game = prepare_game()
	cogmaster = game.currentPlayer.give("GVG_013")
	cogmaster.play()
	assert cogmaster.atk == 1
	game.endTurn(); game.endTurn()

	dummy = game.currentPlayer.give(TARGET_DUMMY)
	dummy.play()
	assert cogmaster.atk == 3
	humility = game.currentPlayer.give("EX1_360")
	humility.play(target=cogmaster)
	assert cogmaster.atk == 3
	dummy.destroy()
	assert cogmaster.atk == 1
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	game.currentPlayer.give(TARGET_DUMMY).play()
	assert cogmaster.atk == 3
	blessedchamp = game.currentPlayer.give("EX1_355")
	blessedchamp.play(target=cogmaster)
	cogmaster.atk == 6


def test_cogmasters_wrench():
	game = prepare_game()
	wrench = game.currentPlayer.summon("GVG_024")
	assert wrench.atk == game.currentPlayer.hero.atk == 1
	game.endTurn(); game.endTurn()

	dummy = game.currentPlayer.give(TARGET_DUMMY)
	dummy.play()
	assert wrench.atk == game.currentPlayer.hero.atk == 3
	dummy.destroy()
	assert wrench.atk == game.currentPlayer.hero.atk == 1


def test_cult_master():
	game = prepare_game()
	cultmaster = game.currentPlayer.give("EX1_595")

	wisp1 = game.currentPlayer.give(WISP)
	wisp1.play()
	wisp2 = game.currentPlayer.give(WISP)
	wisp2.play()

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	cultmaster.play()
	assert len(game.currentPlayer.hand) == 7
	game.currentPlayer.give(MOONFIRE).play(target=wisp1)
	assert len(game.currentPlayer.hand) == 8

	# Make sure cult master doesn't draw off itself
	game.currentPlayer.give(MOONFIRE).play(target=cultmaster)
	game.currentPlayer.give(MOONFIRE).play(target=cultmaster)
	assert len(game.currentPlayer.hand) == 8

	game.currentPlayer.give(MOONFIRE).play(target=wisp2)
	assert len(game.currentPlayer.hand) == 8


def test_mana():
	game = prepare_game()
	footman = game.currentPlayer.give(GOLDSHIRE_FOOTMAN)
	assert footman.cost == 1
	footman.play()
	assert footman.atk == 1
	assert footman.health == 2
	game.endTurn()

	# Play the coin
	coin = game.currentPlayer.getById(THE_COIN)
	coin.play()
	assert game.currentPlayer.mana == 2
	assert game.currentPlayer.tempMana == 1
	game.endTurn()
	assert game.currentPlayer.opponent.tempMana == 0
	assert game.currentPlayer.opponent.mana == 1, game.currentPlayer.opponent.mana

	game.endTurn(); game.endTurn()

	assert game.currentPlayer.mana == 3
	assert game.currentPlayer.maxMana == 3
	felguard = game.currentPlayer.give("EX1_301")
	felguard.play()
	assert game.currentPlayer.mana == 0, game.currentPlayer.mana
	assert game.currentPlayer.maxMana == 2, game.currentPlayer.maxMana


def test_overload():
	game = prepare_game()
	dustdevil = game.currentPlayer.give("EX1_243")
	dustdevil.play()
	assert game.currentPlayer.overloaded == 2
	game.endTurn(); game.endTurn()
	assert game.currentPlayer.mana == 0


def test_charge():
	game = prepare_game()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	assert not wisp.charge
	assert not wisp.canAttack()
	# play Charge on wisp
	game.currentPlayer.give("CS2_103").play(target=wisp)
	assert wisp.buffs[0].tags[GameTag.CHARGE]
	assert wisp.charge
	assert wisp.canAttack()
	wisp.attack(game.currentPlayer.opponent.hero)
	assert not wisp.canAttack()
	game.endTurn()
	game.currentPlayer.getById(THE_COIN).play()
	wolfrider = game.currentPlayer.give("CS2_124")
	wolfrider.play()
	assert wolfrider.charge
	assert wolfrider.canAttack()
	game.endTurn()
	assert wisp.canAttack()
	wisp.attack(game.currentPlayer.opponent.hero)
	assert not wisp.canAttack()
	game.endTurn()
	watcher = game.currentPlayer.give("EX1_045")
	watcher.play()
	assert not watcher.canAttack()
	game.currentPlayer.give("CS2_103").play(target=watcher)
	assert not watcher.canAttack()
	game.endTurn(); game.endTurn()
	assert not watcher.canAttack()
	watcher.silence()
	assert watcher.canAttack()


def test_divine_shield():
	game = prepare_game()
	squire = game.currentPlayer.give("EX1_008")
	squire.play()
	assert squire.divineShield
	game.endTurn()

	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=squire)
	assert len(game.currentPlayer.field) == 1
	assert not squire.divineShield
	game.currentPlayer.getById(THE_COIN).play()
	archer2 = game.currentPlayer.give("CS2_189")
	archer2.play(target=squire)
	assert len(game.currentPlayer.opponent.field) == 0
	assert not squire.divineShield


def test_divine_spirit():
	game = prepare_game()
	wisp = game.currentPlayer.give(WISP)
	assert wisp.health == 1
	wisp.play()
	game.endTurn()

	game.currentPlayer.give("CS2_236").play(target=wisp)
	assert wisp.health == 1 * 2
	game.endTurn()

	game.currentPlayer.give("CS2_236").play(target=wisp)
	assert wisp.health == 1 * 2 * 2
	game.endTurn()

	equality = game.currentPlayer.give("EX1_619")
	equality.play()
	assert wisp.health == 1
	game.currentPlayer.give("CS2_236").play(target=wisp)
	assert wisp.health == 1 * 2
	game.endTurn()


def test_silence():
	game = prepare_game()
	silence = game.currentPlayer.give(SILENCE)
	thrallmar = game.currentPlayer.give("EX1_021")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	thrallmar.play()
	assert not thrallmar.silenced
	assert thrallmar.windfury
	silence.play(target=thrallmar)
	assert thrallmar.silenced
	assert not thrallmar.windfury


def test_earth_shock():
	game = prepare_game()
	crusader = game.currentPlayer.give("EX1_020")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	crusader.play()
	assert crusader.divineShield
	game.endTurn()
	earthshock = game.currentPlayer.give("EX1_245")
	earthshock.play(target=crusader)
	assert crusader.dead


def test_eaglehorn_bow():
	game = prepare_game()
	bow = game.player1.give("EX1_536")
	icebarrier = game.player1.give("EX1_289")
	wisp = game.player2.give(WISP)
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	bow.play()
	assert bow.durability == 2
	game.endTurn()

	wisp.play()
	game.endTurn()

	icebarrier.play()
	assert bow.durability == 2
	game.endTurn()

	assert game.currentPlayer.opponent.secrets
	wisp.attack(target=game.player1.hero)
	assert not game.currentPlayer.opponent.secrets
	assert game.player1.hero.health == 30
	assert game.player1.hero.armor == 7
	assert bow.buffs
	assert bow.durability == 3


def test_equality():
	game = prepare_game()
	equality = game.currentPlayer.give("EX1_619")
	# summon a bunch of big dudes
	game.currentPlayer.summon("CS2_186")
	game.currentPlayer.summon("CS2_186")
	game.currentPlayer.opponent.summon("CS2_186")
	game.currentPlayer.opponent.summon("CS2_186")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	# And a violet teacher too, why not
	game.currentPlayer.summon("NEW1_026")

	pyro = game.currentPlayer.give("NEW1_020")
	pyro.play()
	assert len(game.board) == 6
	equality.play()
	assert not game.board


def test_stealth_windfury():
	game = prepare_game(MAGE, MAGE)
	worgen = game.currentPlayer.give("EX1_010")
	worgen.play()
	assert worgen.stealthed
	assert not worgen.canAttack()
	game.endTurn()

	archer = game.currentPlayer.give("CS2_189")
	assert len(archer.targets) == 2  # Only the heroes
	game.currentPlayer.getById(THE_COIN).play()
	assert len(game.currentPlayer.hero.power.targets) == 2
	game.endTurn()

	worgen.attack(game.currentPlayer.opponent.hero)
	assert not worgen.stealthed
	assert not worgen.canAttack()
	windfury = game.currentPlayer.give("CS2_039")
	windfury.play(target=worgen)
	assert worgen.canAttack()
	worgen.attack(game.currentPlayer.opponent.hero)
	assert not worgen.canAttack()
	game.endTurn()

	assert len(archer.targets) == 3


def test_tags():
	game = prepare_game()

	alakir = game.currentPlayer.give("NEW1_010")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	alakir.play()
	assert alakir.tags[GameTag.CHARGE]
	assert alakir.charge
	assert alakir.tags[GameTag.DIVINE_SHIELD]
	assert alakir.divineShield
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
	game.endTurn(); game.endTurn()

	assert wisp1.canAttack()
	assert wisp1.targets == [wisp2, game.player2.hero]
	game.endTurn()

	goldshire2.play()
	game.endTurn()

	assert wisp1.targets == [goldshire2]
	goldshire1.play()
	game.endTurn()

	assert wisp2.targets == [goldshire1]


def test_card_draw():
	game = prepare_game()
	# pass turn 1
	game.endTurn(); game.endTurn()

	assert game.currentPlayer.cardsDrawnThisTurn == 1
	assert len(game.currentPlayer.hand) == 5
	novice = game.currentPlayer.give("EX1_015")
	assert len(game.currentPlayer.hand) == 6
	# novice should draw 1 card
	novice.play()
	# hand should be 1 card played, 1 card drawn; same size
	assert len(game.currentPlayer.hand) == 6
	assert game.currentPlayer.cardsDrawnThisTurn == 2
	game.endTurn()

	# succubus should discard 1 card
	card = game.currentPlayer.give("EX1_306")
	handlength = len(game.currentPlayer.hand)
	card.play()
	assert len(game.currentPlayer.hand) == handlength - 2


def test_deadly_poison():
	game = prepare_game(ROGUE, ROGUE)
	poison = game.currentPlayer.give("CS2_074")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert not poison.isPlayable()
	game.currentPlayer.hero.power.play()
	assert game.currentPlayer.weapon.atk == 1
	assert game.currentPlayer.hero.atk == 1
	assert poison.isPlayable()
	poison.play()
	assert game.currentPlayer.weapon.atk == 3
	assert game.currentPlayer.hero.atk == 3


def test_deathwing():
	game = prepare_game()
	deathwing = game.currentPlayer.give("NEW1_030")
	# play some wisps
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()

	# fast-forward to turn 10
	for i in range(9 * 2):
		game.endTurn()

	deathwing.play()
	assert not game.currentPlayer.hand
	assert len(game.board) == 1


def test_combo():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.endTurn()
	game.currentPlayer.getById(THE_COIN).play()
	# SI:7 with combo
	assert game.currentPlayer.combo
	game.currentPlayer.give("EX1_134").play(target=game.currentPlayer.hero)
	assert game.currentPlayer.hero.health == 28
	game.endTurn()

	# Without combo should not have a target
	assert not game.currentPlayer.combo
	game.currentPlayer.give("EX1_134").play()


def test_morph():
	game = prepare_game()
	game.player1.discardHand()
	game.player2.discardHand()
	buzzard = game.player2.summon("CS2_237")
	wisp = game.player2.summon(WISP)
	assert not game.player1.hand
	assert not game.player2.hand
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert len(game.player2.hand) == 2
	hex = game.player1.give("EX1_246")
	hex.play(target=wisp)
	assert not game.player2.field.contains(WISP)
	assert game.player2.field.contains("hexfrog")
	# Test that buzzard no longer draws on poly/hex (fixed in GVG)
	assert len(game.player2.hand) == 2
	game.endTurn(); game.endTurn()

	assert len(game.player2.hand) == 3
	polymorph = game.player1.give("CS2_022")
	polymorph.play(target=game.player2.field[-1])
	assert game.player2.field[-1].id == "CS2_tk1"
	assert len(game.currentPlayer.opponent.hand) == 3


def test_power_word_shield():
	game = prepare_game()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	assert wisp.health == 1
	assert len(game.currentPlayer.hand) == 4

	pwshield = game.currentPlayer.give("CS2_004")
	pwshield.play(target=wisp)
	assert wisp.health == 3
	assert len(game.currentPlayer.hand) == 5

	wisp.silence()
	assert wisp.health == 1


def test_preparation():
	game = prepare_game()
	game.player1.discardHand()
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
	game.endTurn(); game.endTurn()

	assert game.player1.mana == 2
	prep1.play()
	assert game.player1.mana == 2
	assert prep2.cost == prep3.cost == 0
	assert pwshield.cost == 0
	assert fireball.cost == 4 - 3
	assert fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	prep2.play()
	assert game.player1.mana == 2
	assert prep2.cost == prep3.cost == 0
	assert pwshield.cost == 0
	assert fireball.cost == 4 - 3
	assert fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	fireball.play(target=game.player2.hero)
	assert game.player1.mana == 1
	assert pwshield.cost == 1
	assert fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	prep3.play()
	assert pwshield.cost == 0
	assert footman.cost == footman2.cost == 1
	game.endTurn()
	assert pwshield.cost == 1
	assert footman.cost == footman2.cost == 1


def test_kill_command():
	game = prepare_game(HUNTER, HUNTER)
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	kc = game.currentPlayer.give("EX1_539")
	kc.play(target=game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 27
	game.endTurn(); game.endTurn()

	# play a timber wolf before this time
	game.currentPlayer.give("DS1_175").play()
	kc = game.currentPlayer.give("EX1_539")
	kc.play(target=game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 22


def test_animal_companion():
	game = prepare_game()
	companion = game.player1.give("NEW1_031")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	companion.play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id in ("NEW1_032", "NEW1_033", "NEW1_034")


def test_ancestors_call():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	game.player1.discardHand()
	game.player2.discardHand()
	novice = game.player1.give("EX1_015")
	wisp = game.player2.give(WISP)
	call = game.currentPlayer.give("GVG_029")
	call.play()
	assert novice in game.player1.field
	assert wisp in game.player2.field
	assert not game.player1.hand
	assert not game.player2.hand


def test_ancestral_healing():
	game = prepare_game()
	ancestral = game.currentPlayer.give("CS2_041")
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	assert not wisp.taunt
	ancestral.play(wisp)
	assert wisp.health == 1
	assert wisp.taunt


def test_ancestral_spirit():
	game = prepare_game()
	game.endTurn(); game.endTurn()

	ancestral = game.player1.give("CS2_038")
	wisp = game.player1.give(WISP)
	wisp.play()
	assert not wisp.hasDeathrattle
	ancestral.play(target=wisp)
	assert wisp.hasDeathrattle
	wisp.destroy()
	assert len(game.board) == 1
	assert game.player1.field[0].id == WISP


def test_ancient_of_lore():
	game = prepare_game()
	ancient1 = game.currentPlayer.give("NEW1_008")
	ancient2 = game.currentPlayer.give("NEW1_008")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	game.currentPlayer.discardHand()
	# damage the hero with 6 moonfires

	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	assert game.currentPlayer.hero.health == 30 - 6

	ancient1 = game.currentPlayer.give("NEW1_008")
	assert len(game.currentPlayer.hand) == 1
	assert ancient1.cost == 7
	# Play to draw 2 cards
	ancient1.play(choose="NEW1_008a")
	assert len(game.currentPlayer.hand) == 2
	assert game.currentPlayer.hero.health == 30 - 6
	game.endTurn(); game.endTurn()

	game.currentPlayer.discardHand()
	ancient2 = game.currentPlayer.give("NEW1_008")
	# Play to heal hero by 5
	ancient2.play(target=game.currentPlayer.hero, choose="NEW1_008b")
	assert not game.currentPlayer.hand
	assert game.currentPlayer.hero.health == 30 - 6 + 5


def test_alarmobot():
	game = prepare_game()
	bot = game.currentPlayer.give("EX1_006")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	bot.play()
	game.currentPlayer.discardHand()
	wisp = game.currentPlayer.give(WISP)
	for i in range(9):
		game.currentPlayer.give(MOONFIRE)
	assert len(game.currentPlayer.hand) == 10
	assert bot.zone == Zone.PLAY
	assert wisp.zone == Zone.HAND
	game.endTurn(); game.endTurn()
	assert bot.zone == Zone.HAND
	assert wisp.zone == Zone.PLAY
	assert len(game.currentPlayer.field) == 1
	assert len(game.currentPlayer.hand) == 10

	# bot should not trigger if hand has no minions
	bot.play()
	game.currentPlayer.give(MOONFIRE)
	assert len(game.currentPlayer.hand) == 10
	game.endTurn(); game.endTurn()
	assert len(game.currentPlayer.hand) == 10
	assert bot.zone == Zone.PLAY
	assert len(game.currentPlayer.field) == 2


def test_avenging_wrath():
	game = prepare_game()
	game.currentPlayer.give("EX1_384")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.currentPlayer.give("EX1_384").play()
	assert game.currentPlayer.opponent.hero.health == 30 - 8

	game.endTurn()
	# Summon Malygos and test that spellpower only increases dmg by 5
	game.currentPlayer.summon("EX1_563")
	game.currentPlayer.give("EX1_384").play()
	assert game.currentPlayer.opponent.hero.health == 30 - (8+5)


def test_doomhammer():
	game = prepare_game()
	doomhammer = game.currentPlayer.give("EX1_567")

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert not game.currentPlayer.hero.atk
	assert not game.currentPlayer.hero.windfury
	doomhammer.play()
	assert game.currentPlayer.hero.atk == 2
	assert game.currentPlayer.hero.windfury
	assert game.currentPlayer.weapon.durability == 8
	game.currentPlayer.hero.attack(target=game.currentPlayer.opponent.hero)
	assert game.currentPlayer.hero.canAttack()
	game.currentPlayer.hero.attack(target=game.currentPlayer.opponent.hero)
	assert not game.currentPlayer.hero.canAttack()
	assert game.currentPlayer.weapon.durability == 6


def test_raging_worgen():
	game = prepare_game()
	worgen = game.currentPlayer.summon("EX1_412")
	assert worgen.health == 3
	game.currentPlayer.give(MOONFIRE).play(target=worgen)
	assert worgen.health == 2
	assert worgen.atk == 4
	assert worgen.windfury
	game.currentPlayer.give(CIRCLE_OF_HEALING).play()
	assert worgen.atk == 3
	assert not worgen.windfury


def test_amani_berserker():
	game = prepare_game()
	amani1 = game.player1.give("EX1_393")
	amani2 = game.player2.give("EX1_393")
	game.endTurn(); game.endTurn()

	amani1.play()
	game.endTurn()

	amani2.play()
	game.endTurn()

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
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert secretkeeper.atk == 1
	assert secretkeeper.health == 2
	icebarrier = game.currentPlayer.give("EX1_289")
	icebarrier.play()
	assert secretkeeper.atk == 2
	assert secretkeeper.health == 3
	game.currentPlayer.give(THE_COIN).play()
	game.currentPlayer.give(WISP).play()
	assert secretkeeper.atk == 2
	assert secretkeeper.health == 3


def test_southsea_deckhand():
	game = prepare_game(ROGUE, ROGUE)
	deckhand = game.currentPlayer.give("CS2_146")
	deckhand.play()
	assert not deckhand.charge
	game.endTurn(); game.endTurn()

	# Play rogue hero power (gives a weapon)
	game.currentPlayer.hero.power.play()
	assert deckhand.charge
	game.endTurn(); game.endTurn()

	assert deckhand.charge
	axe = game.currentPlayer.give("CS2_106")
	axe.play()
	assert deckhand.charge
	axe.destroy()
	assert not deckhand.charge

	game.endTurn(); game.endTurn()
	# play charge
	game.currentPlayer.give("CS2_103").play(target=deckhand)
	assert deckhand.charge
	game.endTurn(); game.endTurn()

	assert deckhand.charge
	game.currentPlayer.hero.power.play()
	assert deckhand.charge
	game.currentPlayer.weapon.destroy()
	# No longer have weapon, but still have the charge buff from earlier
	assert deckhand.charge


def test_spiteful_smith():
	game = prepare_game()
	assert not game.currentPlayer.hero.atk
	smith = game.currentPlayer.summon("CS2_221")
	assert smith.health == 6
	assert not game.currentPlayer.hero.atk
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	axe = game.currentPlayer.give("CS2_106")
	axe.play()
	assert axe.atk == 3
	assert game.currentPlayer.hero.atk == 3
	assert not game.currentPlayer.opponent.hero.atk
	game.currentPlayer.give(MOONFIRE).play(target=smith)
	assert smith.health == 5
	assert axe.atk == 5
	assert axe.buffs
	assert game.currentPlayer.hero.atk == 5
	assert not game.currentPlayer.opponent.hero.atk
	game.currentPlayer.give(CIRCLE_OF_HEALING).play()
	assert axe.atk == 3
	assert game.currentPlayer.hero.atk == 3
	game.currentPlayer.give(MOONFIRE).play(target=smith)
	assert smith.health == 5
	assert axe.atk == 5
	assert game.currentPlayer.hero.atk == 5


def test_sword_of_justice():
	game = prepare_game(PALADIN, PALADIN)
	sword = game.currentPlayer.give("EX1_366")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	sword.play()
	assert sword.durability == 5
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	assert wisp.atk == 2
	assert wisp.health == 2
	assert wisp.buffs
	assert sword.durability == 4
	game.endTurn()

	game.currentPlayer.give(WISP).play()
	assert sword.durability == 4
	game.endTurn()

	game.currentPlayer.hero.power.play()
	assert sword.durability == 3

	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	assert not game.currentPlayer.weapon
	wisp2 = game.currentPlayer.give(WISP)
	wisp2.play()
	assert wisp2.health == 1
	assert wisp2.atk == 1
	assert not wisp2.buffs


def test_ethereal_arcanist():
	game = prepare_game()
	arcanist = game.player1.give("EX1_274")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	arcanist.play()
	assert arcanist.atk == arcanist.health == 3
	game.endTurn(); game.endTurn()

	assert arcanist.atk == arcanist.health == 3
	icebarrier = game.player1.give("EX1_289")
	icebarrier.play()
	assert arcanist.atk == arcanist.health == 3
	game.endTurn()

	assert arcanist.atk == arcanist.health == 3 + 2
	game.endTurn()

	assert arcanist.atk == arcanist.health == 3 + 2
	icebarrier.destroy()
	game.endTurn()

	assert arcanist.atk == arcanist.health == 3 + 2


def test_end_turn_heal():
	game = prepare_game()

	footman = game.currentPlayer.give(GOLDSHIRE_FOOTMAN)
	footman.play()
	assert footman.health == 2
	game.endTurn()

	# play an archer on the footman
	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=footman)
	assert footman.health == 1
	game.endTurn()

	healtotem = game.currentPlayer.give("NEW1_009")
	healtotem.play()
	game.endTurn()
	assert footman.health == 2
	game.endTurn()
	game.endTurn()
	# check it's still at max health after a couple of turns
	assert footman.health == 2


def test_crazed_alchemist():
	game = prepare_game()
	alchemist = game.currentPlayer.give("EX1_059")
	warden = game.currentPlayer.summon("EX1_396")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert warden.atk == 1
	assert not warden.damage
	assert warden.maxHealth == 7
	assert warden.health == 7
	alchemist.play(target=warden)
	assert warden.atk == 7
	assert warden.health == 1


def test_reversing_switch():
	game = prepare_game()
	switch = game.player1.give("PART_006")
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	game.endTurn(); game.endTurn()

	switch.play(goldshire)
	assert goldshire.atk == 2


def test_commanding_shout():
	game = prepare_game()
	shout = game.currentPlayer.give("NEW1_036")
	wisp1 = game.currentPlayer.give(WISP)
	wisp1.play()
	wisp2 = game.currentPlayer.give(WISP)
	bender = game.currentPlayer.give(SPELLBENDERT)
	bender.play()
	giant = game.currentPlayer.opponent.summon("EX1_620")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	assert wisp1.health == 1
	assert bender.health == 3
	assert not wisp1.minHealth
	assert not bender.minHealth
	shout.play()
	assert wisp1.minHealth == 1
	assert bender.minHealth == 1
	wisp1.attack(target=giant)
	assert giant.health == 7
	assert wisp1.health == 1
	assert not wisp1.damage
	assert wisp1.zone == Zone.PLAY
	game.currentPlayer.give(MOONFIRE).play(target=bender)
	assert bender.health == 2
	assert bender.damage == 1
	bender.attack(target=giant)
	assert bender.health == 1
	assert bender.damage == 2
	assert bender.zone == Zone.PLAY

	# TODO test that minions played afterwards still get commanding shout buff


def test_conceal():
	game = prepare_game()
	conceal = game.currentPlayer.give("EX1_128")
	wisp1 = game.currentPlayer.give(WISP)
	wisp1.play()
	wisp2 = game.currentPlayer.give(WISP)
	wisp2.play()
	conceal.play()
	assert wisp1.stealthed
	assert wisp2.stealthed
	game.endTurn()
	assert wisp1.stealthed
	assert wisp2.stealthed
	game.endTurn()
	assert not wisp1.stealthed
	assert not wisp2.stealthed


def test_cruel_taskmaster():
	game = prepare_game()
	taskmaster1 = game.currentPlayer.give("EX1_603")
	taskmaster2 = game.currentPlayer.give("EX1_603")
	game.endTurn(); game.endTurn()

	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	taskmaster1.play(target=wisp)
	assert wisp.dead
	game.endTurn(); game.endTurn()

	assert taskmaster1.health == 2
	assert taskmaster1.atk == 2
	taskmaster2.play(target=taskmaster1)
	assert taskmaster1.health == 1
	assert taskmaster1.atk == 4


def test_demolisher():
	game = prepare_game()

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	demolisher = game.currentPlayer.give("EX1_102")
	demolisher.play()

	assert game.currentPlayer.opponent.hero.health == 30
	game.endTurn()
	assert game.currentPlayer.opponent.hero.health == 30
	game.endTurn()
	assert game.currentPlayer.opponent.hero.health == 28


def test_dire_wolf_alpha():
	game = prepare_game()
	direwolf1 = game.player2.summon("EX1_162")
	assert direwolf1.atk == 2
	direwolf2 = game.player2.summon("EX1_162")
	assert direwolf1.atk == 3
	assert direwolf2.atk == 3
	frostwolf = game.currentPlayer.summon("CS2_121")
	game.endTurn(); game.endTurn();
	frostwolf.attack(direwolf2)


def test_dread_infernal():
	game = prepare_game()
	infernal =  game.currentPlayer.give("CS2_064")
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.endTurn()
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	assert len(game.board) == 6
	infernal.play()
	assert len(game.board) == 1
	assert game.currentPlayer.hero.health == 29
	assert game.currentPlayer.opponent.hero.health == 29
	assert infernal.health == 6


def test_dread_corsair():
	game = prepare_game()
	corsair = game.currentPlayer.give("NEW1_022")
	assert corsair.cost == 4
	game.currentPlayer.give(THE_COIN).play()
	axe = game.player1.give("CS2_106")
	axe.play()
	assert corsair.cost == 4 - 3
	axe.destroy()
	assert corsair.cost == 4


def test_druid_of_the_fang():
	game = prepare_game()
	fang = game.currentPlayer.give("GVG_080")
	fang2 = game.currentPlayer.give("GVG_080")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	fang.play()
	assert not fang.poweredUp
	druid = game.currentPlayer.field[0]
	assert druid.id == "GVG_080"
	assert druid.atk == 4
	assert druid.health == 4

	game.endTurn(); game.endTurn()
	assert not fang2.poweredUp
	webspinner = game.currentPlayer.give("FP1_011")
	webspinner.play()
	assert fang2.poweredUp
	fang2.play()
	druid2 = game.currentPlayer.field[-1]
	assert druid2.id == "GVG_080t"
	assert druid2.atk == 7
	assert druid2.health == 7
	assert druid2.race == Race.BEAST


def test_imp_master():
	game = prepare_game()

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	impmaster = game.currentPlayer.give("EX1_597")
	impmaster.play()

	assert impmaster.health == 5
	assert len(impmaster.controller.field) == 1
	game.endTurn()
	assert impmaster.health == 4
	assert len(impmaster.controller.field) == 2
	assert impmaster.controller.field.contains("EX1_598")


def test_auras():
	game = prepare_game()

	wisp1 = game.currentPlayer.give(WISP)
	wisp1.play()
	assert wisp1.atk == 1
	game.endTurn()

	# pass next few turns to gain some mana
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	webspinner = game.currentPlayer.give("FP1_011")
	webspinner.play()
	raidleader = game.currentPlayer.give("CS2_122")
	raidleader.play()
	assert raidleader.aura
	assert raidleader.atk == 2
	assert wisp1.atk == 1
	assert webspinner.atk == 2
	wisp2 = game.currentPlayer.give(WISP)
	wisp2.play()
	assert webspinner.atk == 2

	# Test the timber wolf (beast-only) too
	game.currentPlayer.getById(THE_COIN).play()
	timberwolf = game.currentPlayer.give("DS1_175")
	timberwolf.play()
	assert timberwolf.atk == 2 # 1 (+1 from RL)
	assert raidleader.atk == 2 # 2 (+0)
	assert len(webspinner.slots) == 2
	assert webspinner.atk == 3 # 1 (+1 from RL, +1 from TW)
	assert wisp2.atk == 2 # 1 (+1 from TW)

	timberwolf2 = game.currentPlayer.give("DS1_175")
	timberwolf2.play()
	assert timberwolf.atk == 3
	assert timberwolf2.atk == 3
	game.currentPlayer.give(MOONFIRE).play(target=timberwolf)
	timberwolf2.atk == 2
	game.currentPlayer.give(MOONFIRE).play(target=timberwolf2)


def test_bounce():
	game = prepare_game()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	assert game.currentPlayer.field == [wisp]
	game.endTurn(); game.endTurn()

	brewmaster = game.currentPlayer.give("EX1_049")
	brewmaster.play(target=wisp)
	assert game.currentPlayer.field == [brewmaster]
	assert wisp in game.currentPlayer.hand
	assert wisp.zone == Zone.HAND
	wisp.play()
	game.endTurn(); game.endTurn()

	# test for damage reset on bounce
	brewmaster2 = game.currentPlayer.give("EX1_049")
	moonfire = game.currentPlayer.give(MOONFIRE)
	moonfire.play(target=brewmaster)
	assert brewmaster.health == 1
	brewmaster2.play(target=brewmaster)
	assert brewmaster.health == 2
	assert brewmaster2.health == 2

	game.endTurn()
	# fill the hand with some bananas
	game.currentPlayer.give("EX1_014t")
	game.currentPlayer.give("EX1_014t")
	game.endTurn()
	vanish = game.currentPlayer.give("NEW1_004")
	vanish.play()
	assert brewmaster not in game.currentPlayer.opponent.hand


def test_weapon_sheathing():
	game = prepare_game()
	axe = game.player1.give("CS2_106")
	game.endTurn(); game.endTurn()

	axe.play()
	assert not axe.exhausted
	assert game.player1.hero.atk == 3
	assert game.player1.hero.canAttack()
	game.player1.hero.attack(target=game.player2.hero)
	assert not axe.exhausted
	assert game.player1.hero.atk == 3
	game.endTurn()

	assert axe.exhausted
	assert game.player1.hero.atk == 0
	assert game.player2.hero.health == 27
	game.player2.give("CS2_106").play()
	game.player2.hero.attack(target=game.player1.hero)
	assert game.player1.hero.health == 27
	assert game.player2.hero.health == 27
	game.endTurn()

	assert not axe.exhausted


def test_arcane_explosion():
	game = prepare_game(MAGE, MAGE)
	# play some wisps
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.endTurn()

	arcanex = game.currentPlayer.give("CS2_025")
	assert len(game.currentPlayer.opponent.field) == 3
	arcanex.play()
	assert len(game.currentPlayer.opponent.field) == 0


def test_arcane_missiles():
	game = prepare_game()
	missiles = game.currentPlayer.give("EX1_277")
	missiles.play()
	assert game.currentPlayer.opponent.hero.health == 27


def test_power_overwhelming():
	game = prepare_game()
	power = game.currentPlayer.give("EX1_316")
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	power.play(target=wisp)
	assert wisp.atk == 5
	assert wisp.health == 5
	game.endTurn()
	assert wisp not in game.board


def test_questing_adventurer():
	game = prepare_game()
	adventurer = game.currentPlayer.give("EX1_044")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	adventurer.play()
	assert adventurer.atk == 2
	assert adventurer.health == 2
	game.currentPlayer.give(THE_COIN).play()
	assert adventurer.atk == 3
	assert adventurer.health == 3
	game.currentPlayer.give(THE_COIN).play()
	game.currentPlayer.give(THE_COIN).play()
	game.currentPlayer.give(THE_COIN).play()
	assert adventurer.atk == 6
	assert adventurer.health == 6


def test_venture_co():
	game = prepare_game()
	ventureco = game.currentPlayer.give("CS2_227")
	fireball = game.currentPlayer.give("CS2_029")
	wisp = game.currentPlayer.give(WISP)
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	assert wisp.cost == 0
	assert fireball.cost == 4
	ventureco.play()
	assert wisp.cost == 0 + 3
	assert fireball.cost == 4
	ventureco2 = game.currentPlayer.summon("CS2_227")
	assert wisp.cost == 0 + 3 + 3
	assert fireball.cost == 4
	game.currentPlayer.give(SILENCE).play(target=ventureco)
	assert wisp.cost == 0 + 3
	assert fireball.cost == 4


def test_voidcaller():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.currentPlayer.discardHand()
	voidcaller = game.currentPlayer.give("FP1_022")
	voidcaller.play()

	# give the player a Doomguard and a couple of wisps
	doomguard = game.currentPlayer.give("EX1_310")
	game.currentPlayer.give(WISP)
	game.currentPlayer.give(WISP)
	game.currentPlayer.give(WISP)
	assert len(game.currentPlayer.hand) == 4

	# sacrificial pact on the voidcaller, should summon the Doomguard w/o discards
	game.currentPlayer.give("NEW1_003").play(target=voidcaller)
	assert voidcaller.dead
	assert doomguard.zone == Zone.PLAY
	assert doomguard.canAttack()
	assert len(game.currentPlayer.hand) == 3


def test_void_terror():
	game = prepare_game()
	terror1 = game.currentPlayer.give("EX1_304")
	terror2 = game.currentPlayer.give("EX1_304")
	terror3 = game.currentPlayer.give("EX1_304")
	power = game.currentPlayer.give("EX1_316")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	terror1.play()
	assert terror1.atk == 3
	assert terror1.health == 3
	game.endTurn(); game.endTurn()

	terror2.play()
	assert terror1.dead
	assert terror2.atk == 3+3
	assert terror2.health == 3+3
	game.endTurn(); game.endTurn()

	power.play(target=terror2)
	assert terror2.health == 3+3+4
	assert terror2.atk == 3+3+4
	terror3.play()
	assert terror2.dead
	assert terror3.atk == 3+3+3+4
	assert terror3.health == 3+3+3+4
	game.endTurn(); game.endTurn()
	assert terror3.zone == Zone.PLAY


def test_voljin():
	game = prepare_game()
	voljin = game.player1.give("GVG_014")
	deathwing = game.player1.summon("NEW1_030")
	assert voljin.health == 2
	assert deathwing.health == 12
	for i in range(5):
		game.endTurn(); game.endTurn()

	voljin.play(target=deathwing)
	assert voljin.health == 12
	assert deathwing.health == 2


def test_voljin_stealth():
	game = prepare_game()
	voljin = game.player1.give("GVG_014")
	tiger = game.player2.give("EX1_028")
	for i in range(5):
		game.endTurn(); game.endTurn()

	tiger.play()
	game.endTurn()

	assert not voljin.targets
	voljin.play()
	assert not voljin.dead
	assert voljin.health == 2
	assert tiger.health == 5


def test_mana_addict():
	game = prepare_game()
	manaaddict = game.currentPlayer.give("EX1_055")
	game.endTurn(); game.endTurn()

	manaaddict.play()
	assert manaaddict.atk == 1
	game.endTurn()

	assert manaaddict.atk == 1
	game.currentPlayer.give(THE_COIN).play()
	assert manaaddict.atk == 1
	game.endTurn()

	game.currentPlayer.give(THE_COIN).play()
	assert manaaddict.atk == 3
	game.currentPlayer.give(THE_COIN).play()
	assert manaaddict.atk == 5
	game.endTurn()
	assert manaaddict.atk == 1


def test_old_murkeye():
	game = prepare_game()
	murkeye = game.player1.give("EX1_062")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	murloc = game.player1.summon("CS2_168")
	murkeye.play()
	assert murkeye.charge
	assert murkeye.canAttack()
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
	goldshire1 = game.currentPlayer.give(GOLDSHIRE_FOOTMAN)
	goldshire2 = game.currentPlayer.give(GOLDSHIRE_FOOTMAN)
	moonfire = game.currentPlayer.give(MOONFIRE)
	frostwolf = game.currentPlayer.give("CS2_121")
	wisp = game.currentPlayer.give(WISP)
	assert goldshire1.cost == 1
	assert goldshire2.cost == 1
	assert frostwolf.cost == 2
	assert wisp.cost == 0

	# summon it directly, minions played still at 0
	summoner = game.currentPlayer.summon("EX1_076")
	assert game.currentPlayer.minionsPlayedThisTurn == 0
	assert goldshire1.buffs
	assert goldshire1.cost == 1 - 1
	assert goldshire2.buffs
	assert goldshire2.cost == 1 - 1
	assert not moonfire.buffs
	assert moonfire.cost == 0
	assert frostwolf.buffs
	assert frostwolf.cost == 2 - 1
	assert wisp.buffs
	assert wisp.cost == 0

	goldshire1.play()
	assert game.currentPlayer.minionsPlayedThisTurn == 1
	assert not goldshire2.buffs
	assert not frostwolf.buffs
	assert not wisp.buffs
	assert goldshire2.cost == 1
	assert frostwolf.cost == 2
	assert wisp.cost == 0
	game.endTurn()

	assert game.currentPlayer.minionsPlayedThisTurn == 0
	assert goldshire1.cost == 1
	assert goldshire2.cost == 1
	assert frostwolf.cost == 2
	assert wisp.cost == 0

	game.endTurn()
	summoner2 = game.currentPlayer.summon("EX1_076")
	assert frostwolf.cost == 2 - 2
	summoner.destroy()
	assert frostwolf.cost == 2 - 1
	summoner2.destroy()
	assert frostwolf.cost == 2


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
	game.endTurn(); game.endTurn()

	wraith = game.currentPlayer.give("EX1_616")
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
	mechwarper = game.currentPlayer.give("GVG_006")
	goldshire = game.currentPlayer.give(GOLDSHIRE_FOOTMAN)
	harvest = game.currentPlayer.give("EX1_556")
	game.endTurn(); game.endTurn()

	assert harvest.cost == 3
	assert goldshire.cost == 1
	mechwarper.play()
	assert harvest.cost == 3 - 1
	assert goldshire.cost == 1
	game.currentPlayer.give(SILENCE).play(target=mechwarper)
	assert harvest.cost == 3
	assert goldshire.cost == 1
	mechwarper.destroy()
	assert harvest.cost == 3
	assert goldshire.cost == 1


def test_metaltooth_leaper():
	game = prepare_game()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	dummy = game.currentPlayer.give(TARGET_DUMMY)
	dummy.play()
	metaltooth = game.currentPlayer.give("GVG_048")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	metaltooth.play()
	assert metaltooth.atk == 3
	assert metaltooth.health == 3
	assert wisp.atk == 1
	assert dummy.atk == 0 + 2


def test_bestial_wrath():
	game = prepare_game()
	wolf = game.currentPlayer.give("DS1_175")
	wolf.play()
	bestial = game.currentPlayer.give("EX1_549")
	wisp1 = game.currentPlayer.give(WISP)
	wisp1.play()
	game.endTurn()

	wisp2 = game.currentPlayer.summon(WISP)
	game.endTurn()

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
	game.endTurn()

	assert wolf.atk == 1
	assert not wolf.immune


def test_betrayal():
	game = prepare_game()
	betrayal = game.currentPlayer.give("EX1_126")
	game.endTurn(); game.endTurn()

	wisp1 = game.currentPlayer.give(WISP)
	wisp1.play()
	wisp2 = game.currentPlayer.give(WISP)
	wisp2.play()
	wisp3 = game.currentPlayer.give(WISP)
	wisp3.play()
	assert len(game.currentPlayer.field) == 3
	betrayal.play(target=wisp2)
	assert len(game.currentPlayer.field) == 1
	assert wisp1.dead
	assert wisp2.zone == Zone.PLAY
	assert wisp3.dead
	game.endTurn(); game.endTurn()

	bender = game.currentPlayer.give(SPELLBENDERT)
	bender.play()
	game.currentPlayer.give("EX1_126").play(target=wisp2)
	assert wisp2.zone == Zone.PLAY
	assert bender.zone == Zone.PLAY
	assert bender.health == 2
	bender.destroy(); wisp2.destroy()
	assert not game.currentPlayer.field
	game.endTurn(); game.endTurn()

	# prepare the board: two War Golems and an Emperor Cobra in the middle
	golem1 = game.currentPlayer.summon("CS2_186")
	cobra = game.currentPlayer.summon("EX1_170")
	golem2 = game.currentPlayer.summon("CS2_186")
	game.currentPlayer.give("EX1_126").play(target=cobra)

	assert golem1.dead
	assert cobra.zone == Zone.PLAY
	assert golem2.dead


def test_cold_blood():
	game = prepare_game()
	cb1 = game.currentPlayer.give("CS2_073")
	cb2 = game.currentPlayer.give("CS2_073")
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	game.endTurn(); game.endTurn()

	assert wisp.atk == 1
	cb1.play(target=wisp)
	assert wisp.atk == 1+2
	cb2.play(target=wisp)
	assert wisp.atk == 1+2+4


def test_corruption():
	game = prepare_game()
	corruption1 = game.currentPlayer.give("CS2_063")
	cabal = game.currentPlayer.give("EX1_091")
	game.endTurn()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	wisp2 = game.currentPlayer.give(WISP)
	wisp2.play()
	corruption2 = game.currentPlayer.give("CS2_063")
	game.endTurn()

	corruption1.play(target=wisp)
	assert wisp.zone == Zone.PLAY
	assert wisp.buffs
	assert wisp.buffs[0].controller == game.currentPlayer
	game.endTurn()
	assert wisp.zone == Zone.PLAY
	game.endTurn()

	assert wisp.dead
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn()

	# corrupt our own wisp. next turn opponent MCs it.
	corruption2.play(target=wisp2)
	assert wisp2.zone == Zone.PLAY
	game.endTurn()

	assert wisp2.zone == Zone.PLAY
	cabal.play(target=wisp2)
	assert wisp2.zone == Zone.PLAY
	game.endTurn()
	assert wisp2.dead


def test_harrison_jones():
	game = prepare_game()
	game.endTurn()

	lightsjustice = game.player2.give("CS2_091")
	lightsjustice.play()
	game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	game.player1.discardHand()
	assert not game.player1.hand
	assert lightsjustice.durability == 4
	jones = game.player1.give("EX1_558")
	jones.play()
	assert len(game.player1.hand) == 4
	assert lightsjustice.dead
	game.endTurn()

	game.player2.discardHand()
	jones2 = game.player2.give("EX1_558")
	jones2.play()
	assert not game.player2.hand


def test_headcrack():
	game = prepare_game(exclude=("EX1_137", ))
	headcrack1 = game.player1.give("EX1_137")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert game.player1.hand.contains("EX1_137")
	headcrack1.play()
	assert not game.player1.hand.contains("EX1_137")
	game.endTurn(); game.endTurn()

	assert not game.player1.hand.contains("EX1_137")
	headcrack2 = game.player1.give("EX1_137")
	game.player1.give(THE_COIN).play()
	headcrack2.play()
	assert not game.player1.hand.contains("EX1_137")
	game.endTurn()
	assert game.player1.hand.contains("EX1_137")
	game.player1.discardHand()
	game.endTurn(); game.endTurn()
	assert not game.player1.hand.contains("EX1_137")


def test_heroic_strike():
	game = prepare_game()
	strike = game.currentPlayer.give("CS2_105")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	assert game.currentPlayer.hero.atk == 0
	strike.play()
	assert game.currentPlayer.hero.atk == 4
	game.endTurn()
	assert game.currentPlayer.hero.atk == 0
	game.endTurn()
	assert game.currentPlayer.hero.atk == 0

	game.currentPlayer.give("CS2_105").play()
	game.currentPlayer.give("CS2_106").play()
	assert game.currentPlayer.hero.atk == 7


def test_humility():
	game = prepare_game()
	humility = game.currentPlayer.give("EX1_360")
	humility2 = game.currentPlayer.give("EX1_360")
	seargent = game.currentPlayer.give("CS2_188")
	seargent2 = game.currentPlayer.give("CS2_188")
	golem = game.currentPlayer.summon("CS2_186")
	game.endTurn(); game.endTurn()

	assert golem.atk == 7
	humility.play(target=golem)
	assert golem.atk == 1
	seargent.play(target=golem)
	assert golem.atk == 3
	game.endTurn()
	assert golem.atk == 1
	game.endTurn()

	seargent2.play(target=golem)
	assert golem.atk == 3
	humility2.play(target=golem)
	assert golem.atk == 1
	game.endTurn()
	assert golem.atk == 1


def test_hunters_mark():
	game = prepare_game()
	token = game.currentPlayer.give(SPELLBENDERT)
	token.play()
	assert token.health == 3
	game.currentPlayer.give(MOONFIRE).play(target=token)
	assert token.health == 2
	mark = game.currentPlayer.give("CS2_084")
	mark.play(target=token)
	assert token.health == 1
	game.currentPlayer.give(SILENCE).play(target=token)
	assert token.health == 3


def test_kezan_mystic():
	game = prepare_game()
	kezan = game.player1.give("GVG_074")
	snipe = game.player2.give("EX1_609")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn()

	snipe.play()
	assert snipe in game.player2.secrets
	game.endTurn()

	kezan.play()
	assert not kezan.dead
	assert snipe in game.player1.secrets
	game.endTurn(); game.endTurn()

	kezan2 = game.player1.give("GVG_074")
	kezan2.play()
	assert not kezan2.dead
	assert snipe in game.player1.secrets


def test_knife_juggler():
	game = prepare_game()
	juggler = game.player1.give("NEW1_019")
	game.endTurn(); game.endTurn()

	juggler.play()
	assert game.player2.hero.health == 30
	game.player1.give(WISP).play()
	assert game.player2.hero.health == 29
	game.player1.give(MOONFIRE).play(target=juggler)
	# kill juggler with archer, shouldnt juggle
	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=juggler)
	assert juggler.dead
	assert game.player2.hero.health == 29


def test_mark_of_nature():
	game = prepare_game()
	mark1 = game.currentPlayer.give("EX1_155")
	mark2 = game.currentPlayer.give("EX1_155")
	wisp1 = game.currentPlayer.give(WISP)
	wisp2 = game.currentPlayer.give(WISP)
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	wisp1 = game.currentPlayer.give(WISP)
	wisp1.play()
	assert wisp1.atk == 1
	assert wisp1.health == 1
	assert not wisp1.taunt
	mark1.play(target=wisp1, choose="EX1_155a")
	assert wisp1.atk == 1 + 4
	assert wisp1.health == 1
	assert not wisp1.taunt
	game.endTurn(); game.endTurn()

	wisp2.play()
	assert wisp2.atk == 1
	assert wisp2.health == 1
	assert not wisp2.taunt
	mark2.play(target=wisp2, choose="EX1_155b")
	assert wisp2.atk == 1
	assert wisp2.health == 1 + 4
	assert wisp2.taunt


def test_mindgames():
	game = prepare_game(PRIEST, PRIEST)
	mindgames = game.currentPlayer.give("EX1_345")

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert len(game.currentPlayer.field) == 0
	mindgames.play()
	assert len(game.currentPlayer.field) == 1
	assert game.currentPlayer.opponent.deck.contains(game.currentPlayer.field[0])


def test_mind_vision():
	game = prepare_game()
	# discard our hand, let's clean this.
	game.currentPlayer.discardHand()
	game.endTurn()

	# play mind vision, should give nothing
	assert len(game.currentPlayer.hand) == 6
	game.currentPlayer.give("CS2_003").play()
	assert len(game.currentPlayer.hand) == 6

	# opponent draws a card, coin mind vision should get that one card
	card = game.currentPlayer.opponent.draw()
	game.currentPlayer.getById(THE_COIN).play()
	game.currentPlayer.give("CS2_003").play()
	assert game.currentPlayer.hand[-1] == card


def test_mirror_image():
	game = prepare_game()
	mirror = game.currentPlayer.give("CS2_027")
	mirror.play()
	assert len(game.currentPlayer.field) == 2
	assert game.currentPlayer.field[0].id == "CS2_mirror"
	assert game.currentPlayer.field[1].id == "CS2_mirror"


def test_archmage_antonidas():
	game = prepare_game()

	antonidas = game.currentPlayer.give("EX1_559")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	antonidas.play()
	game.currentPlayer.discardHand()
	assert len(game.currentPlayer.hand) == 0
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.opponent.hero)
	assert len(game.currentPlayer.hand) == 1
	assert game.currentPlayer.hand[0].id == "CS2_029"
	game.currentPlayer.give(THE_COIN).play()
	assert len(game.currentPlayer.hand) == 2
	assert game.currentPlayer.hand[1].id == "CS2_029"


def test_armorsmith():
	game = prepare_game()
	game.endTurn(); game.endTurn()

	armorsmith1 = game.currentPlayer.give("EX1_402")
	armorsmith1.play()
	game.endTurn()
	armorsmith2 = game.currentPlayer.give("EX1_402")
	armorsmith2.play()
	game.endTurn()

	assert not game.currentPlayer.hero.armor
	armorsmith1.attack(target=armorsmith2)
	assert game.currentPlayer.hero.armor == 1
	assert game.currentPlayer.opponent.hero.armor == 1

	game.endTurn()
	game.currentPlayer.give("EX1_402").play()
	game.currentPlayer.give(WISP).play()

	# Whirlwind. 1 armor on each hero, 2 armorsmiths in play for current player, 1 for opponent.
	game.currentPlayer.give("EX1_400").play()
	assert game.currentPlayer.hero.armor == 7
	assert game.currentPlayer.hero.health == 30
	assert game.currentPlayer.opponent.hero.armor == 2


def test_auchenai_soulpriest():
	game = prepare_game(PRIEST, PRIEST)
	game.endTurn(); game.endTurn()
	auchenai = game.player1.summon("EX1_591")
	game.player1.hero.power.play(target=game.player2.hero)
	assert game.player2.hero.health == 28
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert auchenai.health == 1


def test_blessing_of_wisdom():
	game = prepare_game()
	blessing = game.currentPlayer.give("EX1_363")
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	blessing.play(target=wisp)
	game.endTurn(); game.endTurn()

	game.currentPlayer.discardHand()
	wisp.attack(target=game.currentPlayer.opponent.hero)
	assert len(game.currentPlayer.hand) == 1
	game.endTurn(); game.endTurn()
	game.endTurn()

	shadowmadness = game.currentPlayer.give("EX1_334")
	shadowmadness.play(target=wisp)
	assert len(game.currentPlayer.opponent.hand) == 2
	game.currentPlayer.discardHand()
	wisp.attack(target=game.currentPlayer.opponent.hero)
	assert len(game.currentPlayer.opponent.hand) == 3
	assert not game.currentPlayer.hand


def test_blizzard():
	game = prepare_game()
	blizzard = game.currentPlayer.give("CS2_028")
	game.endTurn()

	game.currentPlayer.give(SPELLBENDERT).play()
	game.currentPlayer.give(SPELLBENDERT).play()
	game.currentPlayer.give(SPELLBENDERT).play()
	game.currentPlayer.give(SPELLBENDERT).play()
	game.currentPlayer.give(SPELLBENDERT).play()
	game.currentPlayer.give(SPELLBENDERT).play()
	game.endTurn()

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	blizzard.play()
	for spellbendert in game.currentPlayer.opponent.field:
		assert spellbendert.health == 1
		assert spellbendert.frozen


def test_brawl():
	game = prepare_game()
	brawl = game.player1.give("EX1_407")
	game.player1.give(GOLDSHIRE_FOOTMAN).play()
	game.player1.give(WISP).play()
	game.endTurn()

	game.player2.give(GOLDSHIRE_FOOTMAN).play()
	game.player2.give(WISP).play()
	game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert len(game.board) == 4
	brawl.play()
	assert len(game.board) == 1
	assert game.board[0].id in (WISP, GOLDSHIRE_FOOTMAN)


def test_bane_of_doom():
	game = prepare_game()
	doom = game.currentPlayer.give("EX1_320")
	doom2 = game.currentPlayer.give("EX1_320")
	token = game.player2.summon(SPELLBENDERT)
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert not game.player1.field
	doom.play(target=token)
	assert not game.player1.field
	game.endTurn(); game.endTurn()

	doom2.play(target=token)
	assert len(game.player1.field) == 1
	assert game.player1.field[0].race == Race.DEMON
	assert game.player1.field[0].data.collectible


def test_baron_rivendare():
	game = prepare_game()
	gnome = game.currentPlayer.give("EX1_029")
	gnome.play()
	assert not game.currentPlayer.extraDeathrattles
	rivendare = game.currentPlayer.summon("FP1_031")
	assert game.currentPlayer.extraDeathrattles
	game.currentPlayer.give(MOONFIRE).play(target=gnome)
	assert game.currentPlayer.opponent.hero.health == 26
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	assert not wisp.hasDeathrattle
	sotf = game.currentPlayer.give("EX1_158")
	sotf.play()
	assert len(game.currentPlayer.field) == 2
	game.currentPlayer.give(MOONFIRE).play(target=wisp)
	assert wisp.dead
	assert rivendare.zone == Zone.PLAY
	assert len(game.currentPlayer.field) == 3 # Rivendare and two treants
	rivendare.destroy()
	assert len(game.currentPlayer.field) == 3 # Only one treant spawns


def test_blood_imp():
	game = prepare_game()
	wisp = game.currentPlayer.give(WISP)
	imp = game.currentPlayer.give("CS2_059")
	imp.play()
	assert imp.health == 1
	game.endTurn(); game.endTurn()

	assert imp.health == 1
	wisp.play()
	assert wisp.health == 1
	game.endTurn()
	assert imp.health == 1
	assert wisp.atk == 1
	assert wisp.health == 2


def test_blood_knight():
	game = prepare_game()
	bloodknight1 = game.currentPlayer.give("EX1_590")
	bloodknight2 = game.currentPlayer.give("EX1_590")
	bloodknight3 = game.currentPlayer.give("EX1_590")
	game.endTurn(); game.endTurn()
	game.endTurn()

	squire = game.currentPlayer.give("EX1_008")
	squire.play()
	assert squire.divineShield
	game.endTurn()
	bloodknight1.play()
	assert not squire.divineShield
	assert bloodknight1.atk == 6
	assert bloodknight1.health == 6
	game.endTurn()
	game.currentPlayer.give("EX1_008").play()
	game.currentPlayer.give("EX1_008").play()
	# Play an argent protector on the squire
	game.currentPlayer.give("EX1_362").play(target=squire)
	assert squire.divineShield
	game.endTurn()
	bloodknight2.play()
	assert not squire.divineShield
	assert bloodknight2.atk == 12
	assert bloodknight2.health == 12
	game.endTurn(); game.endTurn()
	bloodknight3.play()
	assert bloodknight3.atk == 3
	assert bloodknight3.health == 3


def test_bolvar_fordragon():
	game = prepare_game()
	bolvar = game.currentPlayer.give("GVG_063")
	assert bolvar.atk == 1
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	game.currentPlayer.give(MOONFIRE).play(target=wisp)
	assert bolvar.atk == 2
	assert bolvar.buffs
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	game.currentPlayer.give(MOONFIRE).play(target=wisp)
	assert bolvar.atk == 3
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	assert bolvar.atk == 3
	assert bolvar.buffs
	bolvar.play()
	assert bolvar.atk == 3
	assert bolvar.buffs
	# game.currentPlayer.give(DREAM).play(target=bolvar)
	# assert bolvar.atk == 1
	# assert not bolvar.buffs


def test_bomb_lobber():
	game = prepare_game()
	lobber1 = game.currentPlayer.give("GVG_099")
	lobber2 = game.currentPlayer.give("GVG_099")
	game.endTurn()

	wisp = game.currentPlayer.give(WISP)
	warden = game.currentPlayer.give("EX1_396")
	game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	lobber1.play()
	assert game.currentPlayer.opponent.hero.health == 30
	game.endTurn()

	wisp.play()
	warden.play()
	game.endTurn()

	lobber2.play()
	assert wisp.dead or warden.health == 7-4


def test_defias():
	game = prepare_game()

	defias1 = game.currentPlayer.give("EX1_131")
	defias1.play()
	assert len(game.currentPlayer.field) == 1

	game.endTurn()

	# Coin-defias
	game.currentPlayer.getById(THE_COIN).play()
	defias2 = game.currentPlayer.give("EX1_131")
	defias2.play()
	assert len(game.currentPlayer.field) == 2


def test_doomsayer():
	game = prepare_game()

	# play some wisps
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()

	game.endTurn();
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()

	assert len(game.board) == 4
	doomsayer = game.currentPlayer.give("NEW1_021")
	doomsayer.play()
	assert len(game.board) == 5

	game.endTurn()
	assert len(game.board) == 5
	game.endTurn()
	assert len(game.board) == 0


def test_gadgetzan_auctioneer():
	game = prepare_game()

	game.currentPlayer.summon("EX1_095")
	assert len(game.currentPlayer.hand) == 4
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.opponent.hero)
	assert len(game.currentPlayer.hand) == 5
	game.currentPlayer.give(WISP).play()
	assert len(game.currentPlayer.hand) == 5


def test_goblin_blastmage():
	game = prepare_game()
	blastmage1 = game.currentPlayer.give("GVG_004")
	blastmage2 = game.currentPlayer.give("GVG_004")
	clockwork = game.currentPlayer.give("GVG_082")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert not blastmage1.poweredUp
	assert game.currentPlayer.hero.health == 30
	blastmage1.play()
	assert game.currentPlayer.hero.health == 30
	game.endTurn(); game.endTurn()

	assert not blastmage2.poweredUp
	clockwork.play()
	assert clockwork.race == Race.MECHANICAL
	assert blastmage2.poweredUp
	blastmage2.play()
	assert game.currentPlayer.opponent.hero.health == 30 - 4
	game.endTurn(); game.endTurn()


def test_gahzrilla():
	game = prepare_game()
	gahz = game.currentPlayer.summon("GVG_049")
	assert gahz.atk == 6
	game.currentPlayer.give(MOONFIRE).play(target=gahz)
	assert gahz.atk == 6*2
	timberwolf = game.currentPlayer.give("DS1_175")
	timberwolf.play()
	assert gahz.atk == (6*2) + 1
	# TODO: Buffs are always taken into account at the end
	# game.currentPlayer.give(MOONFIRE).play(target=gahz)
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

	game.endTurn(); game.endTurn()
	rewinder = game.player1.give(TIME_REWINDER)
	rewinder.play(target=grimscale)
	assert murloc1.atk == 2
	assert murloc2.atk == 2


def test_gruul():
	game = prepare_game()
	gruul = game.currentPlayer.summon("NEW1_038")
	assert gruul.atk == 7
	assert gruul.health == 7
	assert not gruul.buffs
	game.endTurn()
	assert gruul.buffs
	assert gruul.atk == 8
	assert gruul.health == 8
	game.endTurn()
	assert gruul.atk == 9
	assert gruul.health == 9


def test_hobgoblin():
	game = prepare_game()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	assert wisp.health == 1
	hobgoblin = game.currentPlayer.summon("GVG_104")
	wolf1 = game.currentPlayer.give("DS1_175")
	wolf1.play()
	assert wolf1.atk == 3
	assert wolf1.health == 3
	game.currentPlayer.give(THE_COIN).play()
	wolf2 = game.currentPlayer.give("DS1_175")
	wolf2.play()
	assert wolf1.atk == 4
	assert wolf1.health == 3
	assert wolf2.atk == 4
	assert wolf2.health == 3
	game.endTurn(); game.endTurn()

	loothoarder = game.currentPlayer.give("EX1_096")
	loothoarder.play()
	assert not loothoarder.buffs
	assert loothoarder.atk == 2
	assert loothoarder.health == 1
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	# TODO: Test faceless-hobgoblin interaction
	# assert wisp.health == 1
	# assert wisp.atk == 1
	# faceless = game.currentPlayer.give("EX1_564")
	# faceless.play(target=wisp)
	# assert not faceless.buffs
	# assert faceless.atk == 1
	# assert faceless.health == 1


def test_hogger():
	game = prepare_game()
	hogger = game.currentPlayer.give("NEW1_040")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	hogger.play()
	assert len(game.currentPlayer.field) == 1
	game.endTurn()
	assert len(game.currentPlayer.opponent.field) == 2
	assert game.currentPlayer.opponent.field[1].id == "NEW1_040t"
	game.endTurn()
	assert len(game.currentPlayer.field) == 2
	game.endTurn()
	assert len(game.currentPlayer.opponent.field) == 3


def test_houndmaster():
	game = prepare_game()
	houndmaster = game.currentPlayer.give("DS1_070")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert not houndmaster.targets
	assert not houndmaster.poweredUp
	hound = game.currentPlayer.summon("EX1_538t")
	assert houndmaster.targets == [hound]
	assert houndmaster.poweredUp
	assert hound.atk == 1
	assert hound.health == 1
	assert not hound.taunt
	houndmaster.play(target=hound)
	assert hound.atk == 3
	assert hound.health == 3
	assert hound.taunt


def test_illidan():
	game = prepare_game()
	illidan = game.currentPlayer.give("EX1_614")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	assert len(game.board) == 0
	illidan.play()
	assert len(game.board) == 1
	game.currentPlayer.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 2
	game.currentPlayer.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 3
	game.currentPlayer.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 4
	game.currentPlayer.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 5

	# 5th moonfire kills illidan, but spawns another token before
	game.currentPlayer.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 5
	assert illidan.dead


def test_leeroy():
	game = prepare_game()
	leeroy = game.currentPlayer.give("EX1_116")

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	leeroy.play()
	assert leeroy.canAttack()
	assert game.currentPlayer.opponent.field.contains("EX1_116t")
	assert game.currentPlayer.opponent.field[0] == game.currentPlayer.opponent.field[1]


def test_lorewalker_cho():
	game = prepare_game()
	cho = game.currentPlayer.give("EX1_100")
	game.endTurn(); game.endTurn()

	cho.play()
	game.currentPlayer.discardHand()
	game.currentPlayer.opponent.discardHand()
	assert len(game.currentPlayer.hand) == 0
	assert len(game.currentPlayer.opponent.hand) == 0
	game.currentPlayer.give(THE_COIN).play()
	assert len(game.currentPlayer.hand) == 0
	assert len(game.currentPlayer.opponent.hand) == 1
	assert game.currentPlayer.opponent.hand[0].id == THE_COIN

	game.endTurn()
	game.currentPlayer.discardHand()
	game.currentPlayer.give(THE_COIN).play()
	assert len(game.currentPlayer.hand) == 0
	assert len(game.currentPlayer.opponent.hand) == 1
	assert game.currentPlayer.opponent.hand[0].id == THE_COIN
	game.currentPlayer.give(THE_COIN).play()


def test_light_of_the_naaru():
	game = prepare_game()
	naaru1 = game.player1.give("GVG_012")
	naaru2 = game.player1.give("GVG_012")
	naaru3 = game.player1.give("GVG_012")
	assert game.player1.hero.health == 30
	naaru1.play(target=game.player1.hero)
	assert not game.player1.field
	assert game.player1.hero.health == 30
	game.endTurn(); game.endTurn()

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


	# TODO Auchenai kill test

def test_lightspawn():
	game = prepare_game()
	lightspawn = game.currentPlayer.give("EX1_335")
	flametongue = game.currentPlayer.give("EX1_565")

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	lightspawn.play()
	assert lightspawn.health == 5
	assert lightspawn.atk == 5

	game.endTurn()
	# play archer on lightspawn, goes to 4 health
	game.currentPlayer.give("CS2_189").play(target=lightspawn)
	assert lightspawn.health == 4
	assert lightspawn.atk == 4
	assert not lightspawn.buffs
	game.endTurn(); game.endTurn()
	flametongue.play()

	assert lightspawn.health == 4
	assert lightspawn.buffs
	assert lightspawn.atk == 4

	game.currentPlayer.give(SILENCE).play(target=lightspawn)
	assert lightspawn.buffs
	# 2 attack from the flametongue
	assert lightspawn.atk == 2


def test_lightwarden():
	game = prepare_game(PRIEST, PRIEST)
	lightwarden = game.currentPlayer.give("EX1_001")
	lightwarden.play()
	assert lightwarden.atk == 1
	game.endTurn(); game.endTurn();

	# No-op heal should not do anything.
	assert game.currentPlayer.hero.health == 30
	game.currentPlayer.hero.power.play(target=game.currentPlayer.hero)
	assert game.currentPlayer.hero.health == 30
	assert lightwarden.atk == 1
	lightwarden.attack(target=game.currentPlayer.opponent.hero)
	game.endTurn()
	game.currentPlayer.hero.power.play(target=game.currentPlayer.hero)
	assert lightwarden.atk == 3


def test_lightwell():
	game = prepare_game()
	lightwell = game.currentPlayer.give("EX1_341")

	game.endTurn(); game.endTurn()
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.opponent.hero)
	lightwell.play()
	assert game.currentPlayer.hero.health == 29
	assert game.currentPlayer.opponent.hero.health == 29
	game.endTurn()
	assert game.currentPlayer.opponent.hero.health == 29
	assert game.currentPlayer.hero.health == 29
	game.endTurn()
	assert game.currentPlayer.hero.health == 30
	assert game.currentPlayer.opponent.hero.health == 29


def test_lil_exorcist():
	game = prepare_game()
	exorcist1 = game.player1.give("GVG_097")
	exorcist2 = game.player1.give("GVG_097")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	exorcist1.play()
	assert exorcist1.atk == 2
	assert exorcist1.health == 3
	assert not exorcist1.buffs
	game.endTurn()

	game.player2.give("FP1_001").play()
	game.player2.give("FP1_001").play()
	game.endTurn()

	exorcist2.play()
	assert exorcist2.atk == 2 + 2
	assert exorcist2.health == 3 + 2
	assert exorcist2.buffs


def test_loatheb():
	game = prepare_game(WARRIOR, MAGE)
	game.player1.discardHand()
	game.player2.discardHand()
	loatheb = game.player1.give("FP1_030")
	fireballPlayer1 = game.player1.give("CS2_029")
	fireball1 = game.player2.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	moonfire = game.player2.give(MOONFIRE)
	game.endTurn()

	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballPlayer1.cost == 4
	loatheb.play()
	# costs do not change right away
	assert not fireball1.buffs
	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballPlayer1.cost == 4
	game.endTurn()

	assert fireball1.cost == 4 + 5
	assert fireball2.cost == 4 + 5
	assert moonfire.cost == 0 + 5
	assert fireballPlayer1.cost == 4
	game.endTurn()

	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballPlayer1.cost == 4


def test_micro_machine():
	game = prepare_game()
	micro = game.player1.give("GVG_103")
	game.endTurn(); game.endTurn()

	micro.play()
	assert micro.atk == 1
	game.endTurn()
	assert micro.atk == 2
	game.endTurn()
	assert micro.atk == 3
	game.endTurn()
	assert micro.atk == 4


def test_millhouse_manastorm():
	game = prepare_game(WARRIOR, MAGE)
	game.player1.discardHand()
	game.player2.discardHand()
	millhouse = game.player1.give("NEW1_029")
	fireballPlayer1 = game.player1.give("CS2_029")
	fireball1 = game.player2.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	moonfire = game.player2.give(MOONFIRE)
	game.endTurn()

	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballPlayer1.cost == 4
	millhouse.play()
	# costs change as soon as millhouse is played
	assert game.player2.hero.buffs
	assert fireball1.buffs
	assert fireball1.cost == 0
	assert fireball2.cost == 0
	assert moonfire.cost == 0
	assert fireballPlayer1.cost == 4
	game.endTurn()

	assert fireball1.cost == 0
	assert fireball2.cost == 0
	assert moonfire.cost == 0
	assert fireballPlayer1.cost == 4
	game.endTurn()

	assert fireball1.cost == 4
	assert fireball2.cost == 4
	assert moonfire.cost == 0
	assert fireballPlayer1.cost == 4


def test_molten_giant():
	game = prepare_game()
	molten = game.currentPlayer.give("EX1_620")
	assert molten.cost == 20
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	assert molten.cost == 19
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	assert molten.cost == 18
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	assert molten.cost == 17
	game.endTurn()

	assert molten.cost == 17
	molten2 = game.currentPlayer.give("EX1_620")
	assert molten2.cost == 20


def test_mountain_giant():
	game = prepare_game()
	mountain = game.currentPlayer.give("EX1_105")
	assert mountain.cost == 12 - len(game.currentPlayer.hand) + 1
	game.endTurn(); game.endTurn()
	assert mountain.cost == 12 - len(game.currentPlayer.hand) + 1
	game.endTurn(); game.endTurn()
	assert mountain.cost == 12 - len(game.currentPlayer.hand) + 1


def test_sea_giant():
	game = prepare_game()
	seagiant = game.currentPlayer.give("EX1_586")
	assert seagiant.cost == 10
	game.currentPlayer.give(WISP).play()
	assert seagiant.cost == 9
	game.currentPlayer.give(WISP).play()
	assert seagiant.cost == 8
	game.currentPlayer.give(WISP).play()
	assert seagiant.cost == 7
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	assert seagiant.cost == 3
	game.endTurn()
	for i in range(7):
		game.currentPlayer.give(WISP).play()
	assert seagiant.cost == 0


def test_murloc_tidecaller():
	game = prepare_game()
	tidecaller = game.currentPlayer.give("EX1_509")
	tidecaller.play()
	assert tidecaller.atk == 1
	game.endTurn()
	game.currentPlayer.give("CS2_168").play()
	assert tidecaller.atk == 2
	game.endTurn()
	# Play a tidehunter. Summons two murlocs.
	game.currentPlayer.give("EX1_506").play()
	assert tidecaller.atk == 4


def test_nerubar_weblord():
	game = prepare_game()
	game.player1.discardHand()
	game.player2.discardHand()
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
	nerubar = game.player1.summon("FP1_017")
	assert moonfire1.cost == moonfire2.cost == 0
	assert footman1.cost == footman2.cost == 1
	assert archer1.cost == archer2.cost == 1 + 2
	assert perdition1.cost == perdition2.cost == 3


def test_nortshire_cleric():
	game = prepare_game(PRIEST, PRIEST)
	cleric = game.currentPlayer.give("CS2_235")
	cleric.play()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.currentPlayer.discardHand()
	assert not game.currentPlayer.hand
	game.currentPlayer.hero.power.play(target=game.currentPlayer.hero)
	assert not game.currentPlayer.hand
	pyro = game.currentPlayer.give("NEW1_020")
	pyro.play()
	game.currentPlayer.give(CIRCLE_OF_HEALING).play()
	assert not game.currentPlayer.hand
	game.currentPlayer.give(CIRCLE_OF_HEALING).play()
	assert len(game.currentPlayer.hand) == 2
	game.currentPlayer.give(CIRCLE_OF_HEALING).play()
	assert len(game.currentPlayer.hand) == 4


def test_ragnaros():
	game = prepare_game()
	ragnaros = game.currentPlayer.give("EX1_298")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	ragnaros.play()
	assert not ragnaros.canAttack()
	assert game.currentPlayer.opponent.hero.health == 30
	game.endTurn()

	assert game.currentPlayer.hero.health == 22
	game.endTurn()

	assert game.currentPlayer.opponent.hero.health == 22
	assert not ragnaros.canAttack()


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


def test_tree_of_life():
	game = prepare_game()
	token1 = game.player1.give(SPELLBENDERT)
	token1.play()
	tree = game.player1.give("GVG_033")
	game.endTurn()

	token2 = game.player2.give(SPELLBENDERT)
	token2.play()
	game.endTurn()

	targets = (game.player1.hero, game.player2.hero, token1, token2)
	for target in targets:
		game.player1.give(MOONFIRE).play(target=target)
	for i in range(7):
		game.endTurn(); game.endTurn()

	assert token1.health == token2.health == 3 - 1
	assert game.player1.hero.health == game.player2.hero.health == 30 - 1
	tree.play()
	assert token1.health == token2.health == 3
	assert game.player1.hero.health == game.player2.hero.health == 30


def test_truesilver_champion():
	game = prepare_game()
	truesilver = game.currentPlayer.give("CS2_097")
	lightwarden = game.currentPlayer.give("EX1_001")
	lightwarden.play()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	truesilver.play()
	assert game.currentPlayer.weapon is truesilver
	assert game.currentPlayer.hero.atk == 4
	assert game.currentPlayer.hero.health == 30
	game.currentPlayer.hero.attack(target=game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 26
	assert game.currentPlayer.hero.health == 30
	assert lightwarden.atk == 1
	game.endTurn(); game.endTurn()

	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	game.currentPlayer.hero.attack(target=game.currentPlayer.opponent.hero)
	assert game.currentPlayer.hero.health == 29
	assert lightwarden.atk == 3


def test_twilight_drake():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	assert len(game.currentPlayer.hand) == 7
	drake = game.currentPlayer.give("EX1_043")
	drake.play()
	assert len(game.currentPlayer.hand) == 7
	assert drake.health == 1+7
	assert drake.buffs

	game.endTurn()
	game.currentPlayer.discardHand()
	drake2 = game.currentPlayer.give("EX1_043")
	assert len(game.currentPlayer.hand) == 1
	drake2.play()
	assert not game.currentPlayer.hand
	assert drake2.health == 1
	assert not drake2.buffs


def test_unbound_elemental():
	game = prepare_game()
	unbound = game.currentPlayer.give("EX1_258")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	unbound.play()
	assert unbound.atk == 2
	assert unbound.health == 4
	game.currentPlayer.give(THE_COIN).play()
	assert unbound.atk == 2
	assert unbound.health == 4
	# Lightning Bolt should trigger it
	game.currentPlayer.give("EX1_238").play(target=game.currentPlayer.opponent.hero)
	assert unbound.atk == 3
	assert unbound.health == 5
	game.endTurn()
	game.currentPlayer.give("EX1_238").play(target=game.currentPlayer.opponent.hero)
	assert unbound.atk == 3
	assert unbound.health == 5


def test_undertaker():
	game = prepare_game()
	undertaker = game.currentPlayer.give("FP1_028")
	undertaker.play()
	game.currentPlayer.give(WISP).play()
	assert not undertaker.buffs
	assert undertaker.atk == 1
	assert undertaker.health == 2
	game.endTurn()

	# Play a leper gnome, should not trigger undertaker
	game.currentPlayer.give("EX1_029").play()
	assert undertaker.atk == 1
	assert undertaker.health == 2
	game.endTurn()

	game.currentPlayer.give("EX1_029").play()
	assert undertaker.atk == 2
	assert undertaker.health == 2

	game.currentPlayer.give("EX1_029").play()
	assert undertaker.atk == 3
	assert undertaker.health == 2


def test_vancleef():
	game = prepare_game()
	vancleef1 = game.currentPlayer.give("EX1_613")
	vancleef2 = game.currentPlayer.give("EX1_613")
	game.endTurn(); game.endTurn()

	assert not game.currentPlayer.cardsPlayedThisTurn
	game.currentPlayer.give(THE_COIN).play()
	game.currentPlayer.give(THE_COIN).play()
	game.currentPlayer.give(THE_COIN).play()
	game.currentPlayer.give(THE_COIN).play()
	game.currentPlayer.give(THE_COIN).play()
	assert game.currentPlayer.cardsPlayedThisTurn == 5
	vancleef1.play()
	assert game.currentPlayer.cardsPlayedThisTurn == 6
	assert vancleef1.atk == 12
	assert vancleef1.health == 12
	game.endTurn(); game.endTurn()

	assert not game.currentPlayer.cardsPlayedThisTurn
	vancleef2.play()
	assert game.currentPlayer.cardsPlayedThisTurn == 1
	assert vancleef2.atk == 2
	assert vancleef2.health == 2


def test_water_elemental():
	game = prepare_game()
	elem = game.player1.give("CS2_033")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	elem.play()
	game.endTurn(); game.endTurn()

	assert not game.player2.hero.frozen
	elem.attack(target=game.player2.hero)
	assert game.player2.hero.frozen
	game.endTurn()

	assert game.player2.hero.frozen
	game.endTurn()

	assert not game.player2.hero.frozen
	game.endTurn()

	axe = game.player2.give("CS2_106")
	axe.play()
	game.player2.hero.attack(target=elem)
	assert game.player2.hero.frozen
	game.endTurn()

	assert game.player2.hero.frozen
	game.endTurn()

	assert game.player2.hero.frozen
	game.endTurn()

	assert not game.player2.hero.frozen
	game.endTurn()


def test_webspinner():
	game = prepare_game()
	game.currentPlayer.discardHand()
	webspinner = game.currentPlayer.give("FP1_011")
	webspinner.play()
	game.currentPlayer.give(MOONFIRE).play(target=webspinner)
	assert len(game.currentPlayer.hand) == 1
	assert game.currentPlayer.hand[0].race == Race.BEAST
	assert game.currentPlayer.hand[0].type == CardType.MINION


def test_wild_pyromancer():
	game = prepare_game()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	pyro = game.currentPlayer.give("NEW1_020")
	game.endTurn(); game.endTurn()

	pyro.play()
	assert pyro.health == 2
	assert wisp.zone == Zone.PLAY

	# play moonfire. wisp should die.
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.opponent.hero)
	assert wisp.dead
	assert pyro.health == 1

	# play circle of healing. pyro should go up to 2hp then back to 1.
	game.currentPlayer.give(CIRCLE_OF_HEALING).play()
	assert pyro.health == 1
	assert pyro.zone == Zone.PLAY

	# Silence the pyromancer. It should not trigger.
	game.currentPlayer.give(SILENCE).play(target=pyro)
	assert pyro.health == 1
	assert pyro.zone == Zone.PLAY


def test_young_priestess():
	game = prepare_game()
	priestess = game.player1.give("EX1_004")
	game.endTurn(); game.endTurn()

	priestess.play()
	assert priestess.health == 1
	game.endTurn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.endTurn()

	assert priestess.health == 1
	assert wisp.health == 1
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	assert wisp1.health == 1

	game.endTurn()
	assert wisp1.health == 2


def test_ysera():
	game = prepare_game()
	ysera = game.currentPlayer.summon("EX1_572")
	game.currentPlayer.discardHand()
	assert len(game.player1.hand) == 0
	game.endTurn()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].cardClass == CardClass.DREAM


def test_shadow_madness_wild_pyro():
	game = prepare_game()
	pyro = game.currentPlayer.give("NEW1_020")
	game.endTurn(); game.endTurn()

	pyro.play()
	game.endTurn()
	game.endTurn(); game.endTurn()

	assert pyro.controller == game.player1
	assert pyro in game.player1.field
	assert pyro.health == 2
	shadowmadness = game.currentPlayer.give("EX1_334")
	shadowmadness.play(target=pyro)
	assert pyro.controller == game.player2
	assert pyro in game.player2.field
	assert pyro.health == 1
	game.endTurn()
	assert pyro.controller == game.player1
	assert pyro in game.player1.field


def test_shadow_madness_silence():
	game = prepare_game()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn()

	assert wisp.controller == game.player1
	shadowmadness = game.currentPlayer.give("EX1_334")
	shadowmadness.play(target=wisp)
	assert wisp.controller == game.player2
	game.currentPlayer.give(SILENCE).play(target=wisp)
	assert wisp.controller == game.player1
	game.endTurn()
	assert wisp.controller == game.player1


def test_shadowform():
	game = prepare_game(PRIEST, PRIEST)
	shadowform1 = game.currentPlayer.give("EX1_625")
	shadowform2 = game.currentPlayer.give("EX1_625")
	shadowform3 = game.currentPlayer.give("EX1_625")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	# Hero Power should reset
	assert game.currentPlayer.hero.power.id == "CS1h_001"
	assert game.currentPlayer.hero.power.isPlayable()
	game.currentPlayer.hero.power.play(target=game.currentPlayer.hero)
	assert not game.currentPlayer.hero.power.isPlayable()
	assert shadowform1.isPlayable()
	shadowform1.play()
	assert game.currentPlayer.hero.power.id == "EX1_625t"
	assert game.currentPlayer.hero.power.isPlayable()
	game.currentPlayer.hero.power.play(target=game.currentPlayer.opponent.hero)
	assert not game.currentPlayer.hero.power.isPlayable()
	assert game.currentPlayer.opponent.hero.health == 28
	game.endTurn(); game.endTurn()

	shadowform2.play()
	assert game.currentPlayer.hero.power.id == "EX1_625t2"
	assert game.currentPlayer.hero.power.isPlayable()
	game.currentPlayer.hero.power.play(target=game.currentPlayer.opponent.hero)
	assert not game.currentPlayer.hero.power.isPlayable()
	assert game.currentPlayer.opponent.hero.health == 25

	shadowform3.play()
	assert game.currentPlayer.hero.power.id == "EX1_625t2"
	assert not game.currentPlayer.hero.power.isPlayable()


def test_shadowstep():
	game = prepare_game()
	shadowstep = game.currentPlayer.give("EX1_144")
	deathwing = game.currentPlayer.summon("NEW1_030")
	assert deathwing.zone == Zone.PLAY
	assert deathwing.cost == 10
	shadowstep.play(target=deathwing)
	assert deathwing.zone == Zone.HAND
	assert deathwing in game.currentPlayer.hand
	assert deathwing.cost == 8


def test_shattered_sun_cleric():
	game = prepare_game()
	cleric = game.player1.give("EX1_019")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert not cleric.targets
	cleric.play()
	assert cleric.atk == 3
	assert cleric.health == 2
	game.endTurn(); game.endTurn()

	cleric2 = game.player1.give("EX1_019")
	assert cleric in cleric2.targets
	cleric2.play(target=cleric)
	assert cleric.atk == 3+1
	assert cleric.health == 2+1


def test_acolyte_of_pain():
	game = prepare_game()
	acolyte = game.currentPlayer.give("EX1_007")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert len(game.currentPlayer.hand) == 7
	acolyte.play()
	assert len(game.currentPlayer.hand) == 6
	game.currentPlayer.give(MOONFIRE).play(target=acolyte)
	assert len(game.currentPlayer.hand) == 7
	game.currentPlayer.give(MOONFIRE).play(target=acolyte)
	assert len(game.currentPlayer.hand) == 8
	game.currentPlayer.give(MOONFIRE).play(target=acolyte)
	assert len(game.currentPlayer.hand) == 9
	assert acolyte.dead


def test_poisonous():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.endTurn()
	game.currentPlayer.getById(THE_COIN).play()
	cobra = game.currentPlayer.give("EX1_170")
	cobra.play()
	assert cobra.poisonous
	game.endTurn()
	zchow = game.currentPlayer.give("FP1_001")
	zchow.play()
	zchow2 = game.currentPlayer.give("FP1_001")
	zchow2.play()
	game.endTurn()
	cobra.attack(target=zchow)
	assert zchow not in game.currentPlayer.opponent.field
	assert zchow.dead
	game.endTurn()
	zchow2.attack(target=cobra)
	assert zchow2.dead

	# test silencing the cobra
	zchow3 = game.currentPlayer.give("FP1_001")
	zchow3.play()
	game.endTurn()
	cobra = game.currentPlayer.give("EX1_170")
	cobra.play()
	cobra.silence()
	game.endTurn()
	zchow3.attack(cobra)
	assert zchow3 in game.currentPlayer.field
	assert cobra in game.currentPlayer.opponent.field


def test_cleave():
	game = prepare_game()
	# play some wisps
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.endTurn()

	# Play the coin
	game.currentPlayer.getById(THE_COIN).play()

	cleave = game.currentPlayer.give("CS2_114")
	assert cleave.isPlayable()
	cleave.play()
	assert len(game.currentPlayer.opponent.field) == 0

	# play another wisp
	game.currentPlayer.give(WISP).play()

	game.endTurn()
	cleave2 = game.currentPlayer.give("CS2_114")
	assert not cleave2.isPlayable()


def test_upgrade():
	game = prepare_game()
	axe = game.currentPlayer.give("CS2_106")
	upgrade = game.currentPlayer.give("EX1_409")
	game.endTurn(); game.endTurn()
	axe.play()
	assert game.currentPlayer.weapon.atk == 3
	assert game.currentPlayer.weapon.durability == 2
	game.currentPlayer.hero.attack(game.currentPlayer.opponent.hero)
	assert game.currentPlayer.weapon.atk == 3
	assert game.currentPlayer.weapon.durability == 1
	assert game.currentPlayer.opponent.hero.health == 27

	game.endTurn()
	upgrade2 = game.currentPlayer.give("EX1_409")
	upgrade2.play()
	assert game.currentPlayer.hero.atk == 1
	assert game.currentPlayer.weapon.atk == 1
	game.endTurn()
	assert game.currentPlayer.weapon.atk == 3
	assert game.currentPlayer.weapon.durability == 1
	upgrade.play()
	assert game.currentPlayer.weapon.atk == 4
	assert game.currentPlayer.weapon.durability == 2
	game.currentPlayer.hero.attack(game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 23
	assert game.currentPlayer.weapon.durability == 1

	# test Bloodsail Corsair
	game.endTurn()
	corsair = game.currentPlayer.give("NEW1_025")
	corsair.play()
	assert axe.dead
	assert not game.currentPlayer.opponent.weapon


CHEAT_MIRROR_ENTITY = True
def test_mctech():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.endTurn()
	# play some wisps
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	game.currentPlayer.give(WISP).play()
	# coin mirror entity
	game.currentPlayer.getById(THE_COIN).play()
	if CHEAT_MIRROR_ENTITY:
		# TODO secrets
		game.currentPlayer.give("EX1_294").play()
	game.endTurn()

	assert len(game.currentPlayer.opponent.field) == 3
	# play an mctech. nothing should be controlled.
	game.currentPlayer.give("EX1_085").play()
	assert len(game.currentPlayer.field) == 1
	game.endTurn()
	if CHEAT_MIRROR_ENTITY:
		# mc tech gets copied, board now at 4
		game.currentPlayer.give("EX1_085").play()
	assert len(game.currentPlayer.field) == 4
	game.endTurn()
	game.currentPlayer.give("EX1_085").play()
	assert len(game.currentPlayer.field) == 3
	assert len(game.currentPlayer.opponent.field) == 3


def test_inner_fire():
	game = prepare_game()
	innerfire = game.currentPlayer.give("CS1_129")
	seargent = game.currentPlayer.give("CS2_188")
	gurubashi = game.currentPlayer.summon("EX1_399")
	game.endTurn(); game.endTurn()
	assert gurubashi.atk == 2
	seargent.play(target=gurubashi)
	assert gurubashi.atk == 4
	innerfire.play(target=gurubashi)
	assert gurubashi.atk == 7
	game.endTurn(); game.endTurn()
	assert gurubashi.atk == 7
	equality = game.currentPlayer.give("EX1_619")
	equality.play()
	assert gurubashi.health == 1
	assert gurubashi.atk == 7


def test_ice_barrier():
	game = prepare_game(MAGE, MAGE)
	icebarrier = game.currentPlayer.give("EX1_289")
	icebarrier2 = game.currentPlayer.give("EX1_289")
	friendlywisp = game.currentPlayer.give(WISP)
	friendlywisp.play()
	game.endTurn()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	wisp2 = game.currentPlayer.give(WISP)
	wisp2.play()
	game.endTurn()
	game.endTurn(); game.endTurn()

	assert icebarrier.isPlayable()
	icebarrier.play()
	assert not icebarrier2.isPlayable()
	assert game.currentPlayer.secrets
	assert icebarrier in game.currentPlayer.secrets
	assert not game.currentPlayer.hero.armor
	game.endTurn(); game.endTurn()

	assert not icebarrier2.isPlayable()
	friendlywisp.attack(target=game.currentPlayer.opponent.hero)
	assert not game.currentPlayer.hero.armor
	assert not game.currentPlayer.opponent.hero.armor
	game.endTurn(); game.endTurn()

	friendlywisp.attack(target=wisp2)
	assert not game.currentPlayer.hero.armor
	assert not game.currentPlayer.opponent.hero.armor
	assert friendlywisp.dead
	assert wisp2.dead
	game.endTurn()

	assert len(game.currentPlayer.opponent.secrets) == 1
	wisp.attack(target=game.currentPlayer.opponent.hero)
	assert not game.currentPlayer.opponent.secrets
	assert game.currentPlayer.opponent.hero.armor == 7


def test_vaporize():
	game = prepare_game()
	vaporize = game.currentPlayer.give("EX1_594")
	game.endTurn()
	wisp = game.currentPlayer.give(WISP)
	wisp.play()
	game.endTurn()
	game.endTurn(); game.endTurn()
	vaporize.play()
	assert game.currentPlayer.secrets[0] == vaporize
	game.endTurn()
	assert len(game.currentPlayer.opponent.secrets) == 1
	# Play an axe and hit the hero ourselves
	game.currentPlayer.give("CS2_106").play()
	game.currentPlayer.hero.attack(target=game.currentPlayer.opponent.hero)
	assert len(game.currentPlayer.opponent.secrets) == 1
	assert game.currentPlayer.opponent.hero.health == 27
	wisp.attack(target=game.currentPlayer.opponent.hero)
	assert not game.currentPlayer.opponent.secrets
	assert vaporize.dead
	assert wisp.dead
	assert game.currentPlayer.opponent.hero.health == 27


def test_stoneskin_gargoyle():
	game = prepare_game()
	gargoyle = game.currentPlayer.give("FP1_027")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	gargoyle.play()
	assert gargoyle.health == 4
	# damage the gargoyle by 1
	game.currentPlayer.give(MOONFIRE).play(target=gargoyle)
	assert gargoyle.health == 3
	game.endTurn(); game.endTurn()
	assert gargoyle.health == 4

	# soulpriest test. NYI
	# soulpriest = game.currentPlayer.give("EX1_591")
	# soulpriest.play()
	# game.endTurn(); game.endTurn()
	# assert gargoyle.health == 4
	# game.currentPlayer.give(MOONFIRE).play(target=gargoyle)
	# assert gargoyle.health == 3
	# game.endTurn(); game.endTurn()
	# assert gargoyle.health == 2
	# game.endTurn(); game.endTurn()
	# assert gargoyle.dead


def test_summoning_portal():
	game = prepare_game()
	game.currentPlayer.discardHand()
	wisp = game.currentPlayer.give(WISP)
	assert wisp.cost == 0
	axe = game.currentPlayer.give("CS2_106")
	assert axe.cost == 2
	molten = game.currentPlayer.give("EX1_620")
	assert molten.cost == 20
	goldshire = game.currentPlayer.give(GOLDSHIRE_FOOTMAN)
	assert goldshire.cost == 1
	frostwolf = game.currentPlayer.give("CS2_121")
	assert frostwolf.cost == 2

	portal = game.currentPlayer.summon("EX1_315")
	assert wisp.cost == 0
	assert axe.cost == 2
	assert molten.cost == 18
	assert goldshire.cost == 1
	assert frostwolf.cost == 1
	game.currentPlayer.give(MOONFIRE).play(target=game.currentPlayer.hero)
	assert molten.cost == 17
	portal2 = game.currentPlayer.summon("EX1_315")
	assert wisp.cost == 0
	assert molten.cost == 20 - 2 - 1 - 2
	assert goldshire.cost == 1
	assert frostwolf.cost == 1


def test_sunfury_protector():
	game = prepare_game()
	sunfury = game.currentPlayer.give("EX1_058")
	game.endTurn(); game.endTurn()

	wisp1 = game.currentPlayer.give(WISP)
	wisp1.play()
	wisp2 = game.currentPlayer.give(WISP)
	wisp2.play()
	sunfury.play()
	assert not wisp1.taunt
	assert wisp2.taunt


def test_faerie_dragon():
	game = prepare_game(MAGE, MAGE)
	dragon = game.currentPlayer.give("NEW1_023")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	dragon.play()
	moonfire = game.currentPlayer.give(MOONFIRE)
	assert dragon not in moonfire.targets
	assert dragon not in game.currentPlayer.hero.power.targets
	game.endTurn()

	assert dragon not in game.currentPlayer.hero.power.targets
	archer = game.currentPlayer.give("CS2_189")
	assert dragon in archer.targets


def test_far_sight():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.currentPlayer.discardHand()
	farsight = game.currentPlayer.give("CS2_053")
	farsight.play()
	assert len(game.currentPlayer.hand) == 1
	assert game.currentPlayer.hand[0].buffs
	assert game.currentPlayer.hand[0].cost >= 0


def test_flare():
	game = prepare_game(HUNTER, HUNTER)
	flare = game.currentPlayer.give("EX1_544")
	worgen = game.currentPlayer.give("EX1_010")
	worgen.play()
	game.endTurn()

	avenge = game.currentPlayer.give("FP1_020")
	avenge.play()
	game.endTurn()

	flare.play()
	assert not game.currentPlayer.opponent.secrets
	assert not worgen.stealthed


def test_freezing_trap():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.endTurn(); game.endTurn()
	game.endTurn()

	trap = game.player2.give("EX1_611")
	trap.play()
	assert game.player2.secrets
	game.endTurn()

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
	assert game.player1.usedMana == 2
	assert not wisp.buffs
	assert wisp.cost == 0


def test_warlock():
	game = prepare_game(WARLOCK, WARLOCK)
	sacpact = game.currentPlayer.give("NEW1_003")
	assert not sacpact.isPlayable()
	flameimp = game.currentPlayer.give("EX1_319")
	flameimp.play()
	assert game.currentPlayer.hero.health == 27
	assert sacpact.isPlayable()
	sacpact.play(target=flameimp)
	assert game.currentPlayer.hero.health == 30
	game.endTurn()


def main():
	for name, f in globals().items():
		if name.startswith("test_") and hasattr(f, "__call__"):
			f()
	print("All tests ran OK")


if __name__ == "__main__":
	test_dire_wolf_alpha()
	main()
