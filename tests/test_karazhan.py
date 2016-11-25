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

def test_book_wyrm():
    game = prepare_game()
    game.player1.discard_hand()
    whelp = game.player1.give(WHELP)
    bookwyrm1 = game.player1.give("KAR_033")
    assert not bookwyrm1.powered_up
    bookwyrm1.play()
    assert len(game.player1.field) == 1
    game.end_turn()

    game.player2.discard_hand()
    game.player2.give(WHELP)
    bookwyrm2 = game.player2.give("KAR_033")
    assert bookwyrm2.powered_up
    bookwyrm2.play(target=bookwyrm1)
    assert len(game.player1.field) == 0
    assert len(game.player2.field) == 1
    game.end_turn()

def test_priest_of_the_feast():
    game = prepare_game()
    priest = game.player1.give("KAR_035")
    game.player1.give(DAMAGE_5).play(target=game.player1.hero)
    assert game.player1.hero.health == 25
    priest.play()
    game.player1.give(THE_COIN).play()
    assert game.player1.hero.health == 28

def test_arcane_anomaly():
    game = prepare_game()
    anomaly = game.player1.give("KAR_036")
    anomaly.play()
    assert anomaly.health == 1
    game.player1.give(THE_COIN).play()
    assert anomaly.health == 2
    game.player1.give(THE_COIN).play()
    assert anomaly.health == 3

def test_avian_watcher():
    game = prepare_game()
    watcher1 = game.player1.give("KAR_037")
    assert not watcher1.powered_up
    watcher1.play()
    assert watcher1.health == 6
    assert watcher1.atk == 3
    game.end_turn()

    watcher2 = game.player2.give("KAR_037")
    secret = game.player2.give("EX1_611")
    assert not watcher2.powered_up
    secret.play()
    assert watcher2.powered_up
    watcher2.play()
    assert watcher2.health == 7
    assert watcher2.atk == 4