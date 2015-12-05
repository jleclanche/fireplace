from utils import *


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
