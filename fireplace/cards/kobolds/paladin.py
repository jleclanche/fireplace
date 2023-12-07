from ..utils import *


##
# Minions

class LOOT_216:
	"""Lynessa Sunsorrow"""
	# [x]<b>Battlecry:</b> Cast each spell you cast on your minions this game on this one.
	play = CastSpell(FRIENDLY + CAST_ON_FRIENDLY_MINIONS, SELF)


class LOOT_313:
	"""Crystal Lion"""
	# [x]<b>Divine Shield</b> Costs (1) less for each Silver Hand Recruit you control.
	cost_mod = -Count(FRIENDLY_MINIONS + ID("CS2_101t"))


class LOOT_363:
	"""Drygulch Jailor"""
	# <b>Deathrattle:</b> Add 3 Silver_Hand Recruits to_your_hand.
	deathrattle = Give(CONTROLLER, "CS2_101t") * 3


class LOOT_398:
	"""Benevolent Djinn"""
	# At the end of your turn, restore 3 Health to your_hero.
	events = OWN_TURN_END.on(Heal(FRIENDLY_HERO, 3))


##
# Spells

class LOOT_088:
	"""Potion of Heroism"""
	# Give a minion <b>Divine_Shield</b>. Draw a card.
	play = GiveDivineShield(TARGET), Draw(CONTROLLER)


class LOOT_091:
	"""Lesser Pearl Spellstone"""
	# Summon a 2/2 Spirit with <b>Taunt</b>. @<i>(Restore 3 Health to upgrade.)</i>
	progress_total = 3
	play = Summon(CONTROLLER, "LOOT_091t")
	reward = Morph(SELF, "LOOT_091t1")

	class Hand:
		events = Heal().on(AddProgress(SELF, Heal.TARGET, Heal.AMOUNT))


class LOOT_091t1:
	"""Pearl Spellstone"""
	# Summon a 4/4 Spirit with <b>Taunt</b>. @
	progress_total = 3
	play = Summon(CONTROLLER, "LOOT_091t1t")
	reward = Morph(SELF, "LOOT_091t2")

	class Hand:
		events = Heal().on(AddProgress(SELF, Heal.TARGET, Heal.AMOUNT))


class LOOT_091t2:
	"""Greater Pearl Spellstone"""
	# Summon a 6/6 Spirit with <b>Taunt</b>.
	play = Summon(CONTROLLER, "LOOT_091t2t")


class LOOT_093:
	"""Call to Arms"""
	# [x]<b>Recruit</b> 3 minions that cost (2) or less.
	play = Recruit(COST <= 2) * 3


class LOOT_333:
	"""Level Up!"""
	# Give your Silver Hand Recruits +2/+2 and_<b>Taunt</b>.
	play = Buff(FRIENDLY_MINIONS + ID("CS2_101t"), "LOOT_333e")


LOOT_333e = buff(+2, +2, taunt=True)


##
# Weapons

class LOOT_286:
	"""Unidentified Maul"""
	# Gains a bonus effect in_your hand.
	entourage = ["LOOT_286t1", "LOOT_286t2", "LOOT_286t3", "LOOT_286t4"]
	draw = Morph(SELF, RandomEntourage())


class LOOT_286t1:
	"""Champion's Maul"""
	# <b>Battlecry:</b> Summon two 1/1 Silver Hand Recruits.
	play = Summon(CONTROLLER, "CS2_101t") * 2


class LOOT_286t2:
	"""Sacred Maul"""
	# <b>Battlecry:</b> Give your minions <b>Taunt</b>.
	play = Taunt(FRIENDLY_MINIONS)


class LOOT_286t3:
	"""Blessed Maul"""
	# <b>Battlecry:</b> Give your minions +1 Attack.
	play = Buff(FRIENDLY_MINIONS, "LOOT_286t3e")


LOOT_286t3e = buff(atk=1)


class LOOT_286t4:
	"""Purifier's Maul"""
	# <b>Battlecry:</b> Give your minions <b>Divine Shield</b>.
	play = GiveDivineShield(FRIENDLY_MINIONS)


class LOOT_500:
	"""Val'anyr"""
	# <b>Deathrattle:</b> Give a minion in your hand +4/+2. When it dies, reequip this.
	deathrattle = Buff(RANDOM(FRIENDLY_MINIONS), "LOOT_500e")


class LOOT_500e:
	tags = {
		GameTag.DEATHRATTLE: True,
		GameTag.ATK: 4,
		GameTag.HEALTH: 2,
	}
	deathrattle = Summon(CONTROLLER, "LOOT_500")
