from ..utils import *


##
# Minions

class BOT_243:
	"""Myra Rotspring"""
	# [x]<b>Battlecry:</b> <b>Discover</b> a <b>Deathrattle</b> minion. Also gain its
	# <b>Deathrattle</b>.
	play = Discover(CONTROLLER, RandomMinion(deathrattle=True)).then(
		Retarget(SELF, Discover.CARD),
		Give(CONTROLLER, TARGET),
		CopyDeathrattleBuff(TARGET, "BOT_243e"),
	)


class BOT_283:
	"""Pogo-Hopper"""
	# [x]<b>Battlecry:</b> Gain +2/+2 for each other Pogo-Hopper you played this game.
	play = Buff(SELF, "BOT_283e") * Count(CARDS_PLAYED_THIS_GAME + ID("BOT_283"))


BOT_283e = buff(+2, +2)


class BOT_288:
	"""Lab Recruiter"""
	# <b>Battlecry:</b> Shuffle 3 copies of a friendly minion into your deck.
	play = Shuffle(CONTROLLER, Copy(TARGET)) * 3


class BOT_565:
	"""Blightnozzle Crawler"""
	# <b>Deathrattle:</b> Summon a 1/1 Ooze with <b>Poisonous</b> and <b>Rush</b>.
	deathrattle = Summon(CONTROLLER, "BOT_565t")


class BOT_576:
	"""Crazed Chemist"""
	# <b>Combo:</b> Give a friendly minion +4 Attack.
	combo = Buff(TARGET, "BOT_576e")


BOT_576e = buff(atk=4)


##
# Spells

class BOT_084:
	"""Violet Haze"""
	# Add 2 random <b>Deathrattle</b> cards to_your hand.
	play = Give(CONTROLLER, RandomMinion(deathrattle=True)) * 2


class BOT_087:
	"""Academic Espionage"""
	# Shuffle 10 cards from your opponent's class into your deck. They_cost (1).
	play = Shuffle(CONTROLLER, Buff(
		RandomCollectible(card_class=ENEMY_CLASS), "BOT_087e")) * 10


class BOT_087e:
	cost = SET(1)
	events = REMOVED_IN_PLAY


class BOT_242:
	"""Myra's Unstable Element"""
	# Draw the rest of your deck.
	play = ForceDraw(FRIENDLY_DECK)


class BOT_508:
	"""Necrium Vial"""
	# Trigger a friendly minion's <b>Deathrattle</b> twice.
	play = Deathrattle(TARGET) * 2


##
# Weapons

class BOT_286:
	"""Necrium Blade"""
	# <b>Deathrattle:</b> Trigger the <b>Deathrattle</b> of a random friendly minion.
	deathrattle = Deathrattle(RANDOM(FRIENDLY_MINIONS + DEATHRATTLE))
