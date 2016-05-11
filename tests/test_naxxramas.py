from utils import *


def test_anubar_ambusher():
	game = prepare_empty_game()
	ambusher = game.player1.summon("FP1_026")
	wisp = game.player1.summon(WISP)
	assert wisp in game.player1.field
	ambusher.destroy()
	assert len(game.player1.field) == 0
	assert wisp in game.player1.hand


def test_avenge_board_clear():
	game = prepare_game()
	avenge = game.player1.give("FP1_020")
	wisp1 = game.player1.give(WISP)
	wisp2 = game.player1.give(WISP)
	avenge.play()
	wisp1.play()
	wisp2.play()
	game.end_turn()

	arcane = game.player2.give("CS2_025")
	arcane.play()
	assert avenge in game.player1.secrets


def test_baron_rivendare():
	game = prepare_game()
	gnome = game.player1.give("EX1_029")
	gnome.play()
	assert not game.player1.extra_deathrattles
	rivendare = game.player1.give("FP1_031")
	rivendare.play()
	assert game.player1.extra_deathrattles
	game.player1.give(MOONFIRE).play(target=gnome)
	assert game.player2.hero.health == 26


def test_baron_rivendare_soul_of_the_forest():
	game = prepare_game()
	rivendare = game.player1.give("FP1_031")
	rivendare.play()
	wisp = game.player1.give(WISP)
	wisp.play()
	sotf = game.player1.give("EX1_158")
	sotf.play()
	assert len(game.player1.field) == 2
	assert wisp.has_deathrattle
	assert rivendare.has_deathrattle
	game.player1.give(MOONFIRE).play(target=wisp)
	assert wisp.dead
	assert rivendare.zone == Zone.PLAY
	assert len(game.player1.field) == 3  # Rivendare and two treants
	game.player1.give(DESTROY).play(target=rivendare)
	assert len(game.player1.field) == 3  # Only one treant spawns


def test_baron_rivendare_sylvanas():
	# Test for bug #266
	# When stolen, Rivendare should not apply EXTRA_DEATHRATTLES fast
	# enough to cause a second Steal
	game = prepare_game()
	sylvanas = game.player1.give("EX1_016")
	sylvanas.play()
	game.end_turn()

	rivendare1 = game.player2.give("FP1_031")
	rivendare1.play()
	rivendare2 = game.player2.give("FP1_031")
	rivendare2.play()
	sylvanas.destroy()
	assert len(game.player1.field) == len(game.player2.field) == 1
	assert rivendare1.controller != rivendare2.controller


def test_deaths_bite():
	game = prepare_game()
	deathsbite = game.player1.give("FP1_021")
	deathsbite.play()
	assert game.player1.weapon is deathsbite
	game.player1.hero.attack(game.player2.hero)
	assert game.player2.hero.health == 26
	assert deathsbite.durability == 1
	game.end_turn()

	token = game.player2.give(SPELLBENDERT)
	token.play()
	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	wisp2 = game.player1.give(WISP)
	wisp2.play()
	game.player1.hero.attack(game.player2.hero)
	assert game.player2.hero.health == 22
	assert wisp.dead
	assert wisp2.dead
	assert token.health == 2


def test_deaths_bite_replace():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	deathsbite = game.player1.give("FP1_021")
	deathsbite.play()
	weapon = game.player1.give(LIGHTS_JUSTICE)
	weapon.play()
	assert wisp.dead


def test_deathlord():
	game = prepare_empty_game()
	deathlord1 = game.player1.give("FP1_009")
	deathlord1.play()
	assert len(game.player2.field) == 0
	deathlord1.destroy()
	assert len(game.player2.field) == 0
	game.player2.give(WISP).shuffle_into_deck()
	game.player2.give(WISP).shuffle_into_deck()
	game.player2.give(MOONFIRE).shuffle_into_deck()
	deathlord2 = game.player1.give("FP1_009")
	deathlord2.play()
	assert len(game.player2.field) == 0
	assert len(game.player2.deck) == 3
	deathlord2.destroy()
	assert len(game.player2.field) == 1
	assert game.player2.field[0].id == WISP
	assert len(game.player2.deck) == 2


def test_echoing_ooze():
	game = prepare_game()
	ooze = game.player1.give("FP1_003")
	ooze.play()
	assert len(game.player1.field) == 1
	game.end_turn()

	assert len(game.player1.field) == 2
	assert game.player1.field[0] is ooze
	assert game.player1.field[1].id == ooze.id
	assert game.player1.field[1].atk == ooze.atk
	assert game.player1.field[1].health == ooze.health


