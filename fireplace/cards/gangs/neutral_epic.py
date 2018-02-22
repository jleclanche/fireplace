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

class CFM_095:
 	"Weasel Tunneler"
 	deathrattle = Shuffle(OPPONENT, ExactCopy(SELF))

class CFM_328:
	"Fight Promoter"
	play = Find(FRIENDLY_MINIONS + (CURRENT_HEALTH >= 6)) & Draw(CONTROLLER) * 2

class CFM_609:
	"Fel Orc Soulfiend"
	events = OWN_TURN_BEGIN.on(Hit(SELF, 2))

class CFM_669:
	"Burgly Bully"
	events = Play(OPPONENT, SPELL).on(Give(CONTROLLER, "GAME_005"))

class CFM_790:
	"Dirty Rat"
	play = Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION))

class CFM_810:
	"Leatherclad Hogleader"
	powered_up = Count(ENEMY_HAND) > 5
	play = powered_up & GiveCharge(SELF)

class CFM_855:
	"Defias Cleaner"
	play = Silence(TARGET)


