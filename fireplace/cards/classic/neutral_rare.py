from ..utils import *


# Injured Blademaster
class CS2_181:
	action = [Hit(SELF, 4)]


# Young Priestess
class EX1_004:
	OWN_TURN_END = [Buff(RANDOM_FRIENDLY_MINION - SELF, "EX1_004e")]


# Alarm-o-Bot
class EX1_006:
	OWN_TURN_BEGIN = [Swap(SELF, (CONTROLLER_HAND + MINION))]


# Twilight Drake
class EX1_043:
	def action(self):
		return [Buff(SELF, "EX1_043e") * len(self.controller.hand)]


# Questing Adventurer
class EX1_044:
	OWN_CARD_PLAYED = [Buff(SELF, "EX1_044e")]


# Coldlight Oracle
class EX1_050:
	action = [Draw(ALL_PLAYERS, 2)]


# Mana Addict
class EX1_055:
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			return [Buff(SELF, "EX1_055o")]


# Sunfury Protector
class EX1_058:
	action = [SetTag(SELF_ADJACENT, {GameTag.TAUNT: True})]


# Crazed Alchemist
class EX1_059:
	action = [Buff(TARGET, "EX1_059e")]

class EX1_059e:
	atk = lambda self, i: self._xatk
	maxHealth = lambda self, i: self._xhealth

	def apply(self, target):
		self._xhealth = target.atk
		self._xatk = target.health


# Secretkeeper
class EX1_080:
	def CARD_PLAYED(self, player, card):
		if card.secret:
			return [Buff(SELF, "EX1_080o")]


# Mind Control Tech
class EX1_085:
	def action(self):
		if len(self.controller.opponent.field) >= 4:
			return [TakeControl(RANDOM_ENEMY_MINION)]


# Arcane Golem
class EX1_089:
	action = [GiveMana(OPPONENT, 1)]


# Defender of Argus
class EX1_093:
	action = [Buff(SELF_ADJACENT, "EX1_093e")]


# Gadgetzan Auctioneer
class EX1_095:
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			return [Draw(CONTROLLER, 1)]


# Abomination
class EX1_097:
	deathrattle = [Hit(ALL_CHARACTERS, 2)]


# Coldlight Seer
class EX1_103:
	action = [Buff(ALL_MINIONS + MURLOC - SELF, "EX1_103e")]


# Azure Drake
class EX1_284:
	action = [Draw(CONTROLLER, 1)]


# Murloc Tidecaller
class EX1_509:
	def MINION_SUMMON(self, player, minion):
		if minion.race == Race.MURLOC and minion != self:
			# NOTE: We have to check against ourselves here because the
			# Battlecry happens when we are already in play
			return [Buff(SELF, "EX1_509e")]


# Ancient Mage
class EX1_584:
	action = [Buff(SELF_ADJACENT, "EX1_584e")]


# Imp Master
class EX1_597:
	OWN_TURN_END = [Hit(SELF, 1), Summon(CONTROLLER, "EX1_598")]


# Knife Juggler
class NEW1_019:
	OWN_MINION_SUMMON = [Hit(RANDOM_ENEMY_CHARACTER, 1)]


# Wild Pyromancer
class NEW1_020:
	def AFTER_OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			return [Hit(ALL_MINIONS, 1)]


# Bloodsail Corsair
class NEW1_025:
	action = [Hit(ENEMY_WEAPON, 1)]


# Violet Teacher
class NEW1_026:
	def OWN_CARD_PLAYED(self, card):
		if card.type == CardType.SPELL:
			return [Summon(CONTROLLER, "NEW1_026t")]


# Master Swordsmith
class NEW1_037:
	OWN_TURN_END = [Buff(RANDOM_FRIENDLY_MINION - SELF, "NEW1_037e")]


# Stampeding Kodo
class NEW1_041:
	def action(self):
		targets = [t for t in self.controller.opponent.field if t.atk <= 2]
		if targets:
			return [Destroy(random.choice(targets))]
