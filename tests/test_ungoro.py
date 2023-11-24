from utils import *


def test_adapt_shield_buff():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    wisp.buff(wisp, "UNG_999t8e")
    assert wisp.divine_shield
    game.player1.give(MOONFIRE).play(target=wisp)
    assert not wisp.divine_shield
    assert game.player1.field[0] is wisp


def test_adapt():
    game = prepare_empty_game()
    hatchling = game.player1.give("UNG_001")
    hatchling.play()
    assert game.player1.choice
    cards = game.player1.choice.cards
    game.player1.choice.choose(cards[0])
    assert game.player1.choice is None
    assert hatchling.buffs[0].id == f"{cards[0].id}e"
