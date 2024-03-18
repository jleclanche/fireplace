from ..utils import *


##
# Minions

class LOOT_041:
	"""Kobold Barbarian"""
	# At the start of your turn, attack a random enemy.
	events = OWN_TURN_BEGIN.on(Attack(SELF, RANDOM_ENEMY_CHARACTER))


class LOOT_365:
	"""Gemstudded Golem"""
	# <b>Taunt</b> Can only attack if you have 5 or more Armor.
	update = (ARMOR(FRIENDLY_HAND) >= 5) | Refresh(SELF, {GameTag.CANT_ATTACK: True})


class LOOT_367:
	"""Drywhisker Armorer"""
	# <b>Battlecry:</b> For each enemy minion, gain 2 Armor.
	play = GainArmor(FRIENDLY_HERO, Count(ENEMY_MINIONS) * 2)


class LOOT_519:
	"""Geosculptor Yip"""
	# At the end of your turn, summon a random minion with_Cost_equal_to_your Armor <i>(up
	# to 10)</i>.
	events = OWN_TURN_END.on(
		Summon(CONTROLLER, RandomMinion(cost=Min(ARMOR(FRIENDLY_HERO), 10))))


##
# Spells

class LOOT_203:
	"""Lesser Mithril Spellstone"""
	# Summon one 5/5 Mithril Golem. <i>(Equip a weapon to upgrade.)</i>
	play = Summon(CONTROLLER, "LOOT_203t4")

	class Hand:
		events = Summon(CONTROLLER, WEAPON).after(Morph(SELF, "LOOT_203t2"))


class LOOT_203t2:
	"""Mithril Spellstone"""
	# Summon two 5/5 Mithril Golems. <i>(Equip a weapon to upgrade.)</i>
	play = Summon(CONTROLLER, "LOOT_203t4") * 2

	class Hand:
		events = Summon(CONTROLLER, WEAPON).after(Morph(SELF, "LOOT_203t3"))


class LOOT_203t3:
	"""Greater Mithril Spellstone"""
	# Summon three 5/5 Mithril Golems.
	play = Summon(CONTROLLER, "LOOT_203t4") * 3


class LOOT_285:
	"""Unidentified Shield"""
	# Gain 5 Armor. Gains a bonus effect in_your hand.
	entourage = ["LOOT_285t", "LOOT_285t2", "LOOT_285t3", "LOOT_285t4"]
	play = GainArmor(FRIENDLY_HERO, 5)
	draw = Morph(SELF, RandomEntourage())


class LOOT_285t:
	"""Tower Shield +10"""
	# Gain 5 Armor. Gain 10 more Armor.
	play = GainArmor(FRIENDLY_HERO, 5), GainArmor(FRIENDLY_HERO, 10)


class LOOT_285t2:
	"""Serrated Shield"""
	# Gain 5 Armor. Deal 5 damage.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = GainArmor(FRIENDLY_HERO, 5), Hit(TARGET, 5)


class LOOT_285t3:
	"""Runed Shield"""
	# Gain 5 Armor. Summon a 5/5 Golem.
	play = GainArmor(FRIENDLY_HERO, 5), Summon(CONTROLLER, "LOOT_285t3t")


class LOOT_285t4:
	"""Spiked Shield"""
	# Gain 5 Armor. Equip a 5/2 weapon.
	play = GainArmor(FRIENDLY_HERO, 5), Summon(CONTROLLER, "LOOT_285t4t")


class LOOT_364:
	"""Reckless Flurry"""
	# Spend all your Armor. Deal that much damage to all minions.
	play = GainArmor(FRIENDLY_HERO, -ARMOR(FRIENDLY_HERO)).then(
		Hit(ALL_MINIONS, -GainArmor.AMOUNT)
	)


class LOOT_370:
	"""Gather Your Party"""
	# <b>Recruit</b> a minion.
	requirements = {
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
	}
	play = RECRUIT


##
# Weapons

class LOOT_044:
	"""Bladed Gauntlet"""
	# Has Attack equal to your Armor. Can't attack heroes.
	update = (
		Refresh(FRIENDLY_HERO, {GameTag.CANNOT_ATTACK_HEROES: True}),
		Refresh(SELF, {GameTag.ATK: lambda self, i: self.controller.hero.armor}, priority=100)
	)


class LOOT_380:
	"""Woecleaver"""
	# After your hero attacks, <b>Recruit</b> a minion.
	events = Attack(FRIENDLY_HERO).after(RECRUIT)
