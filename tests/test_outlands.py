from utils import *


def test_kaelthas_sunstrider():
    game = prepare_empty_game()
    fireball = game.player1.give(FIREBALL)
    game.player1.give(THE_COIN).play()
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4
    game.player1.give("BT_255").play()
    assert fireball.cost == 0
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 4
    game.player1.give(THE_COIN).play()
    assert fireball.cost == 0
