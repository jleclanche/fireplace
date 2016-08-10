from ..utils import *


##
# Hero Powers

class CS2_049:
	"Totemic Call"
	def activate(self):
		totems = [t for t in self.entourage if not self.controller.field.contains(t)]
		yield Summon(CONTROLLER, random.choice(totems))

class CS2_049_H1:
	"Totemic Call (Morgl the Oracle)"
	activate = CS2_049.activate


class NEW1_009:
	"Healing Totem"
	events = OWN_TURN_END.on(Heal(FRIENDLY_MINIONS, 1))


##
# Minions

class CS2_042:
	"Fire Elemental"
	play = Hit(TARGET, 3)


class EX1_258:
	"Unbound Elemental"
	events = Play(CONTROLLER, OVERLOAD).on(Buff(SELF, "EX1_258e"))

EX1_258e = buff(+1, +1)


class EX1_565:
	"Flametongue Totem"
	update = Refresh(SELF_ADJACENT, buff="EX1_565o")

EX1_565o = buff(atk=2)


class EX1_575:
	"Mana Tide Totem"
	events = OWN_TURN_END.on(Draw(CONTROLLER))


class EX1_587:
	"Windspeaker"
	play = GiveWindfury(TARGET - WINDFURY)


##
# Spells

class CS2_037:
	"Frost Shock"
	play = Hit(TARGET, 1), Freeze(TARGET)


class CS2_038:
	"Ancestral Spirit"
	play = Buff(TARGET, "CS2_038e")

class CS2_038e:
	deathrattle = Summon(CONTROLLER, Copy(SELF))
	tags = {GameTag.DEATHRATTLE: True}


class CS2_039:
	"Windfury"
	play = GiveWindfury(TARGET - WINDFURY)


class CS2_041:
	"Ancestral Healing"
	play = FullHeal(TARGET), Buff(TARGET, "CS2_041e")

CS2_041e = buff(taunt=True)


class CS2_045:
	"Rockbiter Weapon"
	play = Buff(TARGET, "CS2_045e")

CS2_045e = buff(atk=3)


class CS2_046:
	"Bloodlust"
	play = Buff(FRIENDLY_MINIONS, "CS2_046e")

CS2_046e = buff(atk=3)


class CS2_053:
	"Far Sight"
	play = Draw(CONTROLLER).then(Buff(Draw.CARD, "CS2_053e"))

CS2_053e = buff(cost=-3)


class EX1_238:
	"Lightning Bolt"
	play = Hit(TARGET, 3)


class EX1_241:
	"Lava Burst"
	play = Hit(TARGET, 5)


class EX1_244:
	"Totemic Might"
	play = Buff(FRIENDLY_MINIONS + TOTEM, "EX1_244e")

EX1_244e = buff(health=2)


class EX1_246:
	"Hex"
	play = Morph(TARGET, "hexfrog")


class EX1_248:
	"Feral Spirit"
	play = Summon(CONTROLLER, "EX1_tk11") * 2


class EX1_251:
	"Forked Lightning"
	play = Hit(RANDOM_ENEMY_MINION * 2, 2)


class EX1_245:
	"Earth Shock"
	play = Silence(TARGET), Hit(TARGET, 1)


class EX1_259:
	"Lightning Storm"
	play = Hit(ENEMY_MINIONS, RandomNumber(2, 3))
