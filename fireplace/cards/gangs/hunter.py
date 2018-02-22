from ..utils import *

##
# Minions

class CFM_315:
	"Alleycat"
	play = Summon(CONTROLLER, "CFM_315t")

class CFM_316:
	"Rat Pack"
	def deathrattle(self):
		if self.dead:
			count = self.preatk
		else:
			count = self.atk
		for i in range(count):
			yield Summon(CONTROLLER, "CFM_316t")

class CFM_333:
	"Knuckles"
	def play(self):
		self.game.refresh_auras()
		yield Hit(TARGET, ATK(SELF))

class CFM_335:
	"Dispatch Kodo"
	def play(self):
		self.game.refresh_auras()
		yield Hit(TARGET, ATK(SELF))

class CFM_336:
	"Shaky Zipgunner"
	deathrattle = Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_336e")

CFM_336e = buff(+2, +2)

class CFM_338:
	"Trogg Beastrager"
	powered_up = Count(FRIENDLY_HAND + MINION + BEAST) > 0
	play = powered_up & Buff(RANDOM(FRIENDLY_HAND + MINION + BEAST), "CFM_338e")

CFM_338e = buff(+1, +1)

##
# Spells

class CFM_026:
	"Hidden Cache"
	secret = Play(OPPONENT, MINION).after(
		(Count(FRIENDLY_HAND + MINION) == 0) |
		(Reveal(SELF), Buff(RANDOM(FRIENDLY_HAND + MINION), "CFM_026e"))
		)

CFM_026e = buff(+2, +2)

class CFM_334:
	"Smuggler's Crate"
	play = Buff(RANDOM(FRIENDLY_HAND + MINION + BEAST), "CFM_334e")

CFM_334e = buff(+2, +2)

##
# Weapons

class CFM_337:
	"Piranha Launcher"
	events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "CFM_337t"))
