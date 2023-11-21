from ..utils import *


##
# Minions

class CFM_341:
	"""Sergeant Sally"""
	deathrattle = Hit(ALL_MINIONS, ATK(SELF))


class CFM_344:
	"""Finja, the Flying Star"""
	events = Attack(SELF, ALL_MINIONS).after(
		Dead(ALL_MINIONS + Attack.DEFENDER) & (RECRUIT(MURLOC), RECRUIT(MURLOC))
	)


class CFM_621:
	"""Kazakus"""
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

	def play(self):
		targets = self.controller.deck.filter(type=CardType.MINION)
		if targets:
			target = random.sample(targets, 1)
			target.zone = Zone.SETASIDE
			yield Shuffle(CONTROLLER, TARGET)
			yield Summon(CONTROLLER, target)


class CFM_685:
	"""Don Han'Cho"""
	play = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_685e")


CFM_685e = buff(+5, +5)


class CFM_806:
	"""Wrathion"""
	def play(self):
		while True:
			current_handsize = len(self.controller.hand)
			yield Draw(self.controller)
			if len(self.controller.hand) == current_handsize:
				# Unable to draw card due to fatigue or max hand size
				break
			card = self.controller.hand[-1]
			if card.type != CardType.MINION or card.race != Race.DRAGON:
				break


class CFM_807:
	"""Auctionmaster Beardo"""
	events = OWN_SPELL_PLAY.after(RefreshHeroPower(FRIENDLY_HERO_POWER))


class CFM_808:
	"""Genzo, the Shark"""
	events = Attack(SELF).on(DrawUntil(EndTurn.PLAYER, 3))


class CFM_902:
	"""Aya Blackpaw"""
	play = SummonJadeGolem(CONTROLLER)
	deathrattle = SummonJadeGolem(CONTROLLER)
