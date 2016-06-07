from utils import *


def test_avenge():
	game = prepare_game()
	avenge = game.player1.give("FP1_020")
	wisp1 = game.player1.give(WISP)
	avenge.play()
	wisp1.play()
	assert avenge.exhausted
	game.end_turn()

	assert not avenge.exhausted
	stonetusk1 = game.player2.give("CS2_171")
	stonetusk1.play()
	stonetusk1.attack(wisp1)
	assert avenge in game.player1.secrets
	game.end_turn()

	assert avenge.exhausted
	wisp2 = game.player1.give(WISP)
	wisp3 = game.player1.give(WISP)
	wisp2.play()
	wisp3.play()
	game.end_turn()

	assert not avenge.exhausted
	stonetusk2 = game.player2.give("CS2_171")
	stonetusk2.play()
	stonetusk2.attack(wisp3)
	assert avenge not in game.player1.secrets
	assert wisp2.atk == 4
	assert wisp2.health == 3


def test_bear_trap():
	game = prepare_game()
	trap = game.player1.give("AT_060")
	trap.play()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	game.end_turn()

	wisp2 = game.player2.give(WISP)
	wisp2.play()
	wisp3 = game.player2.give(WISP)
	wisp3.play()
	game.end_turn(); game.end_turn()

	assert trap in game.player1.secrets
	wisp2.attack(wisp1)
	assert wisp1.dead
	assert wisp2.dead
	assert trap in game.player1.secrets
	assert len(game.player1.field) == 0
	wisp3.attack(game.player1.hero)
	assert game.player1.hero.health == 30 - 1
	assert trap not in game.player1.secrets
	assert len(game.player1.field) == 1
	assert game.player1.field[0] == "CS2_125"


def test_counterspell():
	game = prepare_game()
	counterspell = game.player1.give("EX1_287")
	counterspell.play()
	game.end_turn()

	game.player2.give(WISP).play()
	assert counterspell in game.player1.secrets
	bolt = game.player2.give("EX1_238")
	bolt.play(target=game.player1.hero)
	assert not game.player1.secrets
	assert game.player2.used_mana == 1
	assert game.player2.overloaded == 0
	assert game.player1.hero.health == 30


def test_counterspell_wild_pyromancer():
	# Test for bug #12
	game = prepare_game()
	counterspell = game.player1.give("EX1_287")
	counterspell.play()
	game.end_turn()

	pyromancer = game.player2.give("NEW1_020")
	pyromancer.play()
	assert counterspell in game.player1.secrets
	moonfire = game.player2.give(MOONFIRE)
	moonfire.play(target=game.player1.hero)
	assert pyromancer.health == 2


def test_dart_trap():
	game = prepare_game(CardClass.WARLOCK, CardClass.WARLOCK)
	darttrap = game.player1.give("LOE_021")
	darttrap.play()
	game.end_turn()

	assert game.player2.hero.health == 30
	game.player2.hero.power.use()
	assert game.player2.hero.health == 30 - 5 - 2


def test_duplicate():
	game = prepare_game()
	game.player1.discard_hand()
	duplicate = game.player1.give("FP1_018")
	duplicate.play()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	assert duplicate in game.player1.secrets
	game.player2.give(MOONFIRE).play(target=wisp)
	assert duplicate not in game.player1.secrets
	assert len(game.player1.hand) == 2
	assert game.player1.hand[0] == game.player1.hand[1] == WISP


def test_duplicate_full_hand():
	game = prepare_game()
	game.player1.discard_hand()
	duplicate = game.player1.give("FP1_018")
	duplicate.play()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	for i in range(10):
		game.player1.give(TARGET_DUMMY)
	assert len(game.player1.hand) == 10
	game.end_turn()

	assert duplicate in game.player1.secrets
	wisp1.destroy()
	assert duplicate in game.player1.secrets
	game.player1.hand[0].discard()
	assert len(game.player1.hand) == 9
	wisp2.destroy()
	assert duplicate not in game.player1.secrets
	assert len(game.player1.hand) == 10
	assert len(game.player1.hand.filter(id=WISP)) == 1


