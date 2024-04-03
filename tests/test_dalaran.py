from utils import *


def test_lucentbark():
	game = prepare_game()
	lucentbark = game.player1.give("DAL_357").play()
	lucentbark.destroy()
	spirit = game.player1.field[0]
	assert spirit.id == "DAL_357t"
	game.player1.hero.set_current_health(25)
	game.player1.give("AT_055").play(target=game.player1.hero)
	new_lucentbark = game.player1.field[0]
	assert new_lucentbark.id == "DAL_357"


def test_keeper_stalladris():
	game = prepare_empty_game()
	game.player1.give("DAL_732").play()
	wild = game.player1.give("EX1_160")
	wild.play(choose="EX1_160a")
	assert game.player1.hand[0].id == "EX1_160a"
	assert game.player1.hand[1].id == "EX1_160b"


def test_lifeweaver():
	game = prepare_empty_game()
	game.player1.give("DAL_355").play()
	game.player1.hero.set_current_health(25)
	game.player1.give("AT_055").play(target=game.player1.hero)
	assert len(game.player1.hand) == 1
	game.end_turn()
	game.player2.hero.set_current_health(25)
	game.player2.give("AT_055").play(target=game.player2.hero)
	assert len(game.player1.hand) == 1


def test_nine_lives():
	game = prepare_game()
	nine_lives = game.player1.give("DAL_377")
	assert not nine_lives.is_playable()

	gnome = game.player1.give("EX1_029")
	gnome.destroy()

	nine_lives.play()
	assert game.player1.choice
	cards = game.player1.choice.cards
	assert len(cards) == 1
	assert cards[0].id == gnome.id

	count = len(game.player1.hand)
	health = game.player2.hero.health
	game.player1.choice.choose(cards[0])
	assert len(game.player1.hand) == count + 1
	assert game.player2.hero.health == health - 2


def test_khadgar():
	game = prepare_game()
	game.player1.give("DAL_575").play()
	game.player1.give("CFM_315").play()
	assert len(game.player1.field) == 4
	game.end_turn()
	game.player2.give("DAL_575").play()
	game.player2.give("DAL_575").play()
	game.player2.give("CFM_315").play()
	assert len(game.player2.field) == 6


def test_kalecgos():
	game = prepare_game()
	fireball = game.player1.give(FIREBALL)
	assert fireball.cost == 4
	game.player1.give("DAL_609").play()
	game.player1.choice.choose(game.player1.choice.cards[0])
	assert fireball.cost == 0
	game.player1.give(THE_COIN).play()
	assert fireball.cost == 4


def test_unseen_saboteur():
	game = prepare_empty_game()
	game.player2.discard_hand()
	blast = game.player2.give("DS1_233")
	game.player1.give("DAL_538").play()
	assert game.player1.hero.health == 25
	assert blast.zone == Zone.GRAVEYARD


def test_barista_lynchen():
	game = prepare_empty_game()
	for _ in range(3):
		game.player1.give("EX1_015")
	game.player1.give("DAL_546").play()
	assert game.player1.hand == ["EX1_015"] * 6


def test_archivist_elysiana():
	game = prepare_game()
	game.player1.give("DAL_736").play()
	cards = []
	for _ in range(5):
		choice = game.player1.choice
		cards.append(choice.cards[0].id)
		choice.choose(choice.cards[0])
	assert len(game.player1.deck) == 10
	assert sorted([card.id for card in game.player1.deck]) == sorted(cards * 2)


def test_jepetto_joybuzz():
	game = prepare_empty_game()
	for _ in range(2):
		game.player1.give("EX1_543").shuffle_into_deck()
	game.player1.give("DAL_752").play()
	assert game.player1.hand == ["EX1_543"] * 2
	for _ in range(2):
		card = game.player1.hand[0]
		assert card.cost == 1
		assert card.atk == 1
		assert card.health == 1
		card.play()
		assert card.cost == 9
		assert card.atk == 1
		assert card.health == 1


def test_commander_rhyssa():
	game = prepare_game(CardClass.WARLOCK, CardClass.WARLOCK)
	game.player1.give("LOE_021").play()
	game.player1.give("DAL_573").play()
	game.end_turn()

	assert game.player2.hero.health == 30
	game.player2.hero.power.use()
	assert game.player2.hero.health == 30 - 5 - 5 - 2


def test_madame_lazul():
	game = prepare_game()
	game.player2.discard_hand()
	game.player2.give(WISP)
	game.player2.give(MURLOC)
	game.player2.give(CHICKEN)
	game.player1.give("DAL_729").play()
	choice = game.player1.choice
	assert WISP in choice.cards
	assert MURLOC in choice.cards
	assert CHICKEN in choice.cards
	choice.choose(choice.cards[0])
	assert not game.player1.choice


