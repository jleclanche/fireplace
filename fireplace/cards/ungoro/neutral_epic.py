from ..utils import *


##
# Minions

class UNG_085:
	"""Emerald Hive Queen"""
	update = Refresh(FRIENDLY_HAND + MINION, {GameTag.COST: +2})


class UNG_087:
	"""Bittertide Hydra"""
	events = SELF_DAMAGE.on(Hit(FRIENDLY_HERO, 3))


class UNG_088:
	"""Tortollan Primalist"""
	play = Discover(CONTROLLER, RandomSpell()).then(CastSpell(Discover.CARD))


class UNG_089:
	"""Gentle Megasaur"""
	play = Adapt(FRIENDLY_MINIONS + MURLOC)


class UNG_099:
	"""Charged Devilsaur"""
	play = Buff(SELF, "UNG_099o")


@custom_card
class UNG_099o:
	tags = {
		GameTag.CARDNAME: "Charged Devilsaur Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
		GameTag.TAG_ONE_TURN_EFFECT: True,
		GameTag.CANNOT_ATTACK_HEROES: True
	}


class UNG_113:
	"""Bright-Eyed Scout"""
	play = Draw(CONTROLLER).then(Buff(Draw.CARD, "UNG_113e"))


class UNG_113e:
	cost = SET(5)


class UNG_847:
	"""Blazecaller"""
	play = PLAYED_ELEMENTAL_LAST_TURN(CONTROLLER) & Hit(TARGET, 5)


class UNG_848:
	"""Primordial Drake"""
	play = Hit(ALL_MINIONS - SELF, 2)


class UNG_946:
	"""Gluttonous Ooze"""
	def play(self):
		amount = 0
		if self.controller.opponent.weapon:
			amount = self.controller.opponent.weapon.atk
		yield Destroy(ENEMY_WEAPON)
		if amount:
			yield GainArmor(FRIENDLY_HERO, amount)
