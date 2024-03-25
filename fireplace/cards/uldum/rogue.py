from ..utils import *


##
# Minions

class ULD_186:
	"""Pharaoh Cat"""
	# <b>Battlecry:</b> Add a random <b>Reborn</b> minion to your_hand.
	play = Give(CONTROLLER, RandomMinion(reborn=True))


class ULD_231:
	"""Whirlkick Master"""
	# Whenever you play a <b>Combo</b> card, add a random <b>Combo</b> card to your hand.
	events = Play(CONTROLLER, COMBO).on(
		Give(CONTROLLER, RandomCollectible(combo=True))
	)


class ULD_280:
	"""Sahket Sapper"""
	# <b>Deathrattle:</b> Return a _random enemy minion to_ your_opponent's_hand.
	deathrattle = Bounce(RANDOM_ENEMY_MINION)


class ULD_288:
	"""Anka, the Buried"""
	# <b>Battlecry:</b> Change each <b>Deathrattle</b> minion in your hand into a 1/1 that
	# costs (1).
	play = MultiBuff(FRIENDLY_HAND + MINION + DEATHRATTLE, ["ULD_288e", "GBL_001e"])


class ULD_288e:
	atk = SET(1)
	max_health = SET(1)


class ULD_327:
	"""Bazaar Mugger"""
	# <b>Rush</b> <b>Battlecry:</b> Add a random minion from another class to your hand.
	play = Give(CONTROLLER, RandomMinion(card_class=ANOTHER_CLASS))


##
# Spells

class ULD_286:
	"""Shadow of Death"""
	# Choose a minion. Shuffle 3 'Shadows' into your deck that summon a copy when drawn.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Shuffle(CONTROLLER, "ULD_286t")


class ULD_286t:
	play = Summon(CONTROLLER, Copy(CREATOR_TARGET))
	draw = CAST_WHEN_DRAWN


class ULD_326:
	"""Bazaar Burglary"""
	# [x]<b>Quest:</b> Add 4 cards from other classes to your hand. <b>Reward: </b>Ancient
	# Blades.
	progress_total = 4
	quest = Give(CONTROLLER, ANOTHER_CLASS).after(AddProgress(SELF, Give.CARD))
	reward = Summon(CONTROLLER, "ULD_326p")


class ULD_326p:
	"""Ancient Blades"""
	# [x]<b>Hero Power</b> Equip a 3/2 Blade with <b>Immune</b> while attacking.
	activate = Summon(CONTROLLER, "ULD_326t")


class ULD_326t:
	update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})


class ULD_328:
	"""Clever Disguise"""
	# Add 2 random spells from another class to_your hand.
	play = Give(CONTROLLER, RandomSpell(card_class=ANOTHER_CLASS))


class ULD_715:
	"""Plague of Madness"""
	# Each player equips a 2/2 Knife with <b>Poisonous</b>.
	play = Summon(ALL_PLAYERS, "ULD_715t")


##
# Weapons

class ULD_285:
	"""Hooked Scimitar"""
	# [x]<b>Combo:</b> Gain +2 Attack.
	combo = Buff(SELF, "ULD_285e")


ULD_285e = buff(atk=2)
