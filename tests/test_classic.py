#!/usr/bin/env python
from utils import *


def test_abusive_sergeant():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	game.player1.give("CS2_188").play(target=wisp)
	assert wisp.atk == 3
	game.end_turn()
	assert wisp.atk == 1


def test_acolyte_of_pain():
	game = prepare_game()
	acolyte = game.player1.give("EX1_007")
	acolyte.play()
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	game.player1.give(MOONFIRE).play(target=acolyte)
	assert len(game.player1.hand) == 1
	game.player1.give(MOONFIRE).play(target=acolyte)
	assert len(game.player1.hand) == 2
	game.player1.give(MOONFIRE).play(target=acolyte)
	assert len(game.player1.hand) == 3
	assert acolyte.dead


def test_alarmobot():
	game = prepare_game()
	game.player1.discard_hand()
	bot = game.player1.give("EX1_006")
	bot.play()
	wisp = game.player1.give(WISP)
	for i in range(9):
		game.player1.give(MOONFIRE)
	assert len(game.player1.hand) == 10
	assert bot.zone == Zone.PLAY
	assert wisp.zone == Zone.HAND
	game.end_turn(); game.end_turn()
	assert bot in game.player1.hand
	assert wisp in game.player1.field
	assert len(game.player1.field) == 1
	assert len(game.player1.hand) == 10

	# bot should not trigger if hand has no minions
	bot.play()
	game.player1.give(MOONFIRE)
	assert len(game.player1.hand) == 10
	game.end_turn(); game.end_turn()
	assert len(game.player1.hand) == 10
	assert bot.zone == Zone.PLAY
	assert len(game.player1.field) == 2


def test_alexstrasza():
	game = prepare_game()
	alex1 = game.player1.give("EX1_561")
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	alex1.play(target=game.player1.hero)
	assert game.player1.hero.health == 15
	assert game.player1.hero.max_health == 30
	assert game.player2.hero.health == 30
	game.end_turn(); game.end_turn()

	alex2 = game.player1.give("EX1_561")
	assert game.player2.hero.health == 30
	alex2.play(target=game.player2.hero)
	assert game.player2.hero.health == 15


def test_alexstrasza_armor():
	game = prepare_game(CardClass.WARRIOR, CardClass.WARRIOR)
	game.player1.hero.power.use()
	game.end_turn()

	alex = game.player2.give("EX1_561")
	assert game.player1.hero.health == 30
	assert game.player1.hero.armor == 2
	alex.play(target=game.player1.hero)
	assert game.player1.hero.health == 15
	assert game.player1.hero.armor == 2


def test_alexstrasza_ragnaros():
	game = prepare_game()
	majordomo = game.player1.give("BRM_027")
	majordomo.play()
	majordomo.destroy()
	assert game.player1.hero.id == "BRM_027h"
	assert game.player1.hero.health == 8
	assert game.player1.hero.max_health == 8
	game.end_turn(); game.end_turn()

	alex = game.player1.give("EX1_561")
	alex.play(target=game.player1.hero)
	assert game.player1.hero.buffs
	assert game.player1.hero.health == 15
	assert game.player1.hero.max_health == 15


def test_amani_berserker():
	game = prepare_game()
	amani1 = game.player1.give("EX1_393")
	amani1.play()
	game.end_turn()

	amani2 = game.player2.give("EX1_393")
	amani2.play()
	game.end_turn()

	assert amani1.atk == amani2.atk == 2
	amani1.attack(amani2)
	# check both minions are still alive, that the enrage didn't trigger too early
	assert amani1.zone == amani2.zone == Zone.PLAY
	assert amani1 in game.player1.field
	assert amani2 in game.player2.field
	assert amani1.damage == amani2.damage == 2
	assert amani1.atk == amani2.atk == 2 + 3
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert amani1.atk == amani2.atk == 2
	assert amani1.health == amani2.health == 3
	game.player1.give(MOONFIRE).play(target=amani1)
	assert amani1.atk == 2 + 3


def test_ancestral_healing():
	game = prepare_empty_game()
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	game.player1.give(DAMAGE_5).play(target=statue)
	assert not statue.taunt
	assert statue.damage == 5
	assert statue.health == 10 - 5
	game.player1.give("CS2_041").play(statue)
	assert statue.taunt
	assert statue.health == 10


def test_ancestral_spirit():
	game = prepare_game()
	ancestral = game.player1.give("CS2_038")
	wisp = game.player1.give(WISP)
	wisp.play()
	assert not wisp.has_deathrattle
	ancestral.play(target=wisp)
	assert wisp.has_deathrattle
	wisp.destroy()
	assert len(game.board) == 1
	assert game.player1.field[0].id == WISP


def test_ancient_of_lore():
	game = prepare_game()
	game.player1.discard_hand()

	game.player1.give(DAMAGE_5).play(target=game.player1.hero)
	game.player1.give(DAMAGE_5).play(target=game.player1.hero)
	assert game.player1.hero.health == 30 - 10

	ancient1 = game.player1.give("NEW1_008")
	ancient1.play(choose="NEW1_008a")  # Draw 2 Cards
	assert len(game.player1.hand) == 1
	assert game.player1.hero.health == 30 - 10
	game.end_turn(); game.end_turn()

	game.player1.discard_hand()
	ancient2 = game.player1.give("NEW1_008")
	# Play to heal hero by 5
	ancient2.play(target=game.player1.hero, choose="NEW1_008b")
	assert not game.player1.hand
	assert game.player1.hero.health == 30 - 10 + 5


def test_ancient_watcher():
	game = prepare_game()
	watcher = game.player1.give("EX1_045")
	watcher.play()
	game.end_turn(); game.end_turn()
	assert not watcher.can_attack()
	game.player1.give(SILENCE).play(target=watcher)
	assert watcher.can_attack()


def test_animal_companion():
	game = prepare_game()
	companion = game.player1.give("NEW1_031")
	companion.play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id in ("NEW1_032", "NEW1_033", "NEW1_034")


def test_angry_chicken():
	game = prepare_game()
	chicken = game.player1.give("EX1_009")
	chicken.play()
	stormwind = game.player1.give("CS2_222")
	stormwind.play()
	assert chicken.enrage
	assert not chicken.enraged
	assert chicken.atk == chicken.health == 2
	game.player1.give(MOONFIRE).play(target=chicken)
	assert chicken.enraged
	assert chicken.atk == 1 + 1 + 5
	assert chicken.health == 1
	stormwind.destroy()
	assert chicken.atk == chicken.health == 1
	assert not chicken.enraged


def test_arathi_weaponsmith():
	game = prepare_game()
	arathi = game.player1.give("EX1_398")
	assert not game.player1.weapon
	arathi.play()
	assert game.player1.weapon.id == "EX1_398t"


def test_arcane_explosion():
	game = prepare_game()
	# play some wisps
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.end_turn()

	arcanex = game.player2.give("CS2_025")
	arcanex.play()
	assert not game.board


def test_arcane_golem():
	game = prepare_game(game_class=Game)
	golem = game.player1.give("EX1_089")
	for i in range(3):
		game.end_turn(); game.end_turn()

	assert game.player1.max_mana == 4
	assert game.player2.max_mana == 3
	golem.play()
	assert game.player1.max_mana == 4
	assert game.player2.max_mana == 4


def test_arcane_missiles():
	game = prepare_game()
	wisp = game.player2.summon(WISP)
	missiles = game.player1.give("EX1_277")
	missiles.play()
	if wisp.dead:
		assert game.player2.hero.health == 28
	else:
		assert game.player2.hero.health == 27


def test_archmage_antonidas():
	game = prepare_game()
	antonidas = game.player1.give("EX1_559")
	antonidas.play()
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == "CS2_029"
	game.player1.give(THE_COIN).play()
	assert len(game.player1.hand) == 2
	assert game.player1.hand[1].id == "CS2_029"


def test_armorsmith():
	game = prepare_game()
	armorsmith1 = game.player1.give("EX1_402")
	armorsmith1.play()
	game.end_turn()

	armorsmith2 = game.player2.give("EX1_402")
	armorsmith2.play()
	game.end_turn()

	assert game.player1.hero.armor == game.player2.hero.armor == 0
	armorsmith1.attack(target=armorsmith2)
	assert game.player1.hero.armor == game.player2.hero.armor == 1
	game.end_turn()

	game.player2.give("EX1_402").play()
	game.player2.give(WISP).play()

	# Whirlwind
	# 1 armor on each hero, 2 smiths in play for current player, 1 for opponent
	game.player2.give("EX1_400").play()
	assert game.player2.hero.armor == 1 + (2 * 3)
	assert game.current_player.hero.health == 30
	assert game.player1.hero.armor == 1 + 1


def test_avenging_wrath():
	game = prepare_game()
	wisp = game.player2.summon(WISP)
	game.player1.give("EX1_384").play()
	if wisp.dead:
		assert game.player2.hero.health == 30 - 7
	else:
		assert game.player2.hero.health == 30 - 8
	game.end_turn()

	# Summon Malygos and test that spellpower only increases dmg by 5
	game.player2.summon("EX1_563")
	game.player2.give("EX1_384").play()
	assert game.player1.hero.health == 30 - (8 + 5)


def test_bane_of_doom():
	game = prepare_game()
	doom = game.player1.give("EX1_320")
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	doom.play(target=statue)
	assert len(game.player1.field) == 1
	assert statue.health == 10 - 2
	statue.destroy()
	game.end_turn(); game.end_turn()

	wisp = game.player1.give(WISP)
	wisp.play()
	doom2 = game.player1.give("EX1_320")
	doom2.play(target=wisp)
	assert len(game.player1.field) == 1
	assert game.player1.field[0].race == Race.DEMON
	assert game.player1.field[0].data.collectible


def test_baron_geddon():
	game = prepare_game()

	geddon1 = game.player1.give("EX1_249")
	wisp = game.player1.give(WISP)
	geddon1.play()
	wisp.play()
	assert geddon1.health == 5
	assert not wisp.dead
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	game.end_turn()
	assert geddon1.health == 5
	assert wisp.dead
	assert game.player1.hero.health == 28
	assert game.player2.hero.health == 28

	geddon2 = game.player2.give("EX1_249")
	geddon2.play()
	assert geddon1.health == 5
	assert geddon2.health == 5
	game.end_turn()
	assert geddon1.health == 3
	assert geddon2.health == 5


def test_battle_rage():
	game = prepare_game()
	game.player1.discard_hand()
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	for target in (statue, game.player1.hero, game.player2.hero):
		game.player1.give(MOONFIRE).play(target=target)
	cs = game.player1.give("EX1_392")
	cs.play()
	assert len(game.player1.hand) == 2


def test_bestial_wrath():
	game = prepare_game()
	wolf = game.current_player.give("DS1_175")
	wolf.play()
	bestial = game.current_player.give("EX1_549")
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	game.end_turn()

	wisp2 = game.current_player.summon(WISP)
	game.end_turn()

	assert wolf.atk == 1
	assert not wolf.immune
	assert wolf in bestial.targets
	assert wisp1 not in bestial.targets
	assert wisp2 not in bestial.targets
	bestial.play(target=wolf)
	assert wolf.atk == 3
	assert wolf.immune
	wolf.attack(target=wisp2)
	assert wolf.health == 1
	assert wolf.zone == Zone.PLAY
	assert wisp2.dead
	game.end_turn()

	assert wolf.atk == 1
	assert not wolf.immune


def test_betrayal():
	game = prepare_game()
	wisp1 = game.player1.give(WISP).play()
	wisp2 = game.player1.give(WISP).play()
	wisp3 = game.player1.give(WISP).play()
	assert len(game.current_player.field) == 3
	game.end_turn()

	betrayal = game.player2.give("EX1_126")
	betrayal.play(target=wisp2)
	assert len(game.player1.field) == 1
	assert wisp1.dead
	assert not wisp2.dead
	assert wisp3.dead
	game.end_turn()

	bender = game.player1.give(SPELLBENDERT).play()
	game.end_turn()

	game.player2.give("EX1_126").play(target=wisp2)
	assert not wisp2.dead
	assert not bender.dead
	assert bender.health == 2


def test_betrayal_poisonous():
	game = prepare_game()
	statue1 = game.player1.give(ANIMATED_STATUE)
	statue1.play()
	cobra = game.player1.give("EX1_170").play()
	statue2 = game.player1.give(ANIMATED_STATUE)
	statue2.play()
	game.end_turn()

	game.player2.give("EX1_126").play(target=cobra)
	assert statue1.dead
	assert not cobra.dead
	assert statue2.dead


