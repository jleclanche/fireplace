from ..utils import *

##
# Minions

class CFM_025:
	"Wind-up Burglebot"
	events = Attack(SELF, MINION).after((CURRENT_HEALTH(SELF) <= 0) | Draw(CONTROLLER))

class CFM_064:
	"Blubber Baron"
	class Hand:
		events = Play(CONTROLLER, MINION + BATTLECRY).on(Buff(SELF, "CFM_064e"))

CFM_064e = buff(+1, +1)

#class CFM_095:
#	"Weasel Tunneler"

class CFM_328:
	"Fight Promoter"
	play = Find(FRIENDLY_MINIONS + (CURRENT_HEALTH >= 6)) & Draw(CONTROLLER) * 2

class CFM_609:
	"Fel Orc Soulfiend"
	events = OWN_TURN_BEGIN.on(Hit(SELF, 2))

#class CFM_669:
#	"Burgly Bully"

#class CFM_790:
#	"Dirty Rat"

#class CFM_810:
#	"Leatherclad Hogleader"

#class CFM_855:
#	"Defias Cleaner"

