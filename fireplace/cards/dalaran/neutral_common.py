from ..utils import *


##
# Minions

class DAL_077:
	"""Toxfin"""
	# <b>Battlecry:</b> Give a friendly Murloc <b>Poisonous</b>.
	play = GivePoisonous(TARGET)


class DAL_078:
	"""Traveling Healer"""
	# [x]<b>Divine Shield</b> <b>Battlecry:</b> Restore #3 Health.
	play = Heal(TARGET, 3)


class DAL_086:
	"""Sunreaver Spy"""
	# <b>Battlecry:</b> If you control a <b>Secret</b>, gain +1/+1.
	powered_up = Find(FRIENDLY_SECRETS)
	play = powered_up & Buff(SELF, "DAL_086e")


DAL_086e = buff(+1, +1)


class DAL_088:
	"""Safeguard"""
	# [x]<b>Taunt</b> <b>Deathrattle:</b> Summon a 0/5 Vault Safe with <b>Taunt</b>.
	deathrattle = Summon(CONTROLLER, "DAL_088t")


class DAL_089:
	"""Spellbook Binder"""
	# <b>Battlecry:</b> If you have <b>Spell Damage</b>, draw a card.
	powered_up = Find(FRIENDLY + SPELLPOWER)
	play = powered_up & Draw(CONTROLLER)


class DAL_095:
	"""Violet Spellsword"""
	# [x]<b>Battlecry:</b> Gain +1 Attack for each spell in your hand.
	play = Buff(SELF, "DAL_095e") * Count(FRIENDLY_HAND + SPELL)


DAL_095e = buff(atk=1)


class DAL_400:
	"""EVIL Cable Rat"""
	# <b>Battlecry:</b> Add a <b>Lackey</b> to_your hand.
	play = Give(CONTROLLER, RandomLackey())


class DAL_544:
	"""Potion Vendor"""
	# <b>Battlecry:</b> Restore #2 Health to all friendly characters.
	play = Heal(FRIENDLY_CHARACTERS, 2)


class DAL_551:
	"""Proud Defender"""
	# <b>Taunt</b> Has +2 Attack while you [x]have no other minions.
	update = Find(FRIENDLY_MINIONS - SELF) | Refresh(SELF, {GameTag.ATK: +2})


class DAL_560:
	"""Heroic Innkeeper"""
	# <b>Taunt.</b> <b>Battlecry:</b> Gain +2/+2 for each other friendly minion.
	play = Buff(SELF, "DAL_560e2") * Count(FRIENDLY_MINIONS - SELF)


DAL_560e2 = buff(+2, +2)


class DAL_566:
	"""Eccentric Scribe"""
	# <b>Deathrattle:</b> Summon four 1/1 Vengeful Scrolls.
	deathrattle = Summon(CONTROLLER, "DAL_566t") * 4


class DAL_735:
	"""Dalaran Librarian"""
	# <b>Battlecry:</b> <b>Silence</b> adjacent minions.
	play = Silence(SELF_ADJACENT)


class DAL_743:
	"""Hench-Clan Hogsteed"""
	# <b>Rush</b> <b>Deathrattle:</b> Summon a 1/1 Murloc.
	deathrattle = Summon(CONTROLLER, "DAL_743t")


class DAL_744:
	"""Faceless Rager"""
	# <b>Battlecry:</b> Copy a friendly minion's Health.
	play = CopyStateBuff(TARGET, "DAL_744e")


class DAL_744e:
	max_health = lambda self, _: self._xhealth


class DAL_747:
	"""Flight Master"""
	# <b>Battlecry:</b> Summon a 2/2 Gryphon for each player.
	play = Summon(ALL_PLAYERS, "DAL_747t")


class DAL_771:
	"""Soldier of Fortune"""
	# Whenever this minion attacks, give your opponent a Coin.
	events = Attack(SELF).on(Give(OPPONENT, THE_COIN))
