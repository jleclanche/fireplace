from utils import *


def test_ancient_shade():
	game = prepare_empty_game()
	shade = game.player1.give("LOE_110")
	assert len(game.player1.deck) == 0
	shade.play()
	assert len(game.player1.deck) == 1
	assert game.player1.deck[0].id == "LOE_110t"
	game.end_turn()

	assert game.player1.hero.health == 30
	game.end_turn()

	assert game.player1.hero.health == 30 - 7


def test_animated_armor():
	game = prepare_game()
	armor = game.player1.give("LOE_119")
	armor.play()
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.damage == 1
	game.player1.give(DAMAGE_5).play(target=game.player1.hero)
	assert game.player1.hero.damage == 1 + 1


def test_anubisath_sentinel():
	game = prepare_game()
	wisp = game.player2.summon(WISP)
	sentinel1 = game.player1.give("LOE_061")
	sentinel1.play()
	sentinel2 = game.player1.give("LOE_061")
	sentinel2.play()
	game.end_turn(); game.end_turn()

	assert sentinel2.atk == sentinel2.health == 4
	game.player1.give("CS2_029").play(target=sentinel1)
	assert sentinel2.atk == sentinel2.health == 4 + 3
	assert wisp.atk == wisp.health == 1
	game.player1.give("CS2_029").play(target=sentinel2)
	assert wisp.atk == wisp.health == 1


def test_anyfin_can_happen():
	game = prepare_game()

	# kill a Wisp
	wisp = game.player1.give(WISP)
	wisp.play()
	game.player1.give(MOONFIRE).play(target=wisp)
	game.end_turn(); game.end_turn()

	assert len(game.player1.field) == 0
	assert len(game.player2.field) == 0
	game.player1.give("LOE_026").play()
	assert len(game.player1.field) == 0
	assert len(game.player2.field) == 0
	game.end_turn()

	# kill a single Murloc twice
	murloc = game.player2.give(MURLOC)
	murloc.play()
	game.player2.give(MOONFIRE).play(target=murloc)
	game.player2.give("LOE_026").play()
	assert len(game.player2.field) == 1
	game.player2.field[0].destroy()
	game.end_turn()

	# kill another 4 Murloc Tinyfins and 1 Murloc Raider
	for i in range(4):
		murloc = game.player1.give(MURLOC)
		murloc.play()
		game.player1.give(MOONFIRE).play(target=murloc)
	othermurloc = game.player1.give("CS2_168")
	othermurloc.play()
	game.player1.give(MOONFIRE).play(target=othermurloc)
	game.end_turn(); game.end_turn()

	assert len(game.player1.field) == 0
	game.player1.give("LOE_026").play()
	assert len(game.player1.field.filter(id=MURLOC)) == 6
	assert len(game.player1.field.filter(id="CS2_168")) == 1


def test_curse_of_rafaam():
	game = prepare_game()
	game.player2.discard_hand()
	assert len(game.player2.hand) == 0
	curse = game.player1.give("LOE_007")
	curse.play()
	assert len(game.player2.hand) == 1
	cursed = game.player2.hand[0]
	assert cursed.id == "LOE_007t"
	assert cursed.immune_to_spellpower
	assert game.player2.hero.health == 30
	game.end_turn()

	assert game.player2.hero.health == 30 - 2
	game.player2.give(KOBOLD_GEOMANCER).play()
	game.end_turn()
	assert game.player2.hero.health == 30 - 2
	game.end_turn()

	assert game.player2.hero.health == 30 - 2 - 2
	cursed.play()
	game.end_turn(); game.end_turn()

	assert game.player2.hero.health == 30 - 2 - 2


def test_cursed_blade():
	game = prepare_game()
	blade = game.player1.give("LOE_118")
	blade.play()
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 30 - (1*2)


def test_cursed_blade_bolf_ramshield():
	game = prepare_game()
	blade = game.player1.give("LOE_118")
	blade.play()
	bolf = game.player1.give("AT_124")
	bolf.play()
	game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 30
	assert bolf.damage == 2


def test_desert_camel():
	game = prepare_empty_game()
	goldshire1 = game.player1.give(GOLDSHIRE_FOOTMAN)
	assert goldshire1.cost == 1
	goldshire1.shuffle_into_deck()
	game.player1.give(WISP).shuffle_into_deck()
	game.player2.give(WISP).shuffle_into_deck()
	camel1 = game.player1.give("LOE_020")
	camel1.play()
	assert len(game.player1.field) == 2
	assert camel1 in game.player1.field
	assert goldshire1 in game.player1.field
	assert len(game.player2.field) == 0
	game.end_turn(); game.end_turn()

	goldshire2 = game.player2.give(GOLDSHIRE_FOOTMAN)
	goldshire2.shuffle_into_deck()
	camel2 = game.player1.give("LOE_020")
	camel2.play()
	assert len(game.player2.field) == 1
	assert goldshire2 in game.player2.field


