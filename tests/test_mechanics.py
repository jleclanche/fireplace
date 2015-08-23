from utils import *
from fireplace.cards.utils import Give, JOUST


def test_armor():
	game = prepare_game(WARRIOR, WARRIOR)
	assert game.current_player.hero.armor == 0
	assert not game.current_player.hero.power.exhausted
	assert game.current_player.hero.power.is_usable()
	game.current_player.hero.power.use()
	assert game.current_player.hero.power.exhausted
	assert not game.current_player.hero.power.is_usable()
	assert game.current_player.hero.armor == 2
	game.end_turn()

	axe = game.current_player.give("CS2_106")
	axe.play()
	assert axe is game.current_player.weapon
	assert axe in game.current_player.hero.slots
	assert game.current_player.hero.atk == 3
	game.current_player.hero.attack(game.current_player.opponent.hero)
	assert game.current_player.opponent.hero.health == 29
	assert game.current_player.opponent.hero.armor == 0


def test_auras():
	game = prepare_game()
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	assert wisp1.atk == 1
	game.end_turn()

	webspinner = game.current_player.give("FP1_011")
	webspinner.play()
	raidleader = game.current_player.give("CS2_122")
	raidleader.play()
	assert raidleader.aura
	assert raidleader.atk == 2
	assert wisp1.atk == 1
	assert webspinner.atk == 2
	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	assert webspinner.atk == 2

	# Test the timber wolf (beast-only) too
	timberwolf = game.current_player.give("DS1_175")
	timberwolf.play()
	assert timberwolf.atk == 1 + 1
	assert raidleader.atk == 2
	assert len(webspinner.buffs) == 2
	assert webspinner.atk == 1 + 1 + 1
	assert wisp2.atk == 1 + 1

	timberwolf2 = game.current_player.give("DS1_175")
	timberwolf2.play()
	assert timberwolf.atk == 3
	assert timberwolf2.atk == 3
	game.current_player.give(MOONFIRE).play(target=timberwolf)
	timberwolf2.atk == 2
	game.current_player.give(MOONFIRE).play(target=timberwolf2)


def test_bounce():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert game.player1.field == [wisp]
	brewmaster1 = game.player1.give("EX1_049")
	brewmaster1.play(target=wisp)
	assert game.player1.field == [brewmaster1]
	assert wisp in game.player1.hand
	assert wisp.zone == Zone.HAND
	wisp.discard()

	# test for damage reset on bounce
	brewmaster2 = game.player1.give("EX1_049")
	moonfire = game.player1.give(MOONFIRE)
	moonfire.play(target=brewmaster1)
	assert brewmaster1.health == 1
	brewmaster2.play(target=brewmaster1)
	assert brewmaster1.health == 2
	assert brewmaster2.health == 2
	brewmaster1.discard()
	game.end_turn();

	# fill the hand with some bananas
	for i in range(10):
		game.player1.give("EX1_014t")
	assert len(game.player1.hand) == 10
	vanish = game.player2.give("NEW1_004")
	vanish.play()
	assert len(game.player1.hand) == 10
	assert brewmaster2 not in game.player1.hand
	assert brewmaster2 in game.player1.graveyard
	assert brewmaster2 in game.graveyard


def test_card_draw():
	game = prepare_game()
	# pass turn 1
	game.end_turn(); game.end_turn()

	assert game.current_player.cards_drawn_this_turn == 1
	assert len(game.current_player.hand) == 5
	novice = game.current_player.give("EX1_015")
	assert len(game.current_player.hand) == 6
	# novice should draw 1 card
	novice.play()
	# hand should be 1 card played, 1 card drawn; same size
	assert len(game.current_player.hand) == 6
	assert game.current_player.cards_drawn_this_turn == 2
	game.end_turn()

	# succubus should discard 1 card
	card = game.current_player.give("EX1_306")
	handlength = len(game.current_player.hand)
	card.play()
	assert len(game.current_player.hand) == handlength - 2


