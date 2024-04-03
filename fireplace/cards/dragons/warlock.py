from ..utils import *


##
# Minions

class DRG_201:
	"""Crazed Netherwing"""
	# <b>Battlecry:</b> If you're holding a Dragon, deal 3 damage to all other characters.
	powered_up = HOLDING_DRAGON
	play = powered_up & Hit(ALL_CHARACTERS - SELF, 3)


class DRG_202:
	"""Dragonblight Cultist"""
	# [x]<b>Battlecry:</b> <b>Invoke</b> Galakrond. Gain +1 Attack for each other friendly
	# minion.
	play = INVOKE, Buff(SELF, "DRG_202e") * Count(FRIENDLY_MINIONS - SELF)


DRG_202e = buff(atk=1)


class DRG_203:
	"""Veiled Worshipper"""
	# [x]<b>Battlecry:</b> If you've <b>Invoked</b> twice, draw 3 cards.
	play = INVOKED_TWICE & Draw(CONTROLLER) * 3


class DRG_207:
	"""Abyssal Summoner"""
	# [x]<b>Battlecry:</b> Summon a Demon with <b>Taunt</b> and stats equal to your hand
	# size.
	def play(self):
		count = len(self.controller.hand)
		if count <= 0:
			return

		demon = self.controller.card("TRL_309t", source=self)
		demon.custom_card = True

		def create_custom_card(demon):
			demon.atk = count
			demon.max_health = count
			demon.cost = min(count, 10)

		demon.create_custom_card = create_custom_card
		demon.create_custom_card(demon)

		yield Summon(self.controller, demon)


class DRG_208:
	"""Valdris Felgorge"""
	# <b>Battlecry:</b> Increase your maximum hand size to 12. Draw 4 cards.
	play = SetTag(CONTROLLER, {GameTag.MAXHANDSIZE: 12}), Draw(CONTROLLER) * 4


class DRG_209:
	"""Zzeraku the Warped"""
	# [x]Whenever your hero takes damage, summon a 6/6 Nether Drake.
	events = Damage(FRIENDLY_HERO).on(Summon(CONTROLLER, "DRG_209t"))


##
# Spells

class DRG_204:
	"""Dark Skies"""
	# [x]Deal $1 damage to a random minion. Repeat for each card in your hand.
	play = Hit(RANDOM_MINION, 1), Hit(RANDOM_MINION, 1) * Count(FRIENDLY_HAND)


class DRG_205:
	"""Nether Breath"""
	# Deal $2 damage. If you're holding a Dragon, deal $4 damage with <b>Lifesteal</b>
	# instead.
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	powered_up = HOLDING_DRAGON
	play = powered_up & (
		GiveLifesteal(SELF),
		Hit(TARGET, 4)
	) | Hit(TARGET, 2)


class DRG_206:
	"""Rain of Fire"""
	# Deal $1 damage to all_characters.
	play = Hit(ALL_CHARACTERS, 1)


class DRG_250:
	"""Fiendish Rites"""
	# <b>Invoke</b> Galakrond. Give your minions +1_Attack.
	play = INVOKE, Buff(FRIENDLY_MINIONS, "DRG_250e")


DRG_250e = buff(atk=1)


##
# Heros

class DRG_600:
	"""Galakrond, the Wretched"""
	# [x]<b>Battlecry:</b> Summon 1 random Demon. <i>(@)</i>
	progress_total = 2
	play = Summon(CONTROLLER, RandomDemon())
	reward = Find(SELF + FRIENDLY_HERO) | (
		Morph(SELF, "DRG_600t2").then(
			SetAttribute(CONTROLLER, "_galakrond", Morph.CARD),
		)
	)


class DRG_600t2:
	"""Galakrond, the Apocalypse"""
	# [x]<b>Battlecry:</b> Summon 2 random Demons. <i>(@)</i>
	progress_total = 2
	play = Summon(CONTROLLER, RandomDemon()) * 2
	reward = Find(SELF + FRIENDLY_HERO) | (
		Morph(SELF, "DRG_600t3").then(
			SetAttribute(CONTROLLER, "_galakrond", Morph.CARD),
		)
	)


class DRG_600t3:
	"""Galakrond, Azeroth's End"""
	# [x]<b>Battlecry:</b> Summon 4 random Demons. Equip a 5/2 Claw.
	play = (
		Summon(CONTROLLER, RandomDemon()) * 4,
		Summon(CONTROLLER, "DRG_238ht")
	)


class DRG_238p3:
	"""Galakrond's Malice"""
	# [x]<b>Hero Power</b> Summon two 1/1 Imps.
	activate = Summon(CONTROLLER, "DRG_238t12t2") * 2
