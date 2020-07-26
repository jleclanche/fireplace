from ..utils import *


##
# Hero Powers

class BT_429p:
	"""Demonic Blast (Two uses left!)"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

	def activate(self):
		yield Hit(TARGET, 4)
		old_power = self.old_power
		activations_this_turn = self.activations_this_turn
		yield Summon(CONTROLLER, "BT_429p2")
		self.controller.hero.power.old_power = old_power
		self.controller.hero.power.activations_this_turn = activations_this_turn


class BT_429p2:
	"""Demonic Blast (Last use!)"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}

	def activate(self):
		yield Hit(TARGET, 4)
		yield Summon(CONTROLLER, self.old_power)
		self.controller.hero.power.old_power = None


##
# Minions

class BT_480:
	"""Crimson Sigil Runner"""
	outcast = Draw(CONTROLLER)


class BT_496:
	"""Furious Felfin"""
	play = (NUM_ATTACKS(FRIENDLY_HERO) > 0) & Buff(SELF, "BT_496e")


BT_496e = buff(atk=1, rush=True)


class BT_321:
	"""Netherwalker"""
	play = DISCOVER(RandomCollectible(race=Race.DEMON))


class BT_187:
	"""Kayn Sunfury"""
	update = Refresh(ALL_CHARACTERS, {GameTag.IGNORE_TAUNT: True})


class BT_934:
	"""Imprisoned Antaen"""
	dormant = 2
	awaken = Hit(RANDOM_ENEMY_CHARACTER, 1) * 10


class BT_509:
	"""Fel Summoner"""
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + DEMON))


class BT_493:
	"""Priestess of Fury"""
	events = OWN_TURN_END.on(Hit(RANDOM_ENEMY_CHARACTER), 6)


class BT_761:
	"""Coilfang Warlord"""
	deathrattle = Summon(CONTROLLER, "BT_761t")


class BT_486:
	"""Pit Commander"""
	events = OWN_TURN_END.on(Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + DEMON)))


##
# Spells

class BT_491:
	"""Spectral Sight"""
	play = Draw(CONTROLLER)
	outcast = Draw(CONTROLLER) * 2


class BT_514:
	"""Immolation Aura"""
	play = Hit(ALL_MINIONS, 1) * 2


class BT_429:
	"""Metamorphosis"""
	def play(self):
		if self.controller.hero.power.old_power:
			old_power = self.controller.hero.power.old_power
		else:
			old_power = self.controller.hero.power
		yield Summon(CONTROLLER, "BT_429p")
		self.controller.hero.power.old_power = old_power


class BT_601:
	"""Skull of Gul'dan"""
	play = Draw(CONTROLLER) * 3
	outcast = Draw(CONTROLLER).then(Buff(Draw.CARD, "BT_601e")) * 3


BT_601e = buff(cost=-3)


##
# Weapons

class BT_430:
	"""Warglaives of Azzinoth"""
	events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
		ExtraAttack(FRIENDLY_HERO))
