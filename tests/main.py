#!/usr/bin/env python
import sys; sys.path.append("..")
import fireplace
import logging
import random
from fireplace.heroes import *
from fireplace.enums import *

logging.getLogger().setLevel(logging.DEBUG)


def prepare_game(hero1=MAGE, hero2=WARRIOR):
	print("Initializing a new game")
	deck1 = fireplace.Deck.randomDraft(hero=hero1)
	deck2 = fireplace.Deck.randomDraft(hero=hero2)
	player1 = fireplace.Player(name="Player1", deck=deck1)
	player2 = fireplace.Player(name="Player2", deck=deck2)
	game = fireplace.Game(players=(player1, player2))
	game.start()

	return game


def test_positioning():
	game = prepare_game()
	wisp1 = game.currentPlayer.give("CS2_231")
	wisp1.play()
	wisp2 = game.currentPlayer.give("CS2_231")
	wisp2.play()
	wisp3 = game.currentPlayer.give("CS2_231")
	wisp3.play()

	assert wisp1.adjacentMinions == (None, wisp2)
	assert wisp2.adjacentMinions == (wisp1, wisp3)
	assert wisp3.adjacentMinions == (wisp2, None)
	game.endTurn(); game.endTurn()
	flametongue = game.currentPlayer.give("EX1_565")
	flametongue.play()
	wisp4 = game.currentPlayer.give("CS2_231")
	wisp4.play()
	print(game.auras)
	print(flametongue, flametongue.slots)
	assert wisp1.atk == 1
	assert wisp2.atk == 1
	assert wisp3.atk == 3
	assert flametongue.atk == 0, flametongue.atk
	assert wisp4.atk == 3


def test_armor():
	game = prepare_game(WARRIOR, WARRIOR)
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	assert game.currentPlayer.hero.armor == 0
	assert not game.currentPlayer.hero.power.exhausted
	assert game.currentPlayer.hero.power.isPlayable()
	game.currentPlayer.hero.power.play()
	assert game.currentPlayer.hero.power.exhausted
	assert not game.currentPlayer.hero.power.isPlayable()
	assert game.currentPlayer.hero.armor == 2
	assert game.currentPlayer.mana == 2
	game.endTurn()
	# Play an axe
	game.currentPlayer.give("CS2_106").play()
	game.currentPlayer.hero.attack(game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 29
	assert game.currentPlayer.opponent.hero.armor == 0


def test_freeze():
	game = prepare_game()
	flameimp = game.currentPlayer.give("EX1_319")
	flameimp.play()
	game.endTurn()

	frostshock = game.currentPlayer.give("CS2_037")
	frostshock.play(target=flameimp)
	assert flameimp.frozen
	game.endTurn()

	assert flameimp.frozen
	assert not flameimp.canAttack()
	game.endTurn()
	assert not flameimp.frozen


def test_mage_priest():
	game = prepare_game(MAGE, PRIEST)
	# With this seed, Mage starts
	assert game.currentPlayer.hero.id is MAGE
	game.endTurn(); game.endTurn()
	assert game.currentPlayer.hero.health == 30
	game.currentPlayer.hero.power.play(target=game.currentPlayer.opponent.hero)
	game.endTurn()
	assert game.currentPlayer.hero.health == 29
	game.currentPlayer.hero.power.play(target=game.currentPlayer.hero)
	assert game.currentPlayer.hero.health == 30


def test_paladin_shaman():
	game = prepare_game(PALADIN, SHAMAN)
	# With this seed, Shaman starts
	assert game.currentPlayer.hero.id is SHAMAN
	game.endTurn(); game.endTurn()
	assert len(game.currentPlayer.hero.power.data.entourage) == 4
	game.currentPlayer.hero.power.play()
	assert game.currentPlayer.field[0].id == "CS2_051"
	game.endTurn()
	game.currentPlayer.hero.power.play()
	assert game.currentPlayer.field[0].id == "CS2_101t"
	game.endTurn()


def test_deathrattle():
	game = prepare_game()
	game.endTurn(); game.endTurn()

	loothoarder = game.currentPlayer.give("EX1_096")
	loothoarder.play()
	cardcount = len(game.currentPlayer.hand)

	game.endTurn()
	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=loothoarder)

	assert len(game.currentPlayer.opponent.hand) == cardcount + 1

	# test soul of the forest: deathrattle in slots
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	sotf = game.currentPlayer.give("EX1_158")
	sotf.play()
	assert len(archer.slots) == 1
	game.endTurn()

	archer2 = game.currentPlayer.give("CS2_189")
	archer2.play(target=archer)

	assert len(game.currentPlayer.opponent.field) == 1