def test_haunted_creeper():
	game = prepare_game()
	creeper = game.player1.give("FP1_002")
	creeper.play()
	assert len(game.player1.field) == 1
	game.player1.give(MOONFIRE).play(target=creeper)
	game.player1.give(MOONFIRE).play(target=creeper)
	assert creeper.dead
	assert len(game.player1.field) == 2


def test_kel_thuzad():
	game = prepare_game()
	kt = game.player1.summon("FP1_013")
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	game.end_turn()

	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	wisp = game.player2.give(WISP)
	wisp.play()
	game.player2.give(MOONFIRE).play(target=wisp)
	game.end_turn()

	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	assert len(game.player1.field) == 2
	assert len(game.player2.field) == 0
	game.end_turn()

	assert len(game.player1.field) == 2
	assert len(game.player2.field) == 0
	game.player2.give(MOONFIRE).play(target=wisp2)
	assert wisp2.dead
	assert len(game.player1.field) == 1
	game.end_turn()

	assert wisp2.dead
	assert len(game.player1.field) == 2
	assert game.player1.field[1] == WISP
	game.end_turn()

	# ensure the effect is gone when Kel'Thuzad dies
	game.player2.give(MOONFIRE).play(target=game.player1.field[1])
	kt.destroy()
	assert len(game.player1.field) == 0
	game.end_turn()

	assert len(game.player1.field) == 0


def test_kel_thuzad_sylvanas():
	# Test for https://github.com/HearthSim/hs-bugs/issues/137
	game = prepare_game()
	sylvanas = game.player2.summon("EX1_016")
	wisp = game.player1.summon(WISP)
	game.player1.give(MOONFIRE).play(target=wisp)
	assert len(game.player1.field) == 0
	assert len(game.player2.field) == 1
	sylvanas.destroy()
	assert len(game.player1.field) == 0
	assert len(game.player2.field) == 0
	kt = game.player1.give("FP1_013")
	kt.play()
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	game.end_turn()

	assert len(game.player1.field) == 2
	assert len(game.player2.field) == 0


def test_lil_exorcist():
	game = prepare_game()
	exorcist1 = game.player1.give("GVG_097")
	exorcist1.play()
	assert exorcist1.atk == 2
	assert exorcist1.health == 3
	assert not exorcist1.buffs
	game.end_turn()

	game.player2.give("FP1_001").play()
	game.player2.give("FP1_001").play()
	game.end_turn()

	exorcist2 = game.player1.give("GVG_097")
	exorcist2.play()
	assert exorcist2.atk == 2 + 2
	assert exorcist2.health == 3 + 2
	assert exorcist2.buffs


def test_loatheb():
	game = prepare_game()
	loatheb = game.player1.give("FP1_030")
	fireballp1 = game.player1.give("CS2_029")
	fireball1 = game.player2.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	moonfire = game.player2.give(MOONFIRE)

	assert fireball1.cost == fireball2.cost == fireballp1.cost == 4
	assert moonfire.cost == 0
	loatheb.play()
	# costs do not change right away
	assert fireball1.cost == fireball2.cost == fireballp1.cost == 4
	assert moonfire.cost == 0
	game.end_turn()

	assert fireball1.cost == fireball2.cost == 4 + 5
	assert moonfire.cost == 0 + 5
	assert fireballp1.cost == 4
	game.end_turn()

	assert fireball1.cost == fireball2.cost == fireballp1.cost == 4
	assert moonfire.cost == 0


def test_mad_scientist():
	game = prepare_empty_game()
	vaporize = game.player1.give("EX1_594")
	vaporize.shuffle_into_deck()
	counterspell = game.player1.give("EX1_287")
	scientist = game.player1.give("FP1_004")
	scientist.play()
	assert len(game.player1.deck) == 1
	assert len(game.player1.hand) == 1
	assert len(game.player1.secrets) == 0
	game.player1.give(MOONFIRE).play(target=scientist)
	game.player1.give(MOONFIRE).play(target=scientist)
	assert scientist.dead
	assert len(game.player1.deck) == 0
	assert len(game.player1.hand) == 1
	assert vaporize in game.player1.secrets
	assert counterspell in game.player1.hand


