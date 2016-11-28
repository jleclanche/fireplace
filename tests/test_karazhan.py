from utils import *

def test_kindly_grandmother():
	game = prepare_game()
	grandma = game.player1.give("KAR_005")
	grandma.play()
	assert len(game.player1.field) == 1
	# Kill Grandma
	game.player1.give(MOONFIRE).play(target=grandma)
	assert len(game.player1.field) == 1
	assert game.player1.field[0].id == "KAR_005a"

def test_cloaked_huntress():
	game = prepare_game()
	huntress = game.player1.give("KAR_006")
	# Freezing Trap
	secret = game.player1.give("EX1_611")
	huntress.play()
	# Check cost of secret
	assert secret.cost == 0
	# Kill Huntress
	for i in range(4):
		game.player1.give(MOONFIRE).play(target=huntress)
	
	assert secret.cost == 2

def test_babbling_book():
	game = prepare_game()
	game.player1.discard_hand()
	book = game.player1.give("KAR_009")
	book.play()

	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].type == CardType.SPELL

def test_nightbane_templar():
	game = prepare_game()
	nightbane1 = game.player1.give("KAR_010")
	assert not nightbane1.powered_up
	nightbane1.play()
	assert len(game.player1.field) == 1
	game.end_turn()

	game.player2.give(WHELP)
	nightbane2 = game.player2.give("KAR_010")
	assert nightbane2.powered_up
	nightbane2.play()
	assert len(game.player2.field) == 3

def test_wicked_witchdoctor():
	game = prepare_game(CardClass.SHAMAN, CardClass.SHAMAN)
	witchdoc = game.player1.give("KAR_021")
	witchdoc.play()
	game.player1.give(THE_COIN).play()

	assert len(game.player1.field) == 2
	assert game.player1.field[-1].id in game.player1.hero.power.data.entourage

def test_book_wyrm():
	game = prepare_game()
	game.player1.discard_hand()
	whelp = game.player1.give(WHELP)
	bookwyrm1 = game.player1.give("KAR_033")
	assert not bookwyrm1.powered_up
	bookwyrm1.play()
	assert len(game.player1.field) == 1
	game.end_turn()

	game.player2.discard_hand()
	game.player2.give(WHELP)
	bookwyrm2 = game.player2.give("KAR_033")
	assert bookwyrm2.powered_up
	bookwyrm2.play(target=bookwyrm1)
	assert len(game.player1.field) == 0
	assert len(game.player2.field) == 1
	game.end_turn()

def test_priest_of_the_feast():
	game = prepare_game()
	priest = game.player1.give("KAR_035")
	game.player1.give(DAMAGE_5).play(target=game.player1.hero)
	assert game.player1.hero.health == 25
	priest.play()
	game.player1.give(THE_COIN).play()
	assert game.player1.hero.health == 28

def test_arcane_anomaly():
	game = prepare_game()
	anomaly = game.player1.give("KAR_036")
	anomaly.play()
	assert anomaly.health == 1
	game.player1.give(THE_COIN).play()
	assert anomaly.health == 2
	game.player1.give(THE_COIN).play()
	assert anomaly.health == 3

def test_avian_watcher():
	game = prepare_game()
	watcher1 = game.player1.give("KAR_037")
	assert not watcher1.powered_up
	watcher1.play()
	assert watcher1.health == 6
	assert watcher1.atk == 3
	game.end_turn()

	watcher2 = game.player2.give("KAR_037")
	secret = game.player2.give("EX1_611")
	assert not watcher2.powered_up
	secret.play()
	assert watcher2.powered_up
	watcher2.play()
	assert watcher2.health == 7
	assert watcher2.atk == 4

def test_moroes():
	game = prepare_game()
	moroes = game.player1.give("KAR_044")
	moroes.play()
	assert len(game.player1.field) == 1
	game.end_turn()

	assert len(game.player1.field) == 2

def test_the_curator():
	game = prepare_empty_game()
	murloc = game.player1.give("PRO_001at").shuffle_into_deck()
	dragon = game.player1.give("ds1_whelptoken").shuffle_into_deck()
	beast = game.player1.give("GVG_092t").shuffle_into_deck()
	curator = game.player1.give("KAR_061")
	assert len(game.player1.hand) == 1
	curator.play()
	assert len(game.player1.hand) == 3
	game.end_turn()

	game.player2.discard_hand() #RID THE COIN
	murloc2 = game.player2.give("PRO_001at").shuffle_into_deck()
	curator2 = game.player2.give("KAR_061")
	assert len(game.player2.hand) == 1
	curator2.play()
	assert len(game.player2.hand) == 1