def test_djinni_of_zephyrs():
	game = prepare_game()
	game.player1.discard_hand()
	game.player2.discard_hand()
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	djinni = game.player1.give("LOE_053")
	djinni.play()
	game.player1.give(MOONFIRE).play(target=statue)
	assert statue.damage == djinni.damage == 1

	pwshield = game.player1.give("CS2_004")
	pwshield.play(target=statue)
	statue.max_health == 10 + 2
	djinni.max_health == 6 + 2
	assert len(game.player1.hand) == 1 + 1

	# Djinni can trigger on minions that are "dead" (eg. killed by the spell)
	naturalize = game.player1.give("EX1_161")
	naturalize.play(target=statue)
	assert len(game.player2.hand) == 2 + 2
	assert statue.dead
	assert djinni.dead


def test_djinni_of_zephyrs_untargeted():
	game = prepare_game()
	game.player1.discard_hand()

	djinni = game.player1.give("LOE_053")
	djinni.play()
	arcaneint = game.player1.give("CS2_023")
	arcaneint.play()
	assert len(game.player1.hand) == 2


def test_eerie_statue():
	game = prepare_game()
	statue = game.player1.give("LOE_107")
	statue.play()
	assert not statue.can_attack()
	game.end_turn(); game.end_turn()

	assert statue.can_attack()
	wisp = game.player1.give(WISP)
	wisp.play()
	assert statue.cant_attack
	assert not statue.can_attack()
	game.player1.give(MOONFIRE).play(target=wisp)
	assert statue.can_attack()


def test_entomb():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	game.end_turn()

	entomb = game.player2.give("LOE_104")
	assert wisp in game.player1.field
	assert len(game.player1.field) == 1
	assert len(game.player2.deck) == 0
	entomb.play(target=wisp)
	assert len(game.player1.field) == 0
	assert len(game.player2.deck) == 1
	assert wisp in game.player2.deck


def test_ethereal_conjurer():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	conjurer = game.player1.give("LOE_003")
	conjurer.play()
	assert len(game.player1.choice.cards) == 3
	for card in game.player1.choice.cards:
		assert card.type == CardType.SPELL
		assert card.card_class == CardClass.MAGE


def test_everyfin_is_awesome():
	game = prepare_game()
	awesome = game.player1.give("LOE_113")
	assert awesome.cost == 7
	game.player1.give(MURLOC)
	assert awesome.cost == 7
	murloc1 = game.player1.give(MURLOC)
	murloc1.play()
	assert awesome.cost == 6
	murloc2 = game.player2.summon(MURLOC)
	assert awesome.cost == 6

	assert murloc1.atk == murloc1.health == 1
	awesome.play()
	assert murloc1.buffs
	assert murloc1.atk == murloc1.health == 1 + 2
	assert not murloc2.buffs


def test_excavated_evil():
	game = prepare_empty_game()
	evil = game.player1.give("LOE_111")
	wisp1 = game.player1.summon(WISP)
	wisp2 = game.player2.summon(WISP)
	assert len(game.player2.deck) == 0
	evil.play()
	assert wisp1.dead and wisp2.dead
	assert game.player1.hero.health == game.player2.hero.health == 30
	assert len(game.player2.deck) == 1
	assert game.player2.deck[0].id == "LOE_111"


def test_explorers_hat():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).play()
	game.player1.give("LOE_105").play(target=wisp)
	assert wisp.health == 2
	game.end_turn()

	assert len(game.player1.hand) == 0
	game.player2.give(MOONFIRE).play(target=wisp)
	game.player2.give(MOONFIRE).play(target=wisp)
	assert wisp.dead
	assert len(game.player1.hand) == 1


def test_fossilized_devilsaur():
	game = prepare_game()
	game.player1.give(WISP).play()
	game.player2.summon(CHICKEN)
	devilsaur1 = game.player1.give("LOE_073")
	devilsaur1.play()
	assert not devilsaur1.taunt
	game.end_turn(); game.end_turn()

	chicken = game.player1.give(CHICKEN)
	chicken.play()
	devilsaur2 = game.player1.give("LOE_073")
	devilsaur2.play()
	assert devilsaur2.taunt


