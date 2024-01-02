from ..utils import *


##
# Minions

class BOT_216:
	"""Omega Medic"""
	# <b>Battlecry:</b> If you have 10 Mana Crystals, restore #10 Health to your hero.
	powered_up = AT_MAX_MANA(CONTROLLER)
	play = powered_up & Heal(FRIENDLY_HERO, 10)


class BOT_258:
	"""Zerek, Master Cloner"""
	# <b>Deathrattle:</b> If you've cast any spells on this minion, resummon it.
	events = Play(CONTROLLER, SPELL, SELF).on(Buff(SELF, "BOT_258e"))
	deathrattle = Actived(SELF) & Summon(CONTROLLER, "BOT_258")


class BOT_258e:
	def apply(self, target):
		target.actived = True


class BOT_509:
	"""Dead Ringer"""
	# <b>Deathrattle:</b> Draw a <b>Deathrattle</b> minion from your deck.
	deathrattle = ForceDraw(RANDOM(FRIENDLY_DECK + DEATHRATTLE))


class BOT_558:
	"""Test Subject"""
	# [x]<b>Deathrattle:</b> Return any spells you cast on this minion to your hand.
	events = Play(CONTROLLER, SPELL, SELF).on(
		StoringBuff(SELF, "BOT_558e", Play.CARD)
	)


class BOT_558e:
	tags = {GameTag.DEATHRATTLE: True}

	def deathrattle(self):
		yield Give(CONTROLLER, self.store_card.id)


class BOT_566:
	"""Reckless Experimenter"""
	# [x]<b>Deathrattle</b> minions you play cost (3) less, but die at the end of the turn.
	update = Refresh(FRIENDLY_HAND + DEATHRATTLE + MINION, "BOT_556e2")
	events = Play(CONTROLLER, DEATHRATTLE + MINION).after(
		Buff(Play.CARD, "BOT_566e")
	)


BOT_556e2 = buff(cost=-3)


class BOT_566e:
	events = OWN_TURN_END.on(Destroy(OWNER))


##
# Spells

class BOT_219:
	"""Extra Arms"""
	# [x]Give a minion +2/+2. Add 'More Arms!' to your hand that gives +2/+2.
	play = Buff(TARGET, "BOT_219e"), Give(CONTROLLER, "BOT_219t")


class BOT_219t:
	play = Buff(TARGET, "BOT_219te")


BOT_219e = buff(+2, +2)


BOT_219te = buff(+2, +2)


class BOT_435:
	"""Cloning Device"""
	# <b>Discover</b> a copy of a minion in your opponent's deck.
	play = GenericChoice(CONTROLLER, Copy(RANDOM(DeDuplicate(ENEMY_DECK + MINION)) * 3))


class BOT_517:
	"""Topsy Turvy"""
	# Swap a minion's Attack and Health.
	play = Buff(TARGET, "BOT_517e")


BOT_517e = AttackHealthSwapBuff()


class BOT_529:
	"""Power Word: Replicate"""
	# Choose a friendly minion. Summon a 5/5 copy of it.
	play = Summon(CONTROLLER, Buff(ExactCopy(TARGET), "BOT_529e"))


class BOT_529e:
	atk = SET(5)
	max_health = SET(5)


class BOT_567:
	"""Zerek's Cloning Gallery"""
	# Summon a 1/1 copy of_each minion in your_deck.
	play = Summon(CONTROLLER, Buff(Copy(FRIENDLY_DECK + MINION), "BOT_567e"))


class BOT_567e:
	atk = SET(1)
	max_health = SET(1)
