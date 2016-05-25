from utils import *


def test_a_light_in_the_darkness():
	game = prepare_empty_game(CardClass.PALADIN, CardClass.PALADIN)
	a_light_in_the_darkness = game.player1.give("OG_311")
	a_light_in_the_darkness.play()
	assert len(game.player1.choice.cards) == 3
	for card in game.player1.choice.cards:
		assert card.type == CardType.MINION
		buffhp = card.health
		card.clear_buffs()
		basehp = card.health
		assert buffhp == basehp + 1
		# TODO: put a test for card class here, once it's implemented


def test_addled_grizzly():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	grizzly = game.player1.give("OG_313")
	game.player1.give("OG_313").play()
	grizzly.play()
	assert grizzly.atk == grizzly.health == 3
	wisp.play()
	assert wisp.atk == wisp.health == 3


def test_blood_to_ichor():
	game = prepare_game()
	shieldbearer = game.player1.give("EX1_405").play()

	for _ in range(3):
		game.player1.give("OG_314").play(target=shieldbearer)

	assert len(game.player1.field) == 4
	game.player1.give("OG_314").play(target=shieldbearer)
	assert len(game.player1.field) == 3
	for minion in game.player1.field:
		assert minion.id == "OG_314b"


def test_blood_warriors():
	game = prepare_game()
	game.player1.give(ANIMATED_STATUE).play()
	game.player1.give(TARGET_DUMMY).play()
	game.player1.give(GOLDSHIRE_FOOTMAN).play()

	# Whirlwind the board, then play more minions.
	game.player1.give("EX1_400").play()
	game.player1.give(ANIMATED_STATUE).play()
	game.player1.give(GOLDSHIRE_FOOTMAN).play()
	game.end_turn()
	game.end_turn()
	game.player1.discard_hand()

	warriors = game.player1.give("OG_276")
	warriors.play()
	assert game.player1.hand == [ANIMATED_STATUE, TARGET_DUMMY, GOLDSHIRE_FOOTMAN]
	assert len(game.player1.field) == 5


def test_bloodsail_cultist():
	game = prepare_game()
	game.player1.give(TARGET_DUMMY).play()
	weapon = game.player1.give(LIGHTS_JUSTICE)
	weapon.play()
	game.end_turn()

	# Give opponent a pirate.
	game.player2.give("NEW1_018").play()
	game.end_turn()

	# Play Bloodsail Cultist with no friendly pirates.
	game.player1.give("OG_315").play()
	assert weapon.atk == 1
	assert weapon.durability == 4

	# Play Bloodsail Cultist with friendly pirate (previous cultist).
	game.player1.give("OG_315").play()
	assert weapon.atk == 2
	assert weapon.durability == 5


def test_cabalists_tome():
	game = prepare_game()
	game.player1.discard_hand()
	game.player1.give("OG_090").play()
	assert len(game.player1.hand) == 3
	game.player1.give("OG_090").play()
	for card in game.player1.hand:
		assert card.type == CardType.SPELL
		assert card.card_class == CardClass.MAGE
	assert len(game.player1.hand) == 6


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


def test_demented_frostcaller():
	game = prepare_game()
	game.player1.give("OG_085").play()
	game.end_turn()

	game.player2.give(WISP).play()
	game.end_turn()

	for i in range(1, 3):
		game.player1.give(THE_COIN).play()
		assert len(game.player2.characters.filter(frozen=True)) == i
	# Cast one extra coin, ensuring nothing breaks when all enemies are already frozen.
	game.player1.give(THE_COIN).play()


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


def test_malkorok():
	game = prepare_game()
	malkorok = game.player1.give("OG_220")
	malkorok.play()
	assert game.player1.weapon
	assert not game.player2.weapon


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


def test_primal_fusion():
	game = prepare_game(CardClass.SHAMAN, CardClass.SHAMAN)
	fusion0 = game.player1.give("OG_023")
	fusion1 = game.player1.give("OG_023")
	fusion2 = game.player1.give("OG_023")
	wisp = game.player1.give(WISP)
	summon_totem = game.player1.hero.power
	wisp.play()
	fusion0.play(target=wisp)
	assert wisp.atk == wisp.health == 1
	summon_totem.use()
	fusion1.play(target=wisp)
	assert wisp.atk == wisp.health == 2
	game.end_turn(); game.end_turn()

	summon_totem.use()
	fusion2.play(target=wisp)
	assert wisp.atk == wisp.health == 4


def test_ragnaros_lightlord():
	game = prepare_empty_game()
	ragnaros_lightlord = game.player1.give("OG_229")
	injured_blademaster = game.player1.give("CS2_181")
	injured_blademaster.play()
	game.end_turn()
	injured_kvaldir = game.player2.give("AT_105")
	injured_kvaldir.play()
	game.end_turn()
	ragnaros_lightlord.play()
	game.end_turn()
	assert injured_blademaster.health == 7
	assert injured_kvaldir.health == 1


def test_scaled_nightmare():
	game = prepare_game()
	scaled_nightmare = game.player1.give("OG_271")
	scaled_nightmare.play()
	game.end_turn()
	assert scaled_nightmare.atk == 2
	game.end_turn()
	assert scaled_nightmare.atk == 4
	game.end_turn()
	assert scaled_nightmare.atk == 4
	game.end_turn()
	assert scaled_nightmare.atk == 8


def test_scaled_nightmare_buff_ordering():
	# To show that fireplace doesn't have blizzard's truly bizzare bugs.
	# cf: HearthSim/hs-bugs#462 - "Scaled Nightmare stops doubling Attack if its Attack value is Direct Set"
	game = prepare_game()
	scaled_nightmare_debuff_second = game.player1.give("OG_271")
	scaled_nightmare_debuff_first = game.player1.give("OG_271")
	humility1 = game.player1.give("EX1_360")
	humility2 = game.player1.give("EX1_360")

	scaled_nightmare_debuff_second.play()
	game.end_turn(); game.end_turn()

	humility1.play(target=scaled_nightmare_debuff_second)
	game.end_turn(); game.end_turn()

	assert scaled_nightmare_debuff_second.atk == 2
	game.end_turn(); game.end_turn()

	assert scaled_nightmare_debuff_second.atk == 4

	scaled_nightmare_debuff_first.play()
	humility2.play(target=scaled_nightmare_debuff_first)
	game.end_turn(); game.end_turn()

	assert scaled_nightmare_debuff_first.atk == 2
	game.end_turn(); game.end_turn()

	assert scaled_nightmare_debuff_first.atk == 4


def test_shadow_word_horror():
	game = prepare_game()
	shadow_word_horror = game.player1.give("OG_100")
	wisp = game.player1.give(WISP)
	wisp.play()
	bloodfen_raptor = game.player1.give("CS2_172")
	bloodfen_raptor.play()
	game.end_turn()
	river_crocolisk = game.player2.give("CS2_120")
	river_crocolisk.play()
	chillwind_yeti = game.player2.give("CS2_182")
	chillwind_yeti.play()
	game.end_turn()
	shadow_word_horror.play()
	assert len(game.player1.field) == 1
	assert game.player1.field[0] == bloodfen_raptor
	assert len(game.player2.field) == 1
	assert game.player2.field[0] == chillwind_yeti


def test_shatter():
	game = prepare_game()
	wisp1 = game.player1.give(WISP)
	wisp1.play()
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	# Freeze wisp1 with Ice Lance.
	game.player1.give("CS2_031").play(target=wisp1)
	shatter = game.player1.give("OG_081")
	assert shatter.targets == [wisp1]
	# Shatter frozen wisp.
	shatter.play(target=wisp1)
	assert wisp1.dead


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


def test_steward_of_darkshire():
	game = prepare_game(CardClass.PALADIN, CardClass.PALADIN)
	steward_of_darkshire = game.player1.give("OG_310")
	wisp = game.player1.give(WISP)
	injured_kvaldir = game.player1.give("AT_105")
	twilight_drake = game.player1.give("EX1_043")
	steward_of_darkshire.play()
	wisp.play()
	assert wisp.divine_shield
	injured_kvaldir.play()
	assert not injured_kvaldir.divine_shield
	twilight_drake.play()
	assert twilight_drake.divine_shield


def test_tentacles_for_arms():
	game = prepare_game()
	game.player1.discard_hand()
	game.player1.give("OG_033").play()
	game.player1.give(LIGHTS_JUSTICE).play()
	assert game.player1.hand == ["OG_033"]


def test_tentacles_for_arms_full_hand():
	game = prepare_game()
	game.player1.discard_hand()
	tentacles = game.player1.give("OG_033").play()
	for _ in range(10):
		game.player1.give(WISP)
	tentacles.destroy()
	assert tentacles.zone == Zone.GRAVEYARD


def test_thistle_tea():
	game = prepare_game()
	game.player1.discard_hand()
	tea = game.player1.give("OG_073")
	tea.play()
	assert len(game.player1.hand) == 3
	assert game.player1.hand[0] == game.player1.hand[1] == game.player1.hand[2]


def test_vilefin_inquisitor():
	game = prepare_game()
	vilefin_inquisitor = game.player1.give("OG_006")
	vilefin_inquisitor.play()
	tidal_hand = game.player1.hero.power
	tidal_hand.use()
	assert game.player1.field == [vilefin_inquisitor, "OG_006a"]
	assert tidal_hand == "OG_006b"


def test_wisps_of_the_old_gods():
	game = prepare_game()
	game.player1.give("OG_195").play(choose="OG_195a")
	assert len(game.player1.field) == 7
	game.end_turn(); game.end_turn()

	game.player1.give("OG_195").play(choose="OG_195b")
	for wisp in game.player1.field:
		assert wisp.atk ==  wisp.health == 3
		assert wisp.id == "OG_195c"
