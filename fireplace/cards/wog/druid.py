from ..utils import *


##
# Minions

class OG_051:
	"""Forbidden Ancient"""
	def play(self):
		mana = self.controller.mana
		yield SpendMana(CONTROLLER, mana)
		yield Buff(SELF, "OG_051e") * mana


OG_051e = buff(+1, +1)


class OG_044:
	"""Fandral Staghelm"""
	update = Refresh(CONTROLLER, {
		GameTag.CHOOSE_BOTH: True,
	})


class OG_202:
	"""Mire Keeper"""
	choose = ("OG_202a", "OG_202b")
	play = ChooseBoth(CONTROLLER) & (
		Summon(CONTROLLER, "OG_202c"),
		AT_MAX_MANA(CONTROLLER) | GainEmptyMana(CONTROLLER, 1)
	)


class OG_202a:
	play = Summon(CONTROLLER, "OG_202c")


class OG_202b:
	play = AT_MAX_MANA(CONTROLLER) | GainEmptyMana(CONTROLLER, 1)


class OG_313:
	"""Addled Grizzly"""
	events = Summon(CONTROLLER, MINION).after(
		Buff(Summon.CARD, "OG_313e")
	)


OG_313e = buff(+1, +1)


class OG_188:
	"""Klaxxi Amber-Weaver"""
	play = CHECK_CTHUN & Buff(SELF, "OG_188")


OG_188e = buff(health=4)


class OG_293:
	"""Dark Arakkoa"""
	play = Buff(CTHUN, "OG_281e", atk=3, max_health=3)


##
# Spells

class OG_047:
	"""Feral Rage"""
	choose = ("OG_047a", "OG_047b")
	play = ChooseBoth(CONTROLLER) & (
		Buff(FRIENDLY_HERO, "OG_047e"),
		GainArmor(FRIENDLY_HERO, 8)
	)


class OG_047a:
	play = Buff(FRIENDLY_HERO, "OG_047e")


OG_047e = buff(atk=4)


class OG_047b:
	play = GainArmor(FRIENDLY_HERO, 8)


class OG_048:
	"""Mark of Y'Shaarj"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "OG_048e").then(
		Find(Buff.TARGET + BEAST) & Draw(CONTROLLER)
	)


OG_048e = buff(+2, +2)


class OG_195:
	"""Wisps of the Old Gods"""
	choose = ("OG_195a", "OG_195b")
	play = ChooseBoth(CONTROLLER) & (
		Summon(CONTROLLER, "OG_195c") * 7,
		Buff(FRIENDLY_MINIONS, "OG_195e")
	)


class OG_195a:
	play = Summon(CONTROLLER, "OG_195c") * 7


class OG_195b:
	play = Buff(FRIENDLY_MINIONS, "OG_195e")


OG_195e = buff(+2, +2)
