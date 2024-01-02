from ..utils import *


##
# Minions

class BOT_059:
	"""Eternium Rover"""
	# Whenever this minion takes damage, gain 2_Armor.
	events = Damage(SELF).on(GainArmor(SELF, 2))


class BOT_104:
	"""Dyn-o-matic"""
	# <b>Battlecry:</b> Deal 5 damage randomly split among all minions_except_Mechs.
	play = Hit(RANDOM(ALL_MINIONS - MECH), 1) * 5


class BOT_218:
	"""Security Rover"""
	# [x]Whenever this minion takes damage, summon a 2/3 Mech with <b>Taunt</b>.
	events = Damage(SELF).on(Summon(CONTROLLER, "BOT_218t"))


class BOT_237:
	"""Beryllium Nullifier"""
	# <b>Magnetic</b> Can't be targeted by spells or Hero Powers.
	magnetic = MAGNETIC("BOT_237e")


BOT_237e = buff(
	cant_be_targeted_by_spells=True,
	cant_be_targeted_by_hero_powers=True
)


##
# Spells

class BOT_042:
	"""Weapons Project"""
	# Each player equips a 2/3 Weapon and gains 6 Armor.
	play = Summon(PLAYER, "BOT_042t"), GainArmor(PLAYER, 6)


class BOT_067:
	"""Rocket Boots"""
	# Give a minion <b>Rush</b>. Draw a card.
	play = Buff(TARGET, "BOT_067e"), Draw(CONTROLLER)


BOT_067e = buff(rush=True)


class BOT_069:
	"""The Boomship"""
	# Summon 3 random minions from your hand. Give them <b>Rush</b>.
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION) * 3).then(
		Buff(Summon.CARD, "BOT_069e")
	)


BOT_069e = buff(rush=True)


class BOT_299:
	"""Omega Assembly"""
	# [x]<b>Discover</b> a Mech. If you have 10 Mana Crystals, keep all 3 cards.
	powered_up = AT_MAX_MANA(CONTROLLER)
	play = powered_up & Give(CONTROLLER, RandomMech()) * 3 | DISCOVER(RandomMech())


##
# Weapons

class BOT_406:
	"""Supercollider"""
	# [x]After you attack a minion, force it to attack one of its neighbors.
	events = Attack(FRIENDLY_HERO, MINION).after(
		Attack(Attack.DEFENDER, RANDOM(ADJACENT(Attack.DEFENDER)))
	)


##
# Heros

class BOT_238:
	"""Dr. Boom, Mad Genius"""
	# <b>Battlecry:</b> For the rest of the game, your Mechs have <b>Rush</b>.
	entourage = [
		"BOT_238p1",
		"BOT_238p2",
		"BOT_238p3",
		"BOT_238p4",
		"BOT_238p6",
	]
	play = (
		Buff(CONTROLLER, "BOT_238e"),
		Summon(CONTROLLER, RandomEntourage())
	)


class BOT_238e:
	update = Refresh(FRIENDLY + MECH, {GameTag.RUSH: True})


class BOT_238p:
	entourage = BOT_238.entourage
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage()))


class BOT_238p1:
	entourage = BOT_238.entourage
	activate = Hit(TARGET, 3)
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage(exclude=SELF)))


class BOT_238p2:
	entourage = BOT_238.entourage
	activate = GainArmor(FRIENDLY_HERO, 7)
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage(exclude=SELF)))


class BOT_238p3:
	entourage = BOT_238.entourage
	activate = Hit(ENEMY_CHARACTERS, 1)
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage(exclude=SELF)))


class BOT_238p4:
	entourage = BOT_238.entourage
	activate = DISCOVER(RandomMech())
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage(exclude=SELF)))


class BOT_238p6:
	entourage = BOT_238.entourage
	activate = Summon(CONTROLLER, "BOT_312t") * 3
	events = OWN_TURN_END.on(Summon(CONTROLLER, RandomEntourage(exclude=SELF)))