def test_big_game_hunter():
	game = prepare_game()
	bgh1 = game.player1.give("EX1_005")
	assert not bgh1.requires_target()
	bgh1.play()
	game.end_turn()

	wargolem = game.player2.give("CS2_186")
	wargolem.play()
	assert wargolem.atk == 7
	game.end_turn()

	bgh2 = game.player1.give("EX1_005")
	assert bgh2.requires_target()
	bgh2.play(target=wargolem)
	assert wargolem.dead


def test_blade_flurry():
	game = prepare_game()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.end_turn()

	game.player2.give(WISP).play()
	flurry = game.player2.give("CS2_233")
	assert not flurry.is_playable()
	game.player2.give(LIGHTS_JUSTICE).play()
	assert flurry.is_playable()
	flurry.play()
	assert not game.player1.field
	assert len(game.player2.field) == 1
	assert game.player1.hero.health == game.player2.hero.health == 30


def test_blessing_of_wisdom():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	blessing = game.player1.give("EX1_363")
	blessing.play(target=wisp)
	game.end_turn(); game.end_turn()

	game.player1.discard_hand()
	wisp.attack(target=game.current_player.opponent.hero)
	assert len(game.current_player.hand) == 1
	game.end_turn()

	# Shadow Madness should draw for the original caster
	game.player2.discard_hand()
	shadowmadness = game.player2.give("EX1_334")
	shadowmadness.play(target=wisp)
	assert len(game.player1.hand) == 1
	wisp.attack(target=game.player1.hero)
	assert len(game.player1.hand) == 2
	assert not game.player2.hand


def test_blizzard():
	game = prepare_game()
	for i in range(4):
		game.player1.give(ANIMATED_STATUE).play()
	game.end_turn()

	blizzard = game.player2.give("CS2_028")
	blizzard.play()
	for statue in game.player1.field:
		assert statue.damage == 2
		assert statue.frozen


def test_blood_imp():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp2 = game.player1.give(WISP)
	imp = game.player1.give("CS2_059")
	imp.play()
	assert imp.health == 1
	game.end_turn(); game.end_turn()

	assert imp.health == 1
	wisp1.play()
	wisp2.play()
	assert wisp1.health + wisp2.health == 2
	game.end_turn()
	assert wisp1.health + wisp2.health == 3

	assert imp.health == 1
	assert wisp1.atk == 1
	assert wisp2.atk == 1


def test_blood_knight():
	game = prepare_game()
	game.end_turn()

	squire = game.current_player.give("EX1_008")
	squire.play()
	assert squire.divine_shield
	game.end_turn()

	bloodknight1 = game.current_player.give("EX1_590")
	bloodknight1.play()
	assert not squire.divine_shield
	assert bloodknight1.atk == 6
	assert bloodknight1.health == 6
	game.end_turn()

	game.current_player.give("EX1_008").play()
	game.current_player.give("EX1_008").play()
	# Play an argent protector on the squire
	game.current_player.give("EX1_362").play(target=squire)
	assert squire.divine_shield
	game.end_turn()

	bloodknight2 = game.current_player.give("EX1_590")
	bloodknight2.play()
	assert not squire.divine_shield
	assert bloodknight2.atk == 12
	assert bloodknight2.health == 12
	game.end_turn(); game.end_turn()

	bloodknight3 = game.current_player.give("EX1_590")
	bloodknight3.play()
	assert bloodknight3.atk == 3
	assert bloodknight3.health == 3


def test_brawl():
	game = prepare_game()
	brawl = game.player1.give("EX1_407")
	game.player1.give(GOLDSHIRE_FOOTMAN).play()
	game.player1.give(WISP).play()
	game.end_turn()

	game.player2.give(GOLDSHIRE_FOOTMAN).play()
	game.player2.give(WISP).play()
	game.end_turn()

	assert len(game.board) == 4
	brawl.play()
	assert len(game.board) == 1
	assert game.board[0].id in (WISP, GOLDSHIRE_FOOTMAN)


def test_captains_parrot():
	game = prepare_empty_game()
	pirate1 = game.player1.give("NEW1_022")
	pirate1.shuffle_into_deck()
	pirate2 = game.player1.give("CS2_146")
	pirate2.shuffle_into_deck()
	wisp = game.player1.give(WISP)
	wisp.shuffle_into_deck()
	assert len(game.player1.deck) == 3
	game.player1.give("NEW1_016").play()
	assert len(game.player1.deck) == 2
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.PIRATE
	game.player1.discard_hand()
	game.player1.give("NEW1_016").play()
	assert len(game.player1.deck) == 1
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.PIRATE
	game.player1.discard_hand()
	assert len(game.player1.deck) == 1
	assert len(game.player1.hand) == 0
	game.player1.give("NEW1_016").play()
	assert len(game.player1.deck) == 1
	assert len(game.player1.hand) == 0


def test_cleave():
	game = prepare_game()
	# play some wisps
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.end_turn()

	cleave = game.current_player.give("CS2_114")
	assert cleave.is_playable()
	cleave.play()
	assert len(game.current_player.opponent.field) == 0
	game.current_player.give(WISP).play()
	game.end_turn()

	cleave2 = game.player1.give("CS2_114")
	assert not cleave2.is_playable()


def test_cold_blood():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	game.end_turn(); game.end_turn()

	cb1 = game.player1.give("CS2_073")
	cb1.play(target=wisp)
	assert wisp.atk == 1 + 2
	cb2 = game.player1.give("CS2_073")
	cb2.play(target=wisp)
	assert wisp.atk == 1 + 2 + 4


def test_corruption():
	game = prepare_game()
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	corruption1 = game.player1.give("CS2_063")
	corruption1.play(target=wisp)
	assert wisp.buffs
	assert wisp.buffs[0].controller == game.player1
	game.end_turn()

	assert not wisp.dead
	game.end_turn()

	assert wisp.dead
	game.end_turn()

	# corrupt our own wisp. next turn opponent MCs it.
	wisp2 = game.player2.give(WISP)
	wisp2.play()
	lucifron = game.player2.give("BRMC_85")
	lucifron.play()
	assert not wisp2.dead
	game.end_turn()

	assert not wisp2.dead
	cabal = game.player1.give("EX1_091")
	cabal.play(target=wisp2)
	assert not wisp2.dead
	game.end_turn()

	assert wisp2.dead


def test_crazed_alchemist():
	game = prepare_game()
	warden = game.player1.give("EX1_396")
	warden.play()
	alchemist = game.player1.give("EX1_059")
	assert warden.atk == 1
	assert not warden.damage
	assert warden.max_health == 7
	assert warden.health == 7
	alchemist.play(target=warden)
	assert warden.atk == 7
	assert warden.health == 1


def test_crazed_alchemist_damage_silence():
	# Test for bug #9
	game = prepare_game()
	snapjaw = game.player1.give("CS2_119")
	snapjaw.play()
	assert snapjaw.atk == 2
	assert snapjaw.health == 7
	game.player1.give("EX1_059").play(target=snapjaw)
	assert snapjaw.atk == 7
	assert snapjaw.health == 2
	game.player1.give(MOONFIRE).play(target=snapjaw)
	assert snapjaw.atk == 7
	assert snapjaw.health == 1
	game.player1.give(SILENCE).play(target=snapjaw)
	assert snapjaw.atk == 2
	assert snapjaw.health == 6


def test_commanding_shout():
	game = prepare_game()
	shout = game.player1.give("NEW1_036")
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	bender = game.player1.give(SPELLBENDERT)
	bender.play()
	giant = game.player2.summon("EX1_620")
	game.end_turn(); game.end_turn()

	assert wisp1.health == 1
	assert bender.health == 3
	assert not wisp1.min_health
	assert not bender.min_health
	shout.play()
	assert wisp1.min_health == 1
	assert bender.min_health == 1
	wisp1.attack(target=giant)
	assert giant.health == 7
	assert wisp1.health == 1
	assert not wisp1.damage
	assert wisp1.zone == Zone.PLAY
	game.player1.give(MOONFIRE).play(target=bender)
	assert bender.health == 2
	assert bender.damage == 1
	bender.attack(target=giant)
	assert not bender.dead
	assert bender.health == 1
	assert bender.damage == 2
	assert bender.zone == Zone.PLAY

	# TODO test that minions played afterwards still get commanding shout buff


def test_conceal():
	game = prepare_game()
	conceal = game.player1.give("EX1_128")
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	conceal.play()
	assert wisp1.stealthed
	assert wisp2.stealthed
	game.end_turn()
	assert wisp1.stealthed
	assert wisp2.stealthed
	game.end_turn()
	assert not wisp1.stealthed
	assert not wisp2.stealthed


def test_conceal_alarmobot():
	# Test for bug #186
	game = prepare_empty_game()
	alarmobot = game.player1.give("EX1_006")
	alarmobot.play()
	conceal = game.player1.give("EX1_128")
	conceal.play()
	assert alarmobot.stealthed
	wisp = game.player1.give(WISP)
	game.end_turn(); game.end_turn()

	assert alarmobot in game.player1.hand
	assert wisp in game.player1.field
	assert not alarmobot.stealthed


def test_cruel_taskmaster():
	game = prepare_game()
	taskmaster1 = game.current_player.give("EX1_603")
	taskmaster2 = game.current_player.give("EX1_603")
	game.end_turn(); game.end_turn()

	wisp = game.current_player.give(WISP)
	wisp.play()
	taskmaster1.play(target=wisp)
	assert wisp.dead
	game.end_turn(); game.end_turn()

	assert taskmaster1.health == 2
	assert taskmaster1.atk == 2
	taskmaster2.play(target=taskmaster1)
	assert taskmaster1.health == 1
	assert taskmaster1.atk == 4


def test_cult_master():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	cultmaster = game.player1.give("EX1_595")
	cultmaster.play()
	assert len(game.player1.hand) == 4
	game.player1.give(MOONFIRE).play(target=wisp1)
	assert len(game.player1.hand) == 4 + 1

	# Make sure cult master doesn't draw off itself
	game.player1.give(MOONFIRE).play(target=cultmaster)
	game.player1.give(MOONFIRE).play(target=cultmaster)
	assert len(game.player1.hand) == 4 + 1

	game.player1.give(MOONFIRE).play(target=wisp2)
	assert len(game.player1.hand) == 4 + 1


def test_cult_master_board_clear():
	game = prepare_game()
	game.player1.discard_hand()
	for i in range(4):
		game.player1.give(WISP).play()
	cultmaster = game.player1.give("EX1_595")
	cultmaster.play()
	game.player1.give(MOONFIRE).play(target=cultmaster)
	assert len(game.player1.field) == 5
	# Whirlwind the board
	game.player1.give("EX1_400").play()
	assert len(game.player1.hand) == 0


def test_deadly_poison():
	game = prepare_game()
	poison = game.player1.give("CS2_074")
	assert not poison.is_playable()
	game.player1.give(LIGHTS_JUSTICE).play()
	assert game.player1.weapon.atk == 1
	assert game.player1.hero.atk == 1
	assert poison.is_playable()
	poison.play()
	assert game.player1.weapon.atk == 3
	assert game.player1.hero.atk == 3


def test_deathwing():
	game = prepare_game()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	deathwing = game.player1.give("NEW1_030")
	deathwing.play()
	assert not game.player1.hand
	assert len(game.board) == 1
	assert not deathwing.dead


def test_defender_of_argus():
	game = prepare_game()
	defender1 = game.player1.give("EX1_093")
	assert defender1.atk == 2
	assert defender1.health == 3
	assert not defender1.taunt
	defender1.play()
	assert defender1.atk == 2
	assert defender1.health == 3
	assert not defender1.taunt
	game.end_turn(); game.end_turn()

	defender2 = game.player1.give("EX1_093")
	defender2.play()
	assert game.player1.field == [defender1, defender2]
	assert defender1.atk == 2 + 1
	assert defender1.health == 3 + 1
	assert defender1.taunt
	game.end_turn(); game.end_turn()

	defender3 = game.player1.give("EX1_093")
	defender3.play(index=1)
	assert game.player1.field == [defender1, defender3, defender2]
	assert defender1.atk == 2 + 1 + 1
	assert defender1.health == 3 + 1 + 1
	assert defender1.taunt
	assert defender2.atk == 2 + 1
	assert defender2.health == 3 + 1
	assert defender2.taunt


def test_defias():
	game = prepare_game()
	defias1 = game.current_player.give("EX1_131")
	defias1.play()
	assert len(game.current_player.field) == 1
	game.end_turn()

	# Coin-defias
	game.current_player.hand.filter(id=THE_COIN)[0].play()
	defias2 = game.current_player.give("EX1_131")
	defias2.play()
	assert len(game.current_player.field) == 2


def test_demolisher():
	game = prepare_game()
	demolisher = game.player1.give("EX1_102")
	demolisher.play()
	game.end_turn()

	assert game.player2.hero.health == 30
	game.end_turn()

	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 28