def test_netherspite_historian():
	game = prepare_game()
	game.player1.discard_hand()
	historian1 = game.player1.give("KAR_062")
	assert not historian1.powered_up
	historian1.play()
	assert not game.player1.choice

	whelp = game.player1.give(WHELP)
	historian2 = game.player1.give("KAR_062")
	assert historian2.powered_up
	historian2.play()
	assert len(game.player1.choice.cards) == 3
	for card in game.player1.choice.cards:
		assert card.type == CardType.MINION
		assert card.race == Race.DRAGON

def test_menagerie_warden():
	game = prepare_game()
	game.player1.discard_hand()
	warden1 = game.player1.give("KAR_065")
	dragon = game.player1.give(WHELP)
	dragon.play()
	assert not warden1.powered_up
	warden1.play()
	assert len(game.player1.field) == 2
	game.end_turn()

	game.player2.discard_hand()
	warden2 = game.player2.give("KAR_065")
	beast = game.player2.give(CHICKEN)
	beast.play()
	motw = game.player2.give("CS2_009")
	motw.play(target=beast)
	assert beast.atk == 1 + 2
	assert beast.health == 1 + 2
	assert beast.taunt
	game.player2.give(MOONFIRE).play(target=beast)
	assert beast.health == 1 + 2 - 1
	assert warden2.powered_up
	warden2.play(target=beast)
	clone = game.player2.field[-1]
	assert clone.id == CHICKEN
	assert clone.buffs
	assert beast.atk == clone.atk
	assert beast.health == clone.health
	assert beast.max_health == clone.max_health
	assert clone.buffs

def test_swashburglar():
	game = prepare_empty_game()
	burglar = game.player1.give("KAR_069")
	burglar.play()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].card_class == game.player2.hero.card_class
	assert game.player1.hand[0].type != CardType.HERO

def test_malchezaars_imp():
	game = prepare_game()
	imp = game.player1.give("KAR_089")
	imp.play()
	soulfire = game.player1.give(SOULFIRE)
	assert len(game.player1.hand) == 5
	soulfire.play(target=game.player2.hero)
	assert len(game.player1.hand) == 4

	game.end_turn()
	game.end_turn()

	game.player1.discard_hand()
	assert len(game.player1.hand) == 0
	game.player1.give(CHICKEN)
	assert len(game.player1.hand) == 1
	doomguard = game.player1.give("EX1_310")
	doomguard.play()
	assert len(game.player1.hand) == 1

	game.end_turn()
	game.end_turn()

	assert len(game.player1.hand) == 2
	doomguard2 = game.player1.give("EX1_310")
	doomguard2.play()
	assert len(game.player1.hand) == 2

def test_medivhs_valet():
	game = prepare_game()
	secret = game.player1.give("EX1_130")
	valet1 = game.player1.give("KAR_092")
	assert not valet1.powered_up
	valet1.play()
	valet2 = game.player1.give("KAR_092")
	secret.play()
	assert valet2.powered_up
	valet2.play(target=game.player2.hero)
	assert game.player2.hero.health == 27

def test_deadly_fork():
	game=prepare_empty_game()
	fork = game.player1.give("KAR_094")
	fork.play()
	game.player1.give(MOONFIRE).play(target=fork)
	game.player1.give(MOONFIRE).play(target=fork)
	assert game.player1.hand[0].id == "KAR_094a"

	game.player1.hand[0].play()
	assert game.player1.hero.atk == 3

def test_zoobot():
	game = prepare_game()
	zoobot = game.player1.give("KAR_095")
	murloc = game.player1.give(MURLOC).play()
	beast = game.player1.give(CHICKEN).play()
	dragon = game.player1.give(WHELP).play()
	assert zoobot.powered_up
	zoobot.play()

	assert murloc.atk == 2
	assert murloc.health == 2
	assert murloc.buffs
	assert beast.atk == 2
	assert beast.health == 2
	assert beast.buffs
	assert dragon.atk == 2
	assert dragon.health == 2
	assert dragon.buffs

def test_barnes():
	game = prepare_empty_game()
	kobold = game.player1.give(KOBOLD_GEOMANCER)
	kobold.shuffle_into_deck()
	barnes = game.player1.give("KAR_114")
	assert len(game.player1.hand) == 1
	assert len(game.player1.deck) == 1

	barnes.play()

	assert len(game.player1.deck) == 1
	assert len(game.player1.field) == 2
	summon = game.player1.field[-1]
	assert summon.id == kobold.id
	assert summon.atk == 1
	assert summon.health == 1


