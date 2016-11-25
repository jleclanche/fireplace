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

def test_babbling_book():
    game = prepare_game()
    game.player1.discard_hand()
    book = game.player1.give("KAR_009")
    book.play()

    assert len(game.player1.hand) == 1
    assert game.player1.hand[0].type == CardType.SPELL

def test_nightbane_templar():
    game = prepare_game()
    nightbane1 = game.player1.give("KAR_010")
    assert not nightbane1.powered_up
    nightbane1.play()
    assert len(game.player1.field) == 1
    game.end_turn()

    game.player2.give(WHELP)
    nightbane2 = game.player2.give("KAR_010")
    assert nightbane2.powered_up
    nightbane2.play()
    assert len(game.player2.field) == 3

def test_wicked_witchdoctor():
    game = prepare_game(CardClass.SHAMAN, CardClass.SHAMAN)
    witchdoc = game.player1.give("KAR_021")
    witchdoc.play()
    game.player1.give(THE_COIN).play()

    assert len(game.player1.field) == 2
    
    game.player1.give(TIME_REWINDER).play(target=witchdoc)

    assert game.player1.field[-1].id in game.player1.hero.power.data.entourage

