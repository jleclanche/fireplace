from utils import *


# Use the old Warsong Commander as it was nerfed
# implemented in fireplace.cards.custom
WARSONG_COMMANDER = "FIREPLACE_EX1_084"


def test_old_warsong_commander():
	# test 1 - Any minion, then Warsong
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert not wisp.charge
	game.player1.give(WARSONG_COMMANDER).play()
	assert not wisp.charge

	# test 15 - Warsong, Harvest Golem, then kill Harvest Golem to summon Damaged Golem
	golem = game.player1.give("EX1_556")
	golem.play()
	assert golem.buffs
	assert golem.charge
	for i in range(3):
		game.player1.give(MOONFIRE).play(target=golem)
	assert golem.dead
	damaged = game.player1.field.filter(id="skele21")[0]
	assert damaged.charge


def test_old_warsong_commander_buffed():
	# test 4 - Warsong, Fiery War Axe, then Bloodsail Raider
	game = prepare_game()
	game.player1.give(WARSONG_COMMANDER).play()
	game.player1.give("CS2_106").play()
	assert game.player1.hero.atk == 3
	raider = game.player1.give("NEW1_018")
	raider.play()
	assert raider.atk == 2 + 3
	assert not raider.charge
	game.end_turn(); game.end_turn()

	# test 5 - Warsong, Argent Squire, then Blood Knight
	squire = game.player1.give("EX1_008")
	squire.play()
	assert squire.charge
	assert squire.divine_shield
	bloodknight = game.player1.give("EX1_590")
	bloodknight.play()
	assert not squire.divine_shield
	assert not bloodknight.charge


def test_old_warsong_commander_faceless_manipulator():
	# test 7 - Warsong, then Faceless Manipulator on 6/7 Boulderfist Ogre
	game = prepare_game()
	game.player1.give(WARSONG_COMMANDER).play()
	game.end_turn()

	boulderfist = game.player2.summon("CS2_200")
	goldshire = game.player1.summon(GOLDSHIRE_FOOTMAN)
	game.end_turn()

	assert boulderfist.atk == 6
	faceless = game.player1.give("EX1_564")
	faceless.play(target=boulderfist)
	copy = game.player1.field.filter(id="CS2_200")[0]
	assert copy == boulderfist
	assert not copy.charge

	# test 8 - Warsong, then Faceless Manipulator on 1/2 Goldshire Footman
	assert goldshire.atk == 1
	faceless = game.player1.give("EX1_564")
	faceless.play(target=goldshire)
	copy = game.player1.field.filter(id=goldshire.id)[0]
	assert copy == goldshire
	assert copy.charge


def test_old_warsong_commander_faceless_manipulator_buffed():
	# test 6 - Warsong, then Faceless Manipulator on 5/6 damaged Gurubashi Berseker
	game = prepare_game()
	game.player1.give(WARSONG_COMMANDER).play()
	game.end_turn()

	gurubashi = game.player2.give("EX1_399")
	gurubashi.play()
	game.player2.give(MOONFIRE).play(target=gurubashi)
	assert gurubashi.atk == 5
	assert gurubashi.health == 6
	game.end_turn()

	faceless = game.player1.give("EX1_564")
	faceless.play(target=gurubashi)
	copy = game.player1.field.filter(id="EX1_399")[0]
	assert copy == gurubashi
	assert not copy.charge


def test_old_warsong_commander_stormwind_champion():
	# test 9 - Warsong and Stormwind Champion on Play, then Raging Worgen
	game = prepare_game()
	game.player1.give(WARSONG_COMMANDER).play()
	game.player1.give("CS2_222").play()
	game.end_turn(); game.end_turn()

	worgen = game.player1.give("EX1_412")
	worgen.play()
	assert not worgen.charge


def test_old_warsong_commander_lightspawn():
	# test 11 - Warsong, then Lightspawn
	game = prepare_game()
	game.player1.give(WARSONG_COMMANDER).play()
	lightspawn = game.player1.give("EX1_335")
	lightspawn.play()
	assert not lightspawn.charge


def test_old_warsong_commander_bounce():
	# test 12 - Warsong, then play Youthful Brewmaster targeting the Warsong
	game = prepare_game()
	warsong = game.player1.give(WARSONG_COMMANDER)
	warsong.play()
	brewmaster = game.player1.give("EX1_049")
	brewmaster.play(target=warsong)
	assert game.player1.field[0].id == "EX1_049"
	assert not game.player1.field[0].charge


def test_old_warsong_commander_spell_summon():
	# test 13 - Warsong, then play Hex targeting the Warsong
	game = prepare_game()
	warsong = game.player1.give(WARSONG_COMMANDER)
	warsong.play()
	hex = game.player1.give("EX1_246")
	hex.play(target=warsong)
	assert game.player1.field[0].id == "hexfrog"
	assert not game.player1.field[0].charge


def test_old_warsong_commander_mind_control_tech():
	# test 14 - Enemy Warsong and 3 other minions, the Mind Control Tech stealing Warsong
	game = prepare_game()
	for i in range(4):
		game.player1.summon(WARSONG_COMMANDER)
	assert len(game.player1.field) == 4
	assert len(game.player2.field) == 0
	game.end_turn()

	mct = game.player2.give("EX1_085")
	mct.play()
	assert len(game.player1.field) == 3
	assert len(game.player2.field) == 2
	assert mct.charge
