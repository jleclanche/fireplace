from fireplace.logging import get_logger
from fireplace.player import Player


class BaseAI(Player):
	"""
	Interface that AI players must implement
	"""
	def __init__(self, *args):
		super().__init__(*args)

	def mulligan(self):
		raise NotImplementedError

	def turn(self):
		raise NotImplementedError
