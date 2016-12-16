from ..utils import *

##
# Minions

#class CFM_321:
#	"Grimestreet Informant"

class CFM_325:
	"Small-Time Buccaneer"
	update = Find(FRIENDLY_WEAPON) & Refresh(SELF, buff="CFM_325e")

class CFM_325e:
	tags = {GameTag.ATK: +2}

#class CFM_649:
#	"Kabal Courier"

class CFM_652:
	"Second-Rate Bruiser"
	class Hand:
		update = ( 
			(Count(ENEMY_MINIONS) >= 3) & 
			Refresh(SELF, {GameTag.COST: -2}) 
			)

class CFM_658:
	"Backroom Bouncer"
	events = Death(FRIENDLY + MINION).on(Buff(SELF, "CFM_658e"))

CFM_658e = buff(+1)

#class CFM_667:
#	"Bomb Squad"

#class CFM_668:
#	"Doppelgangster"

#class CFM_688:
#	"Spiked Hogrider"

#class CFM_852:
#	"Lotus Agents"

