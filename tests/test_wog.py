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
