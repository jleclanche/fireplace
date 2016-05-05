from utils import *
from fireplace.cards.utils import Give, JOUST


def test_armor():
	game = prepare_game(CardClass.WARRIOR, CardClass.WARRIOR)
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
	assert webspinner.atk == 1
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
	assert webspinner.atk == 4
	game.current_player.give(MOONFIRE).play(target=timberwolf)
	assert timberwolf2.atk == 2
	assert webspinner.atk == 3
	game.current_player.give(MOONFIRE).play(target=timberwolf2)
	assert webspinner.atk == 2


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
	game.end_turn()

	# fill the hand with some bananas
	for i in range(10):
		game.player1.give("EX1_014t")
	assert len(game.player1.hand) == 10
	vanish = game.player2.give("NEW1_004")
	vanish.play()
	assert len(game.player1.hand) == 10
	assert brewmaster2 not in game.player1.hand
	assert brewmaster2 not in game.player1.field
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

	assert game.current_player.cards_drawn_this_turn == 1
	# succubus should discard 1 card
	card = game.current_player.give("EX1_306")
	handlength = len(game.current_player.hand)
	card.play()
	assert len(game.current_player.hand) == handlength - 2
	# Discarding a card should not effect the number of cards drawn.
	assert game.current_player.cards_drawn_this_turn == 1


def test_cant_draw():
	game = prepare_game()

	assert len(game.player1.hand)
	game.player1.discard_hand()

	assert len(game.player1.hand) == 0
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
	# Play Charge on Wisp
	game.current_player.give("CS2_103").play(target=wisp)
	assert wisp.buffs[0].tags[GameTag.CHARGE]
	assert wisp.charge
	assert wisp.can_attack()
	wisp.attack(game.current_player.opponent.hero)
	assert wisp.charge
	assert not wisp.can_attack()
	game.end_turn()

	stonetusk = game.current_player.give("CS2_171")
	stonetusk.play()
	assert stonetusk.charge
	assert stonetusk.can_attack()
	game.end_turn()
	assert wisp.charge
	assert wisp.can_attack()
	wisp.attack(game.current_player.opponent.hero)
	assert not wisp.can_attack()
	game.end_turn()

	watcher = game.current_player.give("EX1_045")
	watcher.play()
	assert not watcher.can_attack()

	# Play Charge on Ancient Watcher
	game.current_player.give("CS2_103").play(target=watcher)
	assert watcher.charge
	assert not watcher.can_attack()
	game.end_turn(); game.end_turn()

	assert not watcher.can_attack()
	watcher.silence()
	assert watcher.can_attack()


def test_choices():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	moonfire = game.player1.give(MOONFIRE)
	game.player1.give(LIGHTS_JUSTICE).play()
	game.end_turn(); game.end_turn()

	assert wisp.can_attack()
	assert moonfire.is_playable()
	assert game.player1.hero.can_attack()
	assert game.player1.hero.power.is_usable()

	tracking = game.player1.give("DS1_184")
	tracking.play()
	assert game.player1.choice

	assert not wisp.can_attack()
	assert not moonfire.is_playable()
	assert not game.player1.hero.can_attack()
	assert not game.player1.hero.power.is_usable()

	game.player1.choice.choose(random.choice(game.player1.choice.cards))
	assert not game.player1.choice

	assert wisp.can_attack()
	assert moonfire.is_playable()
	assert game.player1.hero.can_attack()
	assert game.player1.hero.power.is_usable()


def test_combo():
	game = prepare_game()
	game.end_turn()

	assert not game.current_player.combo
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

	assert loothoarder.damage == 0
	assert not loothoarder.dead
	archer = game.current_player.give("CS2_189")
	archer.play(target=loothoarder)
	# Minions restore to full health when in graveyard.
	assert loothoarder in game.player1.graveyard
	assert loothoarder.damage == 0
	assert loothoarder.dead
	assert len(game.current_player.opponent.hand) == cardcount + 1
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