def test_nerubar_weblord():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	moonfire1 = game.player1.give(MOONFIRE)
	moonfire2 = game.player2.give(MOONFIRE)
	footman1 = game.player1.give(GOLDSHIRE_FOOTMAN)
	footman2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	archer1 = game.player1.give("CS2_189")
	archer2 = game.player2.give("CS2_189")
	perdition1 = game.player1.give("EX1_133")
	perdition2 = game.player2.give("EX1_133")
	assert moonfire1.cost == moonfire2.cost == 0
	assert footman1.cost == footman2.cost == 1
	assert archer1.cost == archer2.cost == 1
	assert perdition1.cost == perdition2.cost == 3
	nerubar = game.player1.give("FP1_017")
	nerubar.play()
	assert moonfire1.cost == moonfire2.cost == 0
	assert footman1.cost == footman2.cost == 1
	assert archer1.cost == archer2.cost == 1 + 2
	assert perdition1.cost == perdition2.cost == 3


def test_poison_seeds():
	game = prepare_game()
	abomination = game.player1.give("EX1_097")
	abomination.play()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.end_turn()

	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	seeds = game.player2.give("FP1_019")
	seeds.play()

	assert len(game.board) == 4 + 4
	assert game.player1.hero.health == 30 - 2
	assert game.player2.hero.health == 30 - 2
	assert game.player1.field == ["FP1_019t"] * 4
	assert game.player2.field == ["FP1_019t"] * 4


def test_reincarnate():
	game = prepare_game()

	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	assert goldshire.health == 2
	game.player1.give(MOONFIRE).play(target=goldshire)
	assert goldshire.health == 1
	assert len(game.player1.field) == 1
	game.player1.give("FP1_025").play(target=goldshire)
	assert len(game.player1.field) == 1
	assert game.player1.field[0].health == 2
	game.player1.field[0].destroy()

	# Ensure charge refresh
	leeroy1 = game.player1.give("EX1_116")
	leeroy1.play()
	assert leeroy1.can_attack()
	leeroy1.attack(target=game.player2.hero)
	assert not leeroy1.can_attack()
	game.player1.give("FP1_025").play(target=leeroy1)
	leeroy2 = game.player1.field[0]
	assert leeroy2.can_attack()
	leeroy2.attack(target=game.player2.hero)
	assert not leeroy2.can_attack()


def test_reincarnate_explosive_sheep():
	"""
	Test Reincarnate's forced deaths by playing it on an Explosive Sheep
	"""
	game = prepare_game()
	sheep = game.player1.give("GVG_076")
	sheep.play()
	reincarnate = game.player1.give("FP1_025")
	reincarnate.play(target=sheep)
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "GVG_076"


def test_reincarnate_kel_thuzad():
	game = prepare_game()
	kelthuzad = game.player1.give("FP1_013")
	kelthuzad.play()
	assert len(game.player1.field) == 1
	game.player1.give("FP1_025").play(target=kelthuzad)
	assert len(game.player1.field) == 1
	game.end_turn()
	assert len(game.player1.field) == 2
	assert len(game.player1.field.filter(id="FP1_013")) == 2


def test_shade_of_naxxramas():
	game = prepare_game()
	shade = game.player1.give("FP1_005")
	shade.play()
	assert shade.atk == shade.health == 2
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	assert shade.atk == shade.health == 2
	game.end_turn()

	assert shade.stealthed
	assert shade.atk == shade.health == 3
	shade.attack(game.player2.hero)
	assert not shade.stealthed
	game.end_turn()

	wisp.attack(target=shade)
	assert shade.health == 2
	game.end_turn()

	assert shade.atk == 4
	assert shade.health == 3
	assert not shade.stealthed


def test_stalagg_feugen():
	game = prepare_game()
	stalagg1 = game.player1.give("FP1_014")
	stalagg2 = game.player1.give("FP1_014")
	feugen = game.player1.give("FP1_015")
	stalagg1.play()
	stalagg2.play()

	stalagg1.destroy()
	assert stalagg1.dead
	stalagg2.destroy()
	assert stalagg2.dead
	assert len(game.player1.field) == 0
	game.end_turn(); game.end_turn()

	feugen.play()
	feugen.destroy()
	assert feugen.dead
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "FP1_014t"


def test_stalagg_feugen_both_killed():
	game = prepare_game()
	stalagg = game.player1.give("FP1_014")
	stalagg.play()
	game.end_turn()

	feugen = game.player2.give("FP1_015")
	feugen.play()
	game.end_turn()

	stalagg.attack(feugen)
	assert stalagg.dead
	assert feugen.dead
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 1
	assert game.player1.field[0].id == "FP1_014t"
	assert game.player2.field[0].id == "FP1_014t"


