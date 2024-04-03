from utils import *


def test_embiggen():
    game = prepare_empty_game()
    cards = []
    for i in range(1, 11):
        id = f"CFM_712_t{i:02d}"
        card = game.player1.give(id)
        cards.append(card)
        card.shuffle_into_deck()
    game.player1.give("DRG_315").play()
    for i in range(1, 11):
        card = cards[i - 1]
        assert card.atk == i + 2
        assert card.health == i + 2
        assert card.cost == min(i + 1, 10)


def test_strength_in_numbers():
    game = prepare_game()
    sidequest = game.player1.give("DRG_051").play()
    assert sidequest.progress == 0
    assert sidequest.zone == Zone.SECRET
    game.player1.give(THE_COIN).play()
    for i in range(5):
        game.player1.give(MECH).play()
        assert sidequest.progress == (i + 1) * 2
    assert sidequest.zone == Zone.GRAVEYARD


def test_dwarven_sharpshooter():
    game = prepare_game(CardClass.HUNTER, CardClass.HUNTER)
    heropower = game.player1.hero.power
    assert not heropower.requires_target()

    sharpshooter = game.player1.give("DRG_253").play()
    assert heropower.requires_target()
    play_targets = heropower.play_targets
    assert len(play_targets) == 2
    assert game.player1.hero not in play_targets
    assert game.player2.hero in play_targets
    assert sharpshooter in play_targets

    sharpshooter.destroy()
    assert not heropower.requires_target()


def test_rolling_fireball():
    game = prepare_game()

    wisps = [game.player1.give(WISP).play() for i in range(7)]
    assert len(game.player1.field) == 7
    game.player1.give("DRG_321").play(target=wisps[0])
    assert len(game.player1.field) == 0

    game.skip_turn()
    wisps = [game.player1.give(WISP).play() for i in range(7)]
    assert len(game.player1.field) == 7
    game.player1.give("DRG_321").play(target=wisps[3])
    assert len(game.player1.field) == 3
    for i in range(3):
        game.player1.field[0].destroy()

    game.skip_turn()
    wisps = [game.player1.give(WISP).play() for i in range(7)]
    assert len(game.player1.field) == 7
    game.player1.give("DRG_321").play(target=wisps[6])
    assert len(game.player1.field) == 0


def test_elemental_allies():
    game = prepare_empty_game()
    allies = game.player1.give("DRG_324").play()
    game.player1.give(ELEMENTAL).play()
    assert allies.progress == 1
    game.player1.give(ELEMENTAL).play()
    assert allies.progress == 1
    game.skip_turn()
    assert allies.progress == 1
    game.skip_turn()
    assert allies.progress == 0
    game.player1.give(ELEMENTAL).play()
    assert allies.progress == 1
    game.skip_turn()
    assert allies.progress == 1
    game.player1.give(ELEMENTAL).play()
    assert allies.progress == 2
    assert allies.zone == Zone.GRAVEYARD


def test_sanctuary():
    game = prepare_game()
    sanctuary = game.player1.give("DRG_258").play()
    assert sanctuary.progress == 0
    game.end_turn()
    game.player2.give(MOONFIRE).play(target=game.player1.hero)
    game.end_turn()
    assert sanctuary.progress == 0
    game.skip_turn()
    assert sanctuary.progress == 1
    assert sanctuary.zone == Zone.GRAVEYARD
    assert game.player1.field[0] == "DRG_258t"


def test_envoy_of_lazul():
    game = prepare_game()
    game.player1.give("DRG_306").play()
    choice = game.player1.choice
    assert game.player2.hand.contains(choice.correct_card.id)
    assert game.player2.deck.contains(choice.card_1.id)
    assert game.player2.deck.contains(choice.card_2.id)
    card = choice.correct_card
    choice.choose(choice.correct_card)
    assert card in game.player1.hand

    game = prepare_empty_game()
    game.player1.give("DRG_306").play()
    assert not game.player1.choice


def test_murozond_the_infinite():
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    game.player1.give("DS1_233").play()
    game.player1.give("ICC_481").play()
    game.end_turn()

    game.player2.give("DRG_090").play()
    assert game.player2.field[1] == WISP
    assert game.player1.hero.damaged_this_turn == 5
    assert game.player2.hero == "ICC_481"


