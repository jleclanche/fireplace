from utils import *


def test_blackwing_corruptor():
	game = prepare_game()
	game.player1.discard_hand()
	blackwing1 = game.player1.give("BRM_034")
	assert not blackwing1.powered_up
	blackwing1.play()
	assert blackwing1.health == 4
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	assert len(game.player1.hand) == 0
	game.end_turn()

	game.player2.discard_hand()
	game.player2.give(WHELP)
	blackwing2 = game.player2.give("BRM_034")
	assert blackwing2.powered_up
	blackwing2.play(target=game.player1.hero)
	assert game.player1.hero.health == 27


def test_blackwing_technician():
	game = prepare_game()
	game.player1.discard_hand()
	blackwing1 = game.player1.give("BRM_033")
	assert not blackwing1.powered_up
	blackwing1.play()
	assert not blackwing1.buffs
	assert blackwing1.atk == 2
	assert blackwing1.health == 4

	blackwing2 = game.player1.give("BRM_033")
	assert not blackwing2.powered_up
	game.player1.give(WHELP)
	assert blackwing2.powered_up
	blackwing2.play()
	assert blackwing2.buffs
	assert blackwing2.atk == 3
	assert blackwing2.health == 5


def test_chromaggus():
	game = prepare_game()
	chromaggus = game.player1.give("BRM_031")
	chromaggus.play()
	game.end_turn(); game.end_turn()

	game.player1.discard_hand()
	arcint = game.player1.give("CS2_023")
	assert len(game.player1.hand) == 1
	arcint.play()
	assert len(game.player1.hand) == 4
	assert game.player1.hand[0] == game.player1.hand[1]
	assert game.player1.hand[2] == game.player1.hand[3]


def test_chromaggus_naturalize():
	game = prepare_game()
	chromaggus = game.player1.give("BRM_031")
	chromaggus.play()
	game.end_turn()
	game.player1.discard_hand()
	naturalize = game.player2.give("EX1_161")
	naturalize.play(target=chromaggus)
	assert len(game.player1.hand) == 4
	assert game.player1.hand[0] == game.player1.hand[1]
	assert game.player1.hand[2] == game.player1.hand[3]


def test_dragon_egg():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)
	egg = game.player1.give("BRM_022")
	egg.play()
	assert len(game.player1.field) == 1
	game.player1.give(MOONFIRE).play(target=egg)
	assert len(game.player1.field) == 2
	assert len(game.player1.field.filter(id="BRM_022t")) == 1
	assert egg.health == 1
	game.player1.hero.power.use(target=egg)
	assert egg.health == 2
	assert len(game.player1.field) == 2
	for i in range(2):
		game.player1.give(MOONFIRE).play(target=egg)
	assert egg.dead
	assert len(game.player1.field) == 3
	assert len(game.player1.field.filter(id="BRM_022t")) == 3


def test_dragonkin_sorcerer():
	game = prepare_game()
	dragonkin = game.player1.give("BRM_020")
	dragonkin.play()
	assert dragonkin.health == 5
	pwshield = game.player1.give("CS2_004")
	pwshield.play(target=dragonkin)
	assert dragonkin.health == 5 + 2 + 1
	assert dragonkin.max_health == 5 + 2 + 1
	game.player1.give(MOONFIRE).play(target=dragonkin)
	assert dragonkin.health == 5 + 2 + 1 + 1 - 1
	assert dragonkin.max_health == 5 + 2 + 1 + 1


def test_druid_of_the_flame():
	game = prepare_game()
	flame1 = game.player1.give("BRM_010")
	flame1.play(choose="BRM_010a")
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "BRM_010t"
	assert game.player1.field[0].atk == 5
	assert game.player1.field[0].health == 2

	flame2 = game.player1.give("BRM_010")
	flame2.play(choose="BRM_010b")
	assert len(game.player1.field) == 2
	assert game.player1.field[1].id == "BRM_010t2"
	assert game.player1.field[1].atk == 2
	assert game.player1.field[1].health == 5


def test_emperor_thaurissan():
	game = prepare_game()
	thaurissan = game.player1.give("BRM_028")
	fireball = game.player1.give("CS2_029")
	wisp = game.player1.give(WISP)
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	deathwing = game.player1.give("NEW1_030")
	thaurissan.play()
	assert fireball.cost == 4
	assert wisp.cost == 0
	assert footman.cost == 1
	assert deathwing.cost == 10
	game.end_turn()

	assert fireball.cost == 4 - 1
	assert wisp.cost == 0
	assert footman.cost == 1 - 1
	assert deathwing.cost == 10 - 1
	game.end_turn()

	assert fireball.cost == 4 - 1
	assert wisp.cost == 0
	assert footman.cost == 1 - 1
	assert deathwing.cost == 10 - 1
	game.end_turn()

	assert fireball.cost == 4 - 2
	assert wisp.cost == 0
	assert footman.cost == 0
	assert deathwing.cost == 10 - 2
	game.end_turn()

	thaurissan.destroy()
	game.end_turn()

	assert fireball.cost == 4 - 2
	assert wisp.cost == 0
	assert footman.cost == 0
	assert deathwing.cost == 10 - 2
	game.end_turn()

	assert fireball.cost == 4 - 2
	assert wisp.cost == 0
	assert footman.cost == 0
	assert deathwing.cost == 10 - 2


