from ..utils import *


##
# Minions

class TRL_300:
	"""Shirvallah, the Tiger"""
	# [x]<b>Divine Shield</b>, <b>Rush</b>, <b>Lifesteal</b> Costs (1) less for each Mana
	# you've spent on spells.
	cost_mod = -AttrValue("spent_mana_on_spells_this_game")(CONTROLLER)


class TRL_306:
	"""Immortal Prelate"""
	# <b>Deathrattle:</b> Shuffle this into your deck. It keeps any enchantments.
	tags = {enums.KEEP_BUFF: True}
	deathrattle = Shuffle(CONTROLLER, SELF)


class TRL_308:
	"""High Priest Thekal"""
	# <b>Battlecry:</b> Convert all but 1_of your Hero's Health into Armor.
	# TODO need test
	play = (
		GainArmor(FRIENDLY_HERO, CURRENT_HEALTH(FRIENDLY_HERO) - 1),
		SetCurrentHealth(FRIENDLY_HERO, 1)
	)

class TRL_309:
	"""Spirit of the Tiger"""
	# [x]<b>Stealth</b> for 1 turn. After you cast a spell, summon a Tiger with stats equal
	# to its Cost.
	events = (
		OWN_TURN_BEGIN.on(Unstealth(SELF)),
		Play(CONTROLLER, SPELL).after(
			SummonTiger(CONTROLLER, COST(Play.CARD))
		)
	)


class TRL_545:
	"""Zandalari Templar"""
	# [x]<b>Battlecry:</b> If you've restored 10 Health this game, gain +4/+4 and
	# <b>Taunt</b>.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
	powered_up = AttrValue(GameTag.AMOUNT_HEALED_THIS_GAME)(CONTROLLER) >= 10
	play = powered_up & Buff(SELF, "TRL_545e")


TRL_545e = buff(+4, +4)


##
# Spells

class TRL_302:
	"""Time Out!"""
	# Your hero is <b>Immune</b> until your next turn.
	play = Buff(SELF, "TRL_302e")


class TRL_302e:
	tags = {
		GameTag.CANT_BE_DAMAGED: True,
		GameTag.CANT_BE_TARGETED_BY_OPPONENTS: True,
	}
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


class TRL_305:
	"""A New Challenger..."""
	# <b>Discover</b> a 6-Cost minion. Summon it with <b>Taunt</b> and <b>Divine
	# Shield</b>.
	play = Discover(CONTROLLER, RandomMinion(cost=6)).then(
		Summon(CONTROLLER, Buff(Discover.CARD, "TRL_305e"))
	)


class TRL_305e:
	tags = {GameTag.TAUNT: True}

	def apply(self, target):
		self.game.trigger(self, (GiveDivineShield(target), ), None)


class TRL_307:
	"""Flash of Light"""
	# Restore #4 Health. Draw a card.
	play = Heal(TARGET, 4), Draw(CONTROLLER)


##
# Weapons

class TRL_304:
	"""Farraki Battleaxe"""
	# <b>Overkill:</b> Give a minion in your hand +2/+2.
	overkill = Buff(FRIENDLY_HAND + MINION, "TRL_304e")


TRL_304e = buff(+2, +2)


class TRL_543:
	"""Bloodclaw"""
	# <b>Battlecry:</b> Deal 5 damage to your hero.
	play = Hit(FRIENDLY_HERO, 5)
