from utils import *


def test_lesser_jasper_spellstone():
    game = prepare_empty_game(CardClass.DRUID, CardClass.DRUID)
    game.player1.give("LOOT_051")
    game.player1.give("CFM_308").play(choose="CFM_308a")
    assert game.player1.hand[0].id == "LOOT_051t1"
    game.skip_turn()
    game.player1.hero.power.use()
    assert game.player1.hand[0].id == "LOOT_051t1"
    assert game.player1.hand[0].progress == 1
    game.skip_turn()
    game.player1.hero.power.use()
    assert game.player1.hand[0].id == "LOOT_051t1"
    assert game.player1.hand[0].progress == 2
    game.skip_turn()
    game.player1.hero.power.use()
    assert game.player1.hand[0].id == "LOOT_051t2"


def test_branching_paths():
    game = prepare_game()
    game.player1.give("LOOT_054").play()
    choice = game.player1.choice
    assert choice
    choice.choose(choice.cards[1])
    assert game.player1.hero.armor == 6
    choice = game.player1.choice
    assert choice
    choice.choose(choice.cards[1])
    choice = game.player1.choice
    assert not choice
    assert game.player1.hero.armor == 12


def test_raven_familiar():
    game = prepare_empty_game()
    game.player1.give(FIREBALL).shuffle_into_deck()
    game.player2.give(MOONFIRE).shuffle_into_deck()
    game.player1.give("LOOT_170").play()
    assert game.player1.hand[0].id == FIREBALL


def test_explosive_runes():
    game = prepare_game()
    game.player1.give("LOOT_101").play()
    game.end_turn()
    game.player2.give(WISP).play()
    assert len(game.player2.field) == 0
    assert game.player2.hero.health == 25


def test_the_darkness():
    game = prepare_empty_game()
    game.player1.give("LOOT_526").play()
    assert game.player1.field[0].id == "LOOT_526d"
    game.skip_turn()
    game.skip_turn()
    game.skip_turn()
    assert game.player1.field[0].id == "LOOT_526"


def test_king_togwaggle():
    game = prepare_game()
    deck1 = [card.id for card in game.player1.deck]
    deck2 = [card.id for card in game.player2.deck]
    game.player1.give("LOOT_541").play()
    assert deck1 == [card.id for card in game.player2.deck]
    assert deck2 == [card.id for card in game.player1.deck]