def test_cant_draw():
	game = prepare_game()
	game.player1.discard_hand()
	game.player1.cant_draw = True
	game.end_turn(); game.end_turn()

	assert len(game.player1.hand) == 0
	game.end_turn(); game.end_turn()

	assert len(game.player1.hand) == 0
	game.player1.cant_draw = False
	game.end_turn(); game.end_turn()

	assert len(game.player1.hand) == 1


def test_charge():
	game = prepare_game()
	wisp = game.current_player.give(WISP)
	wisp.play()
	assert not wisp.charge
	assert not wisp.can_attack()
	# play Charge on wisp
	game.current_player.give("CS2_103").play(target=wisp)
	assert wisp.buffs[0].tags[GameTag.CHARGE]
	assert wisp.charge
	assert wisp.can_attack()
	wisp.attack(game.current_player.opponent.hero)
	assert not wisp.can_attack()
	game.end_turn()

	stonetusk = game.current_player.give("CS2_171")
	stonetusk.play()
	assert stonetusk.charge
	assert stonetusk.can_attack()
	game.end_turn()
	assert wisp.can_attack()
	wisp.attack(game.current_player.opponent.hero)
	assert not wisp.can_attack()
	game.end_turn()

	watcher = game.current_player.give("EX1_045")
	watcher.play()
	assert not watcher.can_attack()
	game.current_player.give("CS2_103").play(target=watcher)
	assert not watcher.can_attack()
	game.end_turn(); game.end_turn()

	assert not watcher.can_attack()
	watcher.silence()
	assert watcher.can_attack()


def test_combo():
	game = prepare_game()
	game.end_turn(); game.end_turn()
	game.end_turn()

	game.current_player.hand.filter(id=THE_COIN)[0].play()
	# SI:7 with combo
	assert game.current_player.combo
	game.current_player.give("EX1_134").play(target=game.current_player.hero)
	assert game.current_player.hero.health == 28
	game.end_turn()

	# Without combo should not have a target
	assert not game.current_player.combo
	game.current_player.give("EX1_134").play()


def test_deathrattle():
	game = prepare_game()
	loothoarder = game.current_player.give("EX1_096")
	loothoarder.play()
	cardcount = len(game.current_player.hand)
	game.end_turn()

	archer = game.current_player.give("CS2_189")
	archer.play(target=loothoarder)
	assert loothoarder.dead
	assert loothoarder.damage == 0
	assert len(game.current_player.opponent.hand) == cardcount + 1
	game.end_turn(); game.end_turn()
	game.end_turn(); game.end_turn()

	# test soul of the forest: deathrattle in slots
	assert not archer.has_deathrattle
	sotf = game.current_player.give("EX1_158")
	sotf.play()
	assert len(archer.buffs) == 1
	assert archer.buffs[0].has_deathrattle
	assert archer.has_deathrattle
	assert len(game.current_player.field) == 1
	game.current_player.give(MOONFIRE).play(target=archer)
	assert archer.dead
	assert len(game.current_player.field) == 1


def test_discard_enchanted_cards():
	# Test for bug #58
	game = prepare_game()
	deathwing = game.player1.give("NEW1_030")
	thaurissan = game.player1.give("BRM_028")
	thaurissan.play()
	game.end_turn(); game.end_turn()

	assert deathwing.cost == 9
	deathwing.play()
	assert not game.player1.hand


def test_divine_shield():
	game = prepare_game()
	squire = game.current_player.give("EX1_008")
	squire.play()
	assert squire.divine_shield
	game.current_player.give(MOONFIRE).play(target=squire)
	assert len(game.current_player.field) == 1
	assert not squire.divine_shield
	game.current_player.give(MOONFIRE).play(target=squire)
	assert len(game.current_player.field) == 0
	assert not squire.divine_shield
	game.end_turn(); game.end_turn()

	# test damage events with Divine Shield
	gurubashi = game.current_player.summon("EX1_399")
	assert gurubashi.atk == 2
	assert gurubashi.health == 7
	assert not gurubashi.divine_shield
	prot = game.current_player.give(HAND_OF_PROTECTION)
	prot.play(target=gurubashi)
	assert gurubashi.divine_shield
	game.current_player.give(MOONFIRE).play(target=gurubashi)
	assert not gurubashi.divine_shield
	assert gurubashi.atk == 2
	assert gurubashi.health == 7


def test_freeze():
	game = prepare_game()
	flameimp = game.current_player.give("EX1_319")
	flameimp.play()
	game.end_turn()

	frostshock = game.current_player.give("CS2_037")
	frostshock.play(target=flameimp)
	assert flameimp.frozen
	game.end_turn()

	assert flameimp.frozen
	assert not flameimp.can_attack()
	game.end_turn()
	assert not flameimp.frozen
	game.end_turn()

	wisp = game.current_player.give(WISP)
	wisp.play()
	wisp.frozen = True
	assert wisp.frozen
	game.end_turn()
	assert not wisp.frozen


def test_graveyard_minions():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player2.summon(WISP)
	game.end_turn(); game.end_turn()
	wisp1.attack(target=wisp2)
	assert wisp1 in game.player1.graveyard
	assert wisp1 not in game.player2.graveyard
	assert wisp1 in game.graveyard
	assert wisp2 in game.player2.graveyard
	assert wisp2 not in game.player1.graveyard
	assert wisp2 in game.graveyard
	wisp3 = game.player1.give(WISP)
	wisp3.discard()
	assert wisp3 not in game.player1.graveyard
	assert wisp3 not in game.graveyard


def test_graveyard_weapons():
	game = prepare_game()
	axe1 = game.player1.give("CS2_106")
	axe1.play()
	axe2 = game.player1.summon("CS2_106")
	assert axe1.dead
	assert axe1 in game.player1.graveyard
	assert axe1 not in game.player2.graveyard
	assert axe1 in game.graveyard
	for i in range(2):
		game.player1.hero.attack(game.player2.hero)
	assert axe2.dead
	assert axe2 in game.player1.graveyard
	assert axe2 not in game.player2.graveyard
	assert axe2 in game.graveyard


def test_graveyard_secrets():
	game = prepare_game()
	snipe = game.player1.give("EX1_609")
	snipe.play()
	game.end_turn()
	wisp = game.player2.give(WISP)
	wisp.play()
	assert wisp.dead
	assert snipe in game.player1.graveyard
	assert snipe not in game.player2.graveyard
	assert snipe in game.graveyard
	assert wisp in game.player2.graveyard
	assert wisp not in game.player1.graveyard
	assert wisp in game.graveyard


def test_joust():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.shuffle_into_deck()
	wisp2 = game.player1.give(WISP)
	wisp2.shuffle_into_deck()
	game.end_turn()

	goldshire = game.player2.give(GOLDSHIRE_FOOTMAN)
	goldshire.shuffle_into_deck()
	game.queue_actions(game.player2, [JOUST & Give(game.player2, TARGET_DUMMY)])
	assert game.player2.hand.filter(id=TARGET_DUMMY)
	game.end_turn()

	game.queue_actions(game.player1, [JOUST & Give(game.player1, TARGET_DUMMY)])
	assert not game.player1.hand.filter(id=TARGET_DUMMY)


def test_mana():
	game = prepare_game(game_class=Game)
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	assert footman.cost == 1
	footman.play()
	assert footman.atk == 1
	assert footman.health == 2
	game.end_turn()

	# Play the coin
	coin = game.player2.hand.filter(id=THE_COIN)[0]
	coin.play()
	assert game.player2.mana == 2
	assert game.player2.temp_mana == 1
	game.end_turn()

	assert game.player2.temp_mana == 0
	assert game.player2.mana == 1
	game.end_turn(); game.end_turn()

	assert game.player1.mana == 3
	assert game.player1.max_mana == 3
	felguard = game.player1.give("EX1_301")
	felguard.play()
	assert game.player1.mana == 0
	assert game.player1.max_mana == 2

	for i in range(10):
		game.end_turn(); game.end_turn()

	assert game.player1.mana == game.player1.max_resources == 10
	assert game.player2.mana == game.player2.max_resources == 10


def test_morph():
	game = prepare_game()
	game.end_turn()

	buzzard = game.player2.give("CS2_237")
	buzzard.play()
	wisp = game.player2.give(WISP)
	wisp.play()
	game.end_turn()

	game.player1.discard_hand()
	game.player2.discard_hand()
	assert not game.player1.hand
	assert not game.player2.hand
	hex = game.player1.give("EX1_246")
	hex.play(target=wisp)
	assert not game.player2.field.contains(WISP)
	assert game.player2.field.contains("hexfrog")
	# Test that buzzard no longer draws on poly/hex (fixed in GVG)
	assert not game.player2.hand
	game.end_turn(); game.end_turn()

	assert len(game.player2.hand) == 1
	polymorph = game.player1.give("CS2_022")
	polymorph.play(target=game.player2.field[-1])
	assert game.player2.field[-1].id == "CS2_tk1"
	assert len(game.current_player.opponent.hand) == 1


def test_overload():
	game = prepare_game(game_class=Game)
	dustdevil = game.player1.give("EX1_243")
	dustdevil.play()
	assert game.player1.overloaded == 2
	game.end_turn(); game.end_turn()
	assert game.player1.overloaded == 0
	assert game.player1.overload_locked == 2
	assert game.current_player.mana == 0


def test_poisonous():
	game = prepare_game()
	game.end_turn()

	cobra = game.current_player.give("EX1_170")
	cobra.play()
	assert cobra.poisonous
	game.end_turn()
	zchow = game.current_player.give("FP1_001")
	zchow.play()
	zchow2 = game.current_player.give("FP1_001")
	zchow2.play()
	game.end_turn()
	cobra.attack(target=zchow)
	assert zchow not in game.current_player.opponent.field
	assert zchow.dead
	game.end_turn()
	zchow2.attack(target=cobra)
	assert zchow2.dead

	# test silencing the cobra
	zchow3 = game.current_player.give("FP1_001")
	zchow3.play()
	game.end_turn()
	cobra = game.current_player.give("EX1_170")
	cobra.play()
	cobra.silence()
	game.end_turn()
	zchow3.attack(cobra)
	assert zchow3 in game.current_player.field
	assert cobra in game.current_player.opponent.field


def test_positioning():
	game = prepare_game()
	wisp1 = game.current_player.give(WISP)
	wisp1.play()
	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	wisp3 = game.current_player.give(WISP)
	wisp3.play()

	assert wisp1.adjacent_minions == [wisp2]
	assert wisp2.adjacent_minions == [wisp1, wisp3]
	assert wisp3.adjacent_minions == [wisp2]
	game.end_turn(); game.end_turn()
	flametongue = game.current_player.give("EX1_565")
	flametongue.play()
	wisp4 = game.current_player.give(WISP)
	wisp4.play()
	assert flametongue.aura
	assert wisp3.buffs, wisp3.buffs
	assert wisp1.atk == 1, wisp1.atk
	assert wisp2.atk == 1
	assert wisp3.atk == 3, wisp3.atk
	assert flametongue.atk == 0, flametongue.atk
	assert flametongue.adjacent_minions == [wisp3, wisp4]
	assert wisp4.atk == 3, wisp4.atk


def test_silence():
	game = prepare_game()
	silence = game.current_player.give(SILENCE)
	thrallmar = game.current_player.give("EX1_021")
	thrallmar.play()
	assert not thrallmar.silenced
	assert thrallmar.windfury
	silence.play(target=thrallmar)
	assert thrallmar.silenced
	assert not thrallmar.windfury


def test_silence_deathrattle():
	game = prepare_game()
	egg = game.player1.give("FP1_007")
	egg.play()
	assert len(game.player1.field) == 1
	game.player1.give(SILENCE).play(target=egg)
	game.player1.give(MOONFIRE).play(target=egg)
	game.player1.give(MOONFIRE).play(target=egg)
	assert egg.dead
	assert len(game.player1.field) == 0


def test_spell_power():
	game = prepare_game(HUNTER, HUNTER)

	expected_health = 30
	assert game.player2.hero.health == expected_health
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 1
	assert game.player2.hero.health == expected_health
	# Play a kobold
	assert game.player1.spellpower == 0
	game.player1.give(KOBOLD_GEOMANCER).play()
	assert game.player1.spellpower == 1
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 1 + 1
	assert game.player2.hero.health == expected_health
	# Summon Malygos
	malygos = game.player1.summon("EX1_563")
	assert game.player1.spellpower == 1 + 5
	game.player1.give(MOONFIRE).play(target=game.player2.hero)
	expected_health -= 1 + 1 + 5
	assert game.player2.hero.health == expected_health
	# Test heals are not affected
	game.player1.give(RESTORE_1).play(target=game.player2.hero)
	expected_health += 1
	assert game.player2.hero.health == expected_health
	game.end_turn(); game.end_turn()

	# Check hero power is unaffected
	game.player1.hero.power.use()
	expected_health -= 2
	assert game.player2.hero.health == expected_health
	# Check battlecries are unaffected
	game.player1.give("CS2_189").play(target=game.player2.hero)
	expected_health -= 1
	assert game.player2.hero.health == expected_health
	game.end_turn(); game.end_turn()

	malygos.destroy()
	# Check arcane missiles doesn't wreck everything
	game.player1.give("EX1_277").play()
	expected_health -= 3 + 1
	assert game.player2.hero.health == expected_health


def test_stealth_windfury():
	game = prepare_game(MAGE, MAGE)
	worgen = game.current_player.give("EX1_010")
	worgen.play()
	assert worgen.stealthed
	assert not worgen.can_attack()
	game.end_turn(); game.end_turn()
	game.end_turn()

	archer = game.current_player.give("CS2_189")
	assert len(archer.targets) == 2  # Only the heroes
	assert len(game.current_player.hero.power.targets) == 2
	game.end_turn()

	worgen.attack(game.current_player.opponent.hero)
	assert not worgen.stealthed
	assert not worgen.can_attack()
	windfury = game.current_player.give("CS2_039")
	windfury.play(target=worgen)
	assert worgen.windfury
	assert worgen.num_attacks == 1
	assert worgen.can_attack()
	worgen.attack(game.current_player.opponent.hero)
	assert not worgen.can_attack()
	game.end_turn()

	assert len(archer.targets) == 3


def test_tags():
	game = prepare_game()
	alakir = game.current_player.give("NEW1_010")
	alakir.play()
	assert alakir.tags[GameTag.CHARGE]
	assert alakir.charge
	assert alakir.tags[GameTag.DIVINE_SHIELD]
	assert alakir.divine_shield
	assert alakir.tags[GameTag.TAUNT]
	assert alakir.taunt
	assert alakir.tags[GameTag.WINDFURY]
	assert alakir.windfury


def test_taunt():
	game = prepare_game()
	goldshire1 = game.player1.give(GOLDSHIRE_FOOTMAN)
	wisp1 = game.player1.summon(WISP)
	goldshire2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	wisp2 = game.player2.summon(WISP)
	game.end_turn(); game.end_turn()

	assert wisp1.can_attack()
	assert wisp1.targets == [wisp2, game.player2.hero]
	game.end_turn()

	goldshire2.play()
	game.end_turn()

	assert wisp1.targets == [goldshire2]
	goldshire1.play()
	game.end_turn()

	assert wisp2.targets == [goldshire1]
