from utils import *

def test_bittertide_hydra():
	game = prepare_game()
	bittertide_hydra = game.player1.give("UNG_087").play()
	game.end_turn()
	assert game.player1.hero.health == 30
	moonfire = game.player2.give(MOONFIRE).play(target=bittertide_hydra)
	assert game.player1.hero.health == 30 - 3
	pyroblast = game.player2.give("EX1_279").play(target=bittertide_hydra)
	assert game.player1.hero.health == 30 - 3 - 3

def test_bright_eyed_scout():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP)
	wisp.shuffle_into_deck()
	assert game.player1.mana == 10
	assert wisp.cost == 0
	scout = game.player1.give("UNG_113").play()
	assert game.player1.mana == 6
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0] == wisp
	assert wisp.cost == 5
	wisp.play()
	assert game.player1.mana == 1

def test_dinomancy():
	game = prepare_game()
	dinomancy = game.player1.give("UNG_917").play()
	river_crocolisk = game.player1.give("CS2_120").play()
	wisp = game.player1.give(WISP).play()

	assert river_crocolisk.atk == 2
	assert river_crocolisk.health == 3
	game.player1.hero.power.use(target=river_crocolisk)
	assert river_crocolisk.atk == 2 + 2
	assert river_crocolisk.health == 3 + 2


def test_earthen_scales():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	scales = game.player1.give("UNG_108").play(target=wisp)
	assert wisp.atk == 2
	assert wisp.health == 2
	assert game.player1.hero.armor == 2

def test_frozen_crusher():
	game = prepare_game()
	frozen_crusher = game.player1.give("UNG_079").play()
	game.end_turn(); game.end_turn()
	assert not frozen_crusher.frozen
	frozen_crusher.attack(game.player2.hero)
	assert frozen_crusher.frozen
	assert game.player2.hero.health == 30 - 8
	game.end_turn(); game.end_turn()
	assert frozen_crusher.frozen
	game.end_turn(); game.end_turn()
	assert not frozen_crusher.frozen

def test_giant_anaconda():
	game = prepare_empty_game()
	anaconda1 = game.player1.give("UNG_086").play()
	anaconda1.destroy()
	assert len(game.player1.field) == 0

	game.end_turn(); game.end_turn()
	anaconda2 = game.player1.give("UNG_086").play()
	ogre = game.player1.give("CS2_200")
	for i in range(8):
		game.player1.give(WISP)
	assert len(game.player1.hand) == 9
	anaconda2.destroy()
	assert len(game.player1.field) == 1
	assert len(game.player1.hand) == 8
	assert game.player1.field[0] == ogre

def test_gluttonous_ooze():
	game = prepare_game();
	ooze = game.player1.give("UNG_946").play()
	assert game.player1.hero.armor == 0
	game.end_turn()
	waraxe = game.player2.give("CS2_106").play()
	game.end_turn()
	ooze2 = game.player1.give("UNG_946").play()
	assert game.player1.hero.armor == 3
	assert waraxe.dead

def test_grievous_bite():
	game = prepare_game()
	for i in range(3):
		river_crocolisk = game.player1.give("CS2_120").play()
	game.end_turn()

	grievous_bite = game.player2.give("UNG_910").play(target=game.player1.field[1])
	assert game.player1.field[0].health == game.player1.field[2].health == 3 - 1
	assert game.player1.field[1].health == 3 - 2

def test_hemet_jungle_hunter():
	game = prepare_empty_game()
	wisp = game.player1.give(WISP).shuffle_into_deck()
	ice_barrier = game.player1.give("EX1_289").shuffle_into_deck()
	fireball = game.player1.give("CS2_029").shuffle_into_deck()
	antonidas = game.player1.give("EX1_559").shuffle_into_deck()

	hemet = game.player1.give("UNG_840")
	assert len(game.player1.deck) == 4
	hemet.play()
	assert len(game.player1.deck) == 2
	for card in game.player1.deck:
		assert card.cost > 3

def test_nesting_roc():
	game = prepare_game()
	wisp = game.player1.give(WISP).play()
	nesting_roc1 = game.player1.give("UNG_801").play()
	assert not nesting_roc1.taunt
	nesting_roc2 = game.player1.give("UNG_801").play()
	assert nesting_roc2.taunt

def test_stampede():
	game = prepare_empty_game()
	stampede = game.player1.give("UNG_916").play()
	assert len(game.player1.hand) == 0
	river_crocolisk = game.player1.give("CS2_120").play()
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].race == Race.BEAST

	game.end_turn(); game.end_turn()
	assert len(game.player1.hand) == 1
	river_crocolisk = game.player1.give("CS2_120").play()
	assert len(game.player1.hand) == 1

def test_razorpetal():
	"UNG_057t1"
	game = prepare_empty_game()
	razorpetal = game.player1.give("UNG_057t1")
	assert game.player2.hero.health == 30
	razorpetal.play(target=game.player2.hero)
	assert game.player2.hero.health == 30 - 1


def test_razorpetal_volley():
	"UNG_058"
	game = prepare_game()
	lasher = game.player1.give("UNG_057")
	assert len(game.player1.hand) == 4 + 1
	lasher.play()
	assert len(game.player1.field) == 0
	assert len(game.player1.hand) == 4 + 1 - 1 + 2
	assert game.player1.hand[-1].id == "UNG_057t1"  # razorpetal
	assert game.player1.hand[-2].id == "UNG_057t1"  # razorpetal



def test_razorpetal_lasher():
	"UNG_058"
	game = prepare_game()
	lasher = game.player1.give("UNG_058")
	assert len(game.player1.hand) == 4 + 1
	lasher.play()
	assert len(game.player1.field) == 1
	assert len(game.player1.hand) == 4 + 1 - 1 + 1
	assert game.player1.hand[-1].id == "UNG_057t1"  # razorpetal


def test_crystalline_oracle():
	"UNG_032"
	game = prepare_empty_game()

	assert len(game.player1.hand) == 0
	assert len(game.player2.deck) == 0
	oracle = game.player1.give("UNG_032").play()
	game.player1.give(SOULFIRE).play(target=oracle)
	assert len(game.player1.hand) == 0

	game.player2.give(WISP).shuffle_into_deck()
	assert len(game.player2.deck) == 1
	oracle = game.player1.give("UNG_032").play()
	game.player1.give(SOULFIRE).play(target=oracle)
	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == WISP
	game.player1.discard_hand()

	assert len(game.player1.hand) == 0
	game.player2.give(TARGET_DUMMY).shuffle_into_deck()
	assert len(game.player2.deck) == 2

	oracle=game.player1.give("UNG_032").play()
	game.player1.give(SOULFIRE).play(target=oracle)
	assert len(game.player1.hand) == 1

	assert (game.player1.hand.contains(WISP)
		   or game.player1.hand.contains(TARGET_DUMMY))


def test_biteweed():

	#similar to vancleef
	game = prepare_game()
	biteweed1 = game.current_player.give("UNG_063")
	biteweed2 = game.current_player.give("UNG_063")

	assert not game.current_player.cards_played_this_turn
	for i in range(5):
		game.player1.give(THE_COIN).play()
	assert game.current_player.cards_played_this_turn == 5
	biteweed1.play()
	assert game.current_player.cards_played_this_turn == 6
	assert biteweed1.atk == 6
	assert biteweed1.health == 6
	game.end_turn()
	game.end_turn()
	assert not game.current_player.cards_played_this_turn
	biteweed2.play()
	assert game.current_player.cards_played_this_turn == 1
	assert biteweed2.atk == 1
	assert biteweed2.health == 1


def test_mana_bind():
	"UNG_024"

	game = prepare_game()
	game.player1.give("UNG_024").play()

	game.player1.discard_hand()
	assert len(game.player1.hand) == 0

	game.end_turn()

	game.player2.give(PYROBLAST).play(target=game.player2.hero)

	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].id == PYROBLAST

	assert game.player1.hand[0].cost == 0
	# TODO: this should eventually work..
	# game.end_turn()
	# game.end_turn()
	#
	# game.player2.give("FP1_030").play() # loatheb
	# assert game.player1.hand[0].cost == 5


