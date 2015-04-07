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


class PlayerManager(Manager):
	map = {
		GameTag.CARDTYPE: "type",
		GameTag.COMBO_ACTIVE: "combo",
		GameTag.FATIGUE: "fatigueCounter",
		GameTag.FIRST_PLAYER: "firstPlayer",
		GameTag.HERO_ENTITY: "hero",
		GameTag.LAST_CARD_PLAYED: "lastCardPlayed",
		GameTag.MAXHANDSIZE: "maxHandSize",
		GameTag.MAXRESOURCES: "maxResources",
		GameTag.NUM_CARDS_DRAWN_THIS_TURN: "cardsDrawnThisTurn",
		GameTag.NUM_CARDS_PLAYED_THIS_TURN: "cardsPlayedThisTurn",
		GameTag.NUM_MINIONS_PLAYED_THIS_TURN: "minionsPlayedThisTurn",
		GameTag.NUM_MINIONS_PLAYER_KILLED_THIS_TURN: "minionsKilledThisTurn",
		GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME: "timesHeroPowerUsedThisGame",
		GameTag.OUTGOING_HEALING_ADJUSTMENT: "outgoingHealingAdjustment",
		GameTag.RECALL_OWED: "overloaded",
		GameTag.RESOURCES_USED: "usedMana",
		GameTag.TEMP_RESOURCES: "tempMana",
	}
