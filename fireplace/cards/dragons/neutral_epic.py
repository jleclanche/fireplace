from ..utils import *


##
# Minions

class DRG_062:
	"""Wyrmrest Purifier"""
	# [x]<b>Battlecry:</b> Transform all Neutral cards in your deck into random cards from
	# your class.
	play = Morph(FRIENDLY_DECK + NEUTRAL, RandomCollectible(card_class=FRIENDLY_CLASS))


class DRG_072:
	"""Skyfin"""
	# <b>Battlecry:</b> If you're holding a Dragon, summon 2 random Murlocs.
	powered_up = HOLDING_DRAGON
	play = powered_up & Summon(CONTROLLER, RandomMurloc()) * 2


class DRG_082:
	"""Kobold Stickyfinger"""
	# <b>Battlecry:</b> Steal your opponent's weapon.
	play = Steal(ENEMY_WEAPON)


class DRG_084:
	"""Tentacled Menace"""
	# <b>Battlecry:</b> Each player draws a card. Swap their_Costs.
	play = SwapStateBuff(Draw(CONTROLLER), Draw(OPPONENT), "DRG_084e")


class DRG_084e:
	cost = lambda self, i: self._xcost
	events = REMOVED_IN_PLAY


class DRG_086:
	"""Chromatic Egg"""
	# [x]<b>Battlecry:</b> Secretly <b>Discover</b> a Dragon to hatch into.
	# <b>Deathrattle:</b> Hatch!
	play = Discover(CONTROLLER, RandomDragon()).then(
		StoringBuff(SELF, "DRG_086e", Discover.CARD))


class DRG_086e:
	tags = {GameTag.DEATHRATTLE: True}

	def deathrattle(self):
		yield Summon(CONTROLLER, self.store_card.id)


class DRG_088:
	"""Dread Raven"""
	# Has +3 Attack for each other Dread Raven you_control.
	update = Find(FRIENDLY_MINIONS + ID("DRG_088")) & Refresh(SELF, {GameTag.ATK: 3})


class DRG_092:
	"""Transmogrifier"""
	# Whenever you draw a card, transform it into a random <b>Legendary</b> minion.
	events = Draw(CONTROLLER).on(Morph(Draw.CARD, RandomLegendaryMinion()))


class DRG_401:
	"""Grizzled Wizard"""
	# <b>Battlecry:</b> Swap Hero Powers with your opponent until your next turn.
	play = (
		SwapController(FRIENDLY_HERO_POWER, ENEMY_HERO_POWER),
		Buff(CONTROLLER, "DRG_401e")
	)


class DRG_401e:
	events = OWN_TURN_BEGIN.on(
		SwapController(FRIENDLY_HERO_POWER, ENEMY_HERO_POWER),
		Destroy(SELF)
	)


class DRG_403:
	"""Blowtorch Saboteur"""
	# <b>Battlecry:</b> Your opponent's next Hero Power costs (3).
	play = Buff(ENEMY_HERO_POWER, "DRG_403e")


class DRG_403e:
	update = Refresh(ENEMY_HERO_POWER, {GameTag.COST: SET(3)})
	events = Activate(None, OWNER).on(Destroy(SELF))
