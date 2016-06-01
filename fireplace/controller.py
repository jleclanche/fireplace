import asyncio
from hearthstone.enums import Step
from fireplace.ai.player import BaseAI
from fireplace.exceptions import GameOver
from fireplace.logging import get_logger


class GameController:
	def __init__(self, game):
		self.log = get_logger("fireplace")
		self.game = game
		self.game.manager.register(self)
		self.previous_step = Step.INVALID

	def action_start(self, type, source, index, target):
		pass

	def action_end(self, type, source):
		pass

	def new_entity(self, entity):
		pass

	def start_game(self):
		self.log.info("Game has started")
		# note: choice will be None here but won't be when mulligan() starts
		for player in self.game.players:
			if isinstance(player, BaseAI):
				self.event_loop.call_soon(player.mulligan)

	def game_step(self, step, next_step):
		self.log.debug("Game.STEP changes to %s", step)
		if step == Step.MAIN_ACTION and self.previous_step == Step.MAIN_START:
			self.log.info("Turn %i starting for player %r", self.game.turn, self.game.current_player)
			self.event_loop.call_soon(self.do_turn)
		self.previous_step = step

	def do_turn(self):
		self.log.debug("Starting turn callback")
		if isinstance(self.game.current_player, BaseAI):
			try:
				self.game.current_player.turn()
				# note: does not return until the next turn has started
				self.game.end_turn()
			except GameOver:
				self.event_loop.stop()
				self.log.info("Game ended normally")
		self.log.debug("Ending turn callback")

	def run(self):
		# note: an event loop for the thread must exist before calling run()
		# this is guaranteed for single-threaded programs
		self.event_loop = asyncio.get_event_loop()
		self.game.start()
		self.event_loop.run_forever()