def test_discover():
	# TODO: use different classes for each player and force player 1 to go first
	game = prepare_empty_game(CardClass.PRIEST, CardClass.PRIEST)

	# Museum Curator
	assert game.player1.choice == None
	curator = game.player1.give("LOE_006")
	curator.play()
	assert not game.player1.choice == None
	assert len(game.player1.choice.cards) == 3

	for card in game.player1.choice.cards:
		assert (fireplace.cards.db[card].card_class == CardClass.NEUTRAL
				or fireplace.cards.db[card].card_class == CardClass.PRIEST)
		assert fireplace.cards.db[card].deathrattle == True

	choice = random.choice(game.player1.choice.cards)
	game.player1.choice.choose(choice)
	assert game.player1.choice == None
	assert len(game.player1.hand) == 1


def test_divine_shield():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	squire = game.player1.give("EX1_008")
	squire.play()
	assert squire.divine_shield
	game.player1.give(MOONFIRE).play(target=squire)
	assert len(game.player1.field) == 1
	assert not squire.divine_shield
	game.player1.give(MOONFIRE).play(target=squire)
	assert len(game.player1.field) == 0
	assert not squire.divine_shield
	game.end_turn(); game.end_turn()

	# test spell damage events with Divine Shield
	gurubashi = game.player1.summon("EX1_399")
	assert gurubashi.atk == 2
	assert gurubashi.health == 7
	assert not gurubashi.divine_shield
	game.player1.give(HAND_OF_PROTECTION).play(target=gurubashi)
	assert gurubashi.divine_shield
	game.player1.give(MOONFIRE).play(target=gurubashi)
	assert not gurubashi.divine_shield
	assert gurubashi.atk == 2
	assert gurubashi.health == 7

	# test hero power damage events with Divine Shield
	game.player1.give(HAND_OF_PROTECTION).play(target=gurubashi)
	assert gurubashi.divine_shield
	game.end_turn()

	game.player2.hero.power.use(target=gurubashi)
	assert not gurubashi.divine_shield
	assert gurubashi.atk == 2
	assert gurubashi.health == 7
	game.end_turn()

	# test combat damage events with Divine Shield
	wisp = game.player2.summon(WISP)
	game.player1.give(HAND_OF_PROTECTION).play(target=gurubashi)
	assert gurubashi.divine_shield
	gurubashi.attack(target=wisp)
	assert wisp.dead
	assert not gurubashi.divine_shield
	assert gurubashi.atk == 2
	assert gurubashi.health == 7


def test_fatigue():
	game = prepare_game()
	game.player1.fatigue()
	assert game.player1.hero.health == 30 - 1
	game.player1.fatigue()
	assert game.player1.hero.health == 30 - 1 - 2
	game.player1.fatigue()
	assert game.player1.hero.health == 30 - 1 - 2 - 3
	assert game.player2.hero.health == 30

	# Draw the deck
	game.player1.draw(26)
	assert game.player1.hero.health == 30 - 1 - 2 - 3
	game.player1.draw(1)
	assert game.player1.hero.health == 30 - 1 - 2 - 3 - 4
	game.end_turn(); game.end_turn()
	assert game.player1.hero.health == 30 - 1 - 2 - 3 - 4 - 5


def test_freeze():
	game = prepare_game()
	flameimp = game.current_player.give("EX1_319")
	flameimp.play()
	wisp = game.current_player.give(WISP)
	wisp.play()
	wisp2 = game.current_player.give(WISP)
	wisp2.play()
	game.end_turn()

	# Unfreeze at end of owner's turn, if it could have attacked (but didn't).
	frostshock = game.current_player.give("CS2_037")
	frostshock.play(target=flameimp)
	assert flameimp.frozen
	game.end_turn()

	assert flameimp.frozen
	assert not flameimp.can_attack()
	game.end_turn()

	assert not flameimp.frozen
	game.end_turn()

	assert wisp.can_attack()
	wisp.frozen = True
	assert not wisp.can_attack()

	assert wisp2.can_attack()
	wisp2.attack(target=game.current_player.opponent.hero)
	assert not wisp2.can_attack()
	wisp2.frozen = True

	wisp3 = game.current_player.give(WISP)
	wisp3.play()
	assert not wisp3.can_attack()
	wisp3.frozen = True
	assert wisp3.frozen
	game.end_turn()
	assert not wisp.frozen
	assert wisp2.frozen
	assert wisp3.frozen


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
	game.player1.hero.attack(game.player2.hero)
	game.end_turn(); game.end_turn()

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

	# Jouster loses by default if she has no minions left.
	game.queue_actions(game.player1, [JOUST & Give(game.player1, TARGET_DUMMY)])
	assert not game.player1.hand.filter(id=TARGET_DUMMY)

	wisp = game.player1.give(WISP)
	wisp.shuffle_into_deck()
	wisp2 = game.player1.give(WISP)
	wisp2.shuffle_into_deck()

	# Jouster wins by default if opponent has no minions left.
	game.queue_actions(game.player1, [JOUST & Give(game.player1, TARGET_DUMMY)])
	assert game.player1.hand.filter(id=TARGET_DUMMY)
	game.player1.hand.filter(id=TARGET_DUMMY)[0].play()
	game.end_turn()

	# Joust succeeds: 1 > 0
	goldshire = game.player2.give(GOLDSHIRE_FOOTMAN)
	goldshire.shuffle_into_deck()
	game.queue_actions(game.player2, [JOUST & Give(game.player2, TARGET_DUMMY)])
	assert game.player2.hand.filter(id=TARGET_DUMMY)
	game.end_turn()

	# Joust fails: 0 <= 1
	game.queue_actions(game.player1, [JOUST & Give(game.player1, TARGET_DUMMY)])
	assert not game.player1.hand.filter(id=TARGET_DUMMY)