def test_eaglehorn_bow():
	game = prepare_game()
	bow = game.player1.give("EX1_536")
	icebarrier = game.player1.give("EX1_289")
	bow.play()
	assert bow.durability == 2
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	icebarrier.play()
	assert bow.durability == 2
	game.end_turn()

	assert icebarrier in game.player1.secrets
	wisp.attack(target=game.player1.hero)
	assert not game.player1.secrets
	assert game.player1.hero.health == 30
	assert game.player1.hero.armor == 7
	assert bow.buffs
	assert bow.durability == 3


def test_explosive_trap():
	game = prepare_game()
	explosivetrap = game.player1.give("EX1_610")
	explosivetrap.play()
	huffer = game.player1.give("NEW1_034")
	huffer.play()
	huffer.attack(game.player2.hero)
	assert game.player2.hero.health == 26
	assert game.player1.hero.health == 30
	assert not huffer.dead
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.end_turn(); game.end_turn()

	assert len(game.player2.field) == 4
	assert explosivetrap in game.player1.secrets
	wisp.attack(game.player1.hero)
	assert explosivetrap not in game.player1.secrets
	assert len(game.player2.field) == 0
	assert game.player2.hero.health == 24
	assert game.player1.hero.health == 30


def test_explosive_trap_truesilver_champion():
	game = prepare_game()
	explosivetrap = game.player1.give("EX1_610")
	explosivetrap.play()
	game.end_turn()

	game.player2.hero.set_current_health(2)
	truesilver = game.player2.give("CS2_097")
	truesilver.play()
	assert explosivetrap in game.player1.secrets
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 2
	game.player2.hero.attack(game.player1.hero)
	assert explosivetrap not in game.player1.secrets
	assert game.player1.hero.health == 26
	assert game.player2.hero.health == 2


def test_explosive_trap_weapon():
	game = prepare_game()
	explosivetrap = game.player1.give("EX1_610")
	explosivetrap.play()
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.player2.give(LIGHTS_JUSTICE).play()
	assert not wisp.dead
	game.player2.hero.attack(game.player1.hero)
	assert wisp.dead
	assert game.player1.hero.health == 30 - 1


def test_eye_for_an_eye():
	game = prepare_game()
	eye_for_eye1 = game.player1.give("EX1_132")
	eye_for_eye1.play()
	game.end_turn()

	stonetusk = game.player2.give("CS2_171")
	eye_for_eye2 = game.player2.give("EX1_132")
	stonetusk.play()
	stonetusk.attack(game.player1.hero)
	assert game.player1.hero.health == 29
	assert game.player2.hero.health == 29
	eye_for_eye2.play()
	game.end_turn()

	hammer = game.player1.give("CS2_094")
	hammer.play(target=game.player2.hero)
	assert game.player2.hero.health == 26
	assert game.player1.hero.health == 26


def test_flare():
	game = prepare_game()
	flare = game.player1.give("EX1_544")
	worgen = game.player1.give("EX1_010")
	worgen.play()
	game.end_turn()

	redemption = game.player2.give("EX1_136")
	redemption.play()
	game.end_turn()

	flare.play()
	assert not game.player1.opponent.secrets
	assert not worgen.stealthed


def test_freezing_trap():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	trap = game.player2.give("EX1_611")
	trap.play()
	assert game.player2.secrets
	game.end_turn()

	assert wisp.cost == 0
	assert not wisp.buffs
	assert wisp.zone == Zone.PLAY
	assert game.player2.hero.health == 30
	assert trap in game.player2.secrets
	wisp.attack(target=game.player2.hero)
	assert trap not in game.player2.secrets
	assert game.player2.hero.health == 30
	assert wisp.zone == Zone.HAND
	assert wisp in game.player1.hand
	assert wisp.buffs
	assert wisp.cost == 2
	assert wisp.zone == Zone.HAND
	wisp.play()
	assert game.player1.used_mana == 2
	assert not wisp.buffs
	assert wisp.cost == 0


