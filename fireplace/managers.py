from .enums import GameTag


class Manager(object):
	def __init__(self, obj):
		self.obj = obj

	def __getitem__(self, tag):
		return getattr(self.obj, self.map[tag])

	def __setitem__(self, tag, value):
		setattr(self.obj, self.map[tag], value)


class GameManager(Manager):
	map = {
		GameTag.NUM_MINIONS_KILLED_THIS_TURN: "minionsKilledThisTurn",
		GameTag.PROPOSED_ATTACKER: "proposedAttacker",
		GameTag.PROPOSED_DEFENDER: "proposedDefender",
		GameTag.TURN: "turn",
	}
