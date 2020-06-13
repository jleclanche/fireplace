from ..utils import *


##
# Minions

class CFM_308:
	"""Kun the Forgotten King"""
	choose = ("CFM_308a", "CFM_308b")
	play = ChooseBoth(CONTROLLER) & (
		GainArmor(FRIENDLY_HERO, 10), FillMana(CONTROLLER, USED_MANA(CONTROLLER))
	)


class CFM_308a:
	play = GainArmor(FRIENDLY_HERO, 10)


class CFM_308b:
	play = FillMana(CONTROLLER, USED_MANA(CONTROLLER))


class CFM_343:
	"""Jade Behemoth"""
	play = SummonJadeGolem(CONTROLLER)


class CFM_617:
	"""Celestial Dreamer"""
	powered_up = Find(FRIENDLY_MINIONS + (ATK >= 1))
	play = powered_up & Buff(SELF, "CFM_617e")


CFM_617e = buff(+2, +2)


class CFM_816:
	"""Virmen Sensei"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
		PlayReq.REQ_TARGET_WITH_RACE: 20}
	play = Buff(TARGET, "CFM_816e")


CFM_816e = buff(+2, +2)


##
# Spells

class CFM_602:
	"""Jade Idol"""
	choose = ("CFM_602a", "CFM_602b")
	play = ChooseBoth(CONTROLLER) & (
		SummonJadeGolem(CONTROLLER), Shuffle(CONTROLLER, "CFM_602") * 3
	)


class CFM_602a:
	play = SummonJadeGolem(CONTROLLER)


class CFM_602b:
	play = Shuffle(CONTROLLER, "CFM_602") * 3


class CFM_614:
	"""Mark of the Lotus"""
	play = Buff(FRIENDLY_MINIONS, "CFM_614e")


CFM_614e = buff(+1, +1)


class CFM_616:
	"""Pilfered Power"""
	def play(self):
		amount = len(self.controller.field)
		yield GainMana(CONTROLLER, amount)
		if self.controller.mana == 10:
			yield Give(CONTROLLER, "CS2_013t")
		yield SpendMana(CONTROLLER, amount)


class CFM_713:
	"""Jade Blossom"""
	requirements = {PlayReq.REQ_MINION_SLOT_OR_MANA_CRYSTAL_SLOT: 0}
	play = SummonJadeGolem(CONTROLLER), GainMana(CONTROLLER, 1), SpendMana(CONTROLLER, 1)


class CFM_811:
	"""Lunar Visions"""
	play = Draw(CONTROLLER).then(
		Find(Draw.CARD + MINION) & Buff(Draw.CARD, "CFM_811e")
	) * 2


class CFM_811e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -2}