def test_ice_barrier():
	game = prepare_game()
	icebarrier = game.player1.give("EX1_289")
	icebarrier2 = game.player1.give("EX1_289")
	friendlywisp = game.player1.give(WISP)
	friendlywisp.play()
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	wisp2 = game.player2.give(WISP)
	wisp2.play()
	game.end_turn()

	assert icebarrier.is_playable()
	icebarrier.play()
	assert not icebarrier2.is_playable()
	assert game.player1.secrets
	assert icebarrier in game.player1.secrets
	assert not game.player1.hero.armor
	game.end_turn(); game.end_turn()

	assert not icebarrier2.is_playable()
	friendlywisp.attack(target=game.player1.opponent.hero)
	assert not game.player1.hero.armor
	assert not game.player1.opponent.hero.armor
	game.end_turn(); game.end_turn()

	friendlywisp.attack(target=wisp2)
	assert not game.player1.hero.armor
	assert not game.player1.opponent.hero.armor
	assert friendlywisp.dead
	assert wisp2.dead
	game.end_turn()

	assert len(game.player1.secrets) == 1
	wisp.attack(target=game.player1.hero)
	assert not game.player1.secrets
	assert game.player1.hero.armor == 7


def test_ice_block():
	game = prepare_game(CardClass.WARRIOR, CardClass.WARRIOR)
	ib = game.player1.give("EX1_295")
	ib.play()
	game.end_turn()

	game.player1.hero.set_current_health(1)
	assert ib in game.player1.secrets
	assert game.player1.hero.health == 1
	game.player2.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 1
	assert game.player1.hero.immune
	assert ib not in game.player1.secrets
	game.end_turn()

	assert not game.player1.hero.immune
	ib2 = game.player1.give("EX1_295")
	ib2.play()
	game.player1.hero.power.use()
	game.end_turn()

	assert game.player1.hero.armor == 2
	assert game.player1.hero.health == 1
	game.player2.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.armor == 1
	assert game.player1.hero.health == 1
	assert ib2 in game.player1.secrets
	game.player2.give(DAMAGE_5).play(target=game.player1.hero)
	assert game.player1.hero.armor == 1
	assert game.player1.hero.health == 1
	assert game.player1.hero.immune
	assert ib2 not in game.player1.secrets


def test_kezan_mystic():
	game = prepare_game()
	kezan = game.player1.give("GVG_074")
	snipe = game.player2.give("EX1_609")
	game.end_turn()

	snipe.play()
	assert snipe in game.player2.secrets
	game.end_turn()

	kezan.play()
	assert not kezan.dead
	assert snipe in game.player1.secrets
	game.end_turn(); game.end_turn()

	kezan2 = game.player1.give("GVG_074")
	kezan2.play()
	assert not kezan2.dead
	assert snipe in game.player1.secrets


def test_mirror_entity():
	game = prepare_game()
	mirror = game.player1.give("EX1_294")
	mirror.play()
	game.end_turn()

	assert mirror in game.player1.secrets
	assert len(game.player1.field) == 0
	game.player2.give(WISP).play()
	assert mirror not in game.player1.secrets
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == WISP


def test_mirror_entity_battlecry():
	game = prepare_game()
	mirror = game.player1.give("EX1_294")
	mirror.play()
	game.end_turn()

	blademaster = game.player2.give("CS2_181")
	blademaster.play()
	assert len(game.player1.field) == len(game.player2.field) == 1
	assert game.player1.field[0].health == game.player2.field[0].health == 3


def test_mirror_entity_bolvar():
	game = prepare_game()
	mirror = game.player1.give("EX1_294")
	mirror.play()
	game.end_turn()

	bolvar = game.player2.give("GVG_063")
	assert bolvar.atk == 1
	wisp = game.player2.summon(WISP)
	game.player2.give(MOONFIRE).play(target=wisp)
	assert bolvar.atk == 2
	bolvar.play()
	assert len(game.player1.field) == len(game.player2.field) == 1
	assert game.player1.field[0].atk == game.player2.field[0].atk == 2


def test_mirror_entity_mind_control_tech():
	game = prepare_game()
	for i in range(3):
		game.player1.give(WISP).play()

	# play mirror entity
	game.player1.give("EX1_294").play()
	game.end_turn()

	# ensure that nothing is stolen (mirror entity triggers after mctech)
	assert len(game.player1.field) == 3
	assert len(game.player2.field) == 0
	game.player2.give("EX1_085").play()
	assert len(game.player1.field) == 4
	assert len(game.player2.field) == 1


