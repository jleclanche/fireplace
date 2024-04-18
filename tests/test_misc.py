from fireplace.exceptions import GameOver
from fireplace.managers import BaseObserver
from fireplace.utils import play_turn, setup_game
from full_game import test_full_game
from utils import *


def test_event_queue_heal():
    game = prepare_game()
    shadowboxer1 = game.player1.give("GVG_072")
    shadowboxer1.play()
    shadowboxer2 = game.player1.give("GVG_072")
    shadowboxer2.play()
    game.player1.give(MOONFIRE).play(target=shadowboxer1)
    game.player1.give(MOONFIRE).play(target=shadowboxer2)
    circle = game.player1.give("EX1_621")
    circle.play()
    assert game.player2.hero.health == 26


def test_event_queue_summon():
    game = prepare_empty_game()
    game.player1.give(WISP).play()
    game.player1.give(WISP).play()
    game.end_turn()

    buzzard = game.player2.give("CS2_237")
    buzzard.play()
    reaver = game.player2.give("AT_130")
    reaver.shuffle_into_deck()

    assert reaver in game.player2.deck

    unleash = game.player2.give("EX1_538")
    unleash.play()

    assert reaver in game.player2.hand
    assert buzzard.health == 1
    assert len(game.player2.field) == 1


def test_silence():
    game = prepare_game()
    minion = game.player1.summon("CS2_182")
    assert minion.health == 5
    game.player1.give("CS2_004").play(target=minion)
    assert minion.health == 7
    game.player1.give("GVG_015").play(target=minion)
    assert minion.health == 4
    game.player1.give("CS2_203").play(target=minion)
    assert minion.health == 4


def test_anubar_ambusher_cult_master():
    # https://github.com/jleclanche/fireplace/issues/126
    game = prepare_game()
    game.player1.discard_hand()
    cultmaster1 = game.player1.summon("EX1_595")
    ambusher1 = game.player1.summon("FP1_026")
    assert len(game.player1.hand) == 0
    ambusher1.destroy()
    assert len(game.player1.hand) == 2
    assert cultmaster1 in game.player1.hand
    game.skip_turn()

    game.player1.discard_hand()
    ambusher2 = game.player1.summon("FP1_026")
    cultmaster2 = game.player1.summon("EX1_595")
    assert len(game.player1.hand) == 0
    ambusher2.destroy()
    assert len(game.player1.hand) == 1
    assert cultmaster2 in game.player1.hand


def test_copy_voljin():
    game = prepare_empty_game()
    wisp = game.player1.give(WISP).play()
    voljin = game.player1.give("GVG_014").play(target=wisp)
    game.end_turn()
    game.player2.give("EX1_564").play(target=voljin)
    voljin_copy = game.player2.field[0]
    assert voljin_copy.atk == voljin.atk
    assert voljin_copy.health == voljin.health


def test_lifesteal_and_auchenai():
    game = prepare_game()
    game.player1.give("EX1_591").play()
    game.player1.give("TRL_512").play(target=game.player2.hero)
    assert game.player1.hero.health == 29
    assert game.player2.hero.health == 29


def test_mirror_entity_and_pumpkin_peasant():
    game = prepare_empty_game()
    game.player1.give("GIL_201")
    game.end_turn()
    game.player2.give("EX1_294").play()
    game.end_turn()
    for _ in range(3):
        game.skip_turn()
    game.player1.hand[0].play()
    minion1 = game.player1.field[0]
    minion2 = game.player2.field[0]
    assert minion1.id == minion2.id
    assert minion1.atk == minion2.atk
    assert minion1.health == minion2.health


def test_nefarian_and_ragnaros_hero():
    game = prepare_empty_game()
    game.end_turn()
    game.player2.give("BRM_027").play().destroy()
    assert game.player2.hero.card_class == CardClass.NEUTRAL
    game.end_turn()
    game.player1.give("BRM_030").play()
    assert len(game.player1.hand) == 2
    assert game.player1.hand[0].id == "BRM_030t"
    assert game.player1.hand[0].id == "BRM_030t"


