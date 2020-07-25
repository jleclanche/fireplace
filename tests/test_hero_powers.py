from utils import *


def test_druid():
	game = prepare_game(CardClass.DRUID, CardClass.DRUID)
	assert game.player1.hero.health == 30
	assert game.player1.hero.armor == 0
	assert game.player1.hero.atk == 0
	assert not game.player1.hero.can_attack()
	game.player1.hero.power.use()
	assert game.player1.hero.armor == 1
	assert game.player1.hero.atk == 1
	assert game.player1.hero.can_attack()
	game.player1.hero.attack(target=game.player2.hero)
	assert not game.player1.hero.can_attack()
	assert not game.player1.hero.power.is_usable()


def test_mage():
	game = prepare_game(CardClass.MAGE, CardClass.MAGE)
	assert game.current_player.hero.health == 30
	assert game.current_player.opponent.hero.health == 30
	assert game.current_player.times_hero_power_used_this_game == 0
	assert game.player1.hero.power.controller is game.player1
	assert game.player2.hero.power.controller is game.player2

	# Fireblast the opponent hero
	game.current_player.hero.power.use(
		target=game.current_player.opponent.hero)
	assert game.current_player.hero.health == 30
	assert game.current_player.opponent.hero.health == 29
	assert game.current_player.times_hero_power_used_this_game == 1
	assert not game.current_player.hero.power.is_usable()
	game.skip_turn()

	# Fireblast the current player's hero
	assert game.current_player.hero.power.is_usable() is True
	game.current_player.hero.power.use(target=game.current_player.hero)
	assert game.current_player.times_hero_power_used_this_game == 2
	assert not game.current_player.hero.power.is_usable()


def test_paladin():
	game = prepare_game(CardClass.PALADIN, CardClass.PALADIN)
	game.current_player.hero.power.use()
	assert len(game.current_player.field) == 1
	assert game.current_player.field[0].id == "CS2_101t"

	# ensure that hero power cannot be used on full board
	game.skip_turn()
	assert game.current_player.hero.power.is_usable()
	for i in range(6):
		game.current_player.give(WISP).play()
	assert len(game.current_player.field) == 7
	assert not game.current_player.hero.power.is_usable()
	game.current_player.field[1].destroy()

	# can have multiple Silver Hand Recruits
	assert game.current_player.hero.power.is_usable()


def test_priest():
	game = prepare_game(CardClass.PRIEST, CardClass.PRIEST)
	# Heal self
	assert game.current_player.hero.health == 30
	game.current_player.hero.power.use(target=game.current_player.hero)
	assert game.current_player.hero.health == 30

	game.skip_turn()
	game.current_player.give(MOONFIRE).play(target=game.current_player.hero)
	assert game.current_player.hero.health == 29
	game.current_player.hero.power.use(target=game.current_player.hero)
	assert game.current_player.hero.health == 30
	assert not game.player1.hero.power.is_usable()

	game.end_turn()
	assert game.current_player.opponent.hero.health == 30
	game.current_player.hero.power.use(
		target=game.current_player.opponent.hero)
	assert game.current_player.opponent.hero.health == 30


def test_shaman():
	game = prepare_game(CardClass.SHAMAN, CardClass.SHAMAN)
	basic_totem = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]
	totem_ids = []

	# use hero power four times
	for i in range(4):
		assert len(game.current_player.field) == i
		assert game.current_player.hero.power.is_usable()
		game.current_player.hero.power.use()
		assert len(game.current_player.field) == i + 1
		assert game.current_player.field[-1].id in basic_totem
		game.skip_turn()

	# ensure that totems are identical
	for totem in game.current_player.field:
		totem_ids.append(totem.id)
	totem_ids.sort()
	assert totem_ids == ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]

	# ensure hero power can only be used again after a totem was destroyed
	assert not game.current_player.hero.power.is_usable()
	game.current_player.field[0].destroy()
	assert game.current_player.hero.power.is_usable()

	# ensure that hero power cannot be used on full board
	for i in range(4):
		game.player1.give(WISP).play()
	assert len(game.player1.field) == 7
	assert not game.player1.hero.power.is_usable()

	game.current_player.field[0].destroy()
	assert game.current_player.hero.power.is_usable()


def test_healing_totem():
	game = prepare_game()
	footman = game.current_player.give(GOLDSHIRE_FOOTMAN)
	footman.play()
	game.current_player.give(MOONFIRE).play(target=footman)
	healtotem = game.current_player.give("NEW1_009")
	healtotem.play()
	game.current_player.give(MOONFIRE).play(target=game.current_player.hero)
	assert footman.health == 1
	assert game.current_player.hero.health == 29
	game.end_turn()

	assert footman.health == 2
	assert game.current_player.opponent.hero.health == 29

	# will not heal when it is not the owner's turn
	game.current_player.give(MOONFIRE).play(target=footman)
	game.end_turn()
	assert footman.health == 1


def test_warlock():
	game = prepare_empty_game(CardClass.WARLOCK, CardClass.WARLOCK)
	game.current_player.discard_hand()
	assert not game.current_player.hero.power.targets
	assert game.current_player.hero.power.is_usable()
	game.current_player.give(WISP).shuffle_into_deck()
	game.current_player.give(WISP).shuffle_into_deck()
	assert len(game.current_player.deck) == 2
	game.current_player.hero.power.use()
	assert len(game.current_player.hand) == 1
	assert game.current_player.hero.health == 28
	game.skip_turn()

	# player draws a card at the beginning of the turn
	assert len(game.current_player.hand) == 2
	game.current_player.give("EX1_096").shuffle_into_deck()
	game.current_player.give("EX1_096").shuffle_into_deck()
	# draw till the hand is full
	for i in range(8):
		game.current_player.give(MOONFIRE)
	assert len(game.current_player.hand) == 10
	assert len(game.current_player.deck) == 2
	assert game.current_player.hero.power.is_usable()
	game.current_player.hero.power.use()
	# discard the card without deathrattles
	assert len(game.current_player.deck) == 1
	assert len(game.current_player.hand) == 10


def test_demon_hunter():
	game = prepare_game(CardClass.DEMONHUNTER, CardClass.DEMONHUNTER)
	assert game.current_player.hero.health == 30
	assert game.current_player.hero.armor == 0
	assert game.current_player.hero.atk == 0
	assert not game.current_player.hero.can_attack()
	game.current_player.hero.power.use()
	assert not game.current_player.hero.power.is_usable()
	assert game.current_player.hero.armor == 0
	assert game.current_player.hero.atk == 1
	assert game.current_player.hero.can_attack()
	game.current_player.hero.attack(target=game.current_player.opponent.hero)
	assert not game.current_player.hero.can_attack()