def test_emperor_thaurissan_molten_recombobulator():
	game = prepare_empty_game()
	molten = game.player1.give("EX1_620")
	thaurissan = game.player1.give("BRM_028")
	thaurissan.play()
	game.end_turn(); game.end_turn()

	assert molten.cost == 25 - 1
	thaurissan.destroy()
	ancestor = game.player1.give("GVG_029")
	ancestor.play()
	assert molten.cost == 25
	assert molten in game.player1.field
	game.end_turn(); game.end_turn()

	recomb = game.player1.give("GVG_108")
	recomb.play(target=molten)
	assert len(game.player1.field) == 2
	assert game.player1.field[0].cost == molten.cost


def test_fireguard_destroyer():
	game = prepare_game()
	fireguard = game.player1.give("BRM_012")
	fireguard.play()
	assert fireguard.atk in (4, 5, 6, 7)


def test_gang_up():
	game = prepare_empty_game()
	wisp = game.player1.summon(WISP)
	assert len(game.player1.deck) == 0
	assert len(game.player2.deck) == 0
	game.player1.give("BRM_007").play(target=wisp)
	assert len(game.player1.deck) == 3
	assert len(game.player2.deck) == 0
	game.end_turn()

	game.player2.give("BRM_007").play(target=wisp)
	assert len(game.player1.deck) == 3
	assert len(game.player2.deck) == 3
	assert len(game.player1.deck.filter(id=WISP)) == 3
	assert len(game.player2.deck.filter(id=WISP)) == 3


def test_imp_gang_boss():
	game = prepare_game()
	igb = game.player1.give("BRM_006")
	igb.play()
	game.player1.give(MOONFIRE).play(target=igb)
	assert len(game.player1.field) == 2
	assert game.player1.field[1].id == "BRM_006t"

	igb2 = game.player1.give("BRM_006")
	igb2.play()
	game.player1.give(MOONFIRE).play(target=igb2)
	assert len(game.player1.field) == 4


def test_lava_shock():
	game = prepare_game()
	game.player1.give("EX1_243").play()
	assert game.player1.overloaded == 2
	lava = game.player1.give("BRM_011")
	lava.play(target=game.player2.hero)
	assert game.player2.hero.health == 28
	assert game.player1.overloaded == 0
	game.end_turn(); game.end_turn()

	game.player1.give("EX1_243").play()
	game.end_turn(); game.end_turn()

	game.player1.give("EX1_243").play()
	assert game.player1.overloaded == 2
	assert game.player1.overload_locked == 2
	lava = game.player1.give("BRM_011")
	lava.play(target=game.player2.hero)
	assert game.player1.overloaded == 0
	assert game.player1.overload_locked == 0


def test_majordomo_executus():
	game = prepare_game(CardClass.WARRIOR, CardClass.WARRIOR)
	majordomo = game.player1.give("BRM_027")
	majordomo.play()
	game.end_turn(); game.end_turn()

	game.player1.hero.power.use()
	assert game.player1.hero.power.exhausted
	assert game.player1.hero.power.controller is game.player1
	assert game.player1.hero.armor == 2
	assert game.player1.hero.health == 30
	majordomo.destroy()
	assert game.player1.hero.armor == 0
	assert game.player1.hero.health == 8
	assert game.player1.hero.power.id == "BRM_027p"
	assert not game.player1.hero.power.exhausted
	assert game.player1.hero.power.controller is game.player1
	game.player1.hero.power.use()
	assert game.player1.hero.power.exhausted
	assert game.player2.hero.health == 22


def test_quick_shot():
	game = prepare_game()
	game.player1.discard_hand()
	quickshot1 = game.player1.give("BRM_013")
	wisp = game.player1.give("CS2_231")
	wisp.play()
	assert quickshot1.powered_up
	quickshot1.play(target=wisp)
	assert wisp.dead
	assert len(game.player1.hand) == 1
	quickshot2 = game.player1.give("BRM_013")
	assert len(game.player1.hand) == 2
	assert not quickshot2.powered_up
	quickshot2.play(target=game.player2.hero)
	assert game.player2.hero.health == 27
	assert len(game.player1.hand) == 1


def test_quick_shot_acolyte():
	game = prepare_game()
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	quickshot = game.player1.give("BRM_013")
	acolyte = game.player1.give("EX1_007")
	acolyte.play()
	assert len(game.player1.hand) == 1
	quickshot.play(target=acolyte)
	assert len(game.player1.hand) == 1
	assert acolyte.dead


