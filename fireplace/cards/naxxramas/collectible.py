from ..utils import *


##
# Minions

# Zombie Chow
class FP1_001:
	deathrattle = Heal(ENEMY_HERO, 5)


# Haunted Creeper
class FP1_002:
	deathrattle = Summon(CONTROLLER, "FP1_002t"), Summon(CONTROLLER, "FP1_002t")


# Mad Scientist
class FP1_004:
	deathrattle = ForcePlay(CONTROLLER, RANDOM(CONTROLLER_DECK + SECRET))


# Shade of Naxxramas
class FP1_005:
	events = OWN_TURN_BEGIN.on(Buff(SELF, "FP1_005e"))


# Nerubian Egg
class FP1_007:
	deathrattle = Summon(CONTROLLER, "FP1_007t")


# Deathlord
class FP1_009:
	deathrattle = ForcePlay(OPPONENT, RANDOM(OPPONENT_DECK + MINION))


# Webspinner
class FP1_011:
	deathrattle = Give(CONTROLLER, RandomMinion(race=Race.BEAST))


# Sludge Belcher
class FP1_012:
	deathrattle = Summon(CONTROLLER, "FP1_012t")


# Kel'Thuzad
class FP1_013:
	def resurrect_friendly_minions(self, *args):
		for minion in self.game.minions_killed_this_turn.filter(controller=self.controller):
			yield Summon(CONTROLLER, minion.id)

	events = TURN_END.on(resurrect_friendly_minions)


# Wailing Soul
class FP1_016:
	play = Silence(FRIENDLY_MINIONS)


# Voidcaller
class FP1_022:
	deathrattle = ForcePlay(CONTROLLER, RANDOM(CONTROLLER_HAND + DEMON))


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
	events = OWN_TURN_BEGIN.on(
		lambda self, player: Heal(self, self.damage)
	)


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
	events = OWN_TURN_BEGIN.on(Destroy(SELF))

class FP1_030ea:
	cost = lambda self, i: i + 5 if self.owner.controller.current_player else i


##
# Spells

# Reincarnate
class FP1_025:
	play = Destroy(TARGET), Summon(CONTROLLER, Copy(TARGET))


##
# Secrets

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