def test_lazuls_scheme():
	game = prepare_game()
	# Turn 1
	scheme = game.player1.give("DAL_011")
	game.end_turn()
	dragon = game.player2.give("NEW1_030").play()
	assert dragon.atk == 12
	game.end_turn()
	# Turn 2
	game.skip_turn()
	# Turn 3
	game.skip_turn()
	# Turn 4
	scheme.play(target=dragon)
	assert dragon.atk == 12 - 4
	game.end_turn()
	assert dragon.atk == 12 - 4
	game.end_turn()
	assert dragon.atk == 12


def test_forbidden_words():
	game = prepare_game()
	words = game.player1.give("DAL_723")
	assert not words.is_playable()
	game.end_turn()

	minion_12 = game.player2.summon("CFM_712_t12")
	minion_10 = game.player2.summon("CFM_712_t10")
	minion_8 = game.player2.summon("CFM_712_t08")
	minion_6 = game.player2.summon("CFM_712_t06")
	minion_4 = game.player2.summon("CFM_712_t04")
	minion_2 = game.player2.summon("CFM_712_t02")

	game.end_turn()
	assert words.is_playable()
	assert minion_12 not in words.play_targets
	assert words.play_targets == [minion_10, minion_8, minion_6, minion_4, minion_2]
	game.player1.pay_cost(game.player1, 4)
	assert words.play_targets == [minion_6, minion_4, minion_2]
	words.play(target=minion_4)
	assert minion_4.dead
	assert game.player1.mana == 0


def test_tak_nozwhisker():
	game = prepare_empty_game()
	game.player1.give("DAL_719").play()
	game.player1.give("CFM_602").play(choose="CFM_602b")
	assert game.player1.hand == ["CFM_602"] * 3
	assert game.player1.deck == ["CFM_602"] * 3


def test_swampqueen_hagatha():
	game = prepare_empty_game()
	game.player1.give("DAL_431").play()
	choice = game.player1.choice
	assert choice
	card1 = choice.cards[0]
	choice.choose(card1)
	choice = game.player1.choice
	assert choice
	card2 = choice.cards[0]
	choice.choose(card2)

	horror = game.player1.hand[0]
	assert horror.id == "DAL_431t"
	assert horror.data.scripts.play == card1.data.scripts.play + card2.data.scripts.play
	assert horror.overload == card1.overload + card2.overload


def test_darkest_hour():
	game = prepare_empty_game()
	for _ in range(4):
		game.player1.give(WISP).play()
		game.player1.give(CHICKEN).shuffle_into_deck()
	game.player1.give("DAL_173").play()
	assert game.player1.field == [CHICKEN] * 4
	assert len(game.player1.deck) == 0


def test_plot_twist():
	game = prepare_game()
	count = len(game.player1.hand)
	game.player1.give("DAL_602").play()
	assert len(game.player1.hand) == count


def test_dimensional_ripper():
	game = prepare_empty_game()
	game.player1.give(WISP).shuffle_into_deck()
	game.player1.give(CHICKEN).shuffle_into_deck()
	game.player1.give("DAL_059").play()
	assert (game.player1.field == [WISP] * 2) ^ (game.player1.field == [CHICKEN] * 2)


def test_zayle():
	player1 = Player("Player1", ["DAL_800"], "DAL_800h")
	player2 = Player("Player1", ["DAL_800"], "DAL_800h")
	game = BaseTestGame(players=(player1, player2))
	game.start()
	assert len(game.player1.starting_deck) == 30
	assert len(game.player2.starting_deck) == 30


def test_twin_spell():
	game = prepare_game()
	twin_spell = game.player1.give("DAL_141")
	game.player1.give("EX1_095").play()
	while len(game.player1.hand) < game.player1.max_hand_size:
		game.player1.give(WISP)
	twin_spell.play()
	assert game.player1.hand[-1].id == "DAL_141ts"


def test_duel():
	game1 = prepare_empty_game()
	game1.player1.give("DAL_731").play()
	assert len(game1.player1.field) == 0
	assert len(game1.player1.field) == 0

	game2 = prepare_empty_game()
	game2.player1.give(MECH).shuffle_into_deck()
	game2.player2.give(MECH).shuffle_into_deck()
	game2.player1.give("DAL_731").play()
	assert game2.player1.field == [MECH]
	assert game2.player1.field == [MECH]
	assert len(game2.player1.deck) == 0
	assert len(game2.player1.deck) == 0
	assert game2.player1.field[0].damage == 1
	assert game2.player2.field[0].damage == 1

	game3 = prepare_empty_game()
	game3.player1.give(MECH).shuffle_into_deck()
	game3.player2.give(MECH).shuffle_into_deck()
	for _ in range(7):
		game3.player1.summon(WISP)
		game3.player2.summon(WISP)
	duel = game3.player1.give("DAL_731")
	assert not duel.is_playable()