def test_demonfire():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.player1.give("EX1_596").play(target=wisp)
	assert wisp.dead
	imp = game.player1.give("CS2_059")
	imp.play()
	game.player1.give("EX1_596").play(target=imp)
	assert imp.atk == 0 + 2
	assert imp.health == 1 + 2
	assert imp.buffs
	game.end_turn()

	imp2 = game.player2.give("CS2_059")
	imp2.play()
	game.end_turn()

	game.player1.give("EX1_596").play(target=imp2)
	assert imp2.dead


def test_dire_wolf_alpha():
	game = prepare_game()
	direwolf1 = game.player2.summon("EX1_162")
	assert direwolf1.atk == 2
	direwolf2 = game.player2.summon("EX1_162")
	assert direwolf1.atk == 3
	assert direwolf2.atk == 3
	frostwolf = game.current_player.summon("CS2_121")
	game.end_turn(); game.end_turn()
	frostwolf.attack(direwolf2)


def test_divine_favor():
	game = prepare_game()
	game.player1.discard_hand()
	for i in range(5):
		game.player1.give(WISP)
	assert len(game.player1.hand) == 5
	game.end_turn()

	game.player2.discard_hand()
	game.player2.give(WISP)
	assert len(game.player2.hand) == 1
	favor = game.player2.give("EX1_349")
	favor.play()
	assert len(game.player2.hand) == len(game.player1.hand)


def test_divine_spirit():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	assert wisp.health == 1
	wisp.play()
	game.end_turn()

	game.player2.give("CS2_236").play(target=wisp)
	assert wisp.health == 1 * 2
	game.end_turn()

	game.player1.give("CS2_236").play(target=wisp)
	assert wisp.health == 1 * 2 * 2
	game.end_turn()

	equality = game.player2.give("EX1_619")
	equality.play()
	assert wisp.health == 1
	game.player2.give("CS2_236").play(target=wisp)
	assert wisp.health == 1 * 2
	game.end_turn()


def test_doomhammer():
	game = prepare_game()
	doomhammer = game.player1.give("EX1_567")
	assert doomhammer.windfury
	assert not game.player1.hero.atk
	assert not game.player1.hero.windfury
	doomhammer.play()
	assert doomhammer.windfury
	assert game.player1.hero.atk == 2
	assert game.player1.hero.windfury
	assert game.player1.weapon.durability == 8
	game.player1.hero.attack(target=game.player2.hero)
	assert game.player1.hero.can_attack()
	game.player1.hero.attack(target=game.player2.hero)
	assert not game.player1.hero.can_attack()
	assert game.player1.weapon.durability == 6


def test_doomsayer():
	game = prepare_game()
	# play some wisps
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()

	game.end_turn()
	game.current_player.give(WISP).play()
	game.current_player.give(WISP).play()

	assert len(game.board) == 4
	doomsayer = game.current_player.give("NEW1_021")
	doomsayer.play()
	assert len(game.board) == 5
	game.end_turn()

	assert len(game.board) == 5
	game.end_turn()

	assert len(game.board) == 0


def test_dread_infernal():
	game = prepare_game()
	infernal = game.player1.give("CS2_064")
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.end_turn()

	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.end_turn()

	assert len(game.board) == 6
	infernal.play()
	assert len(game.board) == 1
	assert game.player1.hero.health == game.player2.hero.health == 29
	assert infernal.health == 6


def test_dread_corsair():
	game = prepare_game()
	corsair = game.player1.give("NEW1_022")
	assert corsair.cost == 4
	weapon = game.player1.give(LIGHTS_JUSTICE)
	weapon.play()
	assert corsair.cost == 4 - 1
	axe = game.player1.give("CS2_106")
	axe.play()
	assert corsair.cost == 4 - 3
	axe.destroy()
	assert corsair.cost == 4


def test_earth_shock():
	game = prepare_game()
	crusader = game.player1.give("EX1_020")
	crusader.play()
	assert crusader.divine_shield
	game.end_turn()

	earthshock = game.player2.give("EX1_245")
	earthshock.play(target=crusader)
	assert crusader.dead


def test_elite_tauren_chieftain():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	assert len(game.player1.hand) == 0
	assert len(game.player2.hand) == 0
	tauren = game.player1.give("PRO_001")
	tauren.play()
	assert len(game.player1.hand) == 1
	assert len(game.player2.hand) == 1
	chords = ("PRO_001a", "PRO_001b", "PRO_001c")
	assert game.player1.hand[0] in chords
	assert game.player2.hand[0] in chords


def test_equality():
	game = prepare_game()
	equality = game.current_player.give("EX1_619")
	# summon a bunch of big dudes
	game.current_player.summon("CS2_186")
	game.current_player.summon("CS2_186")
	game.current_player.opponent.summon("CS2_186")
	game.current_player.opponent.summon("CS2_186")
	# And a violet teacher too, why not
	game.current_player.summon("NEW1_026")

	pyro = game.current_player.give("NEW1_020")
	pyro.play()
	assert len(game.board) == 6
	equality.play()
	assert not game.board


def test_ethereal_arcanist():
	game = prepare_game()
	arcanist = game.player1.give("EX1_274")
	arcanist.play()
	assert arcanist.atk == arcanist.health == 3
	game.end_turn(); game.end_turn()

	assert arcanist.atk == arcanist.health == 3
	icebarrier = game.player1.give("EX1_289")
	icebarrier.play()
	assert arcanist.atk == arcanist.health == 3
	game.end_turn()

	assert arcanist.atk == arcanist.health == 3 + 2
	game.end_turn()

	assert arcanist.atk == arcanist.health == 3 + 2
	icebarrier.destroy()
	game.end_turn()

	assert arcanist.atk == arcanist.health == 3 + 2


def test_faceless_manipulator():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	motw = game.player1.give("CS2_009")
	motw.play(target=wisp)
	assert wisp.atk == 1 + 2
	assert wisp.health == 1 + 2
	assert wisp.taunt
	game.player1.give(MOONFIRE).play(target=wisp)
	assert wisp.health == 1 + 2 - 1
	game.end_turn()

	faceless = game.player2.give("EX1_564")
	faceless.play(target=wisp)
	morphed = game.player2.field[0]
	assert morphed.id == WISP
	assert morphed.buffs
	assert wisp.atk == morphed.atk
	assert wisp.health == morphed.health
	assert wisp.max_health == morphed.max_health
	assert morphed.buffs


def test_faceless_manipulator_velens_chosen():
	game = prepare_game()
	kobold = game.player1.give(KOBOLD_GEOMANCER)
	kobold.play()
	game.player1.give("GVG_010").play(target=kobold)
	assert game.player1.spellpower == 2
	faceless = game.player1.give("EX1_564")
	faceless.play(target=kobold)
	assert faceless.morphed.spellpower == kobold.spellpower == 2
	assert game.player1.spellpower == 2 + 2


def test_faerie_dragon():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	dragon = game.player1.give("NEW1_023")
	dragon.play()
	moonfire = game.player1.give(MOONFIRE)
	assert dragon not in moonfire.targets
	assert dragon not in game.player1.hero.power.targets
	game.end_turn()

	assert dragon not in game.current_player.hero.power.targets
	archer = game.current_player.give("CS2_189")
	assert dragon in archer.targets


def test_far_sight():
	game = prepare_game()
	game.player1.discard_hand()
	farsight = game.player1.give("CS2_053")
	farsight.play()
	assert len(game.player1.hand) == 1
	card1 = game.player1.hand[0]

	assert card1.buffs
	assert card1.cost >= 0
	card2 = game.player1.give(card1.id)
	assert card1.cost == max(card2.cost - 3, 0)


def test_far_sight_fatigue():
	game = prepare_empty_game()
	farsight = game.player1.give("CS2_053")
	farsight.play()  # Should not crash
	assert not game.player1.hand


def test_felguard():
	game = prepare_game(game_class=Game)
	for i in range(3):
		game.end_turn(); game.end_turn()
	assert game.player1.max_mana == 4
	felguard = game.player1.give("EX1_301")
	felguard.play()
	assert game.player1.max_mana == 3
	assert game.player1.mana == 1


def test_felguard_negative_mana():
	game = prepare_game(game_class=Game)
	game.player1.give(INNERVATE).play()
	assert game.player1.max_mana == 1
	assert game.player1.mana == 3
	game.player1.give("EX1_301").play()
	assert game.player1.max_mana == 0
	assert game.player1.mana == 0
	game.current_player.give(THE_COIN).play()
	game.current_player.give(THE_COIN).play()
	game.current_player.give(THE_COIN).play()
	game.player1.give("EX1_301").play()
	assert game.player1.max_mana == 0
	assert game.player1.mana == 0


def test_frostwolf_warlord():
	game = prepare_game()
	warlord1 = game.player1.give("CS2_226")
	warlord1.play()
	assert not warlord1.buffs
	assert warlord1.health == warlord1.atk == 4
	game.player2.summon(WISP)
	warlord2 = game.player1.give("CS2_226")
	warlord2.play()
	assert warlord2.buffs
	assert warlord2.health == warlord2.atk == 4 + 1


def test_frothing_berserker():
	game = prepare_game()
	frothing = game.player1.give("EX1_604")
	assert not frothing.buffs
	wisp1 = game.player1.summon(WISP)
	game.player1.give(MOONFIRE).play(target=wisp1)
	assert not frothing.buffs
	frothing.play()
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert not frothing.buffs
	assert frothing.atk == 2
	wisp2 = game.player1.summon(WISP)
	game.player1.give(MOONFIRE).play(target=wisp2)
	assert frothing.buffs
	assert frothing.atk == 2 + 1


def test_flame_leviathan():
	game = prepare_empty_game()
	assert len(game.player1.deck) == 0
	leviathan = game.player1.give("GVG_007")
	leviathan.shuffle_into_deck()
	assert len(game.player1.deck) == 1
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()

	# draw the flame leviathan
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	assert not wisp.dead
	game.end_turn()
	assert game.player1.hero.health == 28
	assert game.player2.hero.health == 28
	assert wisp.dead


def test_force_of_nature():
	game = prepare_game()
	game.player1.give("EX1_571").play()
	assert game.player1.field == ["EX1_tk9"] * 3


def test_gadgetzan_auctioneer():
	game = prepare_game()
	game.player1.discard_hand()
	auctioneer = game.player1.give("EX1_095")
	auctioneer.play()
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert len(game.player1.hand) == 1
	game.player1.give(WISP).play()
	assert len(game.player1.hand) == 1


def test_gladiators_longbow():
	game = prepare_game()
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	game.end_turn()

	bow = game.player2.give("DS1_188")
	bow.play()
	assert game.player2.hero.immune_while_attacking
	assert not game.player1.hero.immune_while_attacking
	assert not game.player2.hero.immune
	game.player2.give(MOONFIRE).play(game.player2.hero)
	assert game.player2.hero.health == 30 - 1
	game.player2.hero.attack(statue)
	assert game.player2.hero.health == 30 - 1
	assert statue.damage == 5
	game.end_turn()

	statue.attack(game.player2.hero)
	assert game.player2.hero.health == 30 - 1 - 10


def test_gorehowl():
	game = prepare_game()
	gorehowl = game.player1.give("EX1_411")
	gorehowl.play()
	game.end_turn()

	wisp1 = game.player2.give(WISP)
	wisp1.play()
	wisp2 = game.player2.give(WISP)
	wisp2.play()
	game.end_turn()

	assert gorehowl.atk == game.player1.hero.atk == 7
	game.player1.hero.attack(wisp1)
	assert wisp1.dead
	assert gorehowl.atk == game.player1.hero.atk == 7 - 1
	assert gorehowl.durability == 1
	assert game.player1.hero.health == 30 - 1
	game.end_turn(); game.end_turn()

	game.player1.hero.attack(wisp2)
	assert wisp2.dead
	assert gorehowl.atk == game.player1.hero.atk == 7 - 1 - 1
	assert gorehowl.durability == 1
	assert game.player1.hero.health == 30 - 1 - 1

	game.end_turn(); game.end_turn()
	game.player1.hero.attack(game.player2.hero)
	assert game.player2.hero.health == 30 - (7 - 1 - 1)
	assert not game.player1.weapon
	assert not game.player1.hero.atk


def test_grimscale_oracle():
	game = prepare_game()
	grimscale = game.player1.give("EX1_508")
	murloc1 = game.player1.summon(MURLOC)
	murloc2 = game.player2.summon(MURLOC)
	assert murloc1.atk == 1
	assert murloc2.atk == 1
	grimscale.play()
	assert murloc1.atk == 1 + 1
	assert murloc2.atk == 1 + 1
	assert grimscale.atk == 1

	game.player1.give(TIME_REWINDER).play(target=grimscale)
	assert murloc1.atk == 1
	assert murloc2.atk == 1