def test_mirror_entity_repentance():
	game = prepare_game()
	game.end_turn()

	repentance1 = game.player2.give("EX1_379")
	repentance1.play()
	mirror1 = game.player2.give("EX1_294")
	mirror1.play()
	game.end_turn()

	goldshire1 = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire1.play()
	assert mirror1 not in game.player2.secrets
	assert repentance1 not in game.player2.secrets
	assert goldshire1.health == 1
	assert len(game.player1.field) == len(game.player2.field) == 1
	assert game.player1.field[0].health == game.player2.field[0].health

	game.player1.field[0].destroy()
	game.player2.field[0].destroy()
	game.end_turn()

	mirror2 = game.player2.give("EX1_294")
	mirror2.play()
	repentance2 = game.player2.give("EX1_379")
	repentance2.play()
	game.end_turn()

	goldshire2 = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire2.play()
	assert repentance2 not in game.player2.secrets
	assert mirror2 not in game.player2.secrets
	assert goldshire2.health == 1
	assert len(game.player2.field) == 1
	assert game.player2.field[0].health == 2


def test_mirror_entity_summon_trigger():
	game = prepare_empty_game()
	mirror = game.player2.give("EX1_294")
	mirror.shuffle_into_deck()
	scientist = game.player2.summon("FP1_004")
	kodo = game.player1.give("NEW1_041")
	assert len(game.player2.deck) == 1
	assert len(game.player2.field) == 1
	assert len(game.player1.field) == 0
	assert not scientist.dead
	kodo.play()
	assert len(game.player1.field) == 1
	assert len(game.player2.deck) == 0
	assert len(game.player2.field) == 1
	assert scientist.dead
	assert game.player2.field[0].id == "NEW1_041"


def test_misdirection():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	misdirect = game.player2.give("EX1_533")
	misdirect.play()
	game.end_turn()

	wisp.attack(game.player2.hero)
	assert game.player2.hero.health == 30
	assert game.player1.hero.health == 30 - 1
	assert misdirect not in game.player2.secrets


def test_noble_sacrifice():
	game = prepare_game()
	sacrifice = game.player1.give("EX1_130")
	sacrifice.play()
	wisp = game.player2.summon(WISP)
	game.end_turn()

	assert sacrifice in game.player1.secrets
	assert not wisp.dead
	assert len(game.player1.field) == 0
	assert len(game.player2.field) == 1
	wisp.attack(game.player1.hero)
	assert sacrifice not in game.player1.secrets
	assert wisp.dead
	assert len(game.player1.field) == len(game.player2.field) == 0


def test_redemption():
	game = prepare_game()
	redemption = game.player1.give("EX1_136")
	redemption.play()
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	footman.play()
	game.end_turn()

	assert footman.health == 2
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	footman.destroy()
	assert redemption not in game.player1.secrets
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	target = game.player1.field[0]
	assert target.id == GOLDSHIRE_FOOTMAN
	assert target.health == 1


def test_repentance():
	game = prepare_game()
	repentance = game.player1.give("EX1_379")
	repentance.play()
	game.end_turn()

	spellbendert1 = game.player2.summon(SPELLBENDERT)
	assert repentance in game.player1.secrets
	assert spellbendert1.health == 3
	assert spellbendert1.max_health == 3

	spellbendert2 = game.player2.give(SPELLBENDERT)
	spellbendert2.play()
	assert repentance not in game.player1.secrets
	assert spellbendert2.health == 1
	assert spellbendert2.max_health == 1


def test_sacred_trial():
	game = prepare_game()
	trial = game.player1.give("LOE_027")
	trial.play()
	game.end_turn()

	for i in range(4):
		game.player2.give(WISP).play()
	assert trial not in game.player1.secrets
	assert len(game.player2.field) == 3


def test_sacred_trial_dr_boom():
	game = prepare_game()
	trial = game.player1.give("LOE_027")
	trial.play()
	game.end_turn()

	game.player2.give(WISP).play()
	boom = game.player2.give("GVG_110")
	boom.play()
	assert trial not in game.player1.secrets
	assert len(game.player2.field) == 3
	assert boom.dead


