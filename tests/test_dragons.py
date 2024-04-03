from utils import *


# TODO test
# 可能有问题的卡牌列表
# 猎人：矮人神射手
# 法师：元素盟军、火球滚滚
# 圣骑士：庇护
# 牧师：拉祖儿的信使、永恒巨龙姆诺兹多
# 中立：灰发巫师、活化龙息、触手恐吓者、克罗斯·龙蹄
# 迦拉克隆

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
