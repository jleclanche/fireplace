from utils import *


def test_griftah():
	game = prepare_empty_game()
	game.player1.give("TRL_096").play()
	card1 = game.player1.choice.cards[0]
	game.player1.choice.choose(card1)
	card2 = game.player1.choice.cards[0]
	game.player1.choice.choose(card2)
	assert (
		game.player1.hand[0].id == card1.id and
		game.player2.hand[1].id == card2.id
	) ^ (
		game.player1.hand[0].id == card2.id and
		game.player2.hand[1].id == card1.id
	)
	assert not game.player1.choice


def test_hakkar():
	game = prepare_empty_game()
	hakkar = game.player1.give("TRL_541").play()
	hakkar.destroy()
	assert len(game.player1.deck) == 1
	assert game.player1.deck[0].id == "TRL_541t"
	assert len(game.player2.deck) == 1
	assert game.player2.deck[0].id == "TRL_541t"
	game.end_turn()
	assert len(game.player2.deck) == 2
	assert game.player2.deck[0].id == "TRL_541t"
	assert game.player2.deck[1].id == "TRL_541t"
	assert game.player2.hero.health == 27
	game.skip_turn()
	assert game.player2.hero.health == 21
	assert len(game.player2.deck) == 4


def test_overkill():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	game.end_turn()
	direhorn = game.player2.give("TRL_232").play()
	game.skip_turn()
	direhorn.attack(wisp)
	assert len(game.player2.field) == 2


def test_overkill_spell():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	arrow = game.player1.give("TRL_347")
	arrow.play(target=wisp)
	assert len(game.player1.field) == 1


def test_snapjaw_shellfighter():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	shellfighter = game.player1.give("TRL_535").play()
	game.player1.give(MOONFIRE).play(target=wisp)
	assert wisp.damage == 0
	assert shellfighter.damage == 1


def test_treespeaker():
	game = prepare_game()
	game.player1.give("EX1_571").play()
	game.player1.give(WISP).play()
	game.player1.give("TRL_341").play()
	assert len(game.player1.field) == 5
	for i in range(3):
		assert game.player1.field[i].id == "TRL_341t"
	assert game.player1.field[3].id == WISP
	assert game.player1.field[4].id == "TRL_341"


def test_mass_hysteria():
	game = prepare_game()
	for _ in range(7):
		game.player1.give(WISP).play()
	game.player1.give("TRL_258").play()
	assert len(game.player1.field) == 1


def test_high_priest_thekal():
	game = prepare_game()
	game.player1.give("TRL_308").play()
	assert game.player1.hero.health == 1
	assert game.player1.hero.armor == 29


def test_spectral_cutlass():
	game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
	weapon = game.player1.give("GIL_672").play()
	durability = weapon.durability
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert weapon.durability == durability + 1


def test_stolen_steel():
	game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
	game.player1.give("TRL_156").play()
	assert game.player1.choice
	cards = game.player1.choice.cards
	for card in cards:
		assert card.card_class != CardClass.ROGUE
	game.player1.choice.choose(cards[0])


def test_masters_call():
	game = prepare_empty_game()
	beasts = ["NEW1_032", "NEW1_033", "NEW1_034"]
	for beast in beasts:
		game.player1.give(beast).shuffle_into_deck()
	game.player1.give("TRL_339").play()
	assert not game.player1.choice
	assert len(game.player1.hand) == 3

	game = prepare_empty_game()
	minions = [WISP, "NEW1_033", "NEW1_034"]
	for minion in minions:
		game.player1.give(minion).shuffle_into_deck()
	game.player1.give("TRL_339").play()
	assert game.player1.choice
	game.player1.choice.choose(game.player1.choice.cards[0])
	assert len(game.player1.hand) == 1


def test_pyromaniac():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	game.player1.give("TRL_315").play()
	wisp = game.player1.give(WISP).play()
	hand = len(game.player1.hand)
	game.player1.hero.power.use(target=wisp)
	assert len(game.player1.hand) == hand + 1


def test_janalai_the_dragonhawk():
	game = prepare_game(CardClass.HUNTER, CardClass.HUNTER)
	janalai = game.player1.give("TRL_316")
	assert not janalai.powered_up
	for _ in range(4):
		game.player1.hero.power.use()
		game.skip_turn()
	assert janalai.powered_up
	janalai.play()
	assert len(game.player1.field) == 2


def test_spirit_of_the_dragonhawk():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	game.player1.give("TRL_319").play()
	game.end_turn()
	for _ in range(3):
		game.player2.give(WISP).play()
	game.end_turn()
	assert len(game.player2.field) == 3
	game.player1.hero.power.use(target=game.player2.field[1])
	assert len(game.player2.field) == 0


def test_daring_fire_eater():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	game.player1.give("TRL_319").play()
	game.end_turn()
	for _ in range(3):
		game.player2.give(MECH).play()
	game.end_turn()
	game.player1.give("TRL_390").play()
	game.player1.hero.power.use(target=game.player2.field[1])
	for i in range(3):
		assert game.player2.field[i].damage == 3
	game.skip_turn()
	game.player1.hero.power.use(target=game.player2.field[1])
	for i in range(3):
		assert game.player2.field[i].damage == 4
