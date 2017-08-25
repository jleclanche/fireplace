from ..utils import *

##
# Minions

# class UNG_002:
#	"Volcanosaur"

# class UNG_070:
#	"Tol'vir Stoneshaper"

# class UNG_072:
# 	"Stonehill Defender"

# class UNG_075:
# 	"Vicious Fledgling"

class UNG_079:
	"Frozen Crusher"
	events = Attack(SELF).on(Freeze(SELF))

class UNG_083:
	"Devilsaur Egg"
	deathrattle = Summon(CONTROLLER, "EX1_tk29")

class UNG_807:
	"Golakka Crawler"
	play = Destroy(TARGET), Buff(SELF, "UNG_807e")

UNG_807e=buff(atk=+1, health=+1)

# class UNG_816:
#	"Servant of Kalimos"
