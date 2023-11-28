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


def test_primalfin_champion():
    game = prepare_empty_game()
    pc = game.player1.give("UNG_953").play()
    game.player1.give("CS2_092").play(target=pc)
    game.player1.give(FIREBALL).play(target=pc)
    assert game.player1.hand[0].id == "CS2_092"
    assert game.player1.hand[1].id == FIREBALL


def test_curious_glimmerroot():
    game = prepare_game()
    game.player1.give("UNG_035").play()
    choice = game.player1.choice
    starting_ids = [card.id for card in game.player2.starting_deck]
    for card in choice.cards:
        if card is choice.starting_card:
            assert card.id in starting_ids
        else:
            assert card.id not in starting_ids

    hands = len(game.player1.hand)
    choice.choose(choice.starting_card)
    assert game.player1.choice is None
    assert len(game.player1.hand) == hands + 1

    game.player1.give("UNG_035").play()
    choice = game.player1.choice
    choice.choose(choice.other_card_1)
    assert game.player1.choice is None
    assert len(game.player1.hand) == hands + 1


def test_sherazin_corpse_flower():
    game = prepare_game()
    flower = game.player1.give("UNG_065").play()
    game.player1.give(FIREBALL).play(target=flower)
    assert game.player1.field[0].id == "UNG_065t"
    game.end_turn()
    game.end_turn()
    flower = game.player1.give("UNG_065").play()
    game.player1.give("EX1_622").play(target=flower)
    assert game.player1.field[1].id == "UNG_065t"
    game.end_turn()
    game.end_turn()
    flower = game.player1.give("UNG_065").play()
    game.player1.give("GVG_026").play()
    assert game.player1.field[2].id == "UNG_065t"


def test_sherazin_seed():
    game = prepare_game()
    flower = game.player1.give("UNG_065").play()
    game.end_turn()
    game.player2.give(FIREBALL).play(target=flower)
    assert game.player1.field[0].id == "UNG_065t"
    game.end_turn()
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    game.player1.give(MOONFIRE).play(target=game.player2.hero)
    assert game.player1.field[0].id == "UNG_065"


def test_crystal_core():
    game = prepare_game()
    wisp1 = game.player1.give(WISP).play()
    game.player1.give("UNG_067t1").play()
    assert wisp1.atk == 5
    assert wisp1.health == 5
    wisp2 = game.player1.give(WISP)
    assert wisp2.atk == 5
    assert wisp2.health == 5
    wisp2.play()
    assert wisp2.atk == 5
    assert wisp2.health == 5
    game.player1.give(MOONFIRE).play(target=wisp1)
    assert wisp1.health == 4


def test_kalimos_primal_lord():
    game = prepare_game()
    game.player1.give("UNG_809t1").play()
    game.end_turn()
    game.end_turn()
    game.player1.give("UNG_211").play()
    choice = game.player1.choice
    assert choice
    choice.choose(choice.cards[0])
    assert len(game.player1.field) == 7


def test_corrupting_mist():
    game = prepare_game()
    game.player1.give(WISP).play()
    game.end_turn()
    game.player2.give(WISP).play()
    game.end_turn()
    game.player1.give("UNG_831").play()
    game.end_turn()
    assert len(game.player1.field) == 1
    assert len(game.player2.field) == 1
    game.end_turn()
    assert len(game.player1.field) == 0
    assert len(game.player2.field) == 0
