from utils import *

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