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
		assert card.card_class in (CardClass.NEUTRAL, CardClass.PALADIN)


def test_addled_grizzly():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	grizzly = game.player1.give("OG_313")
	game.player1.give("OG_313").play()
	grizzly.play()
	assert grizzly.atk == grizzly.health == 3
	wisp.play()
	assert wisp.atk == wisp.health == 3


def test_ancient_harbinger():
	game = prepare_empty_game()
	game.player1.give(WISP).shuffle_into_deck()
	game.player1.give(IMP).shuffle_into_deck()
	game.player1.give(GOLDSHIRE_FOOTMAN).shuffle_into_deck()
	game.player1.give(MIND_CONTROL).shuffle_into_deck()
	game.player1.give("EX1_279").shuffle_into_deck()
	game.player1.give("NEW1_030").shuffle_into_deck()
	game.player1.give("OG_290").play()
	game.end_turn(); game.end_turn()

	assert game.player1.hand[0].cost == 10
	assert game.player1.hand[0].type == CardType.MINION
	assert len(game.player1.hand) == 2


def test_blackwater_pirate():
	game = prepare_game()
	game.player1.give("OG_322").play()
	reaper = game.player1.give("CS2_112")
	kobold = game.player1.give(KOBOLD_GEOMANCER)
	mc = game.player1.give(MIND_CONTROL)
	assert reaper.cost == 3
	assert kobold.cost == 2
	assert mc.cost == 10
	reaper.play()
	assert reaper.cost == 5


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


def test_cult_apothecary():
	game = prepare_game()
	cult_apothecary = game.player1.give("OG_295")
	game.end_turn()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.player2.give(WISP).play()
	game.end_turn()
	game.player1.hero.set_current_health(10)
	lightwarden = game.player1.give("EX1_001")
	lightwarden.play()
	cult_apothecary.play()
	assert game.player1.hero.health == 10 + 8
	assert lightwarden.atk == 3


def test_deathwing_dragonlord():
	game = prepare_game()
	game.player1.discard_hand()
	deathwing = game.player1.give("OG_317")
	ysera = game.player1.give("EX1_572")
	azure_drake = game.player1.give("EX1_284")
	wisp = game.player1.give(WISP)
	deathwing.play()
	deathwing.destroy()
	assert game.player1.hand == [wisp]
	assert game.player1.field == [ysera, azure_drake]


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


def test_doom():
	game = prepare_game()
	game.player1.discard_hand()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give(WISP).play()
	game.player1.give("OG_239").play()
	assert len(game.player1.hand) == 3


def test_eater_of_secrets():
	game = prepare_game()
	eater_of_secrets = game.player1.give("OG_254")
	game.end_turn()
	game.player2.give("EX1_379").play()
	game.player2.give("EX1_609").play()
	game.player2.give("EX1_294").play()
	game.end_turn()
	eater_of_secrets.play()
	assert eater_of_secrets.atk == 5
	assert eater_of_secrets.health == 7
	assert not game.player2.secrets

def test_embrace_the_shadow():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)
	embrace = game.player1.give("OG_104").play()
	game.player1.hero.power.use(target=game.player2.hero)
	assert game.player2.hero.health == 30 - 2
	flash_heal = game.player1.give("AT_055").play(target=game.player2.hero)
	assert game.player2.hero.health == 30 - 2 - 5
	game.end_turn(); game.end_turn()
	game.player1.hero.power.use(target=game.player2.hero)
	assert game.player2.hero.health == 30 -2 - 5 + 2


def test_evolved_kobold():
	game = prepare_game()
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	game.player1.give(MOONFIRE).play(target=statue)
	assert statue.health == 10 - 1
	game.player1.give("OG_082").play()
	game.player1.give(MOONFIRE).play(target=statue)
	assert statue.health == 10 - 1 - 3


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

def test_forbidden_ancient():
	game = prepare_game()
	assert game.player1.mana == 10
	ancient = game.player1.give("OG_051")
	fireball = game.player1.give("CS2_029").play(target=game.player2.hero)
	innervate = game.player1.give("EX1_169").play()
	assert game.player1.mana == 8
	ancient.play()
	assert len(game.player1.field) == 1
	assert ancient.atk == 8
	assert ancient.health == 8
	assert game.player1.mana == 0


def test_forbidden_flame():
	game = prepare_game()
	ysera = game.player1.give("EX1_572").play()
	assert ysera.health == 12
	game.end_turn()
	flame = game.player2.give("OG_086")
	assert game.player2.mana == 10
	fireball = game.player2.give("CS2_029").play(target=game.player1.hero)
	assert game.player2.mana == 6
	flame.play(target=ysera)
	assert ysera.health == 6
	assert game.player2.mana == 0


def test_forbidden_healing():
	game = prepare_game()
	game.player1.hero.set_current_health(1)
	assert game.player1.mana == 10
	fireball = game.player1.give("CS2_029").play(target=game.player2.hero)
	assert game.player1.mana == 6
	healing = game.player1.give("OG_198").play(target=game.player1.hero)
	assert game.player1.mana == 0
	assert game.player1.hero.health == 1 + 2 * 6


def test_forbidden_ritual():
	game = prepare_game()
	assert game.player1.mana == 10
	ritual = game.player1.give("OG_114").play()
	assert game.player1.mana == 0
	assert len(game.player1.field) == 7
	for i in range(7):
		assert game.player1.field[i].id == "OG_114a"
	
	game.end_turn()
	assert game.player2.mana == 10
	fireball = game.player2.give("CS2_029").play(target=game.player1.hero)
	fireball = game.player2.give("CS2_029").play(target=game.player1.hero)
	assert game.player2.mana == 2
	ritual = game.player2.give("OG_114").play()
	assert game.player2.mana == 0
	assert len(game.player2.field) == 2
	for i in range(2):
		assert game.player2.field[i].id == "OG_114a"


def test_forbidden_shaping():
	game = prepare_game()
	assert game.player1.mana == 10
	shaping = game.player1.give("OG_101").play()
	assert game.player1.mana == 0
	assert len(game.player1.field) == 1
	assert game.player1.field[0].cost == 10


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


def test_journey_below():
	game = prepare_empty_game()
	journey_below = game.player1.give("OG_072")
	journey_below.play()
	assert len(game.player1.choice.cards) == 3
	for card in game.player1.choice.cards:
		assert card.has_deathrattle


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


def test_nerubian_prophet():
	game = prepare_game()
	nerubian_prophet = game.player1.give("OG_138")
	assert nerubian_prophet.cost == 6
	game.end_turn(); game.end_turn()

	assert nerubian_prophet.cost == 5
	game.end_turn(); game.end_turn()

	assert nerubian_prophet.cost == 4
	nerubian_prophet.play()
	assert nerubian_prophet.cost == 6


def test_nzoth():
	game = prepare_game()
	loot_hoarder = game.player1.give("EX1_096").play()
	leper_gnome = game.player1.give("EX1_029").play()
	loot_hoarder.destroy()
	leper_gnome.destroy()
	game.end_turn(); game.end_turn()

	nzoth = game.player1.give("OG_133").play()
	assert len(game.player1.field) == 3
	for i in range(1,3):
		assert game.player1.field[i].has_deathrattle


def test_nzoth_silenced_deathrattle():
	game = prepare_game()
	loot_hoarder = game.player1.give("EX1_096").play()
	assert loot_hoarder.has_deathrattle
	silence = game.player1.give(SILENCE).play(target=loot_hoarder)
	assert not loot_hoarder.has_deathrattle
	loot_hoarder.destroy()
	assert loot_hoarder.has_deathrattle
	game.end_turn(); game.end_turn()
	nzoth = game.player1.give("OG_133").play()
	assert len(game.player1.field) == 2
	assert game.player1.field[1] == loot_hoarder


def test_nzoth_added_deathrattle():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	ancestral_spirit = game.player1.give("CS2_038").play(target=wisp)
	assert wisp.has_deathrattle
	wisp.destroy()
	assert not wisp.has_deathrattle
	game.end_turn(); game.end_turn()
	nzoth = game.player1.give("OG_133").play()
	assert len(game.player1.field) == 2


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


def test_undercity_huckster():
	game = prepare_empty_game()
	undercity_huckster = game.player1.give("OG_330")
	undercity_huckster.play()
	arcane_shot = game.player1.give("DS1_185")
	arcane_shot.play(target=undercity_huckster)
	assert game.player1.hand[0].card_class == game.player2.hero.card_class


def test_validated_doomsayer():
	game = prepare_game()
	validated_doomsayer = game.player1.give("OG_200")
	validated_doomsayer.play()
	assert validated_doomsayer.atk == 0
	game.end_turn()
	assert validated_doomsayer.atk == 0
	game.end_turn()
	assert validated_doomsayer.atk == 7
	game.end_turn()
	game.player2.give("EX1_360").play(target=validated_doomsayer)
	assert validated_doomsayer.atk == 1
	game.end_turn()
	assert validated_doomsayer.atk == 7


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
		assert wisp.atk == wisp.health == 3
		assert wisp.id == "OG_195c"


def test_yshaarj_rage_unbound():
	game = prepare_empty_game()
	yshaarj = game.player1.give("OG_042")
	wisp = game.player1.give(WISP)
	wisp.shuffle_into_deck()
	moonfire = game.player1.give(MOONFIRE)
	moonfire.shuffle_into_deck()
	yshaarj.play()
	game.end_turn()
	assert game.player1.field == [yshaarj, wisp]
	assert game.player1.deck == [moonfire]
	game.end_turn(); game.end_turn()

	assert game.player1.field == [yshaarj, wisp]
	assert len(game.player1.deck) == 0


def test_fandral_staghelm():
	game = prepare_empty_game()
	fandral = game.player1.give("OG_044")
	assert game.player1.choose_both == False
	fandral.play()
	assert game.player1.choose_both == True
	claw = game.player1.give("EX1_165")
	assert claw.must_choose_one == False
	claw.play()
	assert len(game.player1.field) == 2
	assert game.player1.field[1].id == "OG_044a"
	game.end_turn()
	game.end_turn()
	ancient = game.player1.give("EX1_178").play()
	assert ancient.atk == 10
	assert ancient.health == 10
	assert ancient.taunt == True

def test_giant_sand_worm():
	game = prepare_empty_game()
	worm = game.player1.give("OG_308")
	worm.play()
	game.end_turn()
	wisp1 = game.player2.give(WISP).play()
	wisp2 = game.player2.give(WISP).play()
	game.end_turn()
	assert worm.num_attacks == 0
	worm.attack(target=wisp1)
	assert worm.num_attacks == 0
	worm.attack(target=wisp2)
	assert worm.num_attacks == 0
	worm.attack(target=game.player2.hero)
	assert worm.num_attacks == 1

def test_servant_of_yoggsaron():
	game = prepare_empty_game()
	servant = game.player1.give("OG_087")
	servant.play()