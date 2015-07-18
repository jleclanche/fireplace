from ..utils import *


# Injured Blademaster
class CS2_181:
	play = Hit(SELF, 4)


# Young Priestess
class EX1_004:
	events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "EX1_004e"))


# Alarm-o-Bot
class EX1_006:
	events = OWN_TURN_BEGIN.on(Swap(SELF, RANDOM(CONTROLLER_HAND + MINION)))


# Twilight Drake
class EX1_043:
	play = Buff(SELF, "EX1_043e") * Count(CONTROLLER_HAND)


# Questing Adventurer
class EX1_044:
	events = OWN_CARD_PLAY.on(Buff(SELF, "EX1_044e"))


# Coldlight Oracle
class EX1_050:
	play = Draw(ALL_PLAYERS) * 2


# Mana Addict
class EX1_055:
	events = OWN_SPELL_PLAY.on(Buff(SELF, "EX1_055o"))


# Sunfury Protector
class EX1_058:
	play = SetTag(SELF_ADJACENT, {GameTag.TAUNT: True})


# Crazed Alchemist
class EX1_059:
	play = Buff(TARGET, "EX1_059e")

class EX1_059e:
	atk = lambda self, i: self._xatk
	max_health = lambda self, i: self._xhealth

	def apply(self, target):
		self._xhealth = target.atk
		self._xatk = target.health


# Secretkeeper
class EX1_080:
	events = OWN_SECRET_PLAY.on(Buff(SELF, "EX1_080o"))


# Mind Control Tech
class EX1_085:
	play = Find(ENEMY_MINIONS, 4) & Steal(RANDOM_ENEMY_MINION)


# Arcane Golem
class EX1_089:
	play = GainMana(OPPONENT, 1)


# Defender of Argus
class EX1_093:
	play = Buff(SELF_ADJACENT, "EX1_093e")


# Gadgetzan Auctioneer
class EX1_095:
	events = OWN_SPELL_PLAY.on(Draw(CONTROLLER))


# Abomination
class EX1_097:
	deathrattle = Hit(ALL_CHARACTERS, 2)


# Coldlight Seer
class EX1_103:
	play = Buff(ALL_MINIONS + MURLOC - SELF, "EX1_103e")


# Azure Drake
class EX1_284:
	play = Draw(CONTROLLER)


# Murloc Tidecaller
class EX1_509:
	events = Summon(ALL_PLAYERS, MURLOC).on(Buff(SELF, "EX1_509e"))


# Ancient Mage
class EX1_584:
	play = Buff(SELF_ADJACENT, "EX1_584e")


# Imp Master
class EX1_597:
	events = OWN_TURN_END.on(Hit(SELF, 1), Summon(CONTROLLER, "EX1_598"))


# Knife Juggler
class NEW1_019:
	events = Summon(CONTROLLER, MINION - SELF).after(Hit(RANDOM_ENEMY_CHARACTER, 1))


# Wild Pyromancer
class NEW1_020:
	events = OWN_SPELL_PLAY.after(Hit(ALL_MINIONS, 1))


# Bloodsail Corsair
class NEW1_025:
	play = Hit(ENEMY_WEAPON, 1)


# Violet Teacher
class NEW1_026:
	events = OWN_SPELL_PLAY.on(Summon(CONTROLLER, "NEW1_026t"))


# Master Swordsmith
class NEW1_037:
	events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "NEW1_037e"))


# Stampeding Kodo
class NEW1_041:
	def play(self):
		targets = [t for t in self.controller.opponent.field if t.atk <= 2]
		if targets:
			return Destroy(random.choice(targets))
