from ..utils import *


# Big Game Hunter
class EX1_005:
	play = Destroy(TARGET)


# Mountain Giant
class EX1_105:
	cost_mod = -Count(FRIENDLY_HAND - SELF)


# Murloc Warleader
class EX1_507:
	update = Refresh(ALL_MINIONS + MURLOC - SELF, buff="EX1_507e")

EX1_507e = buff(+2, +1)


# Faceless Manipulator
class EX1_564:
	play = Morph(SELF, ExactCopy(TARGET))


# Sea Giant
class EX1_586:
	cost_mod = -Count(ALL_MINIONS)


# Blood Knight
class EX1_590:
	play = (
		Buff(SELF, "EX1_590e") * Count(ALL_MINIONS + DIVINE_SHIELD),
		UnsetTag(ALL_MINIONS, (GameTag.DIVINE_SHIELD, ))
	)

EX1_590e = buff(+3, +3)


# Molten Giant
class EX1_620:
	cost_mod = -DAMAGE(FRIENDLY_HERO)


# Captain's Parrot
class NEW1_016:
	play = ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE))


# Hungry Crab
class NEW1_017:
	play = Destroy(TARGET), Buff(SELF, "NEW1_017e")

NEW1_017e = buff(+2, +2)


# Doomsayer
class NEW1_021:
	events = OWN_TURN_BEGIN.on(Destroy(ALL_MINIONS))


# Southsea Captain
class NEW1_027:
	update = Refresh(FRIENDLY_MINIONS + PIRATE - SELF, buff="NEW1_027e")

NEW1_027e = buff(+1, +1)
