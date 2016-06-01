from utils import *
from fireplace.ai.contrib.examples import PassTurnAI
from fireplace.controller import GameController
from fireplace.game import Game


class ConcedeTurn3AI(PassTurnAI):
	def turn(self):
		if self.game.turn >= 3:
			self.concede()
		else:
			super.turn()


def create_ai_game():
	p1_class = random_class()
	p2_class = random_class()
	deck1 = random_draft(p1_class)
	deck2 = random_draft(p2_class)
	player1 = PlayerAI("Player1", deck1, p1_class.default_hero)
	player2 = PlayerAI("Player2", deck2, p2_class.default_hero)
	game = Game(players=(player1, player2))
	return game


def test_controller():
	game = create_ai_game()
	controller = GameController(game)
	controller.run()
	print("Game loop has ended")
