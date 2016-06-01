from hearthstone.enums import CardClass
from fireplace.ai.player import BaseAI
from fireplace.logging import get_logger


class PassTurnAI(BaseAI):
	"""
	The simplest possible AI mulligans no cards and passes every turn
	"""
	def __init__(self, name, *args):
		super().__init__(name, *args)
		self.logger = get_logger("P-%s" % name)

	def mulligan(self):
		if self.choice is not None:
			self.log("Keeping all cards")
			self.choice.choose()

	def turn(self):
		self.log("Passing the turn")


class HeroPowerAI(BaseAI):
	"""
	An example AI which uses its hero power whenever possible
	"""
	def __init__(self, name, *args):
		super().__init__(name, *args)
		self.logger = get_logger("P-%s" % name)

	def mulligan(self):
		if self.choice is not None:
			self.log("Keeping all cards")
			self.choice.choose()

	def turn(self):
		while self.hero.power.is_usable():
			self.log("Playing hero power")
			if self.hero.power.has_target():
				if self.hero.power.card_class == CardClass.MAGE:
					# mage pings opponent's face
					self.hero.power.use(self.opponent.hero)
				elif self.hero.power.card_class == CardClass.PRIEST:
					# priest heals own face
					self.hero.power.use(self.hero)
			else:
				# other other 7 heroes have no hero power target
				self.hero.power.use()

		self.log("Can't play hero power anymore this turn")
		self.log("Passing the turn")