def test_gruul():
	game = prepare_game()
	gruul = game.current_player.give("NEW1_038")
	gruul.play()
	assert gruul.atk == 7
	assert gruul.health == 7
	assert not gruul.buffs
	game.end_turn()

	assert gruul.buffs
	assert gruul.atk == 8
	assert gruul.health == 8
	game.end_turn()

	assert gruul.atk == 9
	assert gruul.health == 9


def test_harrison_jones():
	game = prepare_game()
	game.end_turn()

	lightsjustice = game.player2.give(LIGHTS_JUSTICE)
	lightsjustice.play()
	game.end_turn()

	game.player1.discard_hand()
	assert not game.player1.hand
	assert lightsjustice.durability == 4
	jones = game.player1.give("EX1_558")
	jones.play()
	assert len(game.player1.hand) == 4
	assert lightsjustice.dead
	game.end_turn()

	game.player2.discard_hand()
	jones2 = game.player2.give("EX1_558")
	jones2.play()
	assert not game.player2.hand


def test_headcrack():
	game = prepare_game(exclude=("EX1_137", ))
	headcrack1 = game.player1.give("EX1_137")
	assert game.player1.hand.contains("EX1_137")
	headcrack1.play()
	assert not game.player1.hand.contains("EX1_137")
	game.end_turn(); game.end_turn()

	assert not game.player1.hand.contains("EX1_137")
	headcrack2 = game.player1.give("EX1_137")
	game.player1.give(THE_COIN).play()
	headcrack2.play()
	assert not game.player1.hand.contains("EX1_137")
	game.end_turn()
	assert game.player1.hand.contains("EX1_137")
	game.player1.discard_hand()
	game.end_turn(); game.end_turn()
	assert not game.player1.hand.contains("EX1_137")


def test_heroic_strike():
	game = prepare_game()
	strike = game.current_player.give("CS2_105")
	assert game.current_player.hero.atk == 0
	strike.play()
	assert game.current_player.hero.atk == 4
	game.end_turn()
	assert game.current_player.hero.atk == 0
	game.end_turn()
	assert game.current_player.hero.atk == 0

	game.current_player.give("CS2_105").play()
	game.current_player.give("CS2_106").play()
	assert game.current_player.hero.atk == 7


def test_hogger():
	game = prepare_game()
	hogger = game.current_player.give("NEW1_040")
	hogger.play()
	assert len(game.current_player.field) == 1
	game.end_turn()
	assert len(game.current_player.opponent.field) == 2
	assert game.current_player.opponent.field[1].id == "NEW1_040t"
	game.end_turn()
	assert len(game.current_player.field) == 2
	game.end_turn()
	assert len(game.current_player.opponent.field) == 3


def test_houndmaster():
	game = prepare_game()
	houndmaster = game.current_player.give("DS1_070")
	assert not houndmaster.targets
	assert not houndmaster.powered_up
	hound = game.current_player.give("EX1_538t")
	hound.play()
	assert houndmaster.targets == [hound]
	assert houndmaster.powered_up
	assert hound.atk == 1
	assert hound.health == 1
	assert not hound.taunt
	houndmaster.play(target=hound)
	assert hound.atk == 3
	assert hound.health == 3
	assert hound.taunt


def test_holy_wrath():
	game = prepare_empty_game()
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire.shuffle_into_deck()
	assert goldshire in game.player1.deck
	assert goldshire.cost == 1
	assert game.player2.hero.health == 30
	game.player1.give("EX1_365").play(target=game.player2.hero)
	assert goldshire not in game.player1.deck
	assert game.player2.hero.health == 30 - 1
	game.player1.give("EX1_365").play(target=game.player2.hero)
	assert game.player2.hero.health == 30 - 1
	game.end_turn(); game.end_turn()


def test_holy_wrath_full_hand():
	game = prepare_empty_game()
	game.player1.give(GOLDSHIRE_FOOTMAN).shuffle_into_deck()
	game.player1.give(GOLDSHIRE_FOOTMAN).shuffle_into_deck()
	holywrath = game.player1.give("EX1_365")
	for i in range(9):
		game.player1.give(WISP)
	game.player1.temp_mana += 1
	holywrath.play(target=game.player2.hero)
	assert game.player2.hero.health == 30 - 1
	assert len(game.player1.hand) == 10


def test_humility():
	game = prepare_game()
	humility = game.current_player.give("EX1_360")
	humility2 = game.current_player.give("EX1_360")
	seargent = game.current_player.give("CS2_188")
	seargent2 = game.current_player.give("CS2_188")
	golem = game.current_player.summon("CS2_186")
	game.end_turn(); game.end_turn()

	assert golem.atk == 7
	humility.play(target=golem)
	assert golem.atk == 1
	seargent.play(target=golem)
	assert golem.atk == 3
	game.end_turn()
	assert golem.atk == 1
	game.end_turn()

	seargent2.play(target=golem)
	assert golem.atk == 3
	humility2.play(target=golem)
	assert golem.atk == 1
	game.end_turn()
	assert golem.atk == 1


def test_hunters_mark():
	game = prepare_game()
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	game.player1.give(MOONFIRE).play(target=statue)
	assert statue.health == 10 - 1
	mark = game.player1.give("CS2_084")
	mark.play(target=statue)
	assert statue.health == statue.max_health == 1
	assert not statue.dead
	game.player1.give(SILENCE).play(target=statue)
	assert statue.health == 10


def test_i_am_murloc():
	game = prepare_game()
	iammurloc = game.player1.give("PRO_001a")
	iammurloc.play()
	assert len(game.player1.field) in (3, 4, 5)
	assert game.player1.field[0].id == "PRO_001at"


def test_illidan():
	game = prepare_game()
	illidan = game.current_player.give("EX1_614")
	assert len(game.board) == 0
	illidan.play()
	assert len(game.board) == 1
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 2
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 3
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 4
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 5

	# 5th moonfire kills illidan, but spawns another token before
	game.current_player.give(MOONFIRE).play(target=illidan)
	assert len(game.board) == 5
	assert illidan.dead


def test_illidan_knife_juggler():
	game = prepare_game()
	illidan = game.player1.give("EX1_614")
	illidan.play()
	juggler = game.player1.give("NEW1_019")
	juggler.play()
	assert len(game.player1.field) == 3
	assert game.player2.hero.health == 30 - 1


def test_illidan_full_board():
	game = prepare_game()
	illidan = game.player1.give("EX1_614")
	illidan.play()
	game.player1.give(THE_COIN).play()
	game.player1.give(THE_COIN).play()
	game.player1.give(THE_COIN).play()
	game.player1.give(THE_COIN).play()
	game.player1.give(THE_COIN).play()
	assert len(game.player1.field) == 6
	juggler = game.player1.give("NEW1_019")
	juggler.play()
	assert len(game.player1.field) == 7
	assert game.player2.hero.health == 30


def test_injured_blademaster():
	game = prepare_game()
	frothing = game.player1.give("EX1_604")
	frothing.play()
	assert not frothing.buffs
	assert frothing.atk == 2
	blademaster = game.player1.give("CS2_181")
	blademaster.play()
	assert frothing.buffs
	assert frothing.atk == 2 + 1
	assert blademaster.health == blademaster.max_health - 4


def test_inner_fire():
	game = prepare_game()
	gurubashi = game.player1.give("EX1_399")
	gurubashi.play()
	assert gurubashi.atk == 2

	seargent = game.player1.give("CS2_188")
	seargent.play(target=gurubashi)
	assert gurubashi.atk == 4

	innerfire = game.player1.give("CS1_129")
	innerfire.play(target=gurubashi)
	assert gurubashi.atk == 7
	game.end_turn()

	assert gurubashi.atk == 7
	equality = game.player2.give("EX1_619")
	equality.play()
	assert gurubashi.health == 1
	assert gurubashi.atk == 7


def test_innervate():
	game = prepare_game()
	assert game.player1.mana == 10
	assert game.player1.temp_mana == 0
	assert game.player1.max_mana == 10
	assert game.player1.max_resources == 10
	game.player1.give("EX1_169").play()
	assert game.player1.mana == 10
	assert game.player1.temp_mana == 0
	game.player1.give(GOLDSHIRE_FOOTMAN).play()
	assert game.player1.mana == 9
	game.player1.give("EX1_169").play()
	assert game.player1.mana == 10
	assert game.player1.temp_mana == 1
	game.player1.give(GOLDSHIRE_FOOTMAN).play()
	assert game.player1.mana == 9
	assert game.player1.temp_mana == 0


def test_ice_lance():
	game = prepare_game()
	lance1 = game.player1.give("CS2_031")
	assert game.player2.hero.health == 30
	assert not game.player2.hero.frozen
	lance1.play(target=game.player2.hero)
	assert game.player2.hero.health == 30
	assert game.player2.hero.frozen
	lance2 = game.player1.give("CS2_031")
	lance2.play(target=game.player2.hero)
	assert game.player2.hero.health == 26
	assert game.player2.hero.frozen
	game.end_turn()

	game.player2.give(LIGHTS_JUSTICE).play()
	assert game.player2.hero.frozen
	assert not game.player2.hero.can_attack()
	game.end_turn()

	assert not game.player2.hero.frozen


def test_imp_master():
	game = prepare_game()
	impmaster = game.player1.give("EX1_597")
	impmaster.play()
	assert impmaster.health == 5
	assert len(impmaster.controller.field) == 1
	game.end_turn()

	assert impmaster.health == 4
	assert len(impmaster.controller.field) == 2
	assert impmaster.controller.field.contains("EX1_598")


def test_kill_command():
	game = prepare_game()
	kc = game.player1.give("EX1_539")
	assert not kc.powered_up
	kc.play(target=game.player1.opponent.hero)
	assert game.player2.hero.health == 30 - 3

	game.player1.give(CHICKEN).play()
	kc = game.player1.give("EX1_539")
	assert kc.powered_up
	kc.play(target=game.player1.hero)
	assert game.player1.hero.health == 30 - 5


def test_king_mukla():
	game = prepare_game()
	mukla = game.player1.give("EX1_014")
	game.player2.discard_hand()
	assert len(game.player2.hand) == 0
	mukla.play()
	assert len(game.player2.hand) == 2
	for i in range(2):
		assert game.player2.hand[i].id == "EX1_014t"
	game.end_turn()
	wisp = game.player2.give(WISP)
	wisp.play()
	assert wisp.health == 1
	assert wisp.atk == 1
	assert game.player2.hand[0].id == "EX1_014t"
	game.player2.hand[0].play(target=wisp)
	assert wisp.health == 2
	assert wisp.atk == 2


def test_kirin_tor_mage():
	game = prepare_game()
	counterspell = game.player1.give("EX1_287")
	assert counterspell.cost == 3
	vaporize = game.player1.give("EX1_594")
	assert vaporize.cost == 3
	missiles = game.player1.give("EX1_277")
	assert missiles.cost == 1

	game.player1.give("EX1_612").play()
	assert counterspell.cost == 0
	assert vaporize.cost == 0
	assert missiles.cost == 1
	counterspell.play()
	assert vaporize.cost == 3
	game.player1.give("EX1_612").play()
	assert vaporize.cost == 0
	game.end_turn(); game.end_turn()

	assert vaporize.cost == 3


def test_knife_juggler():
	game = prepare_game()
	juggler = game.player1.give("NEW1_019")
	juggler.play()
	assert game.player2.hero.health == 30
	game.player1.give(WISP).play()
	assert game.player2.hero.health == 29
	game.player1.give(MOONFIRE).play(target=juggler)
	# kill juggler with archer, shouldnt juggle
	archer = game.current_player.give("CS2_189")
	archer.play(target=juggler)
	assert juggler.dead
	assert game.player2.hero.health == 29


def test_knife_juggler_swipe():
	"""
	Test that a Swipe on Knife Juggler that kills a Haunted Creeper
	does not trigger the Knife Juggler by the time the spiders spawn
	"""
	game = prepare_game()
	creeper = game.player2.summon("FP1_002")
	juggler = game.player2.summon("NEW1_019")
	game.current_player.give(MOONFIRE).play(target=creeper)
	swipe = game.player1.give("CS2_012")
	swipe.play(target=juggler)
	assert juggler.dead
	assert creeper.dead
	assert len(game.player2.field) == 2
	assert game.player1.hero.health == 30


def test_leeroy():
	game = prepare_game()
	leeroy = game.player1.give("EX1_116")
	leeroy.play()
	assert leeroy.can_attack()
	assert len(game.player2.field) == 2
	assert game.player2.field[0].id == game.player2.field[1].id == "EX1_116t"


