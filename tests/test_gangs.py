import pytest
from utils import *


def test_aya_blackpaw():
	game = prepare_game()
	assert game.current_player.jade_golem == 1
	aya = game.current_player.give("CFM_902").play()
	assert game.current_player.field[1].id == "CFM_712_t01"
	assert game.current_player.jade_golem == 2
	aya.destroy()
	assert game.current_player.jade_golem == 3
	jade2 = game.current_player.field[-1]
	assert jade2.id == "CFM_712_t02"
	assert jade2.health == jade2.atk == 2


def test_jade_behemoth():
	game = prepare_empty_game()
	card = game.current_player.give("CFM_343")
	hand_description, description = card.data.description.replace("[x]", "").split("@")
	assert card.description == hand_description.format("1/1", "")
	card.play()
	assert card.taunt
	assert card.description == description
	jade = game.current_player.field[-1]
	assert "CFM_712_t01" == jade.id
	assert jade.health == jade.atk == 1
	jade.destroy()
	card.destroy()

	game.end_turn()
	game.end_turn()
	card2 = game.current_player.give("CFM_343")
	assert card2.description == hand_description.format("2/2", "")
	card2.play()
	assert card2.description == description
	jade2 = game.current_player.field[-1]
	assert jade2.id == "CFM_712_t02"
	assert jade2.health == jade2.atk == 2
	jade2.destroy()
	card2.destroy()

	for i in range(3, 8):
		game.end_turn()
		game.end_turn()
		card = game.current_player.give("CFM_343")
		assert card.description == hand_description.format(f"{i}/{i}", "")
		card.play()
		assert card.taunt
		assert card.description == description
		jade = game.current_player.field[-1]
		assert f"CFM_712_t0{i}" == jade.id
		assert jade.health == jade.atk == i
		jade.destroy()
		card.destroy()

	game.end_turn()
	game.end_turn()
	card = game.current_player.give("CFM_343")
	assert card.description == hand_description.format("8/8", "n")
	card.play()
	assert card.taunt
	assert card.description == description
	jade = game.current_player.field[-1]
	assert "CFM_712_t08" == jade.id
	assert jade.health == jade.atk == 8


def test_pilfered_power():
	game = prepare_game(game_class=Game)
	for _ in range(2):
		game.end_turn()
		game.end_turn()
	assert game.player1.max_mana == 3
	for _ in range(3):
		game.player1.give(WISP).play()
	pilfered_power_1 = game.player1.give("CFM_616")
	pilfered_power_1.play()
	assert game.player1.mana == 0
	assert game.player1.used_mana == 3 + 3
	assert game.player1.max_mana == 3 + 3

	for _ in range(3):
		game.end_turn()
		game.end_turn()
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	assert game.player1.max_mana == 9
	pilfered_power_2 = game.player1.give("CFM_616")
	pilfered_power_2.play()
	assert len(game.player1.hand) == 0
	assert game.player1.mana == 6
	assert game.player1.max_mana == 10
	assert game.player1.used_mana == 4

	game.end_turn()
	game.end_turn()
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	assert game.player1.max_mana == 10
	pilfered_power_3 = game.player1.give("CFM_616")
	pilfered_power_3.play()
	excess_mana = game.player1.hand[0]
	assert excess_mana.id == "CS2_013t"
	excess_mana.play()
	assert len(game.player1.hand) == 1


def test_jade_blossom():
	game = prepare_game(game_class=Game)
	assert game.current_player.mana == 1
	assert game.current_player.max_mana == 1
	for i in range(4):
		game.end_turn()
	assert game.current_player.mana == 3
	assert game.current_player.max_mana == 3
	assert game.current_player.jade_golem == 1
	blossom = game.current_player.give("CFM_713")
	blossom.play()
	assert len(game.current_player.field) == 1
	jade1 = game.current_player.field[-1]
	assert jade1.health == jade1.atk == 1
	assert game.current_player.jade_golem == 2
	assert game.current_player.mana == 0
	assert game.current_player.max_mana == 4
	assert game.current_player.opponent.max_mana == 2


def test_jade_chieftain():
	game = prepare_game()
	assert game.current_player.jade_golem == 1
	chieftain = game.current_player.give("CFM_312").play()
	assert game.current_player.jade_golem == 2
	assert game.current_player.field[1].id == "CFM_712_t01"
	assert game.current_player.field[1].taunt
	assert not chieftain.taunt


