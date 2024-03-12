from ..utils import *


##
# Minions

class DAL_146:
	"""Bronze Herald"""
	# <b>Deathrattle:</b> Add two 4/4 Dragons to your hand.
	pass


class DAL_147:
	"""Dragon Speaker"""
	# <b>Battlecry:</b> Give all Dragons in your hand +3/+3.
	pass


class DAL_573:
	"""Commander Rhyssa"""
	# Your <b>Secrets</b> trigger twice.
	update = Refresh(CONTROLLER, {enums.EXTRA_TRIGGER_SECRET: True})


class DAL_581:
	"""Nozari"""
	# <b>Battlecry:</b> Restore both heroes to full Health.
	play = FullHeal(ALL_HEROES)


##
# Spells

class DAL_141:
	"""Desperate Measures"""
	# <b>Twinspell</b> Cast a random Paladin <b>Secret</b>.
	pass


class DAL_568:
	"""Lightforged Blessing"""
	# <b>Twinspell</b> Give a friendly minion <b>Lifesteal</b>.
	pass


class DAL_570:
	"""Never Surrender!"""
	# <b>Secret:</b> When your opponent casts a spell, give your minions +2_Health.
	pass


class DAL_727:
	"""Call to Adventure"""
	# Draw the lowest Cost minion from your deck. Give it +2/+2.
	pass


class DAL_731:
	"""Duel!"""
	# Summon a minion from each player's deck. They fight!
	pass


##
# Weapons

class DAL_571:
	"""Mysterious Blade"""
	# <b>Battlecry:</b> If you control a <b>Secret</b>, gain +1 Attack.
	pass
