from utils import *

def test_kindly_grandmother():
    game = prepare_game()
    grandma = game.player1.give("KAR_005")
    grandma.play()
    assert len(game.player1.field) == 1
    # Kill Grandma
    game.player1.give(MOONFIRE).play(target=grandma)
    assert len(game.player1.field) == 1
    assert game.player1.field[0].id == "KAR_005a"
