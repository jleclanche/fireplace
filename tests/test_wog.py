from utils import *


def test_silithid_swarmer():
	game = prepare_game(ROGUE, ROGUE)
	silithid = game.player1.give("OG_034")
	silithid.play()
	assert not silithid.can_attack()
	game.end_turn(); game.end_turn()

	assert silithid.cant_attack
	assert not silithid.can_attack()
	game.player1.hero.power.use()
	game.player1.hero.attack(target=game.player2.hero)
	assert not silithid.cant_attack
	assert silithid.can_attack()
	silithid.attack(target=game.player2.hero)
	assert game.player2.hero.health == 30 - 1 - 3
	assert not silithid.cant_attack
	assert not silithid.can_attack()

	
def test_corrupted_healbot():
	game = prepare_game()
	hb1 = game.player1.give("OG_147")
	hb1.play()
	hb2 = game.player1.give("OG_147")
	hb2.play()
	game.end_turn()
	game.end_turn()
	hb3 = game.player1.give("OG_147")
	hb3.play()
	hb4 = game.player1.give("OG_147")
	hb4.play()

	game.player2.hero.set_current_health(13)
	assert game.player2.hero.health == 13
	hb1.destroy()
	assert game.player2.hero.health == 13 + 8
	hb2.destroy()
	assert game.player2.hero.health == 13 + 8 + 8
	hb3.destroy()
	assert game.player2.hero.health == 30
	hb4.destroy()
	assert game.player2.hero.health == 30
