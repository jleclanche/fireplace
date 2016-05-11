from utils import *


def test_auchenai_soulpriest():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)
	auchenai = game.player1.give("EX1_591")
	auchenai.play()
	game.player1.hero.power.use(target=game.player2.hero)
	assert game.player2.hero.health == 28
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert auchenai.health == 1


def test_auchenai_soulpriest_divine_shield():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)
	gurubashi = game.player1.summon("EX1_399")
	auchenai = game.player1.give("EX1_591")
	auchenai.play()
	game.player1.give(HAND_OF_PROTECTION).play(target=gurubashi)
	assert gurubashi.divine_shield
	game.player1.hero.power.use(target=gurubashi)
	assert not gurubashi.divine_shield
	assert gurubashi.atk == 2
	assert gurubashi.health == 7


def test_auchenai_soulpriest_light_of_the_naaru():
	game = prepare_game()
	soulpriest = game.player1.give("EX1_591")
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


def test_auchenai_soulpriest_power_word_glory():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	pwglory = game.player1.give("AT_013")
	pwglory.play(target=wisp)
	auchenai = game.player1.give("EX1_591")
	auchenai.play()
	game.end_turn(); game.end_turn()

	assert game.player1.hero.health == 30
	wisp.attack(game.player2.hero)
	assert game.player1.hero.health == 30 - 4


def test_auchenai_soulpriest_stoneskin_gargoyle_():
	game = prepare_game()
	gargoyle = game.player1.give("FP1_027")
	gargoyle.play()
	soulpriest = game.player1.give("EX1_591")
	soulpriest.play()
	game.end_turn(); game.end_turn()

	assert gargoyle.health == 4
	game.player1.give(MOONFIRE).play(target=gargoyle)
	assert gargoyle.health == 3
	game.end_turn(); game.end_turn()

	assert gargoyle.health == 2
	game.end_turn(); game.end_turn()

	assert gargoyle.dead