def test_mana():
	game = prepare_game()
	footman = game.currentPlayer.give("CS1_042")
	assert footman.cost == 1
	footman.play()
	assert footman.atk == 1
	assert footman.health == 2
	game.endTurn()

	# Play the coin
	coin = game.currentPlayer.getById("GAME_005")
	coin.play()
	assert game.currentPlayer.mana == 2
	game.endTurn()
	assert game.currentPlayer.opponent.mana == 1

	game.endTurn(); game.endTurn()

	assert game.currentPlayer.mana == 3
	assert game.currentPlayer.maxMana == 3
	felguard = game.currentPlayer.give("EX1_301")
	felguard.play()
	assert game.currentPlayer.mana == 0, game.currentPlayer.mana
	assert game.currentPlayer.maxMana == 2, game.currentPlayer.maxMana


def test_overload():
	game = prepare_game()
	dustdevil = game.currentPlayer.give("EX1_243")
	dustdevil.play()
	assert game.currentPlayer.overloaded == 2
	game.endTurn(); game.endTurn()
	assert game.currentPlayer.mana == 0


def test_charge():
	game = prepare_game()
	wisp = game.currentPlayer.give("CS2_231")
	wisp.play()
	assert not wisp.charge
	assert not wisp.canAttack()
	# play Charge on wisp
	game.currentPlayer.give("CS2_103").play(target=wisp)
	assert wisp.charge
	assert wisp.canAttack()
	wisp.attack(game.currentPlayer.opponent.hero)
	assert not wisp.canAttack()
	game.endTurn()
	game.currentPlayer.getById("GAME_005").play()
	wolfrider = game.currentPlayer.give("CS2_124")
	wolfrider.play()
	assert wolfrider.charge
	assert wolfrider.canAttack()
	game.endTurn()
	assert wisp.canAttack()
	wisp.attack(game.currentPlayer.opponent.hero)
	assert not wisp.canAttack()
	game.endTurn()
	watcher = game.currentPlayer.give("EX1_045")
	watcher.play()
	assert not watcher.canAttack()
	game.currentPlayer.give("CS2_103").play(target=watcher)
	assert not watcher.canAttack()
	game.endTurn(); game.endTurn()
	assert not watcher.canAttack()
	watcher.silence()
	assert watcher.canAttack()


def test_divine_shield():
	game = prepare_game()
	squire = game.currentPlayer.give("EX1_008")
	squire.play()
	assert squire.divineShield
	game.endTurn()

	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=squire)
	assert len(game.currentPlayer.field) == 1
	assert not squire.divineShield
	game.currentPlayer.getById("GAME_005").play()
	archer2 = game.currentPlayer.give("CS2_189")
	archer2.play(target=squire)
	assert len(game.currentPlayer.opponent.field) == 0
	assert not squire.divineShield


