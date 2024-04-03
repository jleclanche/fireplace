from ..utils import *


##
# Minions

class DAL_146:
	"""Bronze Herald"""
	# <b>Deathrattle:</b> Add two 4/4 Dragons to your hand.
	deathrattle = Give(CONTROLLER, "DAL_146t") * 2


class DAL_147:
	"""Dragon Speaker"""
	# <b>Battlecry:</b> Give all Dragons in your hand +3/+3.
	play = Buff(FRIENDLY_HAND + DRAGON, "DAL_147e")


DAL_147e = buff(+3, +3)


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
	requirements = {
		PlayReq.REQ_SECRET_ZONE_CAP_FOR_NON_SECRET: 0,
	}
	play = CastSpell(RandomSpell(secret=True, card_class=CardClass.PALADIN))


class DAL_141ts(DAL_141):
	pass


class DAL_568:
	"""Lightforged Blessing"""
	# <b>Twinspell</b> Give a friendly minion <b>Lifesteal</b>.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
	}
	play = GiveLifesteal(TARGET)


class DAL_568ts(DAL_568):
	pass


class DAL_570:
	"""Never Surrender!"""
	# <b>Secret:</b> When your opponent casts a spell, give your minions +2_Health.
	secret = Play(OPPONENT, SPELL).on(
		Reveal(SELF), Buff(FRIENDLY_MINIONS, "DAL_570e")
	)


DAL_570e = buff(health=2)


class DAL_727:
	"""Call to Adventure"""
	# Draw the lowest Cost minion from your deck. Give it +2/+2.
	play = ForceDraw(LOWEST_ATK(FRIENDLY_DECK + MINION)).then(
		Buff(ForceDraw.TARGET, "DAL_727e")
	)


DAL_727e = buff(+2, +2)


class DAL_731:
	"""Duel!"""
	# Summon a minion from each player's deck. They fight!
	requirements = {
		PlayReq.REQ_BOARD_NOT_COMPLETELY_FULL: 0,
	}
	play = Attack(
		Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION)),
		Summon(OPPONENT, RANDOM(ENEMY_DECK + MINION)),
	)


##
# Weapons

class DAL_571:
	"""Mysterious Blade"""
	# <b>Battlecry:</b> If you control a <b>Secret</b>, gain +1 Attack.
	powered_up = Find(FRIENDLY_SECRETS)
	play = powered_up & Buff(SELF, "DAL_571e")


DAL_571e = buff(atk=1)
