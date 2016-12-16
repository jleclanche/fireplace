from ..utils import *

##
# Minions

class CFM_025:
	"Wind-up Burglebot"
	events = Attack(SELF, MINION).after((CURRENT_HEALTH(SELF) <= 0) | Draw(CONTROLLER))

#class CFM_064:
#	"Blubber Baron"

#class CFM_095:
#	"Weasel Tunneler"

#class CFM_328:
#	"Fight Promoter"

#class CFM_609:
#	"Fel Orc Soulfiend"

#class CFM_669:
#	"Burgly Bully"

#class CFM_790:
#	"Dirty Rat"

#class CFM_810:
#	"Leatherclad Hogleader"

#class CFM_855:
#	"Defias Cleaner"