def test_quick_shot_gallywix():
	game = prepare_game()
	gallywix = game.player1.give("GVG_028")
	gallywix.play()
	game.end_turn()

	game.player2.discard_hand()
	assert len(game.player2.hand) == 0
	quickshot = game.player2.give("BRM_013")
	assert len(game.player2.hand) == 1
	quickshot.play(target=game.player1.hero)
	assert len(game.player2.hand) == 1
	assert game.player2.hand[0].id == "GVG_028t"


def test_resurrect():
	# Shouldn't be playable if no minion died
	game = prepare_game()
	resurrect = game.player1.give("BRM_017")
	assert not resurrect.is_playable()
	game.player1.give(LIGHTS_JUSTICE).play()
	game.player1.weapon.destroy()
	assert not resurrect.is_playable()

	# Summons something
	wisp = game.player1.give(WISP)
	wisp.play()
	game.player1.give(MOONFIRE).play(target=wisp)
	assert len(game.player1.field) == 0
	resurrect.play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0] == wisp


def test_resurrect_wild_pyro():
	"""
	Test that Wild Pyromancer triggers if summoned from Resurrect
	"""
	game = prepare_game()
	resurrect = game.player1.give("BRM_017")
	pyromancer = game.player1.give("NEW1_020")
	pyromancer.play()
	game.player1.give(MOONFIRE).play(target=pyromancer)
	assert pyromancer.dead

	game.player1.give(WISP).play()
	assert len(game.player1.field) == 1

	resurrect.play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == pyromancer.id
	assert game.player1.field[0].health == 1


def test_rend_blackhand():
	game = prepare_empty_game()
	rend1 = game.player1.give("BRM_029")
	assert not rend1.powered_up
	assert not rend1.requires_target()
	game.player1.give(WHELP)
	assert not rend1.powered_up
	assert not rend1.requires_target()
	pagle = game.player2.summon("EX1_557")
	assert rend1.powered_up
	assert rend1.requires_target()
	assert rend1.targets == [pagle]
	rend1.play(target=pagle)
	assert pagle.dead
	game.end_turn(); game.end_turn()

	rend2 = game.player1.give("BRM_029")
	assert rend2.battlecry_requires_target()
	assert rend2.requires_target()
	assert rend2.targets == [rend1]
	rend1.destroy()
	assert rend2.battlecry_requires_target()
	assert not rend2.requires_target()
	assert not rend2.targets
	rend2.play()


def test_revenge():
	game = prepare_game()
	dummy1 = game.player1.summon(TARGET_DUMMY)
	assert dummy1.health == 2
	assert game.player1.hero.health == 30
	revenge = game.player1.give("BRM_015")
	assert not revenge.powered_up
	revenge.play()
	assert dummy1.health == 1
	assert game.player1.hero.health == 30
	dummy2 = game.player1.summon(TARGET_DUMMY)
	assert dummy2.health == 2
	revenge2 = game.player1.give("BRM_015")
	assert not revenge2.powered_up
	game.player1.hero.set_current_health(12)
	assert revenge2.powered_up
	revenge2.play()
	assert dummy1.dead
	assert dummy2.dead


def test_solemn_vigil():
	game = prepare_game()
	game.player1.discard_hand()
	vigil = game.player1.give("BRM_001")
	assert vigil.cost == 5
	game.player1.summon(WISP).destroy()
	assert vigil.cost == 4
	game.player2.summon(WISP).destroy()
	assert vigil.cost == 3
	wisp1 = game.player1.summon(WISP)
	game.player1.give(MOONFIRE).play(target=wisp1)
	assert vigil.cost == 2
	wisp2 = game.player1.summon(WISP)
	game.player1.give(MOONFIRE).play(target=wisp2)
	assert vigil.cost == 1
	game.player1.summon(WISP).destroy()
	assert vigil.cost == 0
	game.player1.summon(WISP).destroy()
	assert vigil.cost == 0
	vigil.play()
	assert len(game.player1.hand) == 2
	assert game.player1.used_mana == 0


##
# Adventure

def test_brood_affliction_bronze():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	deathwing = game.player1.give("NEW1_030")

	brood1 = game.player1.give("BRMA12_7")
	assert wisp.cost == 0
	assert footman.cost == 1
	assert deathwing.cost == 10
	brood1.discard()

	game.player2.give("BRMA12_7")
	assert wisp.cost == 0
	assert footman.cost == 1 - 1
	assert deathwing.cost == 10 - 1

	game.player2.give("BRMA12_7H")
	assert wisp.cost == 0
	assert footman.cost == 1 - 1
	assert deathwing.cost == 10 - 1 - 3


def test_dark_iron_bouncer_brawl():
	game = prepare_game()
	bouncer = game.player1.give("BRMA01_3")
	bouncer.play()
	for i in range(6):
		game.player1.give(WISP).play()
	game.end_turn()

	for i in range(7):
		game.player2.give(WISP).play()
	brawl = game.player2.give("EX1_407")
	brawl.play()
	assert len(game.board) == 1
	assert not bouncer.dead
