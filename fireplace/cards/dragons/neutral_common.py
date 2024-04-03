from ..utils import *


##
# Minions

class DRG_049:
	"""Tasty Flyfish"""
	# <b>Deathrattle:</b> Give a Dragon in your hand +2/+2.
	deathrattle = Buff(RANDOM(FRIENDLY_HAND + DRAGON), "DRG_049e")


DRG_049e = buff(+2, +2)


class DRG_050:
	"""Devoted Maniac"""
	# <b>Rush</b> <b>Battlecry:</b> <b>Invoke</b> Galakrond.
	play = INVOKE


class DRG_054:
	"""Big Ol' Whelp"""
	# <b>Battlecry:</b> Draw a card.
	play = Draw(CONTROLLER)


class DRG_056:
	"""Parachute Brigand"""
	# [x]After you play a Pirate, summon this minion from your hand.
	class Hand:
		events = Play(CONTROLLER, PIRATE).after(
			Summon(CONTROLLER, SELF)
		)


class DRG_057:
	"""Hot Air Balloon"""
	# At the start of your turn, gain +1 Health.
	events = OWN_TURN_BEGIN.on(Buff(SELF, "DRG_057e"))


DRG_057e = buff(health=1)


class DRG_058:
	"""Wing Commander"""
	# Has +2 Attack for each Dragon in your hand.
	play = Buff(SELF, "DRG_058e") * Count(FRIENDLY_HAND + DRAGON)


DRG_058e = buff(atk=2)


class DRG_059:
	"""Goboglide Tech"""
	# <b>Battlecry:</b> If you control a_Mech, gain +1/+1 and_<b>Rush</b>.
	powered_up = Find(FRIENDLY_MINIONS + MECH)
	play = powered_up & Buff(SELF, "DRG_059e")


DRG_059e = buff(+1, +1, rush=True)


class DRG_060:
	"""Fire Hawk"""
	# <b>Battlecry:</b> Gain +1 Attack for each card in your opponent's hand.
	play = Buff(SELF, "DRG_060e") * Count(ENEMY_HAND)


DRG_060e = buff(atk=1)


class DRG_067:
	"""Troll Batrider"""
	# <b>Battlecry:</b> Deal 3 damage to a random enemy minion.
	play = Hit(RANDOM_ENEMY_CHARACTER, 3)


class DRG_068:
	"""Living Dragonbreath"""
	# Your minions can't be_<b>Frozen</b>.
	update = Refresh(FRIENDLY_MINIONS, {GameTag.CANT_BE_FROZEN: True})


class DRG_069:
	"""Platebreaker"""
	# <b>Battlecry:</b> Destroy your opponent's Armor.
	def play(self):
		self.controller.opponent.hero.armor = 0


class DRG_074:
	"""Camouflaged Dirigible"""
	# <b>Battlecry:</b> Give your other Mechs <b>Stealth</b> until your_next turn.
	play = (
		Buff(FRIENDLY_MINIONS + MECH - SELF, "DRG_074e"),
		Stealth(FRIENDLY_MINIONS + MECH - SELF)
	)


class DRG_074e:
	events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class DRG_081:
	"""Scalerider"""
	# <b>Battlecry:</b> If you're holding a Dragon, deal 2 damage.
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE_AND_DRAGON_IN_HAND: 0}
	powered_up = HOLDING_DRAGON
	play = powered_up & Hit(TARGET, 2)


class DRG_213:
	"""Twin Tyrant"""
	# <b>Battlecry:</b> Deal 4 damage to two random enemy minions.
	play = Hit(RANDOM_ENEMY_MINION * 2, 4)


class DRG_242:
	"""Shield of Galakrond"""
	# <b>Taunt</b> <b>Battlecry:</b> <b>Invoke</b> Galakrond.
	play = INVOKE
