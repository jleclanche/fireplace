from ..utils import *


##
# Minions

class UNG_022:
	"""Mirage Caller"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Summon(CONTROLLER, ExactCopy(TARGET)).then(
		Buff(Summon.CARD, "UNG_022e")
	)


class UNG_022e:
	atk = SET(1)
	max_health = SET(1)


class UNG_032:
	"""Crystalline Oracle"""
	deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


class UNG_034:
	"""Radiant Elemental"""
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: -1})


class UNG_035:
	"""Curious Glimmerroot"""
	class GlimmerrootAction(TargetedAction):
		def do(self, source, player):
			self.player = player
			self.source = source
			self.min_count = 1
			self.max_count = 1
			self.player.choice = self
			# all class cards involved in this effect belong to the opponent's class
			#
			# If the opponent's deck started with no class cards in the deck,
			# a neutral card is shown from the deck together with two other neutral
			# cards from outside the deck.
			enemy_class = player.opponent.starting_hero.card_class
			starting_cards = [
				card for card in player.opponent.starting_deck if enemy_class in card.classes
			]
			if len(starting_cards) == 0:
				enemy_class = CardClass.NEUTRAL
				starting_cards = player.opponent.starting_deck[:]
			starting_card_ids = [card.id for card in starting_cards]
			starting_card_id = random.choice(starting_card_ids)
			other_card_ids = [
				card for card in RandomCollectible(card_class=enemy_class).find_cards(source)
				if card not in starting_card_ids
			]
			other_card_id_1, other_card_id_2 = random.sample(other_card_ids, 2)
			self.starting_card = player.card(starting_card_id)
			self.other_card_1 = player.card(other_card_id_1)
			self.other_card_2 = player.card(other_card_id_2)
			self.cards = [self.starting_card, self.other_card_1, self.other_card_2]
			random.shuffle(self.cards)
			source.game.manager.targeted_action(self, source, player)

		def choose(self, card):
			if card not in self.cards:
				raise InvalidAction("%r is not a valid choice (one of %r)" % (card, self.cards))
			else:
				if card is self.starting_card:
					if len(self.player.hand) < self.player.max_hand_size:
						card.zone = Zone.HAND
				else:
					log.info("Choose incorrectly, corrent choice is %r", self.starting_card)
			self.player.choice = None
			self.trigger_choice_callback()

	requirements = {PlayReq.REQ_MINION_TARGET: 0}
	play = GlimmerrootAction(CONTROLLER)


class UNG_037:
	"""Tortollan Shellraiser"""
	deathrattle = Buff(RANDOM(FRIENDLY_MINIONS), "UNG_037e")


UNG_037e = buff(+1, +1)


class UNG_963:
	"""Lyra the Sunshard"""
	events = Play(CONTROLLER, SPELL).after(
		Give(CONTROLLER, RandomSpell(card_class=CardClass.PRIEST)))


##
# Spells

class UNG_029:
	"""Shadow Visions"""
	play = GenericChoice(CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY_DECK + SPELL)) * 3))


class UNG_030:
	"""Binding Heal"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Heal(FRIENDLY_HERO, 5), Heal(TARGET, 5)


class UNG_854:
	"""Free From Amber"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0}
	play = Discover(CONTROLLER, RandomMinion(cost=list(range(8, 25)))).then(
		Summon(CONTROLLER, Discover.CARD)
	)


class UNG_940:
	"""Awaken the Makers"""
	progress_total = 7
	quest = Summon(CONTROLLER, DEATHRATTLE).after(AddProgress(SELF, Summon.CARD))
	reward = Give(CONTROLLER, "UNG_940t8")


class UNG_940t8:
	play = Buff(FRIENDLY_HERO, "UNG_940t8e")


@custom_card
class UNG_940t8e:
	tags = {
		GameTag.CARDNAME: "Amara, Warden of Hope Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
	}
	max_health = SET(40)
