from .utils import CardList


class Deck(CardList):
	MAX_CARDS = 30
	MAX_UNIQUE_CARDS = 2
	MAX_UNIQUE_LEGENDARIES = 1

	def __init__(self, cards=None):
		super().__init__(cards or [])
		self.hero = None

	def __repr__(self):
		return "<Deck (%i cards)>" % (len(self))
