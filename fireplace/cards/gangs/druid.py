from ..utils import *

##
# Minions

#class CFM_308:
#	"Kun the Forgotten King"

#class CFM_343:
#	"Jade Behemoth"

class CFM_617:
	"Celestial Dreamer"
	powered_up = Find(FRIENDLY_MINIONS + (ATK >= 5))
	play = powered_up & Buff(SELF, "CFM_617e")

CFM_617e = buff(+2,+2)

class CFM_816:
	"Virmen Sensei"
	powered_up  = Find(FRIENDLY_MINIONS + BEAST)
	play = Buff(TARGET, "CFM_816e")

CFM_816e = buff(+2,+2)

##
# Spells

#class CFM_602:
#	"Jade Idol"

class CFM_614:
	"Mark of the Lotus"
	play = Buff(FRIENDLY_MINIONS, "CFM_614e")

CFM_614e = buff(+1,+1)

#class CFM_616:
#	"Pilfered Power"

#class CFM_713:
#	"Jade Blossom"

#class CFM_811:
#	"Lunar Visions"

