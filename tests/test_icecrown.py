import pytest
from utils import *

from fireplace.exceptions import GameOver


def test_happy_ghoul():
	game = prepare_game()
	ghoul = game.player1.give("ICC_700")
	assert ghoul.cost == 3
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	game.player1.give("AT_055").play(target=game.player1.hero)
	assert ghoul.cost == 0
	game.end_turn()
	assert ghoul.cost == 3


def test_mindbreaker():
	game = prepare_game()
	breaker = game.player1.give("ICC_902").play()
	assert game.player1.hero.power.exhausted
	assert game.player2.hero.power.exhausted
	breaker.destroy()
	assert not game.player1.hero.power.exhausted
	assert not game.player2.hero.power.exhausted


def test_drakkari_enchanter():
	game = prepare_game()
	game.player1.give("EX1_298").play()
	game.player1.give(THE_COIN).play()
	game.player1.give("ICC_901").play()
	game.end_turn()
	assert game.player2.hero.health == 30 - 8 - 8


def test_fatespinner():
	game = prepare_game()
	game.player1.give("ICC_047").play(choose="ICC_047a")
	game.player1.give("ICC_047").play(choose="ICC_047b")
	assert game.player1.field[0].deathrattles
	assert game.player1.field[1].deathrattles


def test_spreading_plague():
	game = prepare_game()
	for _ in range(4):
		game.player1.give(WISP).play()
	game.end_turn()
	game.player2.give("ICC_054").play()
	assert len(game.player2.field) == 4


def test_malfurion_the_pestilent():
	game = prepare_game()
	game.player1.give("ICC_832").play(choose="ICC_832a")
	game.player1.hero.power.use(choose="ICC_832pa")
	assert game.player1.hero.armor == 5 + 3


def test_deathstalker_rexxar():
	game = prepare_empty_game()
	game.player1.give("ICC_828").play()
	game.player1.hero.power.use()
	assert game.player1.choice
	choice = game.player1.choice
	card1 = choice.cards[0]
	choice.choose(card1)
	choice = game.player1.choice
	card2 = choice.cards[0]
	choice.choose(card2)
	assert not game.player1.choice
	game.player1.hand[0].atk = card1.atk + card2.atk
	game.player1.hand[0].atk = card1.health + card2.health
	game.player1.hand[0].atk = card1.cost + card2.cost


def test_bolvar_fireblood():
	game = prepare_game()
	fireblood = game.player1.give("ICC_858").play()
	atk = fireblood.atk
	game.player1.give(MOONFIRE).play(target=fireblood)
	assert fireblood.atk == atk + 2


def test_uther_of_the_ebon_blade():
	game = prepare_game()
	game.player1.give("ICC_829").play()
	game.end_turn()
	game.end_turn()
	for _ in range(3):
		game.player1.hero.power.use()
		game.end_turn()
		game.end_turn()
	with pytest.raises(GameOver):
		game.player1.hero.power.use()


def test_embrace_darkness():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	game.end_turn()
	game.player2.give("ICC_849").play(target=wisp)
	game.end_turn()
	game.end_turn()
	assert len(game.player1.field) == 0
	assert len(game.player2.field) == 1


def test_moorabi():
	game = prepare_empty_game()
	game.player1.give("ICC_289").play()
	wisp = game.player1.give(WISP).play()
	game.player1.give("CS2_031").play(target=wisp)
	assert game.player1.hand[0].id == WISP


def test_frost_lich_jaina():
	game = prepare_game()
	firefly = game.player1.give("UNG_809").play()
	assert not firefly.lifesteal
	game.player1.give("ICC_833").play()
	assert firefly.lifesteal
	game.end_turn()
	wisp = game.player2.give(WISP).play()
	game.end_turn()
	assert len(game.player1.field) == 2
	game.player1.hero.power.use(target=wisp)
	assert len(game.player1.field) == 3


def test_shadowreaper_anduin():
	game = prepare_game()
	game.player1.give("ICC_830").play()
	game.end_turn()
	game.end_turn()
	for _ in range(5):
		wisp = game.player1.give(WISP).play()
		game.player1.hero.power.use(target=wisp)
		assert game.player1.hero.power.exhausted


def test_valeera_the_hollow():
	game = prepare_empty_game()
	game.player1.give("ICC_827").play()
	assert game.player1.hero.stealthed
	game.end_turn()
	assert game.player1.hero.stealthed
	game.end_turn()
	assert not game.player1.hero.stealthed
	assert not game.player1.hero.power.is_usable()
	game.player1.give(WISP).play()
	assert game.player1.hand[0].id == WISP
	game.player1.give(CHICKEN).play()
	assert game.player1.hand[0].id == CHICKEN
	game.player1.hand[0].play()
	assert len(game.player1.hand) == 0
	game.skip_turn()
	assert len(game.player1.hand) == 1


def test_defile():
	game = prepare_empty_game()
	game.player1.give(WISP).play()  # 1/1
	game.player1.give(TARGET_DUMMY).play()  # 0/2
	game.player1.give("EX1_556").play()  # 2/3 deathrattle summon 2/1
	game.player1.give("CS2_033").play()  # 3/6
	game.player1.give("ICC_041").play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].health == 1


def test_defile_max_time():
	game = prepare_empty_game()
	grim1 = game.player1.give("BRM_019").play()
	game.player1.give(MOONFIRE).play(target=grim1)
	game.player1.give(WISP).play()
	game.player1.give("ICC_041").play()
	assert len(game.player1.field) > 0


def test_frostmourne():
	game = prepare_game()
	game.player1.give("ICC_314t1").play()
	game.end_turn()
	for _ in range(3):
		game.player2.give(WISP).play()
	game.end_turn()
	game.player1.hero.attack(game.player2.field[0])
	game.skip_turn()
	game.player1.hero.attack(game.player2.field[0])
	game.skip_turn()
	game.player1.hero.attack(game.player2.field[0])
	assert len(game.player1.field) == 3
	game.player1.field[0].id == WISP
	game.player1.field[1].id == WISP
	game.player1.field[2].id == WISP


def test_hero_armor():
	game = prepare_game(CardClass.WARRIOR, CardClass.WARRIOR)
	game.player1.hero.power.use()
	assert game.player1.hero.armor == 2
	game.player1.give("ICC_481").play()
	assert game.player1.hero.armor == 7


def test_death_grip():
	game = prepare_game()
	grip = game.player1.give("ICC_314t4")
	deck = len(game.player2.deck)
	hand = len(game.player1.hand)
	grip.play()
	assert len(game.player2.deck) == deck - 1
	assert len(game.player1.hand) == hand


def test_phantom_freebooter():
	game = prepare_game()
	weapon = game.player1.give("CS2_106").play()
	freebooter = game.player1.give("ICC_018")
	atk = freebooter.atk
	health = freebooter.health
	freebooter.play()
	assert freebooter.atk == atk + weapon.atk
	assert freebooter.health == health + weapon.durability