def test_lilian_voss_and_ragnaros_hero():
    game = prepare_empty_game()
    game.end_turn()
    game.player2.give("BRM_027").play().destroy()
    assert game.player2.hero.card_class == CardClass.NEUTRAL
    game.end_turn()
    game.player1.give(MOONFIRE)
    game.player1.give(MOONFIRE)
    game.player1.give("ICC_811").play()
    assert len(game.player1.hand) == 2
    assert game.player1.hand[0].id == MOONFIRE
    assert game.player1.hand[0].id == MOONFIRE


def test_darkspeaker_and_shudderwock():
    game = prepare_game()
    darkspeaker = game.player1.give("OG_102").play()
    game.skip_turn()
    shudderwock = game.player1.give("GIL_820")
    darkspeaker_atk = darkspeaker.atk
    darkspeaker_health = darkspeaker.health
    shudder_atk = shudderwock.atk
    shudder_health = shudderwock.health
    shudderwock.play()
    assert darkspeaker.atk == shudder_atk
    assert darkspeaker.health == shudder_health
    assert shudderwock.atk == darkspeaker_atk
    assert shudderwock.health == darkspeaker_health


def test_doppelgangster_and_shudderwock():
    game = prepare_game()
    doppelgangster = game.player1.give("CFM_668").play()
    game.skip_turn()
    shudderwock = game.player1.give("GIL_820").play()
    for i in range(0, 3):
        assert game.player1.field[i].id == doppelgangster.id
    for i in range(3, 6):
        assert game.player1.field[i].id == shudderwock.id


def test_reborn():
    game = prepare_game()
    moon = game.player1.give("ULD_721").play()
    moon.destroy()
    new_moon = game.player1.field[0]
    assert new_moon.id == "ULD_721"
    assert new_moon.health == 1
    assert not new_moon.reborn
    assert new_moon.divine_shield
    new_moon.destroy()
    assert len(game.player1.field) == 0


def test_echo_cannot_be_reduced_below_1_mana():
    game = prepare_empty_game()
    game.player1.summon("EX1_608")
    game.player1.summon("EX1_608")
    bells = game.player1.give("GIL_145")
    assert bells.cost == 0
    bells.play(target=game.player1.field[0])
    bells_echo = game.player1.hand[0]
    assert bells_echo.cost == 1
    bells_echo.play(target=game.player1.field[0])
    bells_echo_2 = game.player1.hand[0]
    assert bells_echo_2.cost == 1


def test_copy_deathrattle_with_store_card():
    game = prepare_empty_game()
    pc = game.player1.give("UNG_953").play()
    game.player1.give("CS2_092").play(target=pc)
    game.player1.give("CS2_092").play(target=pc)
    game.skip_turn()
    raptor = game.player1.give("LOE_019").play(target=pc)
    pc.destroy()
    assert game.player1.hand == ["CS2_092"] * 2
    raptor.destroy()
    assert game.player1.hand == ["CS2_092"] * 4


def test_observer():
    class Manager(BaseObserver):
        def __init__(self, game) -> None:
            super().__init__()
            self.game = game
            self.game_state = {}

        def add_to_state(self, entity):
            state = self.game_state[entity.entity_id] = {}
            state[GameTag.ENTITY_ID] = entity

        def new_entity(self, entity):
            self.add_to_state(entity)

        def start_game(self):
            self.add_to_state(self.game)

        def get_entity(self, entity_id):
            if not entity_id:
                return None
            return self.game_state[entity_id][GameTag.ENTITY_ID]

        def game_action(self, action, source, *args):
            action_data = {
                "type": action.__class__.__name__,
                "source": source,
                "target": None,
                "args": args,
            }
            self.dump_board()

        def targeted_action(self, action, source, target, *args):
            action_data = {
                "type": action.__class__.__name__,
                "source": source,
                "target": target,
                "args": args,
            }
            self.dump_board()

        def dump_board(self):
            for player in self.game.players:
                data = {
                    "entity_id": self.game.entity_id,
                    "players": [
                        player.dump(),
                        player.opponent.dump_hidden(),
                    ],
                }

    try:
        game = setup_game()
        game.manager.register(Manager(game))
        for player in game.players:
            log.info("Can mulligan %r" % (player.choice.cards))
            mull_count = random.randint(0, len(player.choice.cards))
            cards_to_mulligan = random.sample(player.choice.cards, mull_count)
            player.choice.choose(*cards_to_mulligan)
        while True:
            play_turn(game)
    except GameOver:
        log.info("Game completed normally.")
