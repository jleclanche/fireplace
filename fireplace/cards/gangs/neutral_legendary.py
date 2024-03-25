from ..utils import *


##
# Minions

class CFM_341:
	"""Sergeant Sally"""
	deathrattle = Hit(ALL_MINIONS, ATK(SELF))


class CFM_344:
	"""Finja, the Flying Star"""
	events = Attack(SELF, ALL_MINIONS).after(
		Dead(ALL_MINIONS + Attack.DEFENDER) & (Recruit(MURLOC) * 2)
	)


class CFM_621:
	"""Kazakus"""
	class KazakusAction(MultipleChoice):
		PLAYER = ActionArg()
		choose_times = 3

		def do_step1(self):
			self.cost_1_potions = [
				"CFM_621t4", "CFM_621t10", "CFM_621t37",
				"CFM_621t2", "CFM_621t3", "CFM_621t6",
				"CFM_621t8", "CFM_621t9", "CFM_621t5"]
			self.cost_5_potions = [
				"CFM_621t21", "CFM_621t18", "CFM_621t20",
				"CFM_621t38", "CFM_621t16", "CFM_621t17",
				"CFM_621t24", "CFM_621t22", "CFM_621t23",
				"CFM_621t19"]
			self.cost_10_potions = [
				"CFM_621t29", "CFM_621t33", "CFM_621t28",
				"CFM_621t39", "CFM_621t25", "CFM_621t26",
				"CFM_621t32", "CFM_621t30", "CFM_621t31",
				"CFM_621t27"]
			self.cards = [
				self.player.card(card) for card in [
					"CFM_621t11", "CFM_621t12", "CFM_621t13",
				]
			]

		def do_step2(self):
			card1 = self.choosed_cards[0]
			if card1 == "CFM_621t11":
				self.potions_id = self.cost_1_potions
			elif card1 == "CFM_621t12":
				self.potions_id = self.cost_5_potions
			elif card1 == "CFM_621t13":
				self.potions_id = self.cost_10_potions
			self.potions = [
				self.player.card(card) for card in self.potions_id
			]
			self.cards = random.sample(self.potions, 3)

		def do_step3(self):
			card2 = self.choosed_cards[1]
			self.potions.remove(card2)
			self.cards = random.sample(self.potions, 3)

		def done(self):
			card0 = self.choosed_cards[0]
			card1 = self.choosed_cards[1]
			card2 = self.choosed_cards[2]
			if card0 == "CFM_621t11":
				new_card = self.player.card("CFM_621t")
			elif card0 == "CFM_621t12":
				new_card = self.player.card("CFM_621t14")
			elif card0 == "CFM_621t13":
				new_card = self.player.card("CFM_621t15")
			if self.potions_id.index(card1) > self.potions_id.index(card2):
				card1, card2 = card2, card1
			new_card.custom_card = True

			def create_custom_card(new_card):
				new_card.data.scripts.play = card1.data.scripts.play + card2.data.scripts.play
				new_card.requirements = card1.requirements | card2.requirements
				new_card.tags[GameTag.CARDTEXT_ENTITY_0] = card1.data.strings[GameTag.CARDTEXT]
				new_card.tags[GameTag.CARDTEXT_ENTITY_1] = card2.data.strings[GameTag.CARDTEXT]

			new_card.create_custom_card = create_custom_card
			new_card.create_custom_card(new_card)
			self.player.give(new_card)

	powered_up = -FindDuplicates(FRIENDLY_DECK)
	play = powered_up & KazakusAction(CONTROLLER)


class CFM_637:
	"""Patches the Pirate"""
	class Deck:
		events = Play(CONTROLLER, PIRATE).after(Summon(CONTROLLER, SELF))


class CFM_670:
	"""Mayor Noggenfogger"""
	update = Refresh(PLAYER, {GameTag.ALL_TARGETS_RANDOM: True}),
	events = Attack(MINION).on(
		COINFLIP & Retarget(
			Attack.ATTACKER,
			RANDOM(ALL_CHARACTERS - Attack.DEFENDER - CONTROLLED_BY(Attack.ATTACKER))
		)
	)


class CFM_672:
	"""Madam Goya"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}

	play = Swap(TARGET, RANDOM(FRIENDLY_DECK + MINION))


class CFM_685:
	"""Don Han'Cho"""
	play = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_685e")


CFM_685e = buff(+5, +5)


class CFM_806:
	"""Wrathion"""
	play = Draw(CONTROLLER).then(
		Find(Draw.CARD + DRAGON) & (
			Find(LazyValueSelector(Draw.CARD)) & (
				ExtraBattlecry(SELF, None)
			)
		)
	)


class CFM_807:
	"""Auctionmaster Beardo"""
	events = OWN_SPELL_PLAY.after(RefreshHeroPower(FRIENDLY_HERO_POWER))


class CFM_808:
	"""Genzo, the Shark"""
	events = Attack(SELF).on(DrawUntil(PLAYER, 3))


class CFM_902(JadeGolemUtils):
	"""Aya Blackpaw"""
	play = SummonJadeGolem(CONTROLLER)
	deathrattle = SummonJadeGolem(CONTROLLER)
