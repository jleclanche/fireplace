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
    assert wisp1.atk == 4
    assert wisp1.health == 4
    wisp2 = game.player1.give(WISP)
    assert wisp2.atk == 4
    assert wisp2.health == 4
    wisp2.play()
    assert wisp2.atk == 4
    assert wisp2.health == 4
    game.player1.give(MOONFIRE).play(target=wisp1)
    assert wisp1.health == 4 - 1


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


def test_living_mana():
    game = prepare_empty_game()
    assert game.player1.max_mana == 10
    assert game.player1.mana == 10
    game.player1.give("UNG_111").play()
    assert len(game.player1.field) == 7
    assert game.player1.max_mana == 3
    assert game.player1.mana == 3
    for _ in range(7):
        game.player1.field[0].bounce()
    for _ in range(4):
        game.end_turn()
    assert game.player1.max_mana == 5
    assert game.player1.mana == 5
    game.player1.give("UNG_111").play()
    assert len(game.player1.field) == 5
    assert game.player1.max_mana == 0
    assert game.player1.mana == 0
    game.player1.give(MOONFIRE).play(target=game.player1.field[0])
    game.player1.give(MOONFIRE).play(target=game.player1.field[0])
    assert game.player1.max_mana == 1
    assert game.player1.mana == 0


def test_swamp_king_dred():
    game = prepare_game()
    dred = game.player1.give("UNG_919").play()
    game.end_turn()
    game.player2.give(WISP).play()
    assert len(game.player2.field) == 0
    assert dred.health == 9 - 1
    game.player2.give("CS2_033").play()
    assert len(game.player2.field) == 0
    assert dred.health == 9 - 1 - 3
    assert dred.frozen
    game.player2.give(WISP).play()
    assert len(game.player2.field) == 1
    assert dred.health == 9 - 1 - 3


def test_the_voraxx():
    game = prepare_game()
    voraxx = game.player1.give("UNG_843").play()
    game.player1.give("CS2_092").play(target=voraxx)
    assert voraxx.atk == 7
    assert voraxx.health == 7
    assert len(game.player1.field) == 2
    assert game.player1.field[1].atk == 5
    assert game.player1.field[1].health == 5


def test_time_warp():
    game = prepare_game()
    game.player1.give("UNG_028t").play()
    game.end_turn()
    assert game.current_player == game.player1
    game.end_turn()
    assert game.current_player == game.player2
    game.end_turn()
    assert game.current_player == game.player1
    game.player1.give("UNG_028t").play()
    game.player1.give("UNG_028t").play()
    game.end_turn()
    assert game.current_player == game.player1
    game.end_turn()
    assert game.current_player == game.player1
    game.end_turn()
    assert game.current_player == game.player2


def test_clutchmother_zavas():
    game = prepare_empty_game()
    zavas = game.player1.give("UNG_836")
    atk = zavas.atk
    game.player1.give(SOULFIRE).play(target=game.player2.hero)
    assert zavas.atk == atk + 2
    assert zavas.zone == Zone.HAND


def test_quest():
    game = prepare_empty_game()
    quest = game.player1.give("UNG_116").play()
    assert quest.progress == 0
    assert quest.zone == Zone.SECRET
    game.player1.give("CS2_118").play()
    assert quest.progress == 1
    game.player1.give("CS2_118").play()
    assert quest.progress == 2
    game.player1.give("CS2_118").play()
    assert quest.progress == 3
    game.end_turn()
    game.end_turn()
    game.player1.give("CS2_118").play()
    assert quest.progress == 4
    game.player1.give("CS2_118").play()
    assert quest.progress == 5
    assert quest.zone == Zone.GRAVEYARD
    assert game.player1.hand[0].id == "UNG_116t"


def test_rogue_quest():
    game = prepare_empty_game()
    quest = game.player1.give("UNG_067").play()
    assert quest.progress == 0
    game.player1.give(WISP).play()
    assert quest.progress == 1
    game.player1.give(TARGET_DUMMY).play()
    assert quest.progress == 1
    game.player1.give(TARGET_DUMMY).play()
    assert quest.progress == 2
    game.player1.give(WISP).play()
    assert quest.progress == 2
    game.player1.give(WISP).play()
    assert quest.progress == 3
    game.player1.give(WISP).play()
    assert quest.progress == 4
    game.player1.give(WISP).play()
    assert quest.progress == 5
    assert quest.zone == Zone.GRAVEYARD
    assert game.player1.hand[0].id == "UNG_067t1"


def test_mage_quest():
    game = prepare_game(include=tuple(["UNG_028"] + [MOONFIRE] * 29))
    quest = game.player2.hand[0]
    coin = game.player2.hand[-1]
    game.end_turn()
    assert quest.id == "UNG_028"
    quest.play()
    assert quest.progress == 0
    coin.play()
    assert quest.progress == 1
    game.player2.hand[0].play(target=game.player1.hero)
    assert quest.progress == 1
    for i in range(7):
        game.player2.give(MOONFIRE).play(target=game.player1.hero)
        assert quest.progress == i + 2
    assert quest.progress == 8
    assert game.player2.hand[-1].id == "UNG_028t"


def test_blazecaller():
    game = prepare_game()
    blazecaller1 = game.player1.give("UNG_847").play()
    game.end_turn()
    game.end_turn()
    blazecaller1 = game.player1.give("UNG_847").play(target=blazecaller1)


def test_molten_reflection():
    game = prepare_game()
    wisp = game.player1.give(WISP).play()
    game.player1.give("UNG_948").play(target=wisp)
    assert len(game.player1.field) == 2


def test_volcanosaur():
    game = prepare_game()
    game.player1.give("LOE_077").play()
    volcanosaur = game.player1.give("UNG_002").play()
    for _ in range(4):
        choice = game.player1.choice
        assert choice
        choice.choose(choice.cards[0])
    choice = game.player1.choice
    assert not choice
    assert len(volcanosaur.buffs) == 4


def test_hydrologist():
    game = prepare_game(CardClass.WARRIOR, CardClass.WARRIOR)
    game.player1.give("UNG_011").play()
    assert game.player1.choice
    cards = game.player1.choice.cards
    for card in cards:
        assert card.card_class == CardClass.PALADIN
    game.player1.choice.choose(cards[0])

    game = prepare_game(CardClass.MAGE, CardClass.MAGE)
    game.player1.give("UNG_011").play()
    assert game.player1.choice
    cards = game.player1.choice.cards
    for card in cards:
        assert card.card_class == CardClass.MAGE
    game.player1.choice.choose(cards[0])