def test_grizzled_wizard():
    game = prepare_game(CardClass.DRUID, CardClass.HUNTER)
    power1 = game.player1.hero.power
    power2 = game.player2.hero.power
    game.player1.give("DRG_401").play()
    assert game.player1.hero.power == power2.id
    assert game.player2.hero.power == power1.id
    game.end_turn()
    assert game.player1.hero.power == power2.id
    assert game.player2.hero.power == power1.id
    game.end_turn()
    assert game.player1.hero.power == power1.id
    assert game.player2.hero.power == power2.id


def test_living_dragonbreath():
    game = prepare_game()
    dragonbreath = game.player1.give("DRG_068").play()
    wisps = [game.player1.give(WISP).play() for i in range(6)]
    game.end_turn()
    game.player2.give("CS2_026").play()
    assert not dragonbreath.frozen
    for wisp in wisps:
        assert not wisp.frozen
    dragonbreath.destroy()
    for wisp in wisps:
        assert not wisp.frozen
    game.player2.give("CS2_026").play()
    for wisp in wisps:
        assert wisp.frozen
    dragonbreath = game.player1.summon("DRG_068")
    for wisp in wisps:
        assert not wisp.frozen


def test_tentacled_manace():
    game = prepare_empty_game()
    game.player1.give("DRG_084").play()

    game = prepare_game()
    card1_cost = game.player1.deck[-1].cost
    card2_cost = game.player2.deck[-1].cost
    game.player1.give("DRG_084").play()
    assert game.player1.hand[-1].cost == card2_cost
    assert game.player2.hand[-1].cost == card1_cost


def test_kronx_dragonhoof_draw_galakrond():
    game = prepare_empty_game()
    galakrond = game.player1.give("DRG_650")
    galakrond.shuffle_into_deck()
    game.player1.give("DRG_099").play()
    assert galakrond.zone == Zone.HAND


def test_kronx_dragonhoof_draw_unleash_devastation():
    game = prepare_empty_game()
    game.player1.summon("DRG_650")
    wisp = game.player1.give(WISP).play()
    dragonhoof = game.player1.give("DRG_099").play()
    choice = game.player1.choice
    assert choice
    choice.choose(choice.cards[2])
    assert wisp.atk == 1 + 2
    assert wisp.health == 1 + 2
    assert dragonhoof.atk == 6
    assert dragonhoof.health == 6


def test_invoke():
    game = prepare_empty_game()
    galakrond = game.player1.give("DRG_650")
    galakrond.shuffle_into_deck()

    game.player1.give("DRG_303").play()
    assert game.player1.hero.atk == 3
    assert game.player1.invoke_counter == 1
    assert not INVOKED_TWICE.check(game.player1)

    game.player1.give("DRG_303").play()
    assert game.player1.hero.atk == 6
    assert game.player1.invoke_counter == 2
    assert INVOKED_TWICE.check(game.player1)

    assert game.player1.galakrond == "DRG_650t2"
    assert game.player1.deck == ["DRG_650t2"]
    game.player1.give("DRG_303").play()
    game.player1.give("DRG_303").play()
    assert game.player1.galakrond == "DRG_650t3"
    assert game.player1.deck == ["DRG_650t3"]


def test_chaos_gazer():
    game = prepare_empty_game()
    the_coin = game.player2.hand[0]
    game.player1.give("YOD_027").play()
    game.skip_turn()
    assert the_coin.zone == Zone.GRAVEYARD

    molten = game.player2.give("EX1_620")
    game.player1.give("YOD_027").play()
    game.skip_turn()
    assert molten.zone == Zone.HAND

    wisp = game.player2.give(WISP)
    game.player1.give("YOD_027").play()
    game.skip_turn()
    assert wisp.zone == Zone.GRAVEYARD


def test_the_fist_of_raden():
    game = prepare_game()
    coin = game.player1.give(THE_COIN)
    raden = game.player1.give("YOD_042").play()
    coin.play()
    assert raden.damage == 0
    assert len(game.player1.field) == 0

    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert raden.damage == 1
    assert len(game.player1.field) == 1
    assert game.player1.field[0].cost == 4
