from ..utils import *


##
# Hero Powers

class HERO_02bp:
	"""Totemic Call"""
	requirements = {
		PlayReq.REQ_ENTIRE_ENTOURAGE_NOT_IN_PLAY: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1}
	entourage = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]

	def activate(self):
		totems = [t for t in self.entourage if not self.controller.field.contains(t)]
		yield Summon(CONTROLLER, random.choice(totems))


class CS2_049_H1:
	"""Totemic Call (Morgl the Oracle)"""
	requirements = {
		PlayReq.REQ_ENTIRE_ENTOURAGE_NOT_IN_PLAY: 0,
		PlayReq.REQ_NUM_MINION_SLOTS: 1}
	entourage = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]
	activate = HERO_02bp.activate


class NEW1_009:
	"""Healing Totem"""
	events = OWN_TURN_END.on(Heal(FRIENDLY_MINIONS, 1))


##
# Minions

class CS2_042:
	"""Fire Elemental"""
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, 3)


class EX1_258:
	"""Unbound Elemental"""
	events = Play(CONTROLLER, OVERLOAD).on(Buff(SELF, "EX1_258e"))


EX1_258e = buff(+1, +1)


class EX1_565:
	"""Flametongue Totem"""
	update = Refresh(SELF_ADJACENT, buff="EX1_565o")


EX1_565o = buff(atk=2)


class EX1_575:
	"""Mana Tide Totem"""
	events = OWN_TURN_END.on(Draw(CONTROLLER))


class EX1_587:
	"""Windspeaker"""
	requirements = {
		PlayReq.REQ_FRIENDLY_TARGET: 0,
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = GiveWindfury(TARGET - WINDFURY)


##
# Spells

class CS2_037:
	"""Frost Shock"""
	requirements = {PlayReq.REQ_ENEMY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 1), Freeze(TARGET)


class CS2_038:
	"""Ancestral Spirit"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "CS2_038e")


class CS2_038e:
	deathrattle = Summon(CONTROLLER, Copy(SELF))
	tags = {GameTag.DEATHRATTLE: True}


class CS2_039:
	"""Windfury"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = GiveWindfury(TARGET - WINDFURY)


class CS2_041:
	"""Ancestral Healing"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = FullHeal(TARGET), Buff(TARGET, "CS2_041e")


CS2_041e = buff(taunt=True)


class CS2_045:
	"""Rockbiter Weapon"""
	requirements = {PlayReq.REQ_FRIENDLY_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Buff(TARGET, "CS2_045e")


CS2_045e = buff(atk=3)


class CS2_046:
	"""Bloodlust"""
	play = Buff(FRIENDLY_MINIONS, "CS2_046e")


CS2_046e = buff(atk=3)


class CS2_053:
	"""Far Sight"""
	play = Draw(CONTROLLER).then(Buff(Draw.CARD, "CS2_053e"))


CS2_053e = buff(cost=-3)


class EX1_238:
	"""Lightning Bolt"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 3)


class EX1_241:
	"""Lava Burst"""
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 5)


class EX1_244:
	"""Totemic Might"""
	play = Buff(FRIENDLY_MINIONS + TOTEM, "EX1_244e")


EX1_244e = buff(health=2)


class EX1_246:
	"""Hex"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Morph(TARGET, "hexfrog")


class EX1_248:
	"""Feral Spirit"""
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	play = Summon(CONTROLLER, "EX1_tk11") * 2


class EX1_251:
	"""Forked Lightning"""
	requirements = {PlayReq.REQ_MINIMUM_ENEMY_MINIONS: 1}
	play = Hit(RANDOM_ENEMY_MINION * 2, 2)


class EX1_245:
	"""Earth Shock"""
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Silence(TARGET), Hit(TARGET, 1)


class EX1_259:
	"""Lightning Storm"""
	play = Hit(ENEMY_MINIONS, RandomNumber(2, 3))