def test_sacred_trial_deathwing():
	game = prepare_game()
	trial = game.player1.give("LOE_027")
	trial.play()
	game.end_turn()

	for i in range(3):
		game.player2.give(WISP).play()
	deathwing = game.player2.give("NEW1_030")
	deathwing.play()
	assert trial in game.player1.secrets
	assert len(game.player2.field) == 1


def test_secretkeeper():
	game = prepare_game()
	secretkeeper = game.player1.give("EX1_080")
	secretkeeper.play()
	assert secretkeeper.atk == 1
	assert secretkeeper.health == 2
	icebarrier = game.player1.give("EX1_289")
	icebarrier.play()
	assert secretkeeper.atk == 2
	assert secretkeeper.health == 3
	game.player1.give(THE_COIN).play()
	game.player1.give(WISP).play()
	assert secretkeeper.atk == 2
	assert secretkeeper.health == 3


def test_snake_trap():
	game = prepare_game()
	snaketrap = game.player1.give("EX1_554")
	wisp = game.player1.give(WISP)
	snaketrap.play()
	wisp.play()
	game.end_turn()

	stonetusk = game.player2.give("CS2_171")
	stonetusk.play().attack(wisp)
	assert len(game.player2.field) == 0
	assert game.player1.field.contains("EX1_554t")
	assert len(game.player1.field) == 3
	assert stonetusk.health == 1
	assert wisp.dead


def test_snipe():
	game = prepare_game()
	snipe1 = game.player1.give("EX1_609")
	snipe1.play()
	game.end_turn()

	tidehunter = game.player2.give("EX1_506")
	tidehunter.play()
	assert tidehunter.dead
	assert len(game.player2.field) == 1
	snipe2 = game.player2.give("EX1_609")
	snipe2.play()
	game.end_turn()

	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	assert not statue.dead
	assert statue.health == 10 - 4


def test_snipe_druid_of_the_claw():
	game = prepare_game()
	snipe = game.player1.give("EX1_609")
	snipe.play()
	game.end_turn()

	druid = game.player2.give("EX1_165")
	druid.play(choose="EX1_165b")
	assert snipe not in game.player1.secrets
	assert len(game.player2.field) == 1
	assert druid.morphed is game.player2.field[0]
	assert druid.morphed.id == "EX1_165t2"
	assert druid.morphed.damage == 4
	assert not druid.damage


def test_spellbender():
	game = prepare_game()
	spellbender = game.player1.give("tt_010")
	spellbender.play()
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	game.end_turn()

	assert game.player1.hero.health == 30
	game.player2.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 29
	assert spellbender in game.player1.secrets
	assert goldshire.health == 2
	assert len(game.player1.field) == 1
	game.player2.give(MOONFIRE).play(target=goldshire)
	assert spellbender not in game.player1.secrets
	assert goldshire.health == 2
	assert len(game.player1.field) == 2
	target = game.player1.field[1]
	assert target.id == "tt_010a"
	assert target.max_health == 3
	assert target.health == 2


def test_spellbender_echo_of_medivh():
	game = prepare_game()
	game.player1.discard_hand()
	spellbender = game.player1.give("tt_010")
	spellbender.play()
	game.end_turn()

	game.player2.discard_hand()
	wisp = game.player2.give(WISP)
	echo = game.player2.give("GVG_005")
	wisp.play()
	echo.play()

	assert spellbender in game.player1.secrets
	assert len(game.player2.hand) == 1
	assert game.player2.hand[0].id == WISP


def test_vaporize():
	game = prepare_game()
	vaporize = game.player1.give("EX1_594")
	game.end_turn()

	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	vaporize.play()
	assert game.player1.secrets[0] == vaporize
	game.end_turn()

	assert len(game.player1.secrets) == 1
	game.player2.give(LIGHTS_JUSTICE).play()
	game.player2.hero.attack(target=game.player1.hero)
	assert game.player1.hero.health == 30 - 1
	assert vaporize in game.player1.secrets
	wisp.attack(target=game.player1.hero)
	assert vaporize not in game.player1.secrets
	assert wisp.dead
	assert game.player1.hero.health == 30 - 1
