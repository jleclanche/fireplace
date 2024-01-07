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


def test_lynessa_sunsorrow():
	game = prepare_game()
	sunsorrow = game.player1.give("LOOT_216")
	atk = sunsorrow.atk
	for _ in range(3):
		wisp = game.player1.give(WISP).play()
		game.player1.give("CS2_087").play(target=wisp)
	sunsorrow.play()
	assert sunsorrow.atk == atk + 9


def test_sonya_shadowdancer():
	game = prepare_empty_game()
	game.player1.give("LOOT_165").play()
	wisp = game.player1.give(WISP).play()
	game.player1.give(MOONFIRE).play(target=wisp)
	assert game.player1.hand[0].id == WISP
	assert game.player1.hand[0].buffs[0].id == "LOOT_165e"


def test_windshear_stormcaller():
	game = prepare_game()
	for totem in BASIC_TOTEMS:
		game.player1.give(totem).play()
	game.player1.give("LOOT_518").play()
	assert game.player1.field[5].id == "NEW1_010"


def test_crushing_walls():
	game = prepare_game()
	game.player1.give(WISP).play()
	game.end_turn()
	game.player2.give("LOOT_522").play()
	assert len(game.player1.field) == 0
	game.end_turn()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.end_turn()
	game.player2.give("LOOT_522").play()
	assert len(game.player1.field) == 0
	game.end_turn()
	game.player1.give(WISP).play()
	game.player1.give(CHICKEN).play()
	game.player1.give(WISP).play()
	game.end_turn()
	game.player2.give("LOOT_522").play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == CHICKEN


def test_dragon_soul():
	game = prepare_game()
	game.player1.give("LOOT_209").play()
	for _ in range(3):
		game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert len(game.player1.field) == 1
	game.skip_turn()
	for _ in range(3):
		game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert len(game.player1.field) == 2


def test_reckless_flurry():
	game = prepare_game()
	game.player1.give("EX1_606").play()
	assert game.player1.hero.armor == 5
	game.player1.give(WISP).play()
	game.player1.give("LOOT_364").play()
	assert game.player1.hero.armor == 0
	assert len(game.player1.field) == 0


def test_the_runespear():
	game = prepare_game()
	game.player1.give("LOOT_506").play()
	game.player1.hero.attack(game.player2.hero)
	assert game.player1.choice
	game.player1.choice.choose(game.player1.choice.cards[0])


def test_dragons_fury():
	game = prepare_empty_game()
	game.player1.give(FIREBALL).shuffle_into_deck()
	wisp = game.player1.give(WISP).play()
	mech = game.player1.give(MECH).play()
	game.player1.give("LOOT_172").play()
	assert wisp.dead
	assert not mech.dead
	assert mech.health == 1
