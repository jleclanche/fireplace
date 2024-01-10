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
		Find(Draw.CARD + DRAGON) | (
			Find(LazyValueSelector(Draw.CARD)) & ExtraBattlecry(SELF, None)
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