def test_stalagg_feugen_sap_destroy():
	game = prepare_game()
	stalagg = game.player1.give("FP1_014")
	stalagg.destroy()
	feugen = game.player1.give("FP1_015")
	feugen.play()
	game.player1.discard_hand()
	for i in range(10):
		game.player1.give(WISP)
	assert len(game.player1.hand) == 10
	game.end_turn()

	sap = game.player2.give("EX1_581")
	sap.play(target=feugen)
	assert feugen.dead
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "FP1_014t"


def test_stoneskin_gargoyle():
	game = prepare_game()
	gargoyle = game.player1.give("FP1_027")
	gargoyle.play()
	assert gargoyle.health == 4
	# damage the gargoyle by 1
	game.player1.give(MOONFIRE).play(target=gargoyle)
	assert gargoyle.health == 3
	game.end_turn(); game.end_turn()

	assert gargoyle.health == 4


def test_undertaker():
	game = prepare_game()
	undertaker = game.player1.give("FP1_028")
	undertaker.play()
	game.player1.give(WISP).play()
	assert not undertaker.buffs
	assert undertaker.atk == 1
	assert undertaker.health == 2
	game.end_turn()

	# Play a leper gnome, should not trigger undertaker
	game.player2.give("EX1_029").play()
	assert undertaker.atk == 1
	assert undertaker.health == 2
	game.end_turn()

	game.player1.give("EX1_029").play()
	assert undertaker.atk == 2
	assert undertaker.health == 2
	game.player1.give("EX1_029").play()
	assert undertaker.atk == 3
	assert undertaker.health == 2


def test_unstable_ghoul():
	game = prepare_game()
	wisp = game.player2.summon(WISP)
	acolyte = game.player2.summon("EX1_007")
	ghoul = game.player1.give("FP1_024")
	ghoul.play()
	game.end_turn()

	game.player2.discard_hand()
	assert not wisp.dead
	assert not acolyte.dead
	assert acolyte.health == 3
	assert len(game.player2.hand) == 0
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	ghoul.destroy()
	assert wisp.dead
	assert not acolyte.dead
	assert acolyte.health == 3 - 1
	assert len(game.player2.hand) == 1
	assert game.player1.hero.health == game.player2.hero.health == 30


def test_voidcaller():
	game = prepare_game()
	game.player1.discard_hand()
	voidcaller = game.player1.give("FP1_022")
	voidcaller.play()

	# give the player a Doomguard and a couple of wisps
	doomguard = game.player1.give("EX1_310")
	game.player1.give(WISP)
	game.player1.give(WISP)
	game.player1.give(WISP)
	assert len(game.player1.hand) == 4

	# sacrificial pact on the voidcaller, should summon the Doomguard w/o discards
	game.player1.give("NEW1_003").play(target=voidcaller)
	assert voidcaller.dead
	assert doomguard.zone == Zone.PLAY
	assert doomguard.can_attack()
	assert len(game.player1.hand) == 3


def test_wailing_soul():
	game = prepare_game()
	goldshire1 = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire1.play()
	goldshire2 = game.player2.summon(GOLDSHIRE_FOOTMAN)
	wisp = game.player1.give(WISP)
	wisp.play()
	soul = game.player1.give("FP1_016")
	soul.play()
	assert goldshire1.silenced
	assert not goldshire1.taunt
	assert not goldshire2.silenced
	assert wisp.silenced


def test_webspinner():
	game = prepare_game()
	game.player1.discard_hand()
	webspinner = game.player1.give("FP1_011")
	webspinner.play()
	game.player1.give(MOONFIRE).play(target=webspinner)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.BEAST
	assert game.player1.hand[0].type == CardType.MINION


def test_zombie_chow():
	game = prepare_game()
	chow1 = game.player1.give("FP1_001")
	chow1.play()
	chow2 = game.player1.give("FP1_001")
	chow2.play()
	chow3 = game.player1.give("FP1_001")
	chow3.play()
	game.player2.hero.set_current_health(24)
	assert game.player2.hero.health == 24
	chow1.destroy()
	assert game.player2.hero.health == 24 + 5
	chow2.destroy()
	assert game.player2.hero.health == 30
	chow3.destroy()
	assert game.player2.hero.health == 30
