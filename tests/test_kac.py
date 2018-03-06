from utils import *

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