def test_gorillabot_a3():
	game = prepare_game()
	gorillabot1 = game.player1.give("LOE_039")
	assert not gorillabot1.powered_up
	gorillabot1.play()
	assert not game.player1.choice
	game.end_turn(); game.end_turn()

	assert gorillabot1.race == Race.MECHANICAL
	gorillabot2 = game.player1.give("LOE_039")
	assert gorillabot2.powered_up
	gorillabot2.play()
	assert game.player1.choice
	assert len(game.player1.choice.cards) == 3
	for i in range(3):
		assert game.player1.choice.cards[i].race == Race.MECHANICAL


def test_huge_toad():
	game = prepare_game()
	dummy = game.player1.give(TARGET_DUMMY)
	dummy.play()
	game.end_turn()

	assert game.player2.hero.health == 30
	assert dummy.health == 2
	toad = game.player2.give("LOE_046")
	toad.play()
	for i in range(2):
		game.player2.give(MOONFIRE).play(target=toad)
	assert game.player1.hero.health + dummy.health == 30 + 2 - 1


def test_jungle_moonkin():
	game = prepare_game()
	moonkin = game.player1.give("LOE_051")
	moonkin.play()
	statue = game.player2.summon(ANIMATED_STATUE)
	game.player1.give(MOONFIRE).play(target=statue)
	assert statue.health == 7


def test_keeper_of_uldaman():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	goldshire = game.player1.give(GOLDSHIRE_FOOTMAN)
	goldshire.play()
	game.player1.give(MOONFIRE).play(target=goldshire)
	statue = game.player1.give(ANIMATED_STATUE)
	statue.play()
	game.end_turn(); game.end_turn()

	for minion in (wisp, goldshire, statue):
		keeper = game.player1.give("LOE_017")
		keeper.play(target=minion)
		assert minion.atk == minion.health == 3
		assert not minion.damaged
		game.end_turn(); game.end_turn()


def test_naga_sea_witch():
	game = prepare_game()
	game.player1.give(MOONFIRE)
	game.player1.give(WISP)
	game.player1.give(GOLDSHIRE_FOOTMAN)
	game.player1.give("EX1_586")  # Sea Giant
	game.player1.give("BRM_025")  # Volcanic Drake
	naga = game.player1.give("LOE_038")
	naga.play()
	for card in game.player1.hand:
		assert card.cost == 5
	naga.destroy()
	for card in game.player1.hand:
		assert (
			card.cost == card.data.cost or
			hasattr(card.data.scripts, "cost_mod")
		)


def test_obsidian_destroyer():
	game = prepare_game()
	destroy = game.player1.give("LOE_009")
	destroy.play()
	assert len(game.player1.field) == 1
	game.end_turn()

	assert len(game.player1.field) == 2
	scarab = game.player1.field[1]
	assert scarab.id == "LOE_009t"
	assert scarab.taunt


def test_reliquary_seeker():
	game = prepare_game()
	for i in range(6):
		game.player2.summon(WISP)
	seeker1 = game.player1.give("LOE_116")
	assert not seeker1.powered_up
	seeker1.play()
	assert not seeker1.buffs
	for i in range(5):
		game.player1.give(WISP).play()
	assert len(game.player1.field) == 6
	seeker2 = game.player1.give("LOE_116")
	assert seeker2.powered_up
	seeker2.play()
	assert seeker2.buffs
	assert seeker2.atk == seeker1.atk + 4
	assert seeker2.health == seeker1.health + 4


def test_reno_jackson():
	game = prepare_empty_game()

	game.player1.hero.set_current_health(10)
	assert game.player1.hero.health == 10
	game.player1.give(WISP).shuffle_into_deck()
	game.player1.give(WISP).shuffle_into_deck()
	game.player1.give("LOE_011").play()
	assert game.player1.hero.health == 10
	game.end_turn(); game.end_turn()

	assert len(game.player1.deck) == 1
	game.player1.give("LOE_011").play()
	assert game.player1.hero.health == 30
	game.end_turn(); game.end_turn()

	assert len(game.player1.deck) == 0
	game.player1.hero.set_current_health(10)
	assert game.player1.hero.health == 10
	game.player1.give("LOE_011").play()
	assert game.player1.hero.health == 30


