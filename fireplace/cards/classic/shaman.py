from ..utils import *


##
# Hero Powers

# Totemic Call
class CS2_049:
	def activate(self):
		totems = [t for t in self.entourage if not self.controller.field.contains(t)]
		return Summon(CONTROLLER, random.choice(totems))

# Healing Totem
class NEW1_009:
	events = OWN_TURN_END.on(Heal(FRIENDLY_MINIONS, 1))


##
# Minions

# Fire Elemental
class CS2_042:
	play = Hit(TARGET, 3)


# Unbound Elemental
class EX1_258:
	events = Play(CONTROLLER, OVERLOAD).on(Buff(SELF, "EX1_258e"))


# Flametongue Totem
class EX1_565:
	update = Refresh(SELF_ADJACENT, buff="EX1_565o")


# Mana Tide Totem
class EX1_575:
	events = OWN_TURN_END.on(Draw(CONTROLLER))


# Windspeaker
class EX1_587:
	play = SetTag(TARGET, {GameTag.WINDFURY: True})


##
# Spells

# Frost Shock
class CS2_037:
	play = Hit(TARGET, 1), Freeze(TARGET)


# Ancestral Spirit
class CS2_038:
	play = Buff(TARGET, "CS2_038e")

class CS2_038e:
	deathrattle = Summon(CONTROLLER, Copy(SELF))


# Windfury
class CS2_039:
	play = SetTag(TARGET, {GameTag.WINDFURY: True})


# Ancestral Healing
class CS2_041:
	play = FullHeal(TARGET), Buff(TARGET, "CS2_041e")


# Rockbiter Weapon
class CS2_045:
	play = Buff(TARGET, "CS2_045e")


# Bloodlust
class CS2_046:
	play = Buff(FRIENDLY_MINIONS, "CS2_046e")


# Far Sight
class CS2_053:
	play = Buff(Draw(CONTROLLER), "CS2_053e")


# Lightning Bolt
class EX1_238:
	play = Hit(TARGET, 3)


# Lava Burst
class EX1_241:
	play = Hit(TARGET, 5)


# Totemic Might
class EX1_244:
	play = Buff(FRIENDLY_MINIONS + TOTEM, "EX1_244e")


# Hex
class EX1_246:
	play = Morph(TARGET, "hexfrog")


# Feral Spirit
class EX1_248:
	play = Summon(CONTROLLER, "EX1_tk11") * 2


# Forked Lightning
class EX1_251:
	play = Hit(RANDOM_ENEMY_MINION * 2, 2)


# Earth Shock
class EX1_245:
	play = Silence(TARGET), Hit(TARGET, 1)


# Lightning Storm
class EX1_259:
	play = Hit(ENEMY_MINIONS, RandomNumber(2, 3))