def test_lightspawn():
	game = prepare_game()
	lightspawn = game.player1.give("EX1_335")
	lightspawn.play()
	assert lightspawn.health == 5
	assert lightspawn.atk == 5

	# moonfire the lightspawn, goes to 4 health
	game.player1.give(MOONFIRE).play(target=lightspawn)
	assert lightspawn.health == 4
	assert lightspawn.atk == 4
	assert not lightspawn.buffs

	flametongue = game.player1.give("EX1_565")
	flametongue.play()
	assert lightspawn.health == 4
	assert lightspawn.buffs
	assert lightspawn.atk == 4

	game.player1.give(SILENCE).play(target=lightspawn)
	assert lightspawn.buffs
	# 2 attack from the flametongue
	assert lightspawn.atk == 2


def test_lightwarden():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)
	lightwarden = game.player1.give("EX1_001")
	lightwarden.play()
	assert lightwarden.atk == 1
	# No-op heal should not do anything.
	game.player1.hero.power.use(target=game.player1.hero)
	assert lightwarden.atk == 1
	game.end_turn()

	game.player2.give(MOONFIRE).play(target=game.player2.hero)
	game.player2.hero.power.use(target=game.player2.hero)
	assert lightwarden.atk == 3


def test_lightwell():
	game = prepare_game()
	lightwell = game.player1.give("EX1_341")
	lightwell.play()
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert game.player1.hero.health == 29
	assert game.player2.hero.health == 29
	game.end_turn()

	assert game.player1.hero.health == 29
	assert game.player2.hero.health == 29
	game.end_turn()

	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 29


def test_lorewalker_cho():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	cho = game.player1.give("EX1_100")
	cho.play()
	assert len(game.player1.hand) == len(game.player2.hand) == 0
	coin1 = game.player1.give(THE_COIN)
	coin1.play()
	assert len(game.player1.hand) == 0
	assert len(game.player2.hand) == 1
	assert game.player2.hand[0].id == THE_COIN
	assert game.player2.hand[0] is not coin1
	game.end_turn()

	coin2 = game.player2.hand[0]
	coin2.play()
	assert len(game.player2.hand) == 1
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0] is not coin1
	assert game.player1.hand[0] is not coin2
	assert game.player1.hand[0].id == THE_COIN


def test_mad_bomber():
	game = prepare_game()
	statue1 = game.player1.summon(ANIMATED_STATUE)
	statue2 = game.player1.summon(ANIMATED_STATUE)
	bomber = game.player1.give("EX1_082")
	bomber.play()
	assert bomber.damage == 0
	assert (
		statue1.damage +
		statue2.damage +
		game.player1.hero.damage +
		game.player2.hero.damage
	) == 3


def test_mark_of_nature():
	game = prepare_game()
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	assert wisp1.atk == 1
	assert wisp1.health == 1
	assert not wisp1.taunt

	mark1 = game.current_player.give("EX1_155")
	mark1.play(target=wisp1, choose="EX1_155a")
	assert wisp1.atk == 1 + 4
	assert wisp1.health == 1
	assert not wisp1.taunt

	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	assert wisp2.atk == 1
	assert wisp2.health == 1
	assert not wisp2.taunt

	mark2 = game.current_player.give("EX1_155")
	mark2.play(target=wisp2, choose="EX1_155b")
	assert wisp2.atk == 1
	assert wisp2.health == 1 + 4
	assert wisp2.taunt


def test_mana_addict():
	game = prepare_game()
	addict = game.player1.give("EX1_055")
	addict.play()
	assert addict.atk == 1
	game.end_turn()

	assert addict.atk == 1
	game.player2.give(THE_COIN).play()
	assert addict.atk == 1
	game.end_turn()

	game.player1.give(THE_COIN).play()
	assert addict.atk == 3
	game.player1.give(THE_COIN).play()
	assert addict.atk == 5
	game.end_turn()

	assert addict.atk == 1


def test_mana_wyrm():
	game = prepare_game()
	wyrm = game.player1.give("NEW1_012")
	wyrm.play()
	assert wyrm.atk == 1
	game.player1.give(THE_COIN).play()
	assert wyrm.atk == 2
	game.end_turn()

	assert wyrm.atk == 2
	game.player2.give(THE_COIN).play()
	assert wyrm.atk == 2
	game.end_turn()

	assert wyrm.atk == 2
	game.player1.give(THE_COIN).play()
	assert wyrm.atk == 3


def test_master_of_disguise():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	mod = game.player1.give("NEW1_014")
	mod.play(target=wisp)
	assert wisp.stealthed
	game.end_turn()

	assert wisp.stealthed
	game.end_turn()

	assert not wisp.stealthed


def test_mana_wraith():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	goldshire1 = game.player1.give(GOLDSHIRE_FOOTMAN)
	wisp2 = game.player2.give(WISP)
	goldshire2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	fireball1 = game.player1.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	weapon1 = game.player1.give(LIGHTS_JUSTICE)
	weapon2 = game.player2.give(LIGHTS_JUSTICE)
	assert wisp1.cost == wisp2.cost == 0
	assert goldshire1.cost == goldshire2.cost == 1
	assert fireball1.cost == fireball2.cost == 4
	assert weapon1.cost == weapon2.cost == 1
	assert game.player1.hero.power.cost == game.player2.hero.power.cost == 2

	wraith = game.current_player.give("EX1_616")
	wraith.play()
	assert wisp1.cost == wisp2.cost == 0 + 1
	assert goldshire1.cost == goldshire2.cost == 1 + 1
	assert fireball1.cost == fireball2.cost == 4
	assert weapon1.cost == weapon2.cost == 1
	assert game.player1.hero.power.cost == game.player2.hero.power.cost == 2

	wraith.destroy()
	assert wisp1.cost == wisp2.cost == 0
	assert goldshire1.cost == goldshire2.cost == 1
	assert fireball1.cost == fireball2.cost == 4
	assert weapon1.cost == weapon2.cost == 1
	assert game.player1.hero.power.cost == game.player2.hero.power.cost == 2


def test_millhouse_manastorm():
	game = prepare_game()
	millhouse = game.player1.give("NEW1_029")
	fireballp1 = game.player1.give("CS2_029")
	fireball1 = game.player2.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	moonfire = game.player2.give(MOONFIRE)

	assert fireball1.cost == fireball2.cost == fireballp1.cost == 4
	assert moonfire.cost == 0
	assert fireballp1.cost == 4
	millhouse.play()
	# costs change as soon as millhouse is played
	assert game.player2.hero.buffs
	assert fireball1.cost == fireball2.cost == moonfire.cost == 0
	assert fireballp1.cost == 4
	game.end_turn()

	assert fireball1.cost == fireball2.cost == moonfire.cost == 0
	assert fireballp1.cost == 4
	game.end_turn()

	assert fireball1.cost == fireball2.cost == fireballp1.cost == 4
	assert moonfire.cost == 0


def test_mind_control():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	assert wisp.controller is game.player1
	assert wisp.zone == Zone.PLAY
	assert not wisp.asleep
	mc = game.player2.give("CS1_113")
	mc.play(target=wisp)
	assert wisp.controller is game.player2
	assert wisp.zone == Zone.PLAY
	assert wisp.asleep


def test_mind_control_tech():
	game = prepare_game()
	for i in range(4):
		game.player1.give(WISP).play()
	game.end_turn()

	# test normal steal
	assert len(game.player1.field) == 4
	assert len(game.player2.field) == 0
	mct = game.player2.give("EX1_085")
	mct.play()
	assert len(game.player1.field) == 3
	assert len(game.player2.field) == 2

	# ensure no steal with 3 minions or less
	game.player2.give("EX1_085").play()
	assert len(game.player1.field) == 3
	assert len(game.player2.field) == 3


def test_mindgames():
	game = prepare_empty_game()
	wisp = game.player2.give(WISP)
	wisp.shuffle_into_deck()
	mindgames = game.player1.give("EX1_345")
	mindgames.play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == WISP
	assert wisp in game.player2.deck
	game.end_turn()

	mindgames2 = game.player2.give("EX1_345")
	mindgames2.play()
	assert len(game.player2.field) == 1
	assert game.player2.field[0].id == "EX1_345t"


def test_mind_vision():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()

	# play mind vision, should give nothing
	assert len(game.player1.hand) == 0
	game.player1.give("CS2_003").play()
	assert len(game.player1.hand) == 0

	# opponent draws a card, mind vision should get that one card
	assert len(game.player1.hand) == len(game.player2.hand) == 0
	card = game.player2.draw()
	assert len(game.player1.hand) == 0
	assert len(game.player2.hand) == 1
	mind_vision = game.player1.give("CS2_003")
	mind_vision.play()
	copied = game.player1.hand[-1]
	assert copied == card
	assert copied.creator is mind_vision


def test_mirror_image():
	game = prepare_game()
	mirror = game.player1.give("CS2_027")
	mirror.play()
	assert len(game.player1.field) == 2
	assert game.player1.field[0].id == game.player1.field[1].id == "CS2_mirror"


def test_molten_giant():
	game = prepare_game()
	molten = game.current_player.give("EX1_620")
	assert molten.cost == 25
	game.current_player.give(MOONFIRE).play(target=game.player1.hero)
	assert molten.cost == 25 - 1
	game.current_player.give(MOONFIRE).play(target=game.player1.hero)
	assert molten.cost == 25 - 2
	game.current_player.give(MOONFIRE).play(target=game.player1.hero)
	assert molten.cost == 25 - 3
	game.end_turn()

	assert molten.cost == 25 - 3
	molten2 = game.player2.give("EX1_620")
	assert molten2.cost == 25


def test_mortal_coil():
	game = prepare_game()
	dummy = game.player1.summon(TARGET_DUMMY)
	assert dummy.health == 2
	game.end_turn()
	game.player2.discard_hand()
	assert len(game.player2.hand) == 0
	coil1 = game.player2.give("EX1_302")
	assert len(game.player2.hand) == 1
	coil1.play(target=dummy)
	assert len(game.player2.hand) == 0
	coil2 = game.player2.give("EX1_302")
	coil2.play(target=dummy)
	assert len(game.player2.hand) == 1


def test_mortal_strike():
	game = prepare_game()
	game.player1.discard_hand()
	expected_health = 30
	for i in range(5):
		ms = game.player1.give("EX1_408")
		assert not ms.powered_up
		ms.play(target=game.player1.hero)
		expected_health -= 4
		assert game.player1.hero.health == expected_health
		if i % 2:
			game.end_turn(); game.end_turn()

	ms = game.player1.give("EX1_408")
	assert ms.powered_up
	ms.play(target=game.player1.hero)
	expected_health -= 6
	assert game.player1.hero.health == expected_health


def test_mountain_giant():
	game = prepare_game()
	mountain = game.current_player.give("EX1_105")
	assert mountain.cost == 12 - len(game.current_player.hand) + 1
	game.end_turn(); game.end_turn()

	assert mountain.cost == 12 - len(game.current_player.hand) + 1
	game.end_turn(); game.end_turn()

	assert mountain.cost == 12 - len(game.current_player.hand) + 1


def test_murloc_tidecaller():
	game = prepare_game()
	tidecaller = game.player1.give("EX1_509")
	tidecaller.play()
	assert tidecaller.atk == 1
	game.end_turn()

	game.player2.give(MURLOC).play()
	assert tidecaller.atk == 1 + 1
	game.end_turn()

	# Play a tidehunter. Summons two murlocs.
	game.player1.give("EX1_506").play()
	assert tidecaller.atk == 1 + 1 + 2


def test_northshire_cleric():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)
	game.player1.discard_hand()
	game.player2.discard_hand()
	cleric = game.player1.give("CS2_235")
	cleric.play()
	game.player1.hero.power.use(target=game.current_player.hero)
	assert not game.player1.hand

	pyromancer = game.player1.give("NEW1_020")
	pyromancer.play()
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert not game.player1.hand

	game.player2.summon(ANIMATED_STATUE)
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert len(game.player1.hand) == 2

	game.player1.give(CIRCLE_OF_HEALING).play()
	assert len(game.player1.hand) == 5
	assert not game.player2.hand


def test_old_murkeye():
	game = prepare_game()
	murkeye = game.player1.give("EX1_062")
	assert murkeye.atk == 2
	murloc = game.player1.give(MURLOC)
	murloc.play()
	assert murkeye.atk == 2
	murkeye.play()
	assert murkeye.charge
	assert murkeye.can_attack()
	assert murkeye.atk == 2 + 1
	game.player2.summon("CS2_168")
	assert murkeye.atk == 2 + 2
	game.player2.summon("CS2_168")
	assert murkeye.atk == 2 + 3
	murloc.destroy()
	assert murkeye.atk == 2 + 2
	murkeye2 = game.player2.summon("EX1_062")
	assert murkeye.atk == murkeye2.atk == 2 + 3


