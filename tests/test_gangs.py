import pytest
from utils import *

def test_jade_behemoth():
	game = prepare_game()
	jade_behemoth = game.current_player.give("CFM_343").play()
	assert jade_behemoth.taunt
	jade1 = game.current_player.field[-1]
	assert "CFM_712_t01" == jade1.id
	assert jade1.health == jade1.atk == 1
	jade1.destroy()

	game.end_turn()
	game.end_turn()
	game.current_player.give("CFM_343").play()
	jade2 = game.current_player.field[-1]
	assert jade2.id == "CFM_712_t02"
	assert jade2.health == jade2.atk == 2

def test_jade_blossom():
	game = prepare_game(game_class=Game)
	assert game.current_player.mana == 1
	assert game.current_player.max_mana == 1
	for i in range(4):
		game.end_turn()
	assert game.current_player.mana == 3
	assert game.current_player.max_mana == 3
	assert game.current_player.jade_golem == 1
	blossom = game.current_player.give("CFM_713")
	blossom.play()
	assert len(game.current_player.field) == 1
	jade1 = game.current_player.field[-1]
	assert jade1.health == jade1.atk == 1
	assert game.current_player.jade_golem == 2
	assert game.current_player.mana == 0
	assert game.current_player.max_mana == 4
	assert game.current_player.opponent.max_mana == 2


def test_jade_idol():
	game = prepare_game()
	assert game.current_player.jade_golem == 1
	idol1 = game.current_player.give("CFM_602")
	idol1.play(choose="CFM_602a")
	jade1 = game.current_player.field[-1]
	assert jade1.health == jade1.atk == 1

	assert len(game.current_player.deck) == 26
	assert len(game.current_player.field) == 1
	idol2 = game.current_player.give("CFM_602")
	idol2.play(choose="CFM_602b")
	assert game.current_player.jade_golem == 2
	assert len(game.current_player.field) == 1
	assert len(game.current_player.deck) == 29

	game.current_player.summon(FANDRAL_STAGHELM)
	game.current_player.give("CFM_602").play()
	assert len(game.current_player.field) == 3
	jade3 = game.current_player.field[-1]
	assert jade3.health == jade3.atk == 2
	assert game.current_player.jade_golem == 3
	assert len(game.current_player.deck) == 29 + 3

	# reduce jade_idol's cost to 0
	game.current_player.summon("EX1_608")
	for i in range(26):
		game.current_player.give("CFM_602").play()
		assert game.current_player.jade_golem == 4 + i
		jade_i = game.current_player.field[-1]
		assert jade_i.health == jade_i.atk == 3 + i
		jade_i.destroy()
	# assert len(game.current_player.deck) == 60
