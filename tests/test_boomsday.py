from utils import *


def test_magnetic():
    game = prepare_game()
    mech = game.player1.give(MECH).play()
    atk = mech.atk
    health = mech.health
    assert not mech.rush
    magnetic1 = game.player1.give("BOT_020")
    magnetic1.play(index=0)
    assert len(game.player1.field) == 1
    assert mech.atk == atk + 1
    assert mech.health == health + 1
    assert mech.rush
    magnetic1 = game.player1.give("BOT_020")
    magnetic1.play()
    assert len(game.player1.field) == 2


def test_whizbang():
    player1 = Player("Player1", ["BOT_914"], "BOT_914h")
    player2 = Player("Player1", ["BOT_914"], "BOT_914h")
    game = BaseTestGame(players=(player1, player2))
    game.start()
    assert len(game.player1.starting_deck) == 30
    assert len(game.player2.starting_deck) == 30


def test_stargazer_luna():
    game = prepare_game()
    game.player1.discard_hand()
    game.player1.give("BOT_103").play()
    assert len(game.player1.hand) == 0
    for _ in range(3):
        game.player1.give(WISP)
    assert len(game.player1.hand) == 3
    game.player1.hand[-1].play()
    assert len(game.player1.hand) == 3
    game.player1.hand[1].play()
    assert len(game.player1.hand) == 2


def test_prismatic_lens():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP)
    wisp.shuffle_into_deck()
    fireball = game.player1.give(FIREBALL)
    fireball.shuffle_into_deck()
    game.player1.give("BOT_436").play()
    assert wisp in game.player1.hand
    assert fireball in game.player1.hand
    assert wisp.cost == 4
    assert fireball.cost == 0


def test_kangors_endless_army():
    game = prepare_game()
    mech = game.player1.give(MECH).play()
    atk = mech.atk
    health = mech.health
    magnetic = game.player1.give("BOT_020")
    magnetic.play(index=0)
    game.player1.give("CS2_092").play(target=mech)
    mech.destroy()
    game.skip_turn()
    game.player1.give("BOT_912").play()
    assert len(game.player1.field) == 1
    mech = game.player1.field[0]
    assert mech.atk == atk + 1
    assert mech.health == health + 1
    assert mech.rush


def test_myra_rotspring():
    game = prepare_game()
    myra = game.player1.give("BOT_243")
    myra.play()
    game.player1.choice.choose(game.player1.choice.cards[0])


def test_electra_stormsurge():
    game = prepare_game()
    game.player1.give("BOT_411").play()
    game.player1.give("EX1_238").play(target=game.player2.hero)
    assert game.player2.hero.health == 24
    assert game.player1.overloaded == 2

    game.player1.give("EX1_238").play(target=game.player2.hero)
    assert game.player2.hero.health == 21


def test_holomancer():
    game = prepare_game()
    game.player1.give("BOT_280").play()
    game.end_turn()
    game.player2.give(MECH).play()
    assert len(game.player1.field) == 2
    new_mech = game.player1.field[1]
    assert new_mech.id == MECH
    assert new_mech.atk == 1
    assert new_mech.max_health == 1


def test_flarks_boom_zooka():
    game = prepare_game()
    game.player1.give("BOT_429").play()


def test_zereks_cloning_gallery_when_empty():
    game = prepare_empty_game()
    game.player1.give("BOT_567").play()


def test_omega_mind():
    game = prepare_game()
    game.player1.give("BOT_543").play()
    game.player1.hero.set_current_health(1)
    game.player1.give(FIREBALL).play(target=game.player2.hero)
    assert game.player1.hero.health == 1 + 6