def test_mana():
	game = prepare_game(game_class=Game)
	footman = game.player1.give(GOLDSHIRE_FOOTMAN)
	assert footman.cost == 1
	assert game.player1.mana == 1
	footman.play()
	assert game.player1.mana == 0
	assert footman.atk == 1
	assert footman.health == 2
	game.end_turn()

	# Play the coin
	coin = game.player2.hand.filter(id=THE_COIN)[0]
	coin2 = game.player2.give(THE_COIN)
	wisp = game.player2.give(WISP)
	footman2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	assert game.player2.mana == 1
	assert game.player2.temp_mana == 0
	coin.play()
	coin2.play()
	assert game.player2.mana == 3
	assert game.player2.temp_mana == 2
	wisp.play()
	assert game.player2.mana == 3
	assert game.player2.temp_mana == 2
	footman2.play()
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

	wisp = game.player2.give(WISP)
	wisp.play()
	buzzard = game.player2.give("CS2_237")
	buzzard.play()
	game.end_turn()

	game.player1.discard_hand()
	game.player2.discard_hand()
	assert not game.player1.hand
	assert not game.player2.hand
	hex = game.player1.give("EX1_246")
	hex.play(target=wisp)
	assert not game.player2.field.contains(WISP)
	assert game.player2.field[0].id == "hexfrog"
	# Test that buzzard no longer draws on poly/hex (fixed in GVG)
	assert not game.player2.hand
	game.end_turn(); game.end_turn()

	assert len(game.player2.hand) == 1
	polymorph = game.player1.give("CS2_022")
	polymorph.play(target=game.player2.field[-1])
	assert game.player2.field[-1].id == "CS2_tk1"
	assert len(game.current_player.opponent.hand) == 1


def test_mulligan():
	# Create and start a game but do not perform the mulligan yet
	game = init_game(game_class=Game)
	game.start()
	hand1 = game.player1.hand[:]
	hand2 = game.player2.hand[:]
	# Double-check no player has The Coin (yet)
	assert not game.player1.hand.contains(THE_COIN)
	assert not game.player2.hand.contains(THE_COIN)
	assert len(hand1) == 3
	assert len(hand2) == 4
	# Do not choose anything for player 1
	game.player1.choice.choose()
	assert game.player1.hand == hand1

	# Replace the first two cards for player 2
	game.player2.choice.choose(hand2[0], hand2[1])
	assert hand2[0] not in game.player2.hand
	assert hand2[1] not in game.player2.hand
	assert hand2[2] in game.player2.hand
	assert hand2[3] in game.player2.hand
	assert game.player2.hand[4] == THE_COIN


def test_no_death_processing_during_battlecry():
	game = prepare_game()
	illidan = game.player1.give("EX1_614")
	illidan.play()
	juggler = game.player1.give("NEW1_019")
	juggler.play()
	game.end_turn()

	acolyte = game.player2.give("EX1_007")
	acolyte.play()
	acolyte.set_current_health(1)
	game.end_turn()

	game.player2.discard_hand()
	infernal = game.player1.give("CS2_064")
	infernal.play()
	# Check that the acolyte never draws twice
	# Either the juggler hits it and it dies before the battlecry
	# or the dread infernal hits it.
	assert len(game.player2.hand) == 1


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


