import pytest
from fireplace.exceptions import GameOver

from utils import *


def test_happy_ghoul():
	game = prepare_game()
	ghoul = game.player1.give("ICC_700")
	assert ghoul.cost == 3
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	game.player1.give("AT_055").play(target=game.player1.hero)
	assert ghoul.cost == 0
	game.end_turn()
	assert ghoul.cost == 3


def test_mindbreaker():
	game = prepare_game()
	breaker = game.player1.give("ICC_902").play()
	assert game.player1.hero.power.exhausted
	assert game.player2.hero.power.exhausted
	breaker.destroy()
	assert not game.player1.hero.power.exhausted
	assert not game.player2.hero.power.exhausted


def test_drakkari_enchanter():
	game = prepare_game()
	game.player1.give("EX1_298").play()
	game.player1.give(THE_COIN).play()
	game.player1.give("ICC_901").play()
	game.end_turn()
	assert game.player2.hero.health == 30 - 8 - 8


def test_fatespinner():
	game = prepare_game()
	game.player1.give("ICC_047").play(choose="ICC_047a")
	game.player1.give("ICC_047").play(choose="ICC_047b")
	assert game.player1.field[0].deathrattles
	assert game.player1.field[1].deathrattles


def test_spreading_plague():
	game = prepare_game()
	for _ in range(4):
		game.player1.give(WISP).play()
	game.end_turn()
	game.player2.give("ICC_054").play()
	assert len(game.player2.field) == 4


def test_malfurion_the_pestilent():
	game = prepare_game()
	game.player1.give("ICC_832").play(choose="ICC_832a")
	game.player1.hero.power.use(choose="ICC_832pa")
	assert game.player1.hero.armor == 5 + 3


def test_deathstalker_rexxar():
	game = prepare_empty_game()
	game.player1.give("ICC_828").play()
	game.player1.hero.power.use()
	assert game.player1.choice
	assert game.player1.choice


def test_bolvar_fireblood():
	game = prepare_game()
	fireblood = game.player1.give("ICC_858").play()
	atk = fireblood.atk
	game.player1.give(MOONFIRE).play(target=fireblood)
	assert fireblood.atk == atk + 2


def test_uther_of_the_ebon_blade():
	game = prepare_game()
	game.player1.give("ICC_829").play()
	game.end_turn()
	game.end_turn()
	for _ in range(3):
		game.player1.hero.power.use()
		game.end_turn()
		game.end_turn()
	with pytest.raises(GameOver):
		game.player1.hero.power.use()


def test_embrace_darkness():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	game.end_turn()
	game.player2.give("ICC_849").play(target=wisp)
	game.end_turn()
	game.end_turn()
	assert len(game.player1.field) == 0
	assert len(game.player2.field) == 1


def test_moorabi():
	game = prepare_empty_game()
	game.player1.give("ICC_289").play()
	wisp = game.player1.give(WISP).play()
	game.player1.give("CS2_031").play(target=wisp)
	assert game.player1.hand[0].id == WISP
