from utils import *


def test_duskhaven_hunter():
    game = prepare_empty_game()
    game.player1.give("GIL_200")
    game.player1.give("GIL_128").play()
    assert game.player1.hand[0].atk == 4
    assert game.player1.hand[0].health == 10
    game.skip_turn()
    assert game.player1.hand[0].atk == 10
    assert game.player1.hand[0].health == 4


def test_echo():
    game = prepare_empty_game()
    game.player1.give("GIL_680")
    for _ in range(3):
        game.player1.hand[0].play()
        assert game.player1.hand[0].id == "GIL_680"
    game.end_turn()
    assert len(game.player1.hand) == 0
    assert len(game.player1.field) == 3


def test_wing_blast():
    game = prepare_game()
    wing_blast = game.player1.give("GIL_518")
    assert wing_blast.cost == 4
    wisp = game.player1.give(WISP).play()
    game.player1.give(MOONFIRE).play(target=wisp)
    assert wing_blast.cost == 1


def test_tess_greymane():
    game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
    game.player1.give("CS2_065").play()
    game.player1.give("EX1_169").play()
    mana = game.player1.mana
    tess = game.player1.give("GIL_598")
    tess.play()
    assert len(game.player1.field) == 3
    assert game.player1.mana == mana - tess.cost + 1


def test_shudderwock():
    game = prepare_game()
    for _ in range(2):
        engineer = game.player1.give("EX1_015").play()
        engineer.destroy()
    game.skip_turn()
    hand = len(game.player1.hand)
    shudderwock = game.player1.give("GIL_820")
    shudderwock.play()
    assert len(game.player1.hand) == hand + 2


def test_lady_in_white():
    game = prepare_game()
    game.player1.give("GIL_840").play()
    for card in game.player1.deck:
        if card.type == CardType.MINION:
            assert card.atk == card.health


def test_murkspark_eel():
    game = prepare_game()
    eel = game.player1.give("GIL_530")
    assert not eel.requires_target()
    eel.play()

    game = prepare_empty_game()
    eel = game.player1.give("GIL_530")
    assert eel.requires_target()
    eel.play(target=game.player2.hero)


def test_baku_and_genn():
    player1 = Player("Player1", [CHICKEN] * 29 + ["GIL_826"], "HERO_01")
    player2 = Player("Player1", [WISP] * 29 + ["GIL_692"], "HERO_02")
    game = BaseTestGame(players=(player1, player2))
    game.start()
    assert player1.hero.power.id == "HERO_01bp2"
    assert player2.hero.power.cost == 1
