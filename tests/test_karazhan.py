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

def test_cloaked_huntress():
    game = prepare_game()
    huntress = game.player1.give("KAR_006")
    # Freezing Trap
    secret = game.player1.give("EX1_611")
    huntress.play()
    # Check cost of secret
    assert secret.cost == 0
    # Kill Huntress
    for i in range(4):
        game.player1.give(MOONFIRE).play(target=huntress)
    
    assert secret.cost == 2
