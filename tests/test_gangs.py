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