def test_jade_claws():
	game = prepare_game()
	assert game.current_player.jade_golem == 1
	game.current_player.give("CFM_717").play()
	assert game.current_player.field[0].id == "CFM_712_t01"
	assert game.current_player.jade_golem == 2
	game.current_player.hero.attack(game.current_player.opponent.hero)
	assert game.current_player.opponent.hero.health == 28

	game.current_player.summon("LOE_077")
	game.current_player.give("CFM_717").play()
	assert game.current_player.field[2].id == "CFM_712_t02"
	assert game.current_player.field[3].id == "CFM_712_t03"
	assert game.current_player.jade_golem == 4


def test_jade_idol():
	game = prepare_game()
	assert game.current_player.jade_golem == 1
	idol1 = game.current_player.give("CFM_602")
	idol1.play(choose="CFM_602a")
	jade1 = game.current_player.field[-1]
	assert jade1.health == jade1.atk == 1

	assert len(game.current_player.deck) == 26
	assert len(game.current_player.field) == 1
	idol2 = game.current_player.give("CFM_602")
	idol2.play(choose="CFM_602b")
	assert game.current_player.jade_golem == 2
	assert len(game.current_player.field) == 1
	assert len(game.current_player.deck) == 29

	game.current_player.summon(FANDRAL_STAGHELM)
	game.current_player.give("CFM_602").play()
	assert len(game.current_player.field) == 3
	jade3 = game.current_player.field[-1]
	assert jade3.health == jade3.atk == 2
	assert game.current_player.jade_golem == 3
	assert len(game.current_player.deck) == 29 + 3

	# reduce jade_idol's cost to 0
	game.current_player.summon("EX1_608")
	for i in range(26):
		game.current_player.give("CFM_602").play()
		assert game.current_player.jade_golem == 4 + i
		jade_i = game.current_player.field[-1]
		assert jade_i.health == jade_i.atk == 3 + i
		jade_i.destroy()
	# assert len(game.current_player.deck) == 60


def test_jade_lighting():
	game = prepare_game()
	assert game.current_player.jade_golem == 1
	lighting = game.current_player.give("CFM_707")
	lighting.play(target=game.current_player.hero)
	assert game.current_player.field[0].id == "CFM_712_t01"
	assert game.current_player.jade_golem == 2
	assert game.current_player.hero.health == 26


def test_jade_shuriken():
	game = prepare_game()
	assert game.current_player.jade_golem == 1
	shuriken1 = game.current_player.give("CFM_690")
	shuriken2 = game.current_player.give("CFM_690")
	shuriken3 = game.current_player.give("CFM_690")
	wisp = game.current_player.summon(WISP)
	hero2 = game.current_player.opponent.hero
	with pytest.raises(InvalidAction):
		shuriken1.play()
	shuriken1.play(target=hero2)
	assert hero2.health == 28
	assert game.current_player.jade_golem == 1
	assert len(game.current_player.field) == 1

	shuriken2.play(target=wisp)
	assert wisp.dead
	assert game.current_player.jade_golem == 2
	assert len(game.current_player.field) == 1

	game.current_player.summon("EX1_012")
	shuriken3.play(target=hero2)
	assert hero2.health == 25
	assert game.current_player.jade_golem == 3
	assert len(game.current_player.field) == 3

	blade = game.current_player.give("EX1_133")
	blade.play(target=hero2)
	assert hero2.health == 23
	assert game.current_player.jade_golem == 3


def test_jade_spirit():
	game = prepare_game()
	assert game.current_player.jade_golem == 1
	game.current_player.give("CFM_715").play()
	assert game.current_player.field[1].id == "CFM_712_t01"
	assert game.current_player.jade_golem == 2

	game.current_player.summon("LOE_077")
	game.current_player.give("CFM_715").play()
	assert game.current_player.jade_golem == 4
	jade2 = game.current_player.field[5]
	assert jade2.id == "CFM_712_t02"
	assert jade2.health == jade2.atk == 2
	# the extra battlecry comes next to its generator
	jade3 = game.current_player.field[4]
	assert jade3.id == "CFM_712_t03"
	assert jade3.health == jade3.atk == 3