def test_rumbling_elemental():
	game = prepare_game()

	elemental = game.player1.give("LOE_016")
	wisp1 = game.player2.summon(WISP)

	# Rumbling Elemental should not trigger in hand
	vodoo1 = game.player1.give("EX1_011")
	vodoo1.play(target=game.player1.hero)
	assert not wisp1.dead and game.player2.hero.health == 30
	vodoo1.destroy()

	elemental.play()

	# vanilla minions should not trigger
	wisp2 = game.player1.give(WISP)
	wisp2.play()
	wisp2.destroy()
	assert not wisp1.dead and game.player2.hero.health == 30
	game.end_turn()

	# opponent's battlecries should not trigger
	vodoo2 = game.player2.give("EX1_011")
	vodoo2.play(target=game.player2.hero)
	assert not wisp1.dead and game.player2.hero.health == 30
	vodoo2.destroy()
	game.end_turn()

	# Elemental should not trigger on battlecry weapon
	perditionsblade = game.player1.give("EX1_133")
	perditionsblade.play(target=game.player1.hero)
	assert not wisp1.dead and game.player2.hero.health == 30

	vodoo3 = game.player1.give("EX1_011")
	vodoo3.play(target=game.player1.hero)
	assert wisp1.dead ^ (game.player2.hero.health == 28)


def test_sir_finley_mrrgglton():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)
	finley = game.player1.give("LOE_076")
	assert game.player1.hero.power.id == "CS1h_001"
	finley.play()
	assert game.player1.choice
	assert len(game.player1.choice.cards) == 3
	for card in game.player1.choice.cards:
		assert card.type == CardType.HERO_POWER
	new_power = game.player1.choice.cards[0]
	game.player1.choice.choose(new_power)
	assert game.player1.hero.power is new_power


def test_summoning_stone():
	game = prepare_game()
	stone = game.player1.give("LOE_086")
	stone.play()
	game.end_turn()

	game.player2.give(MOONFIRE).play(target=game.player1.hero)
	assert len(game.player1.field) == 1
	assert len(game.player2.field) == 0
	game.end_turn()

	moonfire = game.player1.give(MOONFIRE)
	assert moonfire.cost == 0
	moonfire.play(target=game.player2.hero)
	assert len(game.player1.field) == 2
	assert stone is game.player1.field[0]
	assert game.player1.field[1].cost == 0


def test_tomb_pillager():
	game = prepare_game()
	game.player1.discard_hand()
	pillager = game.player1.give("LOE_012")
	pillager.play()
	fireball = game.player1.give("CS2_029")
	fireball.play(target=pillager)
	assert pillager.dead
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == "GAME_005"


def test_tunnel_trogg():
	game = prepare_game()
	trogg = game.player1.give("LOE_018")
	dustdevil = game.player1.give("EX1_243")
	dustdevil.play()
	assert trogg.atk == 1
	trogg.play()
	assert trogg.atk == 1
	dustdevil = game.player1.give("EX1_243")
	assert dustdevil.overload == 2
	dustdevil.play()
	assert trogg.atk == 3


def test_unearthed_raptor():
	game = prepare_game()
	lepergnome = game.player1.give("EX1_029")
	lepergnome.play()
	raptor = game.player1.give("LOE_019")
	raptor.play(target=lepergnome)
	assert raptor.buffs
	assert raptor.has_deathrattle
	assert len(raptor.deathrattles) == 1
	assert raptor.deathrattles[0] == lepergnome.deathrattles[0]
	raptor2 = game.player1.give("LOE_019")
	raptor2.play(target=raptor)
	assert raptor2.deathrattles[0] == lepergnome.deathrattles[0]
	raptor.destroy()
	assert game.player2.hero.health == 30 - 2
	raptor2.destroy()
	assert game.player2.hero.health == 30 - 2 - 2


def test_wobbling_runts():
	game = prepare_game()
	runts = game.player1.give("LOE_089")
	runts.play()
	assert len(game.player1.field) == 1
	runts.destroy()
	assert len(game.player1.field) == 3
	assert game.player1.field == ["LOE_089t", "LOE_089t2", "LOE_089t3"]


def test_jeweled_scarab():
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

	jeweled_scarab = game.player1.give("LOE_029")
	jeweled_scarab.play()
	assert game.player1.choice

	assert not wisp.can_attack()
	assert not moonfire.is_playable()
	assert not game.player1.hero.can_attack()
	assert not game.player1.hero.power.is_usable()

	assert len(game.player1.choice.cards) == 3
	for card in game.player1.choice.cards:
		assert card.cost == 3

	game.player1.choice.choose(random.choice(game.player1.choice.cards))
	assert not game.player1.choice

	assert wisp.can_attack()
	assert moonfire.is_playable()
	assert game.player1.hero.can_attack()
	assert game.player1.hero.power.is_usable()


##
# Adventure tests

def test_medivhs_locket():
	game = prepare_game()
	assert len(game.player1.hand) == 4
	locket = game.player1.give("LOEA16_12")
	locket.play()
	assert len(game.player1.hand) == 4
	for card in game.player1.hand:
		assert card.id == UNSTABLE_PORTAL
