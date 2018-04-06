from utils import *

def test_living_spores():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	spores = game.player1.give("UNG_999t2")
	assert not wisp.has_deathrattle
	spores.play(target=wisp)
	assert len(game.player1.field) == 1
	assert wisp.has_deathrattle
	wisp.destroy()
	assert len(game.player1.field) == 2
	assert game.player1.field[0].id == game.player1.field[1].id == "UNG_999t2t1"


def test_flaming_claws():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	claws = game.player1.give("UNG_999t3")
	assert wisp.atk == wisp.health == 1
	claws.play(target=wisp)
	assert wisp.atk == 4
	assert wisp.health == 1


def test_rocky_carapace():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	cara = game.player1.give("UNG_999t3")
	assert wisp.atk == wisp.health == 1
	cara.play(target=wisp)
	assert wisp.atk == 1
	assert wisp.health == 4
	

def test_liquid_membrane():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	wisp = game.player1.give(WISP)
	wisp.play()
	cara = game.player1.give("UNG_999t3")
	moonfire1 = game.player1.give(MOONFIRE)
	archer1 = game.player1.give("CS2_189")
	assert wisp in moonfire1.targets
	assert wisp in game.player1.hero.power.targets
	assert wisp in archer1.targets
	game.end_turn()

	moonfire2 = game.player2.give(MOONFIRE)
	archer2 = game.player2.give("CS2_189")
	assert wisp in moonfire2.targets
	assert wisp in game.player2.hero.power.targets
	assert wisp in archer2.targets
	game.end_turn()

	cara.play(target=wisp)
	assert wisp not in moonfire1.targets
	assert wisp not in game.player1.hero.power.targets
	assert wisp in archer1.targets
	game.end_turn()

	assert wisp not in moonfire2.targets
	assert wisp not in game.player2.hero.power.targets
	assert wisp in archer2.targets


def test_massive():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	massive = game.player1.give("UNG_999t6")
	assert not wisp.taunt
	massive.play(target=wisp)
	assert wisp.taunt


def test_lightning_speed():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	speed = game.player1.give("UNG_999t7")
	assert not wisp.windfury
	speed.play(target=wisp)
	assert wisp.windfury


def test_crackling_shield():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	shield = game.player1.give("UNG_999t8")
	assert not wisp.divine_shield
	shield.play(target=wisp)
	assert wisp.divine_shield


def test_shrouding_mist():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	mist = game.player1.give("UNG_999t10")
	assert not wisp.stealth
	mist.play(target=wisp)
	assert wisp.stealth
	game.end_turn()
	game.end_turn()

	assert not wisp.stealth


def test_poison_spit():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	spit = game.player1.give("UNG_999t13")
	assert not wisp.poisonous
	spit.play(target=wisp)
	assert wisp.poisonous


def test_volcanic_might():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	might = game.player1.give("UNG_999t14")
	assert wisp.atk == wisp.health == 1
	might.play(target=wisp)
	assert wisp.atk == wisp.health == 2