def test_stealth_windfury():
	game = prepare_game(MAGE, MAGE)
	worgen = game.currentPlayer.give("EX1_010")
	worgen.play()
	assert worgen.stealthed
	assert not worgen.canAttack()
	game.endTurn()

	archer = game.currentPlayer.give("CS2_189")
	assert len(archer.targets) == 2  # Only the heroes
	game.currentPlayer.getById("GAME_005").play()
	assert len(game.currentPlayer.hero.power.targets) == 2
	game.endTurn()

	worgen.attack(game.currentPlayer.opponent.hero)
	assert not worgen.stealthed
	assert not worgen.canAttack()
	windfury = game.currentPlayer.give("CS2_039")
	windfury.play(target=worgen)
	assert worgen.canAttack()
	worgen.attack(game.currentPlayer.opponent.hero)
	assert not worgen.canAttack()
	game.endTurn()

	assert len(archer.targets) == 3


def test_tags():
	game = prepare_game()

	alakir = game.currentPlayer.give("NEW1_010")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	alakir.play()
	assert alakir.tags[GameTag.CHARGE]
	assert alakir.tags[GameTag.DIVINE_SHIELD]
	assert alakir.tags[GameTag.TAUNT]
	assert alakir.tags[GameTag.WINDFURY]


def test_card_draw():
	game = prepare_game()
	# pass turn 1
	game.endTurn()
	game.endTurn()

	# novice should draw 1 card
	card = game.currentPlayer.give("EX1_015")
	handlength = len(game.currentPlayer.hand)
	card.play()
	# hand should be 1 card played, 1 card drawn; same length
	assert len(game.currentPlayer.hand) == handlength
	game.endTurn()

	# succubus should discard 1 card
	card = game.currentPlayer.give("EX1_306")
	handlength = len(game.currentPlayer.hand)
	card.play()
	assert len(game.currentPlayer.hand) == handlength - 2


def test_deathwing():
	game = prepare_game()
	deathwing = game.currentPlayer.give("NEW1_030")
	# play some wisps
	game.currentPlayer.give("CS2_231").play()
	game.currentPlayer.give("CS2_231").play()
	game.currentPlayer.give("CS2_231").play()

	# fast-forward to turn 10
	for i in range(9 * 2):
		game.endTurn()

	deathwing.play()
	assert not game.currentPlayer.hand
	assert len(game.board) == 1


def test_combo():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.endTurn()
	game.currentPlayer.getById("GAME_005").play()
	# SI:7 with combo
	assert game.currentPlayer.tags[GameTag.COMBO_ACTIVE]
	game.currentPlayer.give("EX1_134").play(target=game.currentPlayer.hero)
	assert game.currentPlayer.hero.health == 28
	game.endTurn()

	# Without combo should not have a target
	assert not game.currentPlayer.tags[GameTag.COMBO_ACTIVE]
	game.currentPlayer.give("EX1_134").play()