def test_onyxia():
	game = prepare_game()
	onyxia = game.player1.give("EX1_562")
	assert len(game.player1.field) == 0
	onyxia.play()
	assert len(game.player1.field) == 7
	assert game.player1.field == ["ds1_whelptoken"] * 3 + ["EX1_562"] + ["ds1_whelptoken"] * 3


def test_pint_sized_summoner():
	game = prepare_game()
	goldshire1 = game.current_player.give(GOLDSHIRE_FOOTMAN)
	goldshire2 = game.current_player.give(GOLDSHIRE_FOOTMAN)
	moonfire = game.current_player.give(MOONFIRE)
	frostwolf = game.current_player.give("CS2_121")
	wisp = game.current_player.give(WISP)
	assert goldshire1.cost == 1
	assert goldshire2.cost == 1
	assert frostwolf.cost == 2
	assert wisp.cost == 0

	# summon it directly, minions played still at 0
	summoner = game.current_player.summon("EX1_076")
	assert game.current_player.minions_played_this_turn == 0
	assert goldshire1.cost == 1 - 1
	assert goldshire2.cost == 1 - 1
	assert not moonfire.buffs
	assert moonfire.cost == 0
	assert frostwolf.cost == 2 - 1
	assert wisp.cost == 0

	goldshire1.play()
	assert game.current_player.minions_played_this_turn == 1
	assert goldshire2.cost == 1
	assert frostwolf.cost == 2
	assert wisp.cost == 0
	game.end_turn()

	assert game.current_player.minions_played_this_turn == 0
	assert goldshire1.cost == 1
	assert goldshire2.cost == 1
	assert frostwolf.cost == 2
	assert wisp.cost == 0

	game.end_turn()
	summoner2 = game.current_player.summon("EX1_076")
	assert frostwolf.cost == 2 - 2
	summoner.destroy()
	assert frostwolf.cost == 2 - 1
	summoner2.destroy()
	assert frostwolf.cost == 2


def test_power_overwhelming():
	game = prepare_game()
	power = game.player1.give("EX1_316")
	wisp = game.player1.give(WISP)
	wisp.play()
	power.play(target=wisp)
	assert wisp.atk == wisp.health == 1 + 4
	game.end_turn()

	assert wisp not in game.board


def test_power_of_the_wild():
	game = prepare_game()
	assert len(game.player1.field) == 0
	game.player1.give("EX1_160").play(choose="EX1_160a")
	assert len(game.player1.field) == 1
	token = game.player1.field[0]
	assert token.id == "EX1_160t"
	teacher = game.player1.give("NEW1_026")
	teacher.play()
	assert token.atk == 3 and token.health == 2
	assert teacher.atk == 3 and teacher.health == 5
	game.player1.give("EX1_160").play(choose="EX1_160b")
	assert len(game.player1.field) == 3
	assert token.atk == 4 and token.health == 3
	assert teacher.atk == 4 and teacher.health == 6
	apprentice = game.player1.field[2]
	assert apprentice.id == "NEW1_026t"
	assert apprentice.atk == 1 + 1 and apprentice.health == 1 + 1


def test_power_word_shield():
	game = prepare_game()
	game.player1.discard_hand()
	wisp = game.player1.give(WISP)
	wisp.play()
	pwshield = game.player1.give("CS2_004")
	pwshield.play(target=wisp)
	assert wisp.health == 3
	assert len(game.player1.hand) == 1
	game.player1.give(SILENCE).play(target=wisp)
	assert wisp.health == 1


def test_preparation():
	game = prepare_game()
	game.player1.discard_hand()
	prep1 = game.player1.give("EX1_145")
	prep2 = game.player1.give("EX1_145")
	prep3 = game.player1.give("EX1_145")
	pwshield = game.player1.give("CS2_004")
	fireball = game.player1.give("CS2_029")
	fireball2 = game.player2.give("CS2_029")
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	footman2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	assert prep1.cost == prep2.cost == prep3.cost == 0
	assert pwshield.cost == 1
	assert fireball.cost == fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	game.end_turn(); game.end_turn()

	assert game.player1.used_mana == 0
	prep1.play()
	assert game.player1.used_mana == 0
	assert prep2.cost == prep3.cost == 0
	assert pwshield.cost == 0
	assert fireball.cost == 4 - 3
	assert fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	prep2.play()
	assert game.player1.used_mana == 0
	assert prep2.cost == prep3.cost == 0
	assert pwshield.cost == 0
	assert fireball.cost == 4 - 3
	assert fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	fireball.play(target=game.player2.hero)
	assert game.player1.used_mana == 1
	assert pwshield.cost == 1
	assert fireball2.cost == 4
	assert footman.cost == footman2.cost == 1
	prep3.play()
	assert pwshield.cost == 0
	assert footman.cost == footman2.cost == 1
	game.end_turn()
	assert pwshield.cost == 1
	assert footman.cost == footman2.cost == 1


def test_prophet_velen():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)

	expected_health = 30
	assert game.player2.hero.health == expected_health
	assert game.player1.healing_double == 0
	assert game.player1.hero_power_double == 0
	assert game.player1.spellpower_double == 0
	velen = game.player1.give("EX1_350")
	velen.play()
	assert game.player1.healing_double == 1
	assert game.player1.hero_power_double == 1
	assert game.player1.spellpower_double == 1

	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 2 * 1
	assert game.player2.hero.health == expected_health

	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 2 * 1
	assert game.player2.hero.health == expected_health

	game.player1.hero.power.use(target=game.player2.hero)
	expected_health += 2 * 2
	assert game.player2.hero.health == expected_health
	game.end_turn(); game.end_turn()

	kobold = game.current_player.give(KOBOLD_GEOMANCER)
	kobold.play()
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 2 * (1 + 1)
	assert game.player2.hero.health == expected_health


def test_prophet_velen_multiple():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)

	expected_health = 30
	assert game.player2.hero.health == expected_health
	assert game.player1.healing_double == 0
	assert game.player1.hero_power_double == 0
	assert game.player1.spellpower_double == 0
	velen1 = game.player1.give("EX1_350")
	velen1.play()
	game.end_turn(); game.end_turn()
	velen2 = game.player1.give("EX1_350")
	velen2.play()
	assert game.player1.healing_double == 2
	assert game.player1.hero_power_double == 2
	assert game.player1.spellpower_double == 2

	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 4 * 1
	assert game.player2.hero.health == expected_health

	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 4 * 1
	assert game.player2.hero.health == expected_health

	game.player1.hero.power.use(target=game.player2.hero)
	expected_health += 4 * 2
	assert game.player2.hero.health == expected_health
	game.end_turn(); game.end_turn()

	kobold = game.current_player.give(KOBOLD_GEOMANCER)
	kobold.play()
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 4 * (1 + 1)
	assert game.player2.hero.health == expected_health


def test_questing_adventurer():
	game = prepare_game()
	adventurer = game.player1.give("EX1_044")
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	adventurer.play()
	assert adventurer.atk == 2
	assert adventurer.health == 2
	game.player1.give(THE_COIN).play()
	assert adventurer.atk == 3
	assert adventurer.health == 3
	for i in range(1, 5):
		game.player1.give(THE_COIN).play()
		assert adventurer.atk == adventurer.health == 3 + i


def test_questing_adventurer_big_game_hunter():
	game = prepare_game()
	adventurer = game.player1.give("EX1_044")
	adventurer.play()
	mightblessing = game.player1.give("CS2_087")
	mightblessing.play(target=adventurer)
	assert adventurer.atk == 6
	bgh = game.player1.give("EX1_005")
	bgh.play()
	assert len(game.player1.field) == 2
	assert adventurer.atk == 7


def test_questing_adventurer_shadow_word_pain():
	game = prepare_game()
	adventurer = game.player1.summon("EX1_044")
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	pain = game.player1.give("CS2_234")
	assert adventurer.atk == 3
	assert adventurer in pain.targets
	pain.play(target=adventurer)
	assert adventurer.dead


def test_raid_leader():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	wisp3 = game.player2.summon(WISP)
	raidleader = game.player1.summon("CS2_122")
	assert wisp1.atk == wisp2.atk == 2
	assert wisp3.atk == 1

	raidleader.destroy()

	assert wisp1.atk == wisp2.atk == 1


def test_raging_worgen():
	game = prepare_game()
	worgen = game.player1.give("EX1_412")
	worgen.play()
	assert worgen.health == 3
	game.player1.give(MOONFIRE).play(target=worgen)
	assert worgen.health == 2
	assert worgen.atk == 4
	assert worgen.windfury
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert worgen.atk == 3
	assert not worgen.windfury


def test_ragnaros():
	game = prepare_game()
	ragnaros = game.player1.give("EX1_298")
	ragnaros.play()
	assert not ragnaros.can_attack()
	game.end_turn()

	assert game.player2.hero.health == 22
	game.end_turn()

	assert game.player2.hero.health == 22
	assert not ragnaros.can_attack()


def test_savage_roar():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	game.end_turn()
	wisp2 = game.player2.give(WISP)
	wisp2.play()
	game.end_turn()

	assert wisp1.atk == 1
	assert wisp2.atk == 1
	assert game.player1.hero.atk == 0
	assert game.player2.hero.atk == 0
	game.player1.give("CS2_011").play()
	assert wisp1.atk == 1 + 2
	assert wisp2.atk == 1
	assert game.player1.hero.atk == 2
	assert game.player2.hero.atk == 0
	game.end_turn()
	assert wisp1.atk == 1
	assert wisp2.atk == 1
	assert game.player1.hero.atk == 0
	assert game.player2.hero.atk == 0


def test_savagery():
	game = prepare_game(CardClass.DRUID, CardClass.DRUID)
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	assert statue.health == 10
	savagery1 = game.player1.give("EX1_578")
	savagery1.play(statue)
	assert statue.health == 10

	game.player1.give(HAND_OF_PROTECTION).play(target=statue)
	savagery2 = game.player1.give("EX1_578")
	savagery2.play(statue)
	assert statue.divine_shield
	game.player1.give(MOONFIRE).play(target=statue)
	assert not statue.divine_shield

	game.player1.hero.power.use()
	savagery3 = game.player1.give("EX1_578")
	savagery3.play(statue)
	assert statue.damage == 1
	game.end_turn(); game.end_turn()

	game.player1.give(KOBOLD_GEOMANCER).play()
	savagery4 = game.player1.give("EX1_578")
	savagery4.play(statue)
	assert statue.damage == 1 + 1


def test_sea_giant():
	game = prepare_game()
	seagiant = game.current_player.give("EX1_586")
	assert seagiant.cost == 10
	game.current_player.give(WISP).play()
	assert seagiant.cost == 9
	game.current_player.give(WISP).play()
	assert seagiant.cost == 8
	for i in range(5):
		game.player1.give(WISP).play()
	assert seagiant.cost == 3
	game.end_turn()

	for i in range(7):
		game.player2.give(WISP).play()
	assert seagiant.cost == 0


def test_sense_demons():
	game = prepare_empty_game()
	game.player1.discard_hand()
	demon1 = game.player1.give(IMP)
	demon1.shuffle_into_deck()
	demon2 = game.player1.give("CS2_065")
	demon2.shuffle_into_deck()
	wisp = game.player1.give(WISP)
	wisp.shuffle_into_deck()
	assert len(game.player1.deck) == 3
	assert len(game.player1.hand) == 0
	sense1 = game.player1.give("EX1_317")
	sense1.play()
	assert len(game.player1.deck) == 1
	assert len(game.player1.hand) == 2
	assert game.player1.hand.contains(demon1)
	assert game.player1.hand.contains(demon2)

	game.player1.discard_hand()
	assert len(game.player1.deck) == 1
	assert len(game.player1.hand) == 0
	sense2 = game.player1.give("EX1_317")
	sense2.play()
	assert len(game.player1.deck) == 1
	assert len(game.player1.hand) == 2
	assert game.player1.hand[0].id == game.player1.hand[1].id == "EX1_317t"


def test_shadow_madness_attacked_last_turn():
	"""
	Test that shadow madnessing a minion that was just played by the opponent
	lets it attack
	"""
	game = prepare_game()

	wisp = game.player1.give(WISP).play()
	game.end_turn()
	assert wisp.controller is game.player1

	shadowmadness = game.player2.give("EX1_334")
	shadowmadness.play(target=wisp)
	assert wisp.controller is game.player2
	assert wisp.can_attack()
	wisp.attack(game.player1.hero)
	game.end_turn()

	# make sure it can attack when control returns
	assert wisp.controller is game.player1
	assert wisp.can_attack()


