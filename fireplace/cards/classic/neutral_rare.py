from ..utils import *


class CS2_181:
	"""Injured Blademaster"""
	play = Hit(SELF, 4)


class EX1_001:
	"""Lightwarden"""
	events = Heal().on(Buff(SELF, "EX1_001e"))


EX1_001e = buff(atk=2)


class EX1_004:
	"""Young Priestess"""
	events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "EX1_004e"))


EX1_004e = buff(health=1)


class EX1_006:
	"""Alarm-o-Bot"""
	events = OWN_TURN_BEGIN.on(Swap(SELF, RANDOM(FRIENDLY_HAND + MINION)))


class EX1_009:
	"""Angry Chicken"""
	enrage = Refresh(SELF, buff="EX1_009e")


EX1_009e = buff(atk=5)


class EX1_043:
	"""Twilight Drake"""
	play = Buff(SELF, "EX1_043e") * Count(FRIENDLY_HAND)


EX1_043e = buff(health=1)


class EX1_044:
	"""Questing Adventurer"""
	events = OWN_CARD_PLAY.on(Buff(SELF, "EX1_044e"))


EX1_044e = buff(+1, +1)


class EX1_050:
	"""Coldlight Oracle"""
	play = Draw(ALL_PLAYERS) * 2


class EX1_055:
	"""Mana Addict"""
	events = OWN_SPELL_PLAY.on(Buff(SELF, "EX1_055o"))


EX1_055o = buff(atk=2)


class EX1_058:
	"""Sunfury Protector"""
	play = Taunt(SELF_ADJACENT)


class EX1_059:
	"""Crazed Alchemist"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Buff(TARGET, "EX1_059e")


EX1_059e = AttackHealthSwapBuff()


class EX1_076:
	"""Pint-Sized Summoner"""
	update = (
		(Attr(CONTROLLER, GameTag.NUM_MINIONS_PLAYED_THIS_TURN) == 0) &
		Refresh(FRIENDLY_HAND + MINION, {GameTag.COST: -1})
	)


class EX1_080:
	"""Secretkeeper"""
	events = OWN_SECRET_PLAY.on(Buff(SELF, "EX1_080o"))


EX1_080o = buff(+1, +1)


class EX1_085:
	"""Mind Control Tech"""
	play = (Count(ENEMY_MINIONS) >= 4) & Steal(RANDOM_ENEMY_MINION)


class EX1_089:
	"""Arcane Golem"""
	play = GainMana(OPPONENT, 1)


class EX1_093:
	"""Defender of Argus"""
	play = Buff(SELF_ADJACENT, "EX1_093e")


EX1_093e = buff(+1, +1, taunt=True)


class EX1_095:
	"""Gadgetzan Auctioneer"""
	events = OWN_SPELL_PLAY.on(Draw(CONTROLLER))


class EX1_097:
	"""Abomination"""
	deathrattle = Hit(ALL_CHARACTERS, 2)


class EX1_103:
	"""Coldlight Seer"""
	play = Buff(FRIENDLY_MINIONS + MURLOC - SELF, "EX1_103e")


EX1_103e = buff(health=2)


class EX1_284:
	"""Azure Drake"""
	play = Draw(CONTROLLER)


class EX1_509:
	"""Murloc Tidecaller"""
	events = Summon(ALL_PLAYERS, MURLOC).on(Buff(SELF, "EX1_509e"))


EX1_509e = buff(atk=1)


class EX1_584:
	"""Ancient Mage"""
	play = Buff(SELF_ADJACENT, "EX1_584e")


class EX1_597:
	"""Imp Master"""
	events = OWN_TURN_END.on(Hit(SELF, 1), Summon(CONTROLLER, "EX1_598"))


class EX1_616:
	"""Mana Wraith"""
	update = Refresh(IN_HAND + MINION, {GameTag.COST: +1})


class NEW1_019:
	"""Knife Juggler"""
	events = Summon(CONTROLLER, MINION - SELF).after(Hit(RANDOM_ENEMY_CHARACTER, 1))


class NEW1_020:
	"""Wild Pyromancer"""
	events = OWN_SPELL_PLAY.after(Hit(ALL_MINIONS, 1))


class NEW1_025:
	"""Bloodsail Corsair"""
	play = Hit(ENEMY_WEAPON, 1)


class NEW1_026:
	"""Violet Teacher"""
	events = OWN_SPELL_PLAY.on(Summon(CONTROLLER, "NEW1_026t"))


class NEW1_037:
	"""Master Swordsmith"""
	events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "NEW1_037e"))


NEW1_037e = buff(atk=1)


class NEW1_041:
	"""Stampeding Kodo"""
	play = Destroy(RANDOM(ENEMY_MINIONS + (ATK <= 2)))