def test_powered_up():
	game = prepare_game()
	minion = game.player1.give(WISP)
	spell = game.player1.give(MOONFIRE)
	weapon = game.player1.give(LIGHTS_JUSTICE)
	killcommand = game.player1.give("EX1_539")
	assert not minion.powered_up
	assert not spell.powered_up
	assert not weapon.powered_up
	assert not killcommand.powered_up
	game.player1.summon(CHICKEN)
	assert killcommand.powered_up


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


def test_silence_multiple_buffs():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert wisp.atk == 1
	# Play Blessing of Might (+3 attack) twice
	game.player1.give("CS2_087").play(target=wisp)
	assert wisp.atk == 1 + 3
	game.player1.give("CS2_087").play(target=wisp)
	assert wisp.atk == 1 + 3 + 3
	game.player1.give(SILENCE).play(target=wisp)
	assert wisp.atk == 1


def test_spell_power():
	game = prepare_game(CardClass.HUNTER, CardClass.HUNTER)

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
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	worgen = game.player1.give("EX1_010")
	worgen.play()
	assert worgen.stealthed
	game.end_turn()

	archer = game.player2.give("CS2_189")
	assert worgen not in archer.targets
	assert len(archer.targets) == 2  # Only the heroes
	assert worgen not in game.player2.hero.power.targets
	assert len(game.player2.hero.power.targets) == 2
	game.end_turn()

	worgen.attack(game.player2.hero)
	assert not worgen.stealthed
	assert not worgen.can_attack()
	game.end_turn()

	assert worgen in archer.targets
	assert len(archer.targets) == 3
	assert worgen in game.player2.hero.power.targets
	assert len(game.player2.hero.power.targets) == 3


def test_windfury():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert not wisp.can_attack()
	game.end_turn(); game.end_turn()

	wisp.attack(game.player2.hero)
	windfury = game.player1.give("CS2_039")
	windfury.play(target=wisp)
	assert wisp.windfury
	assert wisp.num_attacks == 1
	assert wisp.can_attack()
	wisp.attack(game.player2.hero)
	assert not wisp.can_attack()
	assert wisp.windfury
	game.player1.give(SILENCE).play(target=wisp)
	assert not wisp.windfury


def test_stealth_taunt():
	game = prepare_game()
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	assert goldshire.taunt
	masterofdisguise = game.player1.give("NEW1_014")
	masterofdisguise.play(target=goldshire)
	assert goldshire.taunt
	assert goldshire.stealthed
	wisp = game.player2.summon(WISP)
	game.end_turn()

	assert goldshire not in wisp.targets
	assert game.player1.hero in wisp.targets
	game.end_turn()

	goldshire.attack(game.player2.hero)
	assert goldshire.taunt
	assert not goldshire.stealthed
	game.end_turn()

	assert goldshire in wisp.targets
	assert game.player1.hero not in wisp.targets


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
	assert wisp1.targets == [game.player2.hero, wisp2]
	game.end_turn()

	goldshire2.play()
	game.end_turn()

	assert wisp1.targets == [goldshire2]
	goldshire1.play()
	game.end_turn()

	assert wisp2.targets == [goldshire1]


def test_weapon_sheathing():
	game = prepare_game()
	weapon = game.player1.give(LIGHTS_JUSTICE)
	weapon.play()
	assert not weapon.exhausted
	assert game.player1.hero.atk == 1
	assert game.player1.hero.can_attack()
	game.player1.hero.attack(target=game.player2.hero)
	assert not weapon.exhausted
	assert game.player1.hero.atk == 1
	game.end_turn()

	assert weapon.exhausted
	assert game.player1.hero.atk == 0
	assert game.player2.hero.health == 29
	game.player2.give(LIGHTS_JUSTICE).play()
	game.player2.hero.attack(target=game.player1.hero)
	assert game.player1.hero.health == 29
	assert game.player2.hero.health == 29
	game.end_turn()

	assert not weapon.exhausted
