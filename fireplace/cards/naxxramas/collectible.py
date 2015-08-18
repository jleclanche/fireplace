from ..utils import *


##
# Minions

# Zombie Chow
class FP1_001:
	deathrattle = Heal(ENEMY_HERO, 5)


# Haunted Creeper
class FP1_002:
	deathrattle = Summon(CONTROLLER, "FP1_002t"), Summon(CONTROLLER, "FP1_002t")


# Echoing Ooze
class FP1_003:
	play = OWN_TURN_END.on(Summon(CONTROLLER, ExactCopy(SELF)))


# Mad Scientist
class FP1_004:
	deathrattle = Summon(CONTROLLER, RANDOM(CONTROLLER_DECK + SECRET))


# Shade of Naxxramas
class FP1_005:
	events = OWN_TURN_BEGIN.on(Buff(SELF, "FP1_005e"))


# Nerubian Egg
class FP1_007:
	deathrattle = Summon(CONTROLLER, "FP1_007t")


# Deathlord
class FP1_009:
	deathrattle = Summon(OPPONENT, RANDOM(OPPONENT_DECK + MINION))


# Webspinner
class FP1_011:
	deathrattle = Give(CONTROLLER, RandomBeast())


# Sludge Belcher
class FP1_012:
	deathrattle = Summon(CONTROLLER, "FP1_012t")


# Kel'Thuzad
class FP1_013:
	def resurrect_friendly_minions(self, *args):
		for minion in self.game.minions_killed_this_turn.filter(controller=self.controller):
			yield Summon(CONTROLLER, minion.id)

	events = TURN_END.on(resurrect_friendly_minions)


# Stalagg
class FP1_014:
	deathrattle = Find(KILLED + ID("FP1_015")) & Summon(CONTROLLER, "FP1_014t")


# Feugen
class FP1_015:
	deathrattle = Find(KILLED + ID("FP1_014")) & Summon(CONTROLLER, "FP1_014t")


# Wailing Soul
class FP1_016:
	play = Silence(FRIENDLY_MINIONS)


# Nerub'ar Weblord
class FP1_017:
	aura = Buff(MINION + BATTLECRY + IN_HAND, "FP1_017a")


# Voidcaller
class FP1_022:
	deathrattle = Summon(CONTROLLER, RANDOM(CONTROLLER_HAND + DEMON))


# Dark Cultist
class FP1_023:
	deathrattle = Buff(RANDOM_FRIENDLY_MINION, "FP1_023e")


# Unstable Ghoul
class FP1_024:
	deathrattle = Hit(ALL_MINIONS, 1)


# Anub'ar Ambusher
class FP1_026:
	deathrattle = Bounce(RANDOM_FRIENDLY_MINION)


# Stoneskin Gargoyle
class FP1_027:
	events = OWN_TURN_BEGIN.on(Heal(SELF, Attr(SELF, GameTag.DAMAGE)))


# Undertaker
class FP1_028:
	events = Summon(CONTROLLER, MINION + DEATHRATTLE).on(Buff(SELF, "FP1_028e"))


# Dancing Swords
class FP1_029:
	deathrattle = Draw(OPPONENT)


# Loatheb
class FP1_030:
	play = Buff(ENEMY_HERO, "FP1_030e")

class FP1_030e:
	aura = Buff(ENEMY + SPELL + IN_HAND, "FP1_030ea")
	events = OWN_TURN_BEGIN.on(Destroy(SELF))

class FP1_030ea:
	cost = lambda self, i: i + 5 if self.owner.controller.current_player else i


# Baron Rivendare
class FP1_031:
	aura = Buff(CONTROLLER, "FP1_031a")


##
# Spells

# Reincarnate
class FP1_025:
	play = Destroy(TARGET), Summon(CONTROLLER, Copy(TARGET))


##
# Secrets

# Duplicate
class FP1_018:
	events = Death(FRIENDLY + MINION).on(Give(CONTROLLER, Copy(Death.Args.ENTITY)) * 2)


# Avenge
class FP1_020:
	events = Death(FRIENDLY + MINION).on(Find(FRIENDLY_MINIONS) & (
		Buff(RANDOM_FRIENDLY_MINION, "FP1_020e"), Reveal(SELF)
	))


##
# Weapons

# Death's Bite
class FP1_021:
	deathrattle = Hit(ALL_MINIONS, 1)
