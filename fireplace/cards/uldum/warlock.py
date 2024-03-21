from ..utils import *


##
# Minions

class ULD_161:
	"""Neferset Thrasher"""
	# Whenever this attacks, deal 3 damage to your_hero.
	events = Attack(SELF).on(Hit(FRIENDLY_HERO, 3))


class ULD_162:
	"""EVIL Recruiter"""
	# <b>Battlecry:</b> Destroy a friendly <b>Lackey</b> to summon a 5/5 Demon.
	requirements = {
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_FRIENDLY_LACKEY: 0,
	}
	play = Destroy(TARGET), Summon(CONTROLLER, "ULD_162t")


class ULD_163:
	"""Expired Merchant"""
	# [x]<b>Battlecry:</b> Discard your highest Cost card. <b>Deathrattle:</b> Add 2 copies
	# of it to your hand.
	play = Discard(RANDOM(HIGHEST_COST(FRIENDLY_HAND))).then(
		StoringBuff(SELF, "ULD_163e", Discard.CARD)
	)


class ULD_163e:
	tags = {GameTag.DEATHRATTLE: True}

	def deathrattle(self):
		yield Give(CONTROLLER, self.store_card.id) * 2


class ULD_165:
	"""Riftcleaver"""
	# <b>Battlecry:</b> Destroy a minion. Your hero takes damage equal to its Health.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Hit(FRIENDLY_HERO, CURRENT_HEALTH(TARGET)), Destroy(TARGET)


class ULD_167:
	"""Diseased Vulture"""
	# After your hero takes damage on your turn, summon a random 3-Cost minion.
	events = Hit(FRIENDLY_HERO).on(
		CURRENT_PLAYER(CONTROLLER) & Summon(CONTROLLER, RandomMinion(cost=3))
	)


class ULD_168:
	"""Dark Pharaoh Tekahn"""
	# <b>Battlecry:</b> For the rest of the game, your <b>Lackeys</b> are 4/4.
	play = Buff(CONTROLLER, "ULD_168e")


class ULD_168e:
	update = Refresh(
		(IN_DECK | IN_HAND | IN_PLAY) + FRIENDLY + LACKEY,
		buff="ULD_168e3"
	)


class ULD_168e3:
	atk = SET(4)
	max_health = SET(4)


##
# Spells

class ULD_140:
	"""Supreme Archaeology"""
	# <b>Quest:</b> Draw 20 cards. <b>Reward:</b> Tome of Origination.
	progress_total = 20
	quest = Draw(CONTROLLER).after(AddProgress(SELF, Draw.CARD))
	reward = Summon(CONTROLLER, "ULD_140p")


class ULD_140p:
	"""Tome of Origination"""
	# <b>Hero Power</b> Draw a card. It costs (0).
	activate = Draw(CONTROLLER).then(Buff(Draw.CARD, "ULD_140e"))


class ULD_140e:
	cost = SET(0)
	events = REMOVED_IN_PLAY


class ULD_160:
	"""Sinister Deal"""
	# <b>Discover</b> a <b>Lackey</b>.
	play = DISCOVER(RandomLackey())


class ULD_324:
	"""Impbalming"""
	# Destroy a minion. Shuffle 3 Worthless Imps into your deck.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_MINION_TARGET: 0,
	}
	play = Destroy(TARGET), Shuffle(CONTROLLER, "ULD_324t") * 3


class ULD_717:
	"""Plague of Flames"""
	# [x]Destroy all your minions. For each one, destroy a random enemy minion.
	def play(self):
		count = Count(FRIENDLY_MINIONS).evaluate(self)
		yield Destroy(FRIENDLY_MINIONS)
		yield Destroy(RANDOM_ENEMY_MINION * count)
