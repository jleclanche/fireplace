from ..utils import *


##
# Minions

class ULD_209:
	"""Vulpera Scoundrel"""
	# <b>Battlecry</b>: <b>Discover</b> a spell or pick a mystery choice.
	class VulperaScoundrelAction(Discover):
		TARGET = ActionArg()
		CARDS = CardArg()
		CARD = CardArg()

		def get_target_args(self, source, target):
			cards = super().get_target_args(source, target)
			cards[0].append(source.controller.card("ULD_209t"))
			return cards

	play = VulperaScoundrelAction(CONTROLLER, RandomSpell()).then(
		Find(VulperaScoundrelAction.CARD + ID("ULD_209t")) & (
			Give(CONTROLLER, RandomSpell())
		) | (
			Give(CONTROLLER, VulperaScoundrelAction.CARD)
		)
	)


class ULD_229:
	"""Mischief Maker"""
	# <b>Battlecry:</b> Swap the top card of your deck with your_opponent's.
	play = SwapController(FRIENDLY_DECK[:1], ENEMY_DECK[:1])


class ULD_290:
	"""History Buff"""
	# Whenever you play a minion, give a random minion in your hand +1/+1.
	events = Play(CONTROLLER, MINION).on(
		Buff(RANDOM(FRIENDLY_HAND + MINION), "ULD_290e")
	)


ULD_290e = buff(+1, +1)


class ULD_309:
	"""Dwarven Archaeologist"""
	# After you <b>Discover</b> a card, reduce its cost by (1).
	events = Give(CONTROLLER, source=FRIENDLY + HAS_DISCOVER).after(
		Buff(Give.CARD, "ULD_309e")
	)


class ULD_309e:
	tags = {GameTag.COST: -1}
	events = REMOVED_IN_PLAY


class ULD_702:
	"""Mortuary Machine"""
	# After your opponent plays a minion, give it <b>Reborn</b>.
	events = Play(OPPONENT, MINION).after(GiveReborn(Play.CARD))


class ULD_703:
	"""Desert Obelisk"""
	# [x]If you control 3 of these at the end of your turn, deal 5 damage to a random
	# enemy.
	events = OWN_TURN_END.on(
		(Count(FRIENDLY_MINIONS + ID("ULD_703")) >= 3) & Hit(RANDOM_ENEMY_CHARACTER, 5)
	)


class ULD_705:
	"""Mogu Cultist"""
	# <b>Battlecry:</b> If your board is full of Mogu Cultists, sacrifice them all and
	# summon Highkeeper Ra.
	play = (Count(FRIENDLY_MINIONS + ID("ULD_705")) == 7) & (
		Destroy(FRIENDLY_MINIONS), Summon(CONTROLLER, "ULD_705t")
	)


class ULD_705t:
	events = OWN_TURN_END.on(Hit(ENEMY_CHARACTERS, 20))


class ULD_706:
	"""Blatant Decoy"""
	# [x]<b>Deathrattle:</b> Each player summons the lowest Cost minion from their hand.
	deathrattle = (
		Summon(CONTROLLER, LOWEST_ATK(FRIENDLY_HAND + MINION)),
		Summon(OPPONENT, LOWEST_ATK(ENEMY_HAND + MINION)),
	)


class ULD_727:
	"""Body Wrapper"""
	# <b>Battlecry:</b> <b>Discover</b> a friendly minion that died this game. Shuffle it
	# into your deck.
	play = Choice(CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY + KILLED + MINION)) * 3)).then(
		Shuffle(CONTROLLER, Choice.CARD)
	)
