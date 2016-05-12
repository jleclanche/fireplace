from utils import *


def test_addled_grizzly():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	grizzly = game.player1.give("OG_313")
	game.player1.give("OG_313").play()
	grizzly.play()
	assert grizzly.atk == grizzly.health == 3
	wisp.play()
	assert wisp.atk == wisp.health == 3


def test_chogall():
	game = prepare_game()
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	fireball = game.player1.give("CS2_029")
	fireball2 = game.player1.give("CS2_029")
	assert not game.player1.spells_cost_health
	chogall = game.player1.give("OG_121")
	chogall.play()
	assert game.player1.mana == 10 - 7
	assert game.player1.hero.health == 30
	assert game.player1.spells_cost_health
	assert not game.player2.spells_cost_health
	footman.play()
	assert game.player1.mana == 10 - 7 - 1
	assert game.player1.hero.health == 30
	assert fireball.cost == 4
	assert fireball.is_playable()
	fireball.play(target=game.player2.hero)
	assert not game.player1.spells_cost_health
	assert game.player1.mana == 10 - 7 - 1
	assert game.player1.hero.health == 30 - 4
	assert not fireball2.is_playable()


def test_chogall_free_spell():
	game = prepare_game()
	moonfire = game.player1.give(MOONFIRE)
	fireball = game.player1.give("CS2_029")
	chogall = game.player1.give("OG_121")
	chogall.play()
	moonfire.play(target=game.player2.hero)
	assert game.player1.mana == 10 - 7
	assert game.player1.hero.health == 30


def test_chogall_cannot_pay_health():
	game = prepare_game()
	fireball = game.player1.give("CS2_029")
	chogall = game.player1.give("OG_121")
	chogall.play()
	game.player1.hero.set_current_health(5)
	assert fireball.is_playable()
	game.player1.hero.set_current_health(4)
	assert not fireball.is_playable()


def test_feral_rage():
	game = prepare_game()
	game.player1.give("OG_047").play(choose="OG_047a")
	assert game.player1.hero.atk == 4
	assert game.player1.hero.armor == 0
	game.player1.give("OG_047").play(choose="OG_047b")
	assert game.player1.hero.atk == 4
	assert game.player1.hero.armor == 8
	game.end_turn()

	assert game.player1.hero.atk == 0
	assert game.player1.hero.armor == 8


def test_forlorn_stalker():
	game = prepare_game()
	leper = game.player1.give("EX1_029")
	leper2 = game.player1.give("EX1_029")
	leper2.play()
	deathsbite = game.player1.give("FP1_021")
	wisp = game.player1.give(WISP)
	stalker = game.player1.give("OG_292")
	stalker.play()
	assert leper.buffs
	assert leper.atk == leper.health == 1 + 1
	assert not leper2.buffs
	assert leper2.atk == leper2.health == 1
	assert not deathsbite.buffs
	assert deathsbite.atk == 4
	assert deathsbite.durability == 2
	assert not wisp.buffs
	assert wisp.atk == wisp.health == 1


def test_hallazeal_the_ascended():
	game = prepare_game()
	hallazeal = game.player1.give("OG_209")
	hallazeal.play()
	game.player1.hero.set_current_health(1)
	game.end_turn(); game.end_turn()

	moonfire = game.player1.give(MOONFIRE)
	moonfire.play(target=game.player2.hero)
	assert game.player1.hero.health == 1 + 1
	assert game.player2.hero.health == 30 - 1
	game.player1.give(KOBOLD_GEOMANCER).play()
	fireball = game.player1.give("CS2_029")
	fireball.play(target=hallazeal)
	assert game.player1.hero.health == 1 + 1 + 7
	assert hallazeal.dead


def test_mark_of_yshaarj():
	game = prepare_game()
	game.player1.discard_hand()
	mark = game.player1.give("OG_048") 
	mark2 = game.player1.give("OG_048") 
	wisp = game.player1.give(WISP)
	chicken = game.player1.give("EX1_009")
	wisp.play()
	chicken.play()
	assert len(game.player1.hand) == 2
	mark.play(target=wisp)
	assert len(game.player1.hand) == 1
	mark2.play(target=chicken)
	assert len(game.player1.hand) == 1


def test_mire_keeper():
	game = prepare_game()
	game.player1.give("OG_202").play(choose="OG_202a")
	assert len(game.player1.field) == 2
	game.end_turn(); game.end_turn()

	game.player1.max_mana = 9
	game.player1.give("OG_202").play(choose="OG_202b")
	assert game.player1.max_mana == 10


def test_silithid_swarmer():
	game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
	silithid = game.player1.give("OG_034")
	silithid.play()
	assert not silithid.can_attack()
	game.end_turn(); game.end_turn()

	assert silithid.cant_attack
	assert not silithid.can_attack()
	game.player1.hero.power.use()
	game.player1.hero.attack(target=game.player2.hero)
	assert not silithid.cant_attack
	assert silithid.can_attack()
	silithid.attack(target=game.player2.hero)
	assert game.player2.hero.health == 30 - 1 - 3
	assert not silithid.cant_attack
	assert not silithid.can_attack()


def test_thistle_tea():
	game = prepare_game()
	game.player1.discard_hand()
	tea = game.player1.give("OG_073")
	tea.play()
	assert len(game.player1.hand) == 3
	assert game.player1.hand[0] == game.player1.hand[1] == game.player1.hand[2]
