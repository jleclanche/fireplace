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


def test_vulpera_scoundrel():
    game = prepare_empty_game()
    game.player1.give("ULD_209").play()
    choice = game.player1.choice
    assert len(choice.cards) == 4
    assert choice.cards[3].id == "ULD_209t"
    choice.choose(choice.cards[3])
    assert game.player1.hand[0].type == CardType.SPELL
    assert not game.player1.choice


def test_dwarven_archaeologist():
    game = prepare_empty_game()
    game.player1.give("ULD_309").play()
    game.player1.give("DAL_741").play()
    choice = game.player1.choice
    card = choice.cards[0]
    origin_cost = card.cost
    choice.choose(card)
    assert card.zone == Zone.HAND
    assert card.cost == max(origin_cost - 1, 0)


def test_evil_recruiter():
    game = prepare_game()
    recruiter = game.player1.give("ULD_162")
    assert not recruiter.requires_target()
    wisp = game.player1.summon(WISP)
    assert not recruiter.requires_target()
    lackey = game.player1.summon("DAL_613")
    assert recruiter.requires_target()
    assert wisp not in recruiter.targets
    assert lackey in recruiter.targets