def test_jade_swarmer():
	game = prepare_game()
	assert game.current_player.jade_golem == 1
	swarmer = game.current_player.give("CFM_691")
	swarmer.play()
	assert game.current_player.jade_golem == 1
	swarmer.destroy()
	assert game.current_player.jade_golem == 2
	assert game.current_player.field[0].id == "CFM_712_t01"


def test_weasel_tunneler():
	game = prepare_game()
	weasel = game.player1.give("CFM_095").play()
	assert weasel.zone == Zone.PLAY
	assert weasel.controller == game.player1
	game.player1.give("CS2_008").play(target=weasel)
	assert weasel.zone == Zone.DECK
	assert weasel.controller == game.player2


def test_finja():
	game = prepare_empty_game()
	finja = game.player1.give("CFM_344").play()
	game.end_turn()
	wisp = game.player2.give(WISP).play()
	game.end_turn()
	murloc1 = game.player1.give(MURLOC)
	murloc1.shuffle_into_deck()
	murloc2 = game.player1.give(MURLOC)
	murloc2.shuffle_into_deck()
	murloc3 = game.player1.give(MURLOC)
	murloc3.shuffle_into_deck()
	finja.attack(target=wisp)
	assert game.player1.field[0] == finja
	assert len(game.player1.field) == 3


def test_doppelgangster():
	game = prepare_game()
	doppel = game.player1.give("CFM_668")
	assert doppel.atk == 2
	game.player1.give("CFM_305").play()
	assert doppel.atk == 3
	doppel.play()
	assert len(game.player1.field) == 3
	assert game.player1.field[0].id == "CFM_668"
	assert game.player1.field[1].id == "CFM_668"
	assert game.player1.field[2].id == "CFM_668"


def test_seadevil_stinger():
	game = prepare_game()
	sea = game.player1.give("CFM_699")
	assert game.player1.murlocs_cost_health is False
	sea.play()
	assert game.player1.murlocs_cost_health is True
	assert game.player1.mana == 6
	assert game.player1.hero.health == 30
	murloc = game.player1.give("EX1_507")
	murloc.play()
	assert game.player1.murlocs_cost_health is False
	assert game.player1.mana == 6
	assert game.player1.hero.health == (30 - murloc.cost)


def test_kazakus():
	game = prepare_empty_game()
	assert len(game.player1.hand) == 0
	kazakus = game.player1.give("CFM_621")
	kazakus.play()
	chooses = []
	for _ in range(3):
		cards = game.player1.choice.cards
		chooses.append(cards[0])
		game.player1.choice.choose(cards[0])
	card = game.player1.hand[0]
	assert card.cost == 1
	assert (
		card.description == f"{chooses[1].description}\n{chooses[2].description}" or
		card.description == f"{chooses[2].description}\n{chooses[1].description}"
	)


def test_i_know_a_guy():
	game = prepare_game()
	guy = game.player1.give("CFM_940")
	guy.play()
	for card in game.player1.choice.cards:
		assert card.type == CardType.MINION
		assert card.taunt


def test_kabal_crystal_runner():
	game = prepare_game()
	runner = game.player1.give("CFM_760")
	runner_cost = runner.cost
	game.player1.give("EX1_295").play()
	assert runner.cost == runner_cost - 2
	runner2 = game.player1.give("CFM_760")
	assert runner2.cost == runner_cost - 2


def test_madam_goya():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	murloc = game.player1.give(MURLOC)
	murloc.shuffle_into_deck()
	assert wisp.zone == Zone.PLAY
	assert murloc.zone == Zone.DECK
	game.player1.give("CFM_672").play(target=wisp)
	assert wisp.zone == Zone.DECK
	assert murloc.zone == Zone.PLAY


def test_wrathion():
	game = prepare_empty_game()
	game.player1.give(WISP).put_on_top()
	for _ in range(4):
		game.player1.give("NEW1_023").put_on_top()
	assert len(game.player1.hand) == 0
	game.player1.give("CFM_806").play()
	assert len(game.player1.hand) == 5


def test_wrathion_empty():
	game = prepare_empty_game()
	game.player1.cant_fatigue = False
	game.player1.give("NEW1_023").put_on_top()
	game.player1.give("CFM_806").play()
	assert game.player1.hero.health == 30 - 1