def test_kill_command():
	game = prepare_game(HUNTER, HUNTER)
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	kc = game.currentPlayer.give("EX1_539")
	kc.play(target=game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 27
	game.endTurn(); game.endTurn()

	# play a timber wolf before this time
	game.currentPlayer.give("DS1_175").play()
	kc = game.currentPlayer.give("EX1_539")
	kc.play(target=game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 22


def test_end_turn_heal():
	game = prepare_game()

	footman = game.currentPlayer.give("CS1_042")
	footman.play()
	assert footman.health == 2
	game.endTurn()

	# play an archer on the footman
	archer = game.currentPlayer.give("CS2_189")
	archer.play(target=footman)
	assert footman.health == 1
	game.endTurn()

	healtotem = game.currentPlayer.give("NEW1_009")
	healtotem.play()
	game.endTurn()
	assert footman.health == 2
	game.endTurn()
	game.endTurn()
	# check it's still at max health after a couple of turns
	assert footman.health == 2


def test_demolisher():
	game = prepare_game()

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	demolisher = game.currentPlayer.give("EX1_102")
	demolisher.play()

	assert game.currentPlayer.opponent.hero.health == 30
	game.endTurn()
	assert game.currentPlayer.opponent.hero.health == 30
	game.endTurn()
	assert game.currentPlayer.opponent.hero.health == 28


def test_imp_master():
	game = prepare_game()

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	impmaster = game.currentPlayer.give("EX1_597")
	impmaster.play()

	assert impmaster.health == 5
	assert len(impmaster.controller.field) == 1
	game.endTurn()
	assert impmaster.health == 4
	assert len(impmaster.controller.field) == 2
	assert impmaster.controller.field.contains("EX1_598")


def test_auras():
	game = prepare_game()

	wisp1 = game.currentPlayer.give("CS2_231")
	wisp1.play()
	assert wisp1.atk == 1
	game.endTurn()

	# pass next few turns to gain some mana
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	webspinner = game.currentPlayer.give("FP1_011")
	webspinner.play()
	raidleader = game.currentPlayer.give("CS2_122")
	raidleader.play()
	assert raidleader.data.hasAura
	assert raidleader.atk == 2
	assert wisp1.atk == 1
	assert webspinner.atk == 2
	wisp2 = game.currentPlayer.give("CS2_231")
	wisp2.play()
	assert webspinner.atk == 2

	# Test the timber wolf (beast-only) too
	game.currentPlayer.getById("GAME_005").play()
	timberwolf = game.currentPlayer.give("DS1_175")
	timberwolf.play()
	assert timberwolf.atk == 2 # 1 (+1 from RL)
	assert raidleader.atk == 2 # 2 (+0)
	assert len(webspinner.slots) == 2
	assert webspinner.atk == 3 # 1 (+1 from RL, +1 from TW)
	assert wisp2.atk == 2 # 1 (+1 from TW)


def test_bounce():
	game = prepare_game()
	wisp = game.currentPlayer.give("CS2_231")
	wisp.play()
	assert game.currentPlayer.field == [wisp]
	game.endTurn(); game.endTurn()

	brewmaster = game.currentPlayer.give("EX1_049")
	brewmaster.play(target=wisp)
	assert game.currentPlayer.field == [brewmaster]
	assert wisp in game.currentPlayer.hand
	wisp.play()
	game.endTurn(); game.endTurn()

	# test for damage reset on bounce
	brewmaster2 = game.currentPlayer.give("EX1_049")
	moonfire = game.currentPlayer.give("CS2_008")
	moonfire.play(target=brewmaster)
	assert brewmaster.health == 1
	brewmaster2.play(target=brewmaster)
	assert brewmaster.health == 2
	assert brewmaster2.health == 2

	game.endTurn()
	# fill the hand with some bananas
	game.currentPlayer.give("EX1_014t")
	game.currentPlayer.give("EX1_014t")
	game.endTurn()
	vanish = game.currentPlayer.give("NEW1_004")
	vanish.play()
	assert brewmaster not in game.currentPlayer.opponent.hand


def test_arcane_explosion():
	game = prepare_game(MAGE, MAGE)
	# play some wisps
	game.currentPlayer.give("CS2_231").play()
	game.currentPlayer.give("CS2_231").play()
	game.currentPlayer.give("CS2_231").play()
	game.endTurn()

	arcanex = game.currentPlayer.give("CS2_025")
	assert len(game.currentPlayer.opponent.field) == 3
	arcanex.play()
	assert len(game.currentPlayer.opponent.field) == 0


def test_power_overwhelming():
	game = prepare_game()
	power = game.currentPlayer.give("EX1_316")
	wisp = game.currentPlayer.give("CS2_231")
	wisp.play()
	power.play(target=wisp)
	assert wisp.atk == 5
	assert wisp.health == 5
	game.endTurn()
	assert wisp not in game.board


def test_mindgames():
	game = prepare_game(PRIEST, PRIEST)
	mindgames = game.currentPlayer.give("EX1_345")

	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert len(game.currentPlayer.field) == 0
	mindgames.play()
	assert len(game.currentPlayer.field) == 1
	assert game.currentPlayer.field[0].id in game.currentPlayer.opponent.deck


def test_mind_vision():
	game = prepare_game()
	# discard our hand, let's clean this.
	game.currentPlayer.discardHand()
	game.endTurn()

	# play mind vision, should give nothing
	assert len(game.currentPlayer.hand) == 6
	game.currentPlayer.give("CS2_003").play()
	assert len(game.currentPlayer.hand) == 6

	# opponent draws a card, coin mind vision should get that one card
	drawn = game.currentPlayer.opponent.draw()
	game.currentPlayer.getById("GAME_005").play()
	game.currentPlayer.give("CS2_003").play()
	assert game.currentPlayer.hand[-1] == drawn[0]


def test_wild_pyromancer():
	game = prepare_game()
	wisp = game.currentPlayer.give("CS2_231")
	wisp.play()

	game.endTurn(); game.endTurn()

	pyro = game.currentPlayer.give("NEW1_020")
	pyro.play()
	assert pyro.health == 2
	assert wisp.zone == Zone.PLAY

	# play moonfire. wisp should die.
	game.currentPlayer.give("CS2_008").play(target=game.currentPlayer.opponent.hero)
	assert wisp.zone == Zone.GRAVEYARD
	assert pyro.health == 1

	# play circle of healing. pyro should go up to 2hp then back to 1.
	game.currentPlayer.give("EX1_621").play()
	assert pyro.health == 1


def test_poisonous():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.endTurn()
	game.currentPlayer.getById("GAME_005").play()
	cobra = game.currentPlayer.give("EX1_170")
	cobra.play()
	assert cobra.data.poisonous
	game.endTurn()
	zchow = game.currentPlayer.give("FP1_001")
	zchow.play()
	zchow2 = game.currentPlayer.give("FP1_001")
	zchow2.play()
	game.endTurn()
	cobra.attack(target=zchow)
	assert zchow not in game.currentPlayer.opponent.field
	assert zchow.zone == Zone.GRAVEYARD
	game.endTurn()
	zchow2.attack(target=cobra)
	assert zchow2.zone == Zone.GRAVEYARD

	# test silencing the cobra
	zchow3 = game.currentPlayer.give("FP1_001")
	zchow3.play()
	game.endTurn()
	cobra = game.currentPlayer.give("EX1_170")
	cobra.play()
	cobra.silence()
	game.endTurn()
	zchow3.attack(cobra)
	assert zchow3 in game.currentPlayer.field
	assert cobra in game.currentPlayer.opponent.field


def test_cleave():
	game = prepare_game()
	# play some wisps
	game.currentPlayer.give("CS2_231").play()
	game.currentPlayer.give("CS2_231").play()
	game.endTurn()

	# Play the coin
	game.currentPlayer.getById("GAME_005").play()

	cleave = game.currentPlayer.give("CS2_114")
	assert cleave.data.minTargets == 2, cleave.data.minTargets
	assert cleave.isPlayable()
	cleave.play()
	assert len(game.currentPlayer.opponent.field) == 0

	# play another wisp
	game.currentPlayer.give("CS2_231").play()

	game.endTurn()
	cleave2 = game.currentPlayer.give("CS2_114")
	assert not cleave2.isPlayable()


def test_upgrade():
	game = prepare_game()
	axe = game.currentPlayer.give("CS2_106")
	upgrade = game.currentPlayer.give("EX1_409")
	game.endTurn(); game.endTurn()
	axe.play()
	game.currentPlayer.hero.attack(game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 27

	game.endTurn()
	upgrade2 = game.currentPlayer.give("EX1_409")
	upgrade2.play()
	assert game.currentPlayer.hero.atk == 1
	assert game.currentPlayer.hero.weapon.atk == 1
	game.endTurn()
	assert game.currentPlayer.hero.weapon.atk == 3
	assert game.currentPlayer.hero.weapon.durability == 1
	upgrade.play()
	assert game.currentPlayer.hero.weapon.atk == 4
	assert game.currentPlayer.hero.weapon.durability == 2
	game.currentPlayer.hero.attack(game.currentPlayer.opponent.hero)
	assert game.currentPlayer.opponent.hero.health == 23
	assert game.currentPlayer.hero.weapon.durability == 1


CHEAT_MIRROR_ENTITY = True
def test_mctech():
	game = prepare_game()
	game.endTurn(); game.endTurn()
	game.endTurn()
	# play some wisps
	game.currentPlayer.give("CS2_231").play()
	game.currentPlayer.give("CS2_231").play()
	game.currentPlayer.give("CS2_231").play()
	# coin mirror entity
	game.currentPlayer.getById("GAME_005").play()
	if CHEAT_MIRROR_ENTITY:
		# TODO secrets
		game.currentPlayer.give("EX1_294").play()
	game.endTurn()

	assert len(game.currentPlayer.opponent.field) == 3
	# play an mctech. nothing should be controlled.
	game.currentPlayer.give("EX1_085").play()
	assert len(game.currentPlayer.field) == 1
	game.endTurn()
	if CHEAT_MIRROR_ENTITY:
		# mc tech gets copied, board now at 4
		game.currentPlayer.give("EX1_085").play()
	assert len(game.currentPlayer.field) == 4
	game.endTurn()
	game.currentPlayer.give("EX1_085").play()
	assert len(game.currentPlayer.field) == 3
	assert len(game.currentPlayer.opponent.field) == 3


def test_ice_barrier():
	game = prepare_game(MAGE, MAGE)
	icebarrier = game.currentPlayer.give("EX1_289")
	icebarrier2 = game.currentPlayer.give("EX1_289")
	game.endTurn(); game.endTurn()
	game.endTurn(); game.endTurn()

	assert icebarrier.isPlayable()
	icebarrier.play()
	assert not icebarrier2.isPlayable()
	assert game.currentPlayer.secrets
	assert icebarrier in game.currentPlayer.secrets
	game.endTurn(); game.endTurn()
	assert not icebarrier2.isPlayable()


def test_flare():
	game = prepare_game(HUNTER, HUNTER)
	flare = game.currentPlayer.give("EX1_544")
	worgen = game.currentPlayer.give("EX1_010")
	worgen.play()
	game.endTurn()

	avenge = game.currentPlayer.give("FP1_020")
	avenge.play()
	game.endTurn()

	flare.play()
	assert not game.currentPlayer.opponent.secrets
	assert not worgen.stealthed


def test_warlock():
	game = prepare_game(WARLOCK, WARLOCK)
	sacpact = game.currentPlayer.give("NEW1_003")
	assert not sacpact.isPlayable()
	flameimp = game.currentPlayer.give("EX1_319")
	flameimp.play()
	assert game.currentPlayer.hero.health == 27
	assert sacpact.isPlayable()
	sacpact.play(target=flameimp)
	assert game.currentPlayer.hero.health == 30
	game.endTurn()


def main():
	random.seed(12345)
	test_mage_priest()
	test_paladin_shaman()
	test_positioning()
	test_deathrattle()
	test_mana()
	test_card_draw()
	test_deathwing()
	test_armor()
	test_freeze()
	test_bounce()
	test_end_turn_heal()
	test_auras()
	test_divine_shield()
	test_poisonous()
	test_warlock()
	test_overload()
	test_combo()
	test_charge()
	test_stealth_windfury()
	test_tags()
	test_kill_command()
	test_arcane_explosion()
	test_power_overwhelming()
	test_mindgames()
	test_mind_vision()
	test_wild_pyromancer()
	test_demolisher()
	test_imp_master()
	test_cleave()
	test_ice_barrier()
	test_flare()
	test_upgrade()
	test_mctech()
	print("All tests ran OK")


if __name__ == "__main__":
	main()