def test_shadow_madness_bounce():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	game.player2.discard_hand()
	shadowmadness = game.player2.give("EX1_334")
	assert wisp.controller is game.player1
	shadowmadness.play(target=wisp)
	assert wisp.controller is game.player2
	game.player2.give(TIME_REWINDER).play(target=wisp)
	assert wisp in game.player2.hand
	assert wisp.controller is game.player2
	game.end_turn()

	assert wisp in game.player2.hand
	assert wisp.controller is game.player2
	game.end_turn()

	assert wisp in game.player2.hand
	assert wisp.controller is game.player2
	game.end_turn()

	assert wisp in game.player2.hand
	assert wisp.controller is game.player2


def test_shadow_madness_just_played():
	"""
	test that shadow madnessing a minion that attacked on the opponent's previous
	turn lets it attack
	"""
	game = prepare_game()

	wisp = game.player1.give(WISP).play()
	game.end_turn(); game.end_turn()
	assert wisp.controller is game.player1
	assert wisp.can_attack()
	wisp.attack(game.player2.hero)
	game.end_turn()

	shadowmadness = game.player2.give("EX1_334")
	shadowmadness.play(target=wisp)
	assert wisp.controller is game.player2
	assert wisp.can_attack()
	wisp.attack(game.player1.hero)
	game.end_turn()

	# make sure it can attack when the player regains control
	assert wisp.controller is game.player1
	assert wisp.can_attack()


def test_shadow_madness_silence():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	assert wisp.controller == game.player1
	shadowmadness = game.player2.give("EX1_334")
	shadowmadness.play(target=wisp)
	assert wisp.controller == game.player2
	game.player2.give(SILENCE).play(target=wisp)
	assert wisp.controller == game.player1
	game.end_turn()

	assert wisp.controller == game.player1


def test_shadow_madness_wild_pyro():
	game = prepare_game()
	pyromancer = game.player1.give("NEW1_020")
	pyromancer.play()
	game.end_turn()

	assert pyromancer.controller == game.player1
	assert pyromancer in game.player1.field
	assert pyromancer.health == 2
	shadowmadness = game.player2.give("EX1_334")
	shadowmadness.play(target=pyromancer)
	assert pyromancer.controller == game.player2
	assert pyromancer in game.player2.field
	assert pyromancer.health == 1
	game.end_turn()

	assert pyromancer.controller == game.player1
	assert pyromancer in game.player1.field


def test_shadow_word_pain():
	game = prepare_game()
	yeti = game.player1.summon("CS2_182")
	wisp1 = game.player1.summon(WISP)
	wisp2 = game.player1.summon(WISP)
	pain = game.player1.give("CS2_234")
	assert pain.targets == [wisp1, wisp2]
	pain.play(target=wisp1)
	assert wisp1.dead
	assert not wisp2.dead
	assert not yeti.dead


def test_shadowflame():
	game = prepare_game()
	dummy1 = game.player1.give(TARGET_DUMMY)
	dummy1.play()
	game.end_turn()
	goldshire = game.player2.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	dummy2 = game.player2.give(TARGET_DUMMY)
	dummy2.play()

	assert dummy1.health == 2
	assert goldshire.health == 2
	assert not dummy2.dead
	game.player2.give("EX1_303").play(target=dummy2)
	assert dummy1.health == 2
	assert goldshire.health == 2
	assert dummy2.dead
	game.player2.give("EX1_303").play(target=goldshire)
	assert dummy1.health == 1


def test_shadowform():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)
	# Hero Power should reset
	shadowform1 = game.player1.give("EX1_625")
	assert game.player1.hero.power.id == "CS1h_001"
	assert game.player1.hero.power.is_usable()
	game.player1.hero.power.use(target=game.player1.hero)
	assert not game.player1.hero.power.is_usable()
	assert not game.player1.shadowform
	assert shadowform1.is_playable()
	print(game.player1.slots)
	shadowform1.play()
	print(game.player1.slots)
	assert game.player1.shadowform
	assert game.player1.hero.power.id == "EX1_625t"
	assert game.player1.hero.power.is_usable()
	game.player1.hero.power.use(target=game.player2.hero)
	assert not game.player1.hero.power.is_usable()
	assert game.player2.hero.health == 28
	game.end_turn(); game.end_turn()

	shadowform2 = game.player1.give("EX1_625")
	shadowform2.play()
	assert game.player1.shadowform
	assert game.player1.hero.power.id == "EX1_625t2"
	assert game.player1.hero.power.is_usable()
	game.player1.hero.power.use(target=game.player2.hero)
	assert not game.player1.hero.power.is_usable()
	assert game.player2.hero.health == 25

	shadowform3 = game.player1.give("EX1_625")
	shadowform3.play()
	assert game.player1.shadowform
	assert game.player1.hero.power.id == "EX1_625t2"
	assert not game.player1.hero.power.is_usable()


def test_shadowstep():
	game = prepare_game()
	shadowstep = game.player1.give("EX1_144")
	deathwing = game.player1.summon("NEW1_030")
	assert deathwing.zone == Zone.PLAY
	assert deathwing.cost == 10
	shadowstep.play(target=deathwing)
	assert deathwing.zone == Zone.HAND
	assert deathwing in game.player1.hand
	assert deathwing.cost == 8


def test_shattered_sun_cleric():
	game = prepare_game()
	cleric = game.player1.give("EX1_019")
	assert not cleric.targets
	cleric.play()
	assert cleric.atk == 3
	assert cleric.health == 2
	game.end_turn(); game.end_turn()

	cleric2 = game.player1.give("EX1_019")
	assert cleric in cleric2.targets
	cleric2.play(target=cleric)
	assert cleric.atk == 3 + 1
	assert cleric.health == 2 + 1


def test_shield_slam():
	game = prepare_game(CardClass.WARRIOR, CardClass.WARRIOR)
	wisp = game.player2.summon(WISP)
	assert game.player1.hero.armor == 0
	shieldslam1 = game.player1.give("EX1_410")
	shieldslam1.play(target=wisp)
	assert not wisp.dead

	game.player1.give(HAND_OF_PROTECTION).play(target=wisp)
	assert wisp.divine_shield
	shieldslam2 = game.player1.give("EX1_410")
	shieldslam2.play(target=wisp)
	assert wisp.divine_shield

	geomancer = game.player1.summon(KOBOLD_GEOMANCER)
	shieldslam3 = game.player1.give("EX1_410")
	shieldslam3.play(target=wisp)
	assert not wisp.divine_shield
	geomancer.destroy()

	game.player1.hero.power.use()
	assert game.player1.hero.armor == 2
	shieldslam4 = game.player1.give("EX1_410")
	shieldslam4.play(target=wisp)
	assert wisp.dead


def test_si7_agent():
	game = prepare_game()
	agent = game.player1.give("EX1_134")
	agent2 = game.player1.give("EX1_134")
	assert not agent.requires_target()
	assert not agent2.requires_target()
	agent.play()
	assert agent2.requires_target()
	agent2.play(target=agent)
	assert agent.health == 3 - 2


def test_slam():
	game = prepare_game()
	wisp = game.player1.summon(WISP)
	mogushan = game.player1.summon("EX1_396")
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	game.player1.give("EX1_391").play(target=wisp)
	assert wisp.dead
	assert len(game.player1.hand) == 0
	game.player1.give("EX1_391").play(target=mogushan)
	assert not mogushan.dead
	assert len(game.player1.hand) == 1


def test_sorcerers_apprentice():
	game = prepare_game()
	apprentice1 = game.player1.give("EX1_608")
	fireball1 = game.player1.give("CS2_029")
	assert fireball1.cost == 4
	apprentice1.play()
	assert fireball1.cost == 3
	apprentice2 = game.player1.give("EX1_608")
	apprentice2.play()
	assert fireball1.cost == 2
	apprentice1.destroy()
	assert fireball1.cost == 3
	game.end_turn()

	fireball2 = game.player2.give("CS2_029")
	assert fireball2.cost == 4
	game.end_turn()

	assert fireball1.cost == 3


def test_southsea_deckhand():
	game = prepare_game(CardClass.ROGUE, CardClass.ROGUE)
	deckhand = game.player1.give("CS2_146")
	deckhand.play()
	assert not deckhand.charge
	# Play rogue hero power (gives a weapon)
	game.player1.hero.power.use()
	assert deckhand.charge
	game.player1.give(LIGHTS_JUSTICE).play()
	assert deckhand.charge
	game.player1.weapon.destroy()
	assert not deckhand.charge

	# play charge
	game.player1.give("CS2_103").play(target=deckhand)
	assert deckhand.charge
	game.end_turn(); game.end_turn()

	assert deckhand.charge
	game.player1.hero.power.use()
	assert deckhand.charge
	game.player1.weapon.destroy()
	# No longer have weapon, but still have the charge buff from earlier
	assert deckhand.charge


def test_spiteful_smith():
	game = prepare_game()
	smith = game.player1.give("CS2_221")
	smith.play()
	assert not game.player1.hero.atk
	weapon = game.player1.give(LIGHTS_JUSTICE)
	weapon.play()
	assert game.player1.hero.atk == weapon.atk == 1
	assert not game.player2.hero.atk
	game.player1.give(MOONFIRE).play(target=smith)
	assert smith.damaged
	assert smith.enraged
	assert weapon.atk == 1 + 2
	assert weapon.buffs
	assert game.player1.hero.atk == 1 + 2
	assert not game.player2.hero.atk
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert not smith.enraged
	assert game.player1.hero.atk == weapon.atk == 1
	assert not weapon.buffs
	game.player1.give(MOONFIRE).play(target=smith)
	assert smith.enraged
	assert weapon.atk == game.player1.hero.atk == 1 + 2


def test_stampeding_kodo():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	game.end_turn()

	kodo = game.player2.give("NEW1_041")
	kodo.play()
	assert wisp.dead
	assert not statue.dead
	kodo2 = game.player2.give("NEW1_041")
	kodo2.play()
	assert not statue.dead


def test_starfall_5_to_one():
	game = prepare_game()

	snapjaw = game.player1.give("CS2_119")
	snapjaw.play()
	assert snapjaw.health == 7
	starfall = game.player1.give("NEW1_007")
	starfall.play(choose="NEW1_007b", target=snapjaw)
	assert snapjaw.health == 2


def test_starving_buzzard():
	game = prepare_game()
	game.player1.discard_hand()
	buzzard = game.player1.give("CS2_237")
	buzzard.play()
	assert not game.player1.hand
	game.player1.give(CHICKEN).play()
	assert len(game.player1.hand) == 1
	game.player1.give("NEW1_031").play()  # Animal Companion
	assert len(game.player1.hand) == 2


def test_stormwind_champion():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	stormwind = game.player1.give("CS2_222")
	stormwind.play()
	assert wisp.atk == wisp.health == 1 + 1
	game.end_turn(); game.end_turn()

	# ensure bounce removes the buff
	game.player1.give(TIME_REWINDER).play(target=stormwind)
	assert stormwind not in game.player1.field
	assert wisp.atk == wisp.health == 1
	stormwind.play()
	assert wisp.atk == wisp.health == 1 + 1

	# destroy Stormwind Champion
	stormwind.destroy()
	assert wisp.atk == wisp.health == 1


def test_summoning_portal():
	game = prepare_game()
	game.player1.discard_hand()
	wisp = game.player1.give(WISP)
	assert wisp.cost == 0
	weapon = game.player1.give(LIGHTS_JUSTICE)
	assert weapon.cost == 1
	molten = game.player1.give("EX1_620")
	assert molten.cost == 25
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	assert goldshire.cost == 1
	frostwolf = game.player1.give("CS2_121")
	assert frostwolf.cost == 2

	portal = game.player1.give("EX1_315")
	portal.play()
	assert wisp.cost == 0
	assert weapon.cost == 1
	assert molten.cost == 25 - 2
	assert goldshire.cost == 1
	assert frostwolf.cost == 1
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert molten.cost == 25 - 3
	portal2 = game.player1.give("EX1_315")
	portal2.play()
	assert wisp.cost == 0
	assert molten.cost == 25 - 2 - 1 - 2
	assert goldshire.cost == 1
	assert frostwolf.cost == 1


def test_sunfury_protector():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	sunfury = game.player1.give("EX1_058")
	sunfury.play()
	assert not wisp1.taunt
	assert wisp2.taunt


def test_sword_of_justice():
	game = prepare_game(CardClass.PALADIN, CardClass.PALADIN)
	sword = game.player1.give("EX1_366")
	sword.play()
	assert sword.durability == 5
	wisp = game.player1.give(WISP)
	wisp.play()
	assert wisp.atk == 2
	assert wisp.health == 2
	assert wisp.buffs
	assert sword.durability == 4
	game.end_turn()

	game.player2.give(WISP).play()
	assert sword.durability == 4
	game.end_turn()

	game.player1.hero.power.use()
	assert sword.durability == 3

	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	assert not game.player1.weapon
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	assert wisp2.health == wisp2.atk == 1
	assert not wisp2.buffs


def test_sylvanas_windrunner():
	game = prepare_game()
	sylvanas1 = game.player1.give("EX1_016")
	sylvanas1.play()
	sylvanas1.destroy()
	assert len(game.player1.field) == 0
	game.end_turn(); game.end_turn()

	wisp = game.player2.summon(WISP)
	sylvanas2 = game.player1.give("EX1_016")
	sylvanas2.play()
	assert wisp in game.player2.field
	sylvanas2.destroy()
	assert wisp in game.player1.field


def test_the_black_knight():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	dummy1 = game.player1.give(TARGET_DUMMY)
	dummy1.play()
	game.end_turn()

	dummy2 = game.player2.give(TARGET_DUMMY)
	dummy2.play()
	blackknight = game.player2.give("EX1_002")
	assert blackknight.targets == [dummy1]
	blackknight.play(target=dummy1)
	assert dummy1.dead


def test_thoughtsteal():
	game = prepare_empty_game()

	assert len(game.player1.hand) == 0
	assert len(game.player2.deck) == 0
	game.player1.give("EX1_339").play()
	assert len(game.player1.hand) == 0

	game.player2.give(WISP).shuffle_into_deck()
	assert len(game.player2.deck) == 1
	game.player1.give("EX1_339").play()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == WISP
	game.player1.discard_hand()

	assert len(game.player1.hand) == 0
	game.player2.give(TARGET_DUMMY).shuffle_into_deck()
	assert len(game.player2.deck) == 2
	game.player1.give("EX1_339").play()
	assert len(game.player1.hand) == 2

	assert game.player1.hand.contains(WISP)
	assert game.player1.hand.contains(TARGET_DUMMY)


def test_tinkmaster_overspark():
	game = prepare_game()
	tinkmaster1 = game.player1.give("EX1_083")
	tinkmaster1.play()
	assert tinkmaster1 in game.board
	tinkmaster2 = game.player1.give("EX1_083")
	tinkmaster2.play()
	assert tinkmaster1 not in game.board
	assert len(game.player1.field) == 2
	assert game.board.contains("EX1_tk28") ^ game.board.contains("EX1_tk29")


def test_totemic_might():
	game = prepare_game()
	searing = game.player1.give("CS2_050")
	searing.play()
	assert searing.atk == 1
	assert searing.health == 1
	game.player1.give("EX1_244").play()
	assert searing.atk == 1
	assert searing.health == 3


def test_tracking():
	game = prepare_game()
	game.player1.discard_hand()
	tracking = game.player1.give("DS1_184")
	tracking.play()
	assert game.player1.choice
	assert len(game.player1.choice.cards) == 3
	pick = game.player1.choice.cards[0]
	game.player1.choice.choose(pick)
	assert game.player1.hand == [pick]


def test_truesilver_champion():
	game = prepare_game()
	truesilver = game.current_player.give("CS2_097")
	truesilver.play()
	lightwarden = game.current_player.give("EX1_001")
	lightwarden.play()
	assert game.player1.weapon is truesilver
	assert game.player1.hero.atk == 4
	assert game.player1.hero.health == 30
	game.current_player.hero.attack(target=game.player2.hero)
	assert game.player2.hero.health == 26
	assert game.player1.hero.health == 30
	assert lightwarden.atk == 1
	game.end_turn(); game.end_turn()

	for i in range(3):
		game.player1.give(MOONFIRE).play(target=game.player1.hero)
	game.player1.hero.attack(target=game.player2.hero)
	assert game.current_player.hero.health == 29
	assert lightwarden.atk == 3


def test_twilight_drake():
	game = prepare_game()
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	assert len(game.current_player.hand) == 7
	drake = game.current_player.give("EX1_043")
	drake.play()
	assert len(game.current_player.hand) == 7
	assert drake.health == 1 + 7
	assert drake.buffs

	game.end_turn()
	game.current_player.discard_hand()
	drake2 = game.current_player.give("EX1_043")
	assert len(game.current_player.hand) == 1
	drake2.play()
	assert not game.current_player.hand
	assert drake2.health == 1
	assert not drake2.buffs


def test_unbound_elemental():
	game = prepare_game()
	unbound = game.player1.give("EX1_258")
	unbound.play()
	assert unbound.atk == 2
	assert unbound.health == 4
	game.player1.give(THE_COIN).play()
	assert unbound.atk == 2
	assert unbound.health == 4
	# Lightning Bolt should trigger it
	game.player1.give("EX1_238").play(target=game.player2.hero)
	assert unbound.atk == 3
	assert unbound.health == 5
	game.end_turn()

	game.player2.give("EX1_238").play(target=game.player2.hero)
	assert unbound.atk == 3
	assert unbound.health == 5


def test_upgrade():
	game = prepare_game()
	weapon = game.player1.give(LIGHTS_JUSTICE)
	weapon.play()
	assert game.player1.weapon.atk == 1
	assert game.player1.weapon.durability == 4
	game.player1.hero.attack(game.player2.hero)
	assert game.player1.weapon.durability == 4 - 1
	upgrade = game.player1.give("EX1_409")
	upgrade.play()
	assert game.player1.weapon.atk == 1 + 1
	assert game.player1.weapon.durability == 4 - 1 + 1
	game.end_turn(); game.end_turn()

	game.player1.hero.attack(game.player2.hero)
	assert game.player2.hero.health == 30 - 1 - 2
	game.end_turn()

	# test Bloodsail Corsair
	corsair = game.player2.give("NEW1_025")
	corsair.play()
	assert game.player1.weapon.atk == 1 + 1
	assert game.player1.weapon.durability == 4 - 1 + 1 - 1 - 1


def test_upgrade_no_weapon():
	game = prepare_game()
	# Upgrade without a weapon
	upgrade = game.player1.give("EX1_409")
	upgrade.play()
	assert game.player1.hero.atk == 1
	assert game.player1.weapon.atk == 1
	assert game.player1.weapon.id == "EX1_409t"


def test_vancleef():
	game = prepare_game()
	vancleef1 = game.current_player.give("EX1_613")
	vancleef2 = game.current_player.give("EX1_613")

	assert not game.current_player.cards_played_this_turn
	for i in range(5):
		game.player1.give(THE_COIN).play()
	assert game.current_player.cards_played_this_turn == 5
	vancleef1.play()
	assert game.current_player.cards_played_this_turn == 6
	assert vancleef1.atk == 12
	assert vancleef1.health == 12
	game.end_turn(); game.end_turn()

	assert not game.current_player.cards_played_this_turn
	vancleef2.play()
	assert game.current_player.cards_played_this_turn == 1
	assert vancleef2.atk == 2
	assert vancleef2.health == 2


def test_venture_co_mercenary():
	game = prepare_game()
	fireball = game.player1.give("CS2_029")
	wisp = game.player1.give(WISP)
	assert wisp.cost == 0
	assert fireball.cost == 4
	ventureco = game.player1.give("CS2_227")
	ventureco.play()
	assert wisp.cost == 0 + 3
	assert fireball.cost == 4
	game.end_turn(); game.end_turn()

	ventureco2 = game.player1.give("CS2_227")
	assert ventureco2.cost == 5 + 3
	ventureco2.play()
	assert wisp.cost == 0 + 3 + 3
	assert fireball.cost == 4
	game.player1.give(SILENCE).play(target=ventureco)
	assert wisp.cost == 0 + 3
	assert fireball.cost == 4


def test_violet_teacher():
	game = prepare_game()
	teacher = game.player1.give("NEW1_026")
	teacher.play()
	assert len(game.player1.field) == 1
	game.player1.give(THE_COIN).play()
	assert len(game.player1.field) == 2
	assert len(game.player1.field.filter(id="NEW1_026t")) == 1
	game.end_turn()
	game.player2.give(THE_COIN).play()
	assert len(game.player1.field) == 2


def test_void_terror():
	game = prepare_game()
	terror1 = game.player1.give("EX1_304")
	terror2 = game.player1.give("EX1_304")
	terror3 = game.player1.give("EX1_304")
	power = game.player1.give("EX1_316")
	terror1.play()
	assert terror1.atk == 3
	assert terror1.health == 3

	terror2.play()
	assert terror1.dead
	assert terror2.atk == 3 + 3
	assert terror2.health == 3 + 3

	power.play(target=terror2)
	assert terror2.health == 3 + 3 + 4
	assert terror2.atk == 3 + 3 + 4
	terror3.play()
	assert terror2.dead
	assert terror3.atk == 3 + 3 + 3 + 4
	assert terror3.health == 3 + 3 + 3 + 4
	game.end_turn(); game.end_turn()
	assert terror3.zone == Zone.PLAY


def test_warsong_commander():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	boar = game.player1.give("CS2_171")
	boar.play()
	assert wisp.atk == boar.atk == 1
	assert not wisp.charge
	assert boar.charge
	warsong = game.player1.give("EX1_084")
	warsong.play()
	assert wisp.atk == 1
	assert boar.atk == 1 + 1
	assert not wisp.charge
	assert boar.charge
	game.player1.give(SILENCE).play(target=boar)
	assert boar.atk == 1
	assert not boar.charge


def test_water_elemental():
	game = prepare_game()
	elem = game.player1.give("CS2_033")
	elem.play()
	game.end_turn(); game.end_turn()

	assert not game.player2.hero.frozen
	elem.attack(target=game.player2.hero)
	assert game.player2.hero.frozen
	game.end_turn()

	assert game.player2.hero.frozen
	game.end_turn()

	assert not game.player2.hero.frozen
	game.end_turn()

	game.player2.give(LIGHTS_JUSTICE).play()
	game.player2.hero.attack(target=elem)
	assert game.player2.hero.frozen
	game.end_turn()

	assert game.player2.hero.frozen
	game.end_turn()

	assert game.player2.hero.frozen
	game.end_turn()

	assert not game.player2.hero.frozen
	game.end_turn()


def test_wild_growth():
	game = prepare_game(game_class=Game)
	game.end_turn(); game.end_turn()
	assert game.player1.max_mana == 2
	wildgrowth1 = game.player1.give("CS2_013")
	wildgrowth1.play()
	assert game.player1.mana == 0
	assert game.player1.used_mana == 2 + 1
	assert game.player1.max_mana == 2 + 1
	for i in range(8):
		game.end_turn(); game.end_turn()

	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	assert game.player1.max_mana == 10
	wildgrowth2 = game.player1.give("CS2_013")
	wildgrowth2.play()
	assert len(game.player1.hand) == 1
	assert game.player1.max_mana == 10
	excess_mana = game.player1.hand[0]
	assert excess_mana.id == "CS2_013t"
	excess_mana.play()
	assert len(game.player1.hand) == 1


def test_wild_pyromancer():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	pyro = game.player1.give("NEW1_020")
	game.end_turn(); game.end_turn()

	pyro.play()
	assert pyro.health == 2
	assert wisp.zone == Zone.PLAY

	# play moonfire. wisp should die.
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert wisp.dead
	assert pyro.health == 1

	# play circle of healing. pyro should go up to 2hp then back to 1.
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert pyro.health == 1
	assert pyro.zone == Zone.PLAY

	# Silence the pyromancer. It should not trigger.
	game.player1.give(SILENCE).play(target=pyro)
	assert pyro.health == 1
	assert pyro.zone == Zone.PLAY


def test_whirlwind():
	game = prepare_game()
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	wisp2 = game.player2.give(WISP)
	wisp2.play()
	game.player2.give("EX1_400").play()
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 30
	assert wisp.dead
	assert wisp2.dead
	assert statue.health == 10 - 1


def test_young_priestess():
	game = prepare_game()
	priestess = game.player1.give("EX1_004")
	game.end_turn(); game.end_turn()

	priestess.play()
	assert priestess.health == 1
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	assert priestess.health == 1
	assert wisp.health == 1
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	assert wisp1.health == 1
	game.end_turn()

	assert wisp1.health == 2


def test_ysera():
	game = prepare_game()
	ysera = game.player1.give("EX1_572")
	ysera.play()
	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	game.end_turn()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].card_class == CardClass.DREAM


def test_ysera_awakens():
	game = prepare_game()
	game.player1.give(WISP).play()
	ysera = game.player1.give("EX1_572")
	ysera.play()
	game.end_turn()

	game.player2.give(WISP).play()
	game.player2.give("DREAM_02").play()
	assert game.player1.hero.health == game.player2.hero.health == 30 - 5
	assert len(game.board) == 1
	assert ysera.health == 12


def main():
	for name, f in globals().items():
		if name.startswith("test_") and callable(f):
			f()
	print("All tests ran OK")


if __name__ == "__main__":
	main()
