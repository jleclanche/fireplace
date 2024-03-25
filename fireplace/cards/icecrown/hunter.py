from ...cards import get_script_definition
from ..utils import *


##
# Minions

class ICC_021:
	"""Exploding Bloatbat"""
	deathrattle = Hit(ENEMY_MINIONS, 2)


class ICC_204:
	"""Professor Putricide"""
	events = Play(CONTROLLER, SECRET).after(
		Summon(CONTROLLER, RandomSpell(
			secret=True,
			card_class=CardClass.HUNTER,
			exclude=FRIENDLY_SECRETS)))


class ICC_243:
	"""Corpse Widow"""
	update = Refresh(FRIENDLY_HAND + DEATHRATTLE, {GameTag.COST: -2})


class ICC_415:
	"""Stitched Tracker"""
	play = GenericChoice(CONTROLLER, Copy(RANDOM(DeDuplicate(FRIENDLY_DECK + MINION)) * 3))


class ICC_825:
	"""Abominable Bowman"""
	deathrattle = Summon(CONTROLLER, Copy(FRIENDLY + KILLED + BEAST))


##
# Spells

class ICC_049:
	"""Toxic Arrow"""
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = Hit(TARGET, 2), Dead(TARGET) | GivePoisonous(TARGET)


class ICC_052:
	"""Play Dead"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = Deathrattle(TARGET)


class ICC_200:
	"""Venomstrike Trap"""
	secret = Attack(None, FRIENDLY_MINIONS).on(FULL_BOARD | (
		Reveal(SELF), Summon(CONTROLLER, "EX1_170")
	))


##
# Heros

class ICC_828:
	"""Deathstalker Rexxar"""
	play = Hit(ENEMY_MINIONS, 2)


class ICC_828p:
	class CreateZombeast(MultipleChoice):
		PLAYER = ActionArg()
		choose_times = 2

		def do_step1(self):
			beast_ids = RandomBeast(
				card_class=[CardClass.HUNTER, CardClass.NEUTRAL],
				cost=range(0, 6)).find_cards(self.source)
			self.first_ids = []
			self.second_ids = []
			for id in beast_ids:
				if get_script_definition(id):
					self.first_ids.append(id)
				else:
					self.second_ids.append(id)
			self.cards = [self.player.card(id) for id in random.sample(self.first_ids, 3)]

		def do_step2(self):
			self.cards = [self.player.card(id) for id in random.sample(self.second_ids, 3)]

		def done(self):
			card1 = self.choosed_cards[0]
			card2 = self.choosed_cards[1]

			zombeast = self.player.card("ICC_828t")
			zombeast.custom_card = True

			def create_custom_card(zombeast):
				zombeast.tags[GameTag.CARDTEXT_ENTITY_0] = card2.data.strings[GameTag.CARDTEXT]
				zombeast.tags[GameTag.CARDTEXT_ENTITY_1] = card1.data.strings[GameTag.CARDTEXT]
				zombeast.data.scripts = card1.data.scripts

				for k in zombeast.silenceable_attributes:
					v1 = getattr(card1, k)
					v2 = getattr(card2, k)
					setattr(zombeast, k, v1 + v2)

				zombeast.cost = card1.cost + card2.cost
				zombeast.atk = card1.atk + card2.atk
				zombeast.max_health = card1.max_health + card2.max_health

			zombeast.create_custom_card = create_custom_card
			zombeast.create_custom_card(zombeast)
			self.player.give(zombeast)

		def choose(self, card):
			if card not in self.cards:
				raise InvalidAction("%r is not a valid choice (one of %r)" % (card, self.cards))
			else:
				self.choosed_cards.append(card)
				if len(self.choosed_cards) == 1:
					self.do_step2()
				elif len(self.choosed_cards) == 2:
					self.player.choice = None
					self.done()
					self.trigger_choice_callback()

	requirements = {
		PlayReq.REQ_HAND_NOT_FULL: 0,
	}
	activate = CreateZombeast(CONTROLLER)
