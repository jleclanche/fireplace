from utils import *

def test_amethyst_spellstone():
	game = prepare_empty_game() #LOOT_043,CS2_062
	wisp1 = game.player1.give(WISP)
	wisp2 = game.player1.give(WISP)
	wisp3 = game.player1.give(WISP)
	wisp4 = game.player1.give(WISP)
	for _ in range(10):
		game.player1.give(MOONFIRE).play(target=game.player1.hero)
	assert game.player1.hero.health == 20
	stone1 = game.player1.give("LOOT_043") #lesser spellstone
	wisp1.play()
	stone1.play(target = wisp1)
	assert game.player1.hero.health == 23
	stone2 = game.player1.give("LOOT_043")
	game.player1.give("CS2_062").play() #Hellfire
	stone2 = game.player1.hand[end]
	assert stone2.id == "LOOT_043t2"
	game.end_turn()
	
	game.player2.give("CS2_062").play() #Hellfire
	assert stone2 in game.player1.hand
	game.end_turn()
	
	assert game.player1.hero.health == 20
	wisp2.play()
	stone2.play(target = wisp2) #Not sure how to refer to upgraded spellstone, because it's no longer stone
	assert game.player1.hero.health == 25 #Currently fails because stone does not upgrade

def test_barkskin():
	game = prepare_game()
	wisp = game.player1.give(WISP)
	wisp.play()
	barkskin = game.player1.give("LOOT_047")
	assert wisp.health == 1
	barkskin.play(target=wisp)
	assert wisp.health == 4
	assert game.player1.hero.armor == 3

def test_bladed_gauntlet():
	game = prepare_game()
	gauntlet = game.player1.give("LOOT_044")
	gauntlet.play()
	assert game.player1.hero.armor == 0
	assert gauntlet.atk == game.player1.hero.atk == 0
	game.player1.give("EX1_606").play()
	assert game.player1.hero.armor == 5
	assert gauntlet.atk == game.player1.hero.atk == 5
	game.end_turn()
	
	wolfrider = game.player2.give("CS2_124")
	wolfrider.play()
	wolfrider.attack(game.player1.hero)
	assert game.player1.hero.armor == 2
	assert gauntlet.atk == game.player1.hero.atk == 2

def test_branching_paths():
	game = prepare_game()
	game.player1.discard_hand()
	wisp1 = game.player1.give(WISP)
	wisp2 = game.player1.give(WISP)
	wisp1.play()
	wisp2.play()
	branching1 = game.player1.give("LOOT_054")
	branching2 = game.player1.give("LOOT_054")
	assert game.player1.hero.armor == 0
	assert wisp1.atk == wisp2.atk == 1
	assert len(game.player1.hand) == 2
	branching1.play(choose="LOOT_054c")#, choose="LOOT_054d")
	assert game.player1.hero.armor == 6
	assert wisp1.atk == wisp2.atk == 1
	assert len(game.player1.hand) == 2
	branching2.play(choose="LOOT_054b")#, choose="LOOT_054b")
	assert game.player1.hero.armor == 6
	assert wisp1.atk == wisp2.atk == 3
	assert len(game.player1.hand) == 1

def test_cavern_shinyfinder():
	game = prepare_empty_game()
	assert len(game.player1.deck) == 0
	weapon = game.player1.give("AT_077")
	wisp = game.player1.give(WISP)
	weapon.shuffle_into_deck()
	wisp.shuffle_into_deck()
	assert len(game.player1.deck) == 2
	game.player1.give("LOOT_033").play()
	assert len(game.player1.deck) == 1
	game.player1.give("LOOT_033").play()
	assert len(game.player1.deck) == 1

def test_dark_pact():
	game = prepare_game()
	vulgar = game.player1.give("LOOT_013").play()
	pact = game.player1.give("LOOT_017")
	assert game.player1.hero.health == 28
	pact.play(target=vulgar)
	assert game.player1.hero.health == 30

def test_faldorei_strider():
	game = prepare_empty_game()
	assert len(game.player1.deck) == 0
	game.player1.give("LOOT_026").play()
	assert len(game.player1.deck) == 3
	assert len(game.player1.field) == 1
	game.end_turn()
	game.end_turn()
	
	assert len(game.player1.field) == 4
	assert len(game.player1.deck) == 0

def test_hooked_reaver():
	game = prepare_game()
	hooked1 = game.player1.give("LOOT_018")
	hooked2 = game.player2.give("LOOT_018")
	assert not hooked1.powered_up
	assert not hooked2.powered_up
	for _ in range(15):
		game.player1.give(MOONFIRE).play(target=game.player2.hero)
	assert not hooked1.powered_up
	assert hooked2.powered_up
	assert game.player1.hero.health == 30
	assert game.player2.hero.health == 15
	hooked1.play()
	game.end_turn()
	
	hooked2.play()
	assert hooked1.health == hooked1.atk == 4
	assert hooked2.health == hooked2.atk == 7
	assert not hooked1.taunt
	assert hooked2.taunt

def test_ironwood_golem():
	game = prepare_game()
	golem = game.player1.give("LOOT_048")
	golem.play()
	game.end_turn()
	game.end_turn()
	
	assert game.player1.hero.armor < 3
	assert not golem.can_attack()
	game.player1.give("EX1_606").play()
	assert game.player1.hero.armor >= 3
	assert golem.can_attack()

def test_jasper_spellstone():
	game = prepare_game()
	stone1 = game.player1.give("LOOT_051")
	assert stone1 in game.player1.hand
	game.player1.give("CS2_005").play()
	assert stone1 in game.player1.hand
	game.player1.give("CS2_005").play()
	assert not stone1 in game.player1.hand
	stone2 = game.player1.give("LOOT_051t2")
	game.player1.give("EX1_606").play()
	assert not stone2 in game.player1.hand

def test_kobold_barbarian():
	game = prepare_game()
	assert game.player2.hero.health == 30
	game.player1.give("LOOT_041").play()
	game.end_turn()
	game.end_turn()
	
	assert game.player2.hero.health == 26
	
def test_psychic_scream():
	game = prepare_game()
	decksize = len(game.player1.deck)
	wisp1 = game.player1.give(WISP).play()
	wisp2 = game.player1.give(WISP).play()
	wisp3 = game.player1.give(WISP).play()
	wisp4 = game.player1.give(WISP).play()
	wisp5 = game.player1.give(WISP).play()
	wisp6 = game.player1.give(WISP).play()
	wisp7 = game.player1.give(WISP).play()
	game.end_turn()
	
	wisp8 = game.player2.give(WISP).play()
	wisp9 = game.player2.give(WISP).play()
	wisp10 = game.player2.give(WISP).play()
	wisp11 = game.player2.give(WISP).play()
	wisp12 = game.player2.give(WISP).play()
	wisp13 = game.player2.give(WISP).play()
	wisp14 = game.player2.give(WISP).play()
	assert len(game.player1.field)==7
	assert len(game.player2.field)==7
	game.player2.give("LOOT_008").play()
	assert len(game.player1.field)==0
	assert len(game.player2.field)==0
	assert len(game.player1.deck)==decksize+14

def test_vulgar_homunculus():
	game = prepare_game()
	assert game.player1.hero.health == 30
	game.player1.give("LOOT_013").play()
	assert game.player1.hero.health == 28
