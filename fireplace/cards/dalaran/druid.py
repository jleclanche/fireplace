from ..utils import *


##
# Minions

class DAL_354:
	"""Acornbearer"""
	# <b>Deathrattle:</b> Add two 1/1 Squirrels to your hand.
	deathrattle = Give(CONTROLLER, "DAL_354t") * 2


class DAL_355:
	"""Lifeweaver"""
	# Whenever you restore Health, add a random Druid spell to your hand.
	events = Heal(source=FRIENDLY).on(
		Give(CONTROLLER, RandomSpell(card_class=CardClass.DRUID)))


class DAL_357:
	"""Lucentbark"""
	# <b>Taunt</b> <b>Deathrattle:</b> Go dormant. Restore 5 Health to awaken this minion.
	deathrattle = Find(FRIENDLY_MINIONS + SELF) & (
		Morph(SELF, "DAL_357t")
	) | (
		Summon(CONTROLLER, "DAL_357t")
	)


class DAL_357t:
	progress_total = 5
	events = Heal().on(AddProgress(SELF, Heal.TARGET, Heal.AMOUNT))
	reward = Morph(SELF, "DAL_357")


class DAL_732:
	"""Keeper Stalladris"""
	# After you cast a <b>Choose One</b> spell, add copies of both choices_to_your_hand.
	events = Play(CONTROLLER, CHOOSE_ONE + SPELL).after(
		Give(CONTROLLER, Copy(GetAttribute(Play.CARD, "choose_cards")))
	)


class DAL_799:
	"""Crystal Stag"""
	# <b>Rush</b>. <b>Battlecry:</b> If you've restored 5 Health this game, summon a copy
	# of this.@ <i>({0} left!)</i>@ <i>(Ready!)</i>
	powered_up = AttrValue(GameTag.AMOUNT_HEALED_THIS_GAME)(CONTROLLER) >= 5
	play = powered_up & Summon(CONTROLLER, ExactCopy(SELF))


##
# Spells

class DAL_256:
	"""The Forest's Aid"""
	# <b>Twinspell</b> Summon five 2/2 Treants.
	play = Give(CONTROLLER, "DAL_256ts"), Summon(CONTROLLER, "DAL_256t2") * 5


class DAL_256ts:
	play = Summon(CONTROLLER, "DAL_256t2") * 5


class DAL_350:
	"""Crystal Power"""
	# <b>Choose One -</b> Deal $2 damage to a minion; or_Restore #5 Health.
	choose = ("DAL_350a", "DAL_350b")
	play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 2), Heal(TARGET, 5))


class DAL_350a:
	play = Hit(TARGET, 2)


class DAL_350b:
	play = Heal(TARGET, 5)


class DAL_351:
	"""Blessing of the Ancients"""
	# <b>Twinspell</b> Give your minions +1/+1.
	play = Give(CONTROLLER, "DAL_351ts"), Buff(FRIENDLY_MINIONS, "DAL_351e")


class DAL_351ts:
	play = Buff(FRIENDLY_MINIONS, "DAL_351e")


DAL_351e = buff(+1, +1)


class DAL_352:
	"""Crystalsong Portal"""
	# <b>Discover</b> a Druid minion. If your hand has no minions, keep all 3.
	powered_up = -Find(FRIENDLY_HAND + MINION)
	play = powered_up & (
		Give(CONTROLLER, RandomCollectible(card_class=CardClass.DRUID)) * 3
	) | (
		DISCOVER(RandomCollectible(card_class=CardClass.DRUID))
	)


class DAL_733:
	"""Dreamway Guardians"""
	# Summon two 1/2 Dryads with <b>Lifesteal</b>.
	play = Summon(CONTROLLER, "DAL_733t") * 2
