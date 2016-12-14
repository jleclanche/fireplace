from utils import *

def test_celestial_dreamer():
	game = prepare_game()
	dreamer = game.player1.give("CFM_617")
	assert not dreamer.powered_up

	wisp = game.player1.give(WISP).play()
	po = game.player1.give("EX1_316").play(target=wisp) #Power Overwhelming

	assert dreamer.powered_up

	dreamer.play()
	assert dreamer.buffs
	assert dreamer.atk == 5
	assert dreamer. health == 5

def test_virmen_sensei():
	game = prepare_empty_game()
	sensei1 = game.player1.give("CFM_816")
	wisp = game.player1.give(WISP).play()
	assert not sensei1.powered_up

	sensei1.play()

	beast = game.player1.give(CHICKEN).play()
	sensei2 = game.player1.give("CFM_816")
	assert sensei2.powered_up
	game.player1.give(INNERVATE).play()
	sensei2.play(target=beast)

	assert beast.buffs
	assert beast.atk == 3
	assert beast.health == 3

def test_mark_of_the_lotus():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	chicken = game.player1.give(CHICKEN).play()

	assert wisp.atk == 1
	assert chicken.atk == 1
	lotus = game.player1.give("CFM_614").play()

	assert wisp.buffs
	assert wisp.atk == 2
	assert wisp.health == 2
	assert chicken.buffs
	assert chicken.atk == 2
	assert chicken.health == 2

def test_pilfered_power():
	game = prepare_game(game_class=Game)
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	assert game.player1.max_mana == 3
	pilfered1 = game.player1.give("CFM_616")
	pilfered1.play()
	assert game.player1.mana == 0
	assert game.player1.used_mana == 3
	assert game.player1.max_mana == 3

	game.end_turn(); game.end_turn()

	assert game.player1.max_mana == 4
	livingroots = game.player1.give("AT_037").play(choose="AT_037b")
	assert len(game.player1.field) == 2
	pilfered2 = game.player1.give("CFM_616").play()
	assert game.player1.mana == 0
	assert game.player1.used_mana == 4 + 2
	assert game.player1.max_mana ==  4 + 2

	for i in range(4):
		game.end_turn(); game.end_turn()

	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	assert game.player1.max_mana == 10
	pilfered3 = game.player1.give("CFM_616").play()
	assert len(game.player1.hand) == 1
	assert game.player1.max_mana == 10
	excess_mana = game.player1.hand[0]
	assert excess_mana.id == "CS2_013t"
	excess_mana.play()
	assert len(game.player1.hand) == 1