def test_molten_reflection():
	"UNG_948"
	game = prepare_game()
	game.player1.discard_hand()
	molten = game.player1.give("UNG_948")
	assert not molten.is_playable()
	game.player1.give(WISP).play()
	assert molten.is_playable()
	molten.play(game.player1.field[0])

	assert len(game.player1.field) == 2

	assert game.player1.field[0].id == WISP and game.player1.field[1].id == WISP

	game.end_turn()

	molten = game.player2.give("UNG_948")
	assert not molten.is_playable()

	wisp = game.player2.give(WISP).play()

	game.player2.give("CS2_087").play(target=wisp) # blessing of might
	assert wisp.atk == 1 + 3

	molten.play(target=wisp)

	assert len(game.player2.field) == 2
	assert game.player2.field[0].id == WISP and game.player2.field[1].id == WISP

	assert game.player2.field[0].atk == 4 and game.player2.field[1].atk == 4


def test_direhorn_hatchling():
	"UNG_957"
	game = prepare_game()
	direhorn = game.player1.give("UNG_957").play()
	game.player1.give("EX1_161").play(direhorn) #naturalize it

	assert game.player1.deck.contains("UNG_957t1")


def test_lyra_the_sunshard():
	"UNG_963"
	game = prepare_empty_game()

	game.player1.give("UNG_963").play()

	assert len(game.player1.hand) == 0
	game.player1.give(THE_COIN).play()

	assert len(game.player1.hand) == 1
	assert game.player1.hand[0].card_class == CardClass.PRIEST

	game.player1.give(THE_COIN).play()
	assert len(game.player1.hand) == 2
	assert game.player1.hand[-1].card_class == CardClass.PRIEST

	assert len(game.player2.hand) == 1


def test_bloodbloom():
	"UNG_832"

	game = prepare_empty_game()

	assert game.player1.mana == 10

	game.player1.give("UNG_832").play()
	assert game.player1.mana == 10 - 2

	game.player1.give(PYROBLAST).play(game.player2.hero)
	assert game.player1.mana == 10 - 2
	assert game.player2.hero.health == 30 - 10
	assert game.player1.hero.health == 30 - 10

	game.player1.give(SOULFIRE).play(game.player2.hero)
	assert game.player1.mana == 10 - 2 - 1
	assert game.player1.hero.health == 30 - 10


def test_pyros():
	"UNG_027"
	game = prepare_empty_game()

	pyro = game.player1.give("UNG_027").play()

	assert len(game.player1.field) == 1

	game.player1.give("EX1_161").play(target=pyro) # naturalize

	assert len(game.player1.field) == 0
	assert len(game.player1.hand) == 1

	pyro = game.player1.hand[0]

	assert pyro.cost == 6
	assert pyro.atk == 6
	assert pyro.health == 6

	pyro.play()

	assert len(game.player1.field) == 1
	assert len(game.player1.hand) == 0

	game.player1.give("EX1_161").play(target=pyro)  # naturalize

	assert len(game.player1.field) == 0
	assert len(game.player1.hand) == 1

	pyro = game.player1.hand[0]

	assert pyro.cost == 10
	assert pyro.atk == 10
	assert pyro.health == 10

	# TODO: baron rivendale should not trigger this deathrattle twice
	
	# game.player1.discard_hand()
	#
	# game.end_turn()
	# game.end_turn()
	#
	# pyro = game.player1.give("UNG_027").play()
	#
	# game.player1.give("FP1_031").play() # baron rivendale
	# game.player1.give("EX1_161").play(target=pyro)  # naturalize
	#
	# assert len(game.player1.field) == 1
	# assert len(game.player1.hand) == 1
	#
	# pyro = game.player1.hand[0]
	#
	# assert pyro.cost == 6
	# assert pyro.atk == 6
	# assert pyro.health == 6



