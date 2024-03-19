from utils import *


def test_siamat():
    game = prepare_game()
    siamat = game.player1.give("ULD_178").play()
    choice = game.player1.choice
    choice.choose(choice.cards[0])
    choice = game.player1.choice
    choice.choose(choice.cards[0])
    assert siamat.windfury
    assert siamat.divine_shield


def test_vulpera_scoundrel
ULD_209