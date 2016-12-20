from utils import *

def test_celestial_dreamer():
	game = prepare_game()
	dreamer = game.player1.give("CFM_617")
	assert not dreamer.powered_up

	wisp = game.player1.give(WISP).play()
	po = game.player1.give("EX1_316").play(target=wisp) #Power Overwhelming

	assert dreamer.powered_up

	dreamer.play()
	assert dreamer.buffs
	assert dreamer.atk == 5
	assert dreamer. health == 5

def test_virmen_sensei():
	game = prepare_empty_game()
	sensei1 = game.player1.give("CFM_816")
	wisp = game.player1.give(WISP).play()
	assert not sensei1.powered_up

	sensei1.play()

	beast = game.player1.give(CHICKEN).play()
	sensei2 = game.player1.give("CFM_816")
	assert sensei2.powered_up
	game.player1.give(INNERVATE).play()
	sensei2.play(target=beast)

	assert beast.buffs
	assert beast.atk == 3
	assert beast.health == 3

def test_mark_of_the_lotus():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	chicken = game.player1.give(CHICKEN).play()

	assert wisp.atk == 1
	assert chicken.atk == 1
	lotus = game.player1.give("CFM_614").play()

	assert wisp.buffs
	assert wisp.atk == 2
	assert wisp.health == 2
	assert chicken.buffs
	assert chicken.atk == 2
	assert chicken.health == 2

def test_pilfered_power():
	game = prepare_game(game_class=Game)
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()
	assert game.player1.max_mana == 3
	pilfered1 = game.player1.give("CFM_616")
	pilfered1.play()
	assert game.player1.mana == 0
	assert game.player1.used_mana == 3
	assert game.player1.max_mana == 3

	game.end_turn(); game.end_turn()

	assert game.player1.max_mana == 4
	livingroots = game.player1.give("AT_037").play(choose="AT_037b")
	assert len(game.player1.field) == 2
	pilfered2 = game.player1.give("CFM_616").play()
	assert game.player1.mana == 0
	assert game.player1.used_mana == 4 + 2
	assert game.player1.max_mana ==  4 + 2

	for i in range(4):
		game.end_turn(); game.end_turn()

	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	assert game.player1.max_mana == 10
	pilfered3 = game.player1.give("CFM_616").play()
	assert len(game.player1.hand) == 1
	assert game.player1.max_mana == 10
	excess_mana = game.player1.hand[0]
	assert excess_mana.id == "CS2_013t"
	excess_mana.play()
	assert len(game.player1.hand) == 1

def test_lunar_visions():
	game = prepare_empty_game()
	golem = game.player1.give("CS2_186").shuffle_into_deck() #War Golem
	portal = game.player1.give(UNSTABLE_PORTAL).shuffle_into_deck()

	game.player1.give("CFM_811").play()
	assert len(game.player1.hand) == 2
	def check_cost(c):
		if c.id == "CS2_186":
			assert c.cost == 5
		else:
			assert c.cost == 2
	for c in game.player1.hand:
		check_cost(c)

def test_alleycat():
	game = prepare_game()
	game.player1.give("CFM_315").play()
	assert len(game.player1.field) == 2
	assert game.player1.field[0].id == "CFM_315"
	assert game.player1.field[1].id == "CFM_315t"

def test_shaky_zipgunner():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	gunner = game.player1.give("CFM_336").play()
	game.player1.give("CS2_057").play(target=gunner) #Shadow Bolt
	assert wisp.atk == 3
	assert wisp.health == 3

	wisp.play()

	assert wisp.atk == 3
	assert wisp.health == 3

def test_trogg_beastrager():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	trogg1 = game.player1.give("CFM_338").play()
	assert wisp.atk == 1
	beast = game.player1.give(CHICKEN)
	trogg2 = game.player1.give("CFM_338").play()
	assert beast.buffs
	assert beast.atk == 2
	assert beast.health == 2

	beast.play()

	assert beast.buffs
	assert beast.atk == 2
	assert beast.health == 2

def test_hidden_cache():
	game = prepare_empty_game()
	cache = game.player1.give("CFM_026").play()
	assert game.player1.secrets
	game.end_turn()
	game.player2.give(WISP).play()
	assert game.player1.secrets

	game.end_turn()
	wisp = game.player1.give(WISP)
	game.end_turn()
	game.player2.give(WISP).play()
	assert not game.player1.secrets
	assert wisp.buffs
	assert wisp.atk == 3
	assert wisp.health == 3

	game.end_turn()

	wisp.play()
	assert wisp.buffs
	assert wisp.atk == 3
	assert wisp.health == 3

def test_smugglers_crate():
	# Game allows card to be played with no beast in hand
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	game.player1.give("CFM_334").play()
	assert not wisp.buffs
	crate = game.player1.give("CFM_334")
	beast = game.player1.give(CHICKEN)
	crate.play()
	assert beast.buffs
	assert beast.atk == 3
	assert beast.health == 3

	beast.play()
	assert beast.buffs
	assert beast.atk == 3
	assert beast.health == 3

def test_piranha_launcher():
	game = prepare_empty_game()
	game.player1.give("CFM_337").play()
	game.end_turn()
	wisp = game.player2.give(WISP).play()
	game.end_turn()
	game.player1.hero.attack(target=wisp)

	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "CFM_337t"

def test_kabal_lackey():
	game = prepare_empty_game()
	counterspell = game.player1.give("EX1_287")
	assert counterspell.cost == 3
	vaporize = game.player1.give("EX1_594")
	assert vaporize.cost == 3
	missiles = game.player1.give("EX1_277")
	assert missiles.cost == 1
	game.player1.give("CFM_066").play()
	assert counterspell.cost == 0
	assert vaporize.cost == 0
	assert missiles.cost == 1

	missiles.play()
	assert counterspell.cost == 0
	assert vaporize.cost == 0

	counterspell.play()
	assert vaporize.cost == 3

	game.player1.give("CFM_066").play()
	assert vaporize.cost == 0

	game.end_turn()
	assert vaporize.cost == 3
	game.end_turn()
	assert vaporize.cost == 3

def test_manic_soulcaster():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	game.player1.give(HAND_OF_PROTECTION).play(target=wisp)
	game.player1.give("CS2_236").play(target=wisp) #Inner Fire
	assert wisp.divine_shield
	assert wisp.health == 2
	game.player1.give("CFM_660").play(target=wisp)
	assert len(game.player1.deck) == 1

	game.end_turn()
	game.end_turn()
	assert len(game.player1.hand) == 1
	assert not game.player1.hand[0].divine_shield
	assert game.player1.hand[0].health == 1

def test_cryomancer():
	game = prepare_empty_game()
	cryomancer = game.player1.give("CFM_671")
	assert not cryomancer.powered_up

	game.player1.give("CS2_031").play(target=game.player2.hero)
	assert cryomancer.powered_up
	cryomancer.play()
	assert cryomancer.buffs
	assert cryomancer.atk == 7
	assert cryomancer.health == 7

def test_inkmaster_solia():
	game = prepare_empty_game()
	btg = game.player1.give("AT_035")# Beneath the Grounds
	soulfire = game.player1.give(SOULFIRE)
	assert btg.cost == 3
	assert soulfire.cost == 1
	game.player1.give("CFM_687").play()
	assert btg.cost == 0
	assert soulfire.cost == 0
	btg.play()
	assert soulfire.cost == 1
	game.end_turn()

	game.player2.give(WISP).shuffle_into_deck()
	game.player2.give(WISP).shuffle_into_deck()
	solia = game.player2.give("CFM_687")
	mc = game.player2.give(MIND_CONTROL)
	solia.play()
	assert mc.cost == 10
	game.end_turn()
	game.end_turn()
	game.player2.give("CFM_687").play()
	assert mc.cost == 0
	game.end_turn()
	game.end_turn()
	assert mc.cost == 10

def test_potion_of_polymorph():
	game = prepare_game()
	game.player1.give("CFM_620").play()
	game.player1.give(WISP).play()
	assert game.player1.secrets
	game.end_turn()

	game.player2.give(WISP).play()
	assert len(game.player2.field) == 1
	assert game.player2.field[0].id == "CS2_tk1"
	assert not game.player1.secrets

def test_greater_arcane_missiles():
	game = prepare_game()
	acolyte = game.player1.give("EX1_007").play()
	game.player1.give("CS2_004").play(target=acolyte) #Power Word: Shield
	game.player1.discard_hand()
	game.end_turn()
	game.player2.give(KOBOLD_GEOMANCER).play()
	game.player2.give("CFM_623").play()
	
	if acolyte.dead:
		assert len(game.player1.hand) == 2
		assert game.player1.hero.health == 30 - 4
	elif acolyte.health == 1:
		assert len(game.player1.hand) == 1
		assert game.player1.hero.health == 30 - 8
	elif acolyte.health == 5:
		assert len(game.player1.hand) == 0
		assert game.player1.hero.health == 30 - 12
	else:
		assert False

def test_red_mana_wyrm():
	game = prepare_game()
	wyrm = game.player1.give("CFM_060").play()
	assert wyrm.atk == 2

	game.player1.give(INNERVATE).play()
	assert wyrm.atk == 4

	game.player1.give(CIRCLE_OF_HEALING).play()
	assert wyrm.atk == 6

def test_hozen_healer():
	game = prepare_empty_game()
	blademaster1 = game.player1.give("CS2_181").play()
	assert blademaster1.health == 3
	game.player1.give("CFM_067").play(target=blademaster1)
	assert blademaster1.health == 7
	game.end_turn()

	game.player2.give("EX1_591").play()
	game.player2.give("CFM_067").play(target=blademaster1)
	assert blademaster1.dead

def test_kabal_chemist():
	game = prepare_empty_game()
	game.player1.give("CFM_619").play()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id in fireplace.cards.utils.POTIONS

def test_big_time_racketeer():
	game = prepare_empty_game()
	game.player1.give("CFM_648").play()
	assert len(game.player1.field) == 2
	assert game.player1.field[1].id == "CFM_648t"

def test_naga_corsair():
	game = prepare_empty_game()
	game.player1.give(LIGHTS_JUSTICE).play()
	game.player1.give("CFM_651").play()

	assert game.player1.hero.atk == 2

def test_friendly_bartender():
	game = prepare_empty_game()
	game.player1.give("CFM_654").play()
	game.player1.give(KOBOLD_GEOMANCER).play()
	game.player1.hero.set_current_health(1)
	game.end_turn()
	assert game.player1.hero.health == 1 + 1

def test_streetwise_investigator():
	game = prepare_empty_game()
	stealthy1 = game.player1.give("EX1_010").play() #Worgen Infiltrator
	game.end_turn()
	stealthy2 = game.player2.give("EX1_010").play() #Worgen Infiltrator
	game.player2.give("CFM_656").play()

	assert not stealthy1.stealthed
	assert stealthy2.stealthed

def test_tanaris_hogchopper():
	game = prepare_empty_game()
	hog1 = game.player1.give("CFM_809")
	assert not hog1.powered_up #Opponent bas Coin
	hog1.play()
	assert not hog1.charge
	game.end_turn()

	assert len(game.player1.hand) == 0
	hog2 = game.player2.give("CFM_809")
	assert hog2.powered_up
	hog2.play()
	assert hog2.charge
	hog2.attack(game.player1.hero)

def test_daring_reporter():
	game = prepare_game()
	reporter = game.player1.give("CFM_851").play()
	assert reporter.health == 3
	game.end_turn()

	assert reporter.atk == 4
	assert reporter.health == 4
	game.player2.give("EX1_164").play(choose="EX1_164b") #Nourish, draw 3
	assert reporter.atk == 7
	assert reporter.health == 7
	reporter.set_current_health(1)
	game.player2.give("EX1_154").play(target=reporter, choose="EX1_154b") #Wrath, 1 damage
	assert not reporter.dead
	assert reporter.atk == 8
	assert reporter.max_health == 8
	assert reporter.health == 1

def test_grimstreet_smuggler():
	game = prepare_empty_game()
	smuggler1 = game.player1.give("CFM_853").play()
	wisp = game.player1.give(WISP)
	smuggler2 = game.player1.give("CFM_853").play()
	assert wisp.atk == 2
	assert wisp.health == 2

	wisp.play()

	assert "CFM_853e" in wisp.buffs
	assert wisp.atk == 2
	assert wisp.health == 2

def test_wind_up_burglebot():
	game = prepare_game()
	windupbot = game.player1.give("CFM_025").play()
	game.end_turn()

	wolfrider1 = game.player2.give("CS2_124").play()
	handsize = len(game.player1.hand)
	wolfrider1.attack(windupbot)
	assert len(game.player1.hand) == handsize
	wisp = game.player2.give(WISP).play()
	wolfrider2 = game.player2.give("CS2_124").play()
	game.end_turn()

	handsize = len(game.player1.hand)
	windupbot.attack(wisp)
	assert len(game.player1.hand) == handsize + 1
	game.end_turn(); game.end_turn()
	game.player1.discard_hand()
	handsize = len(game.player1.hand)
	windupbot.attack(wolfrider2)
	assert len(game.player1.hand) == handsize

def test_blubber_baron():
	game = prepare_game()
	baron = game.player1.give("CFM_064")
	assert baron.atk == 1
	assert baron.health == 1
	game.player1.give("EX1_015").play()
	assert baron.atk == 2
	assert baron.health == 2
	game.player1.give("EX1_015").play()
	assert baron.atk == 3
	assert baron.health == 3

	baron.play()
	assert baron.atk == 3
	assert baron.health == 3

def test_fight_promoter():
	game = prepare_game()
	game.player1.discard_hand()
	promoter = game.player1.give("CFM_328")
	zipgunner = game.player1.give("CFM_336").play().destroy()
	assert promoter.health == 6
	promoter.play()
	assert len(game.player1.hand) == 2

def test_fel_orc_soulfiend():
	game = prepare_empty_game()
	orc = game.player1.give("CFM_609").play()
	assert orc.health == 7
	game.end_turn();game.end_turn()
	assert orc.health == 5
	game.end_turn();game.end_turn()	
	assert orc.health == 3
	game.end_turn();game.end_turn()
	assert orc.health == 1
	game.end_turn();game.end_turn()
	assert orc.dead

def test_burgly_bully():
	game = prepare_empty_game()
	bully = game.player1.give("CFM_669").play()
	game.player1.give(INNERVATE).play()
	assert len(game.player1.hand) == 0
	game.end_turn()
	game.player2.give(INNERVATE).play()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == "GAME_005"

def test_dirty_rat():
	game = prepare_game()
	game.player1.discard_hand()
	game.player1.give("EX1_015") #Novice Engineer
	game.end_turn()
	game.player2.give("CFM_790").play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "EX1_015"
	assert len(game.player1.hand) == 0

def test_leatherclad_hogleader():
	game = prepare_game()
	for i in range(3):
		game.player1.give(WISP)
	assert len(game.player1.hand) > 5
	hog1 = game.player1.give("CFM_810")
	assert not hog1.powered_up
	hog1.play()
	assert not hog1.charge
	game.end_turn()

	hog2 = game.player2.give("CFM_810")
	assert hog2.powered_up
	hog2.play()
	assert hog2.charge

def test_defias_cleaner():
	game = prepare_empty_game()
	game.player1.give("CFM_855").play()
	loothoarder = game.player1.give("EX1_096").play()
	game.end_turn()
	game.player2.give("CFM_855").play(target=loothoarder)
	game.player2.give(MOONFIRE).play(target=loothoarder)
	assert len(game.player1.hand) == 0

def test_small_time_buccaneer():
	game = prepare_game()
	buccaneer = game.player1.give("CFM_325").play()
	assert buccaneer.atk == 1
	game.player1.give(LIGHTS_JUSTICE).play()
	assert buccaneer.atk == 3

def test_second_rate_bruiser():
	game = prepare_game()
	bruiser = game.player1.give("CFM_652")
	assert bruiser.cost == 5
	bruiser.play()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	assert len(game.player1.field) == 3
	game.end_turn()

	bruiser2 = game.player2.give("CFM_652")
	assert bruiser2.cost == 3
	bruiser2.play()
	assert game.player2.mana == 7
	assert bruiser2.cost == 5

def test_backroom_bouncer():
	game = prepare_empty_game()
	bouncer = game.player1.give("CFM_658").play()
	assert bouncer.atk == 4
	friendly_wisp = game.player1.give(WISP).play()
	game.end_turn()
	unfriendly_wisp = game.player2.give(WISP).play()
	game.player2.give("EX1_400").play() #Whirlwind
	assert friendly_wisp.dead
	assert unfriendly_wisp.dead
	assert bouncer.atk == 5

def test_bomb_squad():
	game = prepare_empty_game()
	defender = game.player1.give("CFM_300").play() #Public Defender
	game.end_turn()
	bombsquad = game.player2.give("CFM_667")
	bombsquad.play(target=defender)
	assert defender.health == 2
	bombsquad.destroy()
	assert game.player2.hero.health == 25

def test_spiked_hogrider():
	game = prepare_empty_game()
	hog1 = game.player1.give("CFM_688")
	assert not hog1.powered_up
	defender = game.player1.give("CFM_300").play() #Public Defender
	game.end_turn()
	hog2 = game.player2.give("CFM_688")
	assert hog2.powered_up
	hog2.play()
	assert hog2.charge

def test_grimestreet_protector():
	game = prepare_empty_game()
	wisp1 = game.player1.give(WISP).play()
	wisp2 = game.player1.give(WISP).play()
	wisp3 = game.player1.give(WISP).play()
	protector = game.player1.give("CFM_062").play(index=1)
	assert game.player1.field == [wisp1, protector, wisp2, wisp3]
	assert wisp1.divine_shield
	assert wisp2.divine_shield
	assert not wisp3.divine_shield

def test_grimestreet_enforcer():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	beast = game.player1.give(CHICKEN)
	spell = game.player1.give(INNERVATE)
	summoned_dummy = game.player1.give(TARGET_DUMMY).play()
	game.player1.give("CFM_639").play()
	game.end_turn()
	assert wisp.buffs
	assert wisp.atk == 2
	assert wisp.health == 2
	assert beast.buffs
	assert beast.atk == 2
	assert beast.health == 2
	assert not summoned_dummy.buffs	
	assert summoned_dummy.atk == 0
	assert summoned_dummy.health == 2

def test_grimscale_chum():
	game = prepare_empty_game()
	murloc = game.player1.give(MURLOC)
	wisp = game.player1.give(WISP)
	game.player1.give("CFM_650").play()
	assert murloc.buffs
	assert murloc.atk == 2
	assert murloc.health == 2
	assert not wisp.buffs

def test_grimestreet_outfitter():
	game = prepare_empty_game()
	murloc = game.player1.give(MURLOC)
	wisp = game.player1.give(WISP)
	spell = game.player1.give(INNERVATE)
	summoned_dummy = game.player1.give(TARGET_DUMMY).play()
	game.player1.give("CFM_753").play()
	assert murloc.buffs
	assert murloc.atk == 2
	assert murloc.health == 2
	assert wisp.buffs
	assert wisp.atk == 2
	assert wisp.health == 2
	assert not summoned_dummy.buffs	
	assert summoned_dummy.atk == 0
	assert summoned_dummy.health == 2

def test_wickerflame_burnbristle():
	game = prepare_game()
	wickerflame = game.player1.give("CFM_815").play()
	game.end_turn()
	game.player1.hero.set_current_health(10)
	game.player2.give(LIGHTS_JUSTICE).play()
	game.player2.hero.attack(target=wickerflame)
	assert game.player1.hero.health == 10 + wickerflame.atk

def test_smugglers_run():
	game = prepare_empty_game()
	murloc = game.player1.give(MURLOC)
	wisp = game.player1.give(WISP)
	spell = game.player1.give(INNERVATE)
	summoned_dummy = game.player1.give(TARGET_DUMMY).play()
	game.player1.give("CFM_305").play()
	assert murloc.buffs
	assert murloc.atk == 2
	assert murloc.health == 2
	assert wisp.buffs
	assert wisp.atk == 2
	assert wisp.health == 2
	assert not summoned_dummy.buffs	
	assert summoned_dummy.atk == 0
	assert summoned_dummy.health == 2

def test_getaway_kodo():
	game = prepare_game()
	game.player1.give("CFM_800").play()
	loothoarder = game.player1.give("EX1_096").play()
	game.player1.discard_hand()
	game.end_turn()
	game.player2.give(MOONFIRE).play(target=loothoarder)
	assert not game.player1.secrets
	assert len(game.player1.hand) == 2
	assert loothoarder in game.player1.hand

def test_small_time_recruits():
	game = prepare_empty_game()
	game.player1.give(GOLDSHIRE_FOOTMAN).shuffle_into_deck()
	game.player1.give(GOLDSHIRE_FOOTMAN).shuffle_into_deck()
	game.player1.give(GOLDSHIRE_FOOTMAN).shuffle_into_deck()
	game.player1.give(KOBOLD_GEOMANCER).shuffle_into_deck()
	game.player1.give(SOULFIRE).shuffle_into_deck()
	game.player1.give("CFM_905").play()
	assert len(game.player1.hand) == 3
	assert len(game.player1.deck) == 2
	assert game.player1.deck
	for i in range(3):
		assert game.player1.hand[i].id == GOLDSHIRE_FOOTMAN

def test_raza_the_chained():
	game = prepare_empty_game()
	game.player1.give("CFM_020").play()
	assert game.player1.hero.power.cost == 0
	game.player1.give("EX1_625").play()
	assert game.player1.hero.power.cost == 0
	game.end_turn();game.end_turn()
	game.player1.give("EX1_323").play()
	assert game.player1.hero.power.cost == 0

def test_mana_geode():
	game = prepare_empty_game()
	geode = game.player1.give("CFM_606").play()
	geode.set_current_health(1)
	game.player1.give(CIRCLE_OF_HEALING).play()
	assert len(game.player1.field) == 2
	assert geode.health == 3
	assert game.player1.field[-1].id == "CFM_606t"

def test_kabal_talonpriest():
	game = prepare_empty_game()
	talonpriest1 = game.player1.give("CFM_626").play()
	talonpriest2 = game.player1.give("CFM_626").play(target=talonpriest1)
	assert "CFM_626e" in talonpriest1.buffs
	assert talonpriest1.atk == 3
	assert talonpriest1.health == 4 + 3

def test_potion_of_madness_attacked_last_turn():
	"""
	Test that Potion of Madness-ing a minion that was just played by the opponent
	lets it attack
	"""
	game = prepare_game()

	wisp = game.player1.give(WISP).play()
	game.end_turn()
	assert wisp.controller is game.player1

	shadowmadness = game.player2.give("CFM_603")
	shadowmadness.play(target=wisp)
	assert wisp.controller is game.player2
	assert wisp.can_attack()
	wisp.attack(game.player1.hero)
	game.end_turn()

	# make sure it can attack when control returns
	assert wisp.controller is game.player1
	assert wisp.can_attack()


def test_potion_of_madness_bounce():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	game.player2.discard_hand()
	shadowmadness = game.player2.give("CFM_603")
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


def test_potion_of_madness_just_played():
	"""
	test that Potion of Madness-ing a minion that attacked on the opponent's previous
	turn lets it attack
	"""
	game = prepare_game()

	wisp = game.player1.give(WISP).play()
	game.end_turn(); game.end_turn()
	assert wisp.controller is game.player1
	assert wisp.can_attack()
	wisp.attack(game.player2.hero)
	game.end_turn()

	shadowmadness = game.player2.give("CFM_603")
	shadowmadness.play(target=wisp)
	assert wisp.controller is game.player2
	assert wisp.can_attack()
	wisp.attack(game.player1.hero)
	game.end_turn()

	# make sure it can attack when the player regains control
	assert wisp.controller is game.player1
	assert wisp.can_attack()


def test_potion_of_madness_silence():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	assert wisp.controller == game.player1
	shadowmadness = game.player2.give("CFM_603")
	shadowmadness.play(target=wisp)
	assert wisp.controller == game.player2
	game.player2.give(SILENCE).play(target=wisp)
	assert wisp.controller == game.player1
	game.end_turn()

	assert wisp.controller == game.player1


def test_potion_of_madness_wild_pyro():
	game = prepare_game()
	pyromancer = game.player1.give("NEW1_020")
	pyromancer.play()
	game.end_turn()

	assert pyromancer.controller == game.player1
	assert pyromancer in game.player1.field
	assert pyromancer.health == 2
	game.player2.give("GVG_011").play(target=pyromancer) # Shrinkmeister
	shadowmadness = game.player2.give("CFM_603")
	shadowmadness.play(target=pyromancer)
	assert pyromancer.controller == game.player2
	assert pyromancer in game.player2.field
	assert pyromancer.health == 1
	game.end_turn()

	assert pyromancer.controller == game.player1
	assert pyromancer in game.player1.field

def test_pint_size_potion():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	kobold = game.player1.give(KOBOLD_GEOMANCER).play()
	wargolem = game.player1.give("CS2_186").play()

	game.end_turn()

	chicken = game.player2.give(CHICKEN).play()
	game.player2.give("CFM_661").play()

	assert wisp.atk == 0
	assert kobold.atk == 0
	assert wargolem.atk == 7 - 3
	assert chicken.atk == 1

	game.player2.give("AT_016").play()
	
	assert len(game.player1.field) == 1
	assert wisp.dead
	assert kobold.dead
	
	game.end_turn()
	assert wargolem.health == 4
	assert wargolem.atk == 7

def test_dragonfire_potion():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	whelp = game.player1.give(WHELP).play()
	wargolem = game.player1.give("CS2_186").play()
	game.end_turn()

	murloc = game.player2.give(MURLOC).play()
	beast = game.player2.give(CHICKEN).play()
	game.player2.give("CFM_662").play()
	assert wisp.dead
	assert murloc.dead
	assert beast.dead
	assert not whelp.dead
	assert wargolem.health == 2

def test_luckydo_buccaneer():
	game = prepare_game()
	buc1 = game.player1.give("CFM_342")
	assert not buc1.powered_up
	buc1.play()
	assert buc1.atk == 5
	assert buc1.health == 5

	game.end_turn()
	game.player2.give("CS2_106").play()
	buc2 = game.player2.give("CFM_342")
	assert buc2.powered_up
	buc2.play()
	assert "CFM_342e" in buc2.buffs
	assert buc2.atk == 9
	assert buc2.health == 9

def test_gadgetzan_ferryman():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	ferryman = game.player1.give("CFM_693").play(target=wisp)
	assert len(game.player1.field) == 1

	#Unconfirmed but ferryman does not have a REQ_TARGET_IF_AVAIL so it theoretically cannot be played with empty board
	# game.end_turn()
	# game.player2.hand[0].play() #The Coin
	# game.player2.give("CFM_693").play(target=self)
	# assert len(game.player2.field) == 1

def test_shadow_sensei():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	sensei1 = game.player1.give("CFM_694")
	assert wisp not in sensei1.targets
	sensei1.play()
	infiltrator = game.player1.give("EX1_010").play()
	sensei2 = game.player1.give("CFM_694")
	assert infiltrator in sensei2.targets
	sensei2.play(target=infiltrator)
	assert infiltrator.buffs
	assert infiltrator.atk == 4
	assert infiltrator.health == 3

def test_shaku_the_collector():
	game = prepare_empty_game()
	shaku = game.player1.give("CFM_781").play()
	game.end_turn();game.end_turn()
	game.player1.discard_hand()
	shaku.attack(game.player2.hero)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].card_class == game.player2.hero.card_class

def test_white_eyes():
	game = prepare_empty_game()
	assert len(game.player1.deck) == 0
	whiteeyes = game.player1.give("CFM_324").play()
	whiteeyes.destroy()
	assert len(game.player1.deck) == 1
	assert "CFM_324t" == game.player1.deck[0]

def test_lotus_illusionist():
	game = prepare_empty_game()
	lotus1 = game.player1.give("CFM_697").play()
	game.end_turn()
	lotus2 = game.player2.give("CFM_697").play()
	wisp = game.player2.give(WISP).play()
	game.end_turn()
	lotus1.attack(wisp)
	assert lotus1.id == "CFM_697"
	game.end_turn()
	lotus2.attack(game.player1.hero)
	assert lotus2.morphed
	assert len(game.player2.field) == 1
	assert game.player2.field[0].cost == 6
	game.end_turn(); game.end_turn()
	current_id = game.player2.field[0].id
	game.player2.field[0].attack(game.player1.hero)
	assert game.player2.field[0].id == current_id

def test_call_in_the_finishers():
	game = prepare_empty_game()
	game.player1.give("CFM_310").play()
	assert len(game.player1.field) == 4
	for i in game.player1.field:
		assert i.id == "CFM_310t"

	game.end_turn()
	game.player2.give("EX1_538").play()
	assert len(game.player2.field) == 4
	game.player2.give("CFM_310").play()
	assert len(game.player2.field) == 7
	game.end_turn();game.end_turn()
	callin = game.player2.give("CFM_310")
	assert not callin.is_playable()

def test_finders_keepers():
	game = prepare_empty_game()
	game.player1.give("CFM_313").play()
	assert game.player1.choice
	for card in game.player1.choice.cards:
		assert card.overload

def test_crystalweaver():
	game = prepare_empty_game()
	imp = game.player1.give(IMP).play()
	wisp = game.player1.give(WISP).play()
	imp_in_hand = game.player1.give(IMP)
	crystalweaver = game.player1.give("CFM_610").play()
	assert imp.buffs
	assert imp.atk == 2
	assert imp.health == 2
	assert not wisp.buffs
	assert wisp.atk == 1
	assert wisp.health == 1
	assert not imp_in_hand.buffs
	assert imp_in_hand.atk == 1
	assert imp_in_hand.health == 1

def test_kabal_trafficker():
	game = prepare_empty_game()
	trafficker = game.player1.give("CFM_663").play()
	game.end_turn()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.DEMON
	game.end_turn()
	assert len(game.player1.hand) == 1
	assert len(game.player2.hand) == 1

def test_krul_the_unshackled():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	imp = game.player1.give(IMP)
	flameimp = game.player1.give("EX1_319")
	jaraxxus = game.player1.give("EX1_323")
	krul = game.player1.give("CFM_750").play()
	assert len(game.player1.field) == 4
	assert len(game.player1.hand) == 1

def test_unlicensed_apothecary():
	game = prepare_empty_game()
	apothecary = game.player1.give("CFM_900").play()
	assert game.player1.hero.health == 30
	game.player1.give(WISP).play()
	assert game.player1.hero.health == 25
	game.end_turn()
	game.player2.give("BRM_026").play()
	assert game.player1.hero.health == 20

def test_blastcrystal_potion():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	game.end_turn()
	assert game.player2.max_mana == 10
	game.player2.give("CFM_608").play(target=wisp)
	assert wisp.dead
	assert game.player2.max_mana == 9

def test_bloodfury_potion():
	game = prepare_empty_game()
	imp = game.player1.give(IMP).play()
	wisp =game.player1.give(WISP).play()
	game.player1.give("CFM_611").play(target=imp)
	assert "CFM_611e2" in imp.buffs
	assert imp.atk == 4
	assert imp.health == 4
	game.player1.give("CFM_611").play(target=wisp)
	assert "CFM_611e" in wisp.buffs
	assert wisp.atk == 4
	assert wisp.health == 1

def test_hobart_grapplehammer():
	game = prepare_empty_game()
	lightsjustice = game.player1.give(LIGHTS_JUSTICE).play()
	fwa = game.player1.give("CS2_106")
	gorehowl = game.player1.give("EX1_411").shuffle_into_deck()
	game.player1.give("CFM_643").play()
	assert not lightsjustice.buffs
	assert fwa.buffs
	game.end_turn();game.end_turn()
	gorehowl = game.player1.hand[-1]
	assert gorehowl.buffs
	assert fwa.atk == 4
	assert gorehowl.atk == 8

def test_grimy_gadgeteer():
	game = prepare_empty_game()
	gadgeteer = game.player1.give("CFM_754").play()
	game.end_turn();game.end_turn()
	wisp = game.player1.give(WISP)
	game.end_turn();game.end_turn()
	assert wisp.buffs
	assert wisp.atk == 3
	assert wisp.health == 3
	wisp.play()
	assert wisp.buffs
	assert wisp.atk == 3
	assert wisp.health == 3

def test_grimestreet_pawnbroker():
	game = prepare_empty_game()
	lightsjustice1 = game.player1.give(LIGHTS_JUSTICE).play()
	lightsjustice2 = game.player1.give(LIGHTS_JUSTICE)
	game.player1.give("CFM_755").play()
	assert not lightsjustice1.buffs
	assert lightsjustice2.buffs
	assert lightsjustice1.atk == 1
	assert lightsjustice1.durability == 4
	assert lightsjustice2.atk == 2
	assert lightsjustice2.durability == 5

def test_alley_armorsmith():
	game = prepare_empty_game()
	armorsmith = game.player1.give("CFM_756").play()
	assert game.player1.hero.armor == 0
	game.player1.give(MOONFIRE).play(target=armorsmith)
	assert game.player1.hero.armor == 0
	game.end_turn();game.end_turn()
	armorsmith.attack(game.player2.hero)
	assert game.player1.hero.armor == 2