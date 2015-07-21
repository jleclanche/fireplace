from ..utils import *


##
# Minions

# Flamewaker
class BRM_002:
	events = OWN_SPELL_PLAY.after(Hit(RANDOM_ENEMY_MINION, 1) * 2)


# Twilight Whelp
class BRM_004:
	play = HOLDING_DRAGON & Buff(SELF, "BRM_004e")


# Imp Gang Boss
class BRM_006:
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_006t"))


# Dark Iron Skulker
class BRM_008:
	play = Hit(ENEMY_MINIONS - DAMAGED, 2)


# Volcanic Lumberer
class BRM_009:
	cost = lambda self, i: i - len(self.game.minions_killed_this_turn)


# Druid of the Flame (Firecat Form)
class BRM_010a:
	play = Morph(SELF, "BRM_010t")

# Druid of the Flame (Firehawk Form)
class BRM_010b:
	play = Morph(SELF, "BRM_010t2")


# Core Rager
class BRM_014:
	play = Find(CONTROLLER_HAND) | Buff(SELF, "BRM_014e")


# Axe Flinger
class BRM_016:
	events = SELF_DAMAGE.on(Hit(ENEMY_HERO, 2))


# Dragonkin Sorcerer
class BRM_020:
	events = Play(CONTROLLER, SPELL, SELF).on(Buff(SELF, "BRM_020e"))


# Dragon Egg
class BRM_022:
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_022t"))


# Drakonid Crusher
class BRM_024:
	play = (Attr(ENEMY_HERO, "health") <= 15) & Buff(SELF, "BRM_024e")


# Volcanic Drake
class BRM_025:
	cost = lambda self, i: i - len(self.game.minions_killed_this_turn)


# Hungry Dragon
class BRM_026:
	play = Summon(OPPONENT, RandomMinion(cost=1))


# Majordomo Executus
class BRM_027:
	deathrattle = Summon(CONTROLLER, "BRM_027h"), Summon(CONTROLLER, "BRM_027p")

# DIE, INSECT!
class BRM_027p:
	activate = Hit(RANDOM_ENEMY_CHARACTER, 8)


# Emperor Thaurissan
class BRM_028:
	events = OWN_TURN_END.on(Buff(CONTROLLER_HAND, "BRM_028e"))


# Blackwing Technician
class BRM_033:
	play = HOLDING_DRAGON & Buff(SELF, "BRM_033e")


##
# Spells

# Solemn Vigil
class BRM_001:
	play = Draw(CONTROLLER) * 2
	cost = lambda self, i: i - len(self.game.minions_killed_this_turn)


# Dragon's Breath
class BRM_003:
	play = Hit(TARGET, 4)
	cost = lambda self, i: i - len(self.game.minions_killed_this_turn)


# Demonwrath
class BRM_005:
	play = Hit(ALL_MINIONS - DEMON, 2)


# Gang Up
class BRM_007:
	play = Shuffle(CONTROLLER, Copy(TARGET)) * 3


# Quick Shot
class BRM_013:
	play = Hit(TARGET, 3), Find(CONTROLLER_HAND) | Draw(CONTROLLER)


# Revenge
class BRM_015:
	play = (Attr(FRIENDLY_HERO, "health") <= 12) & Hit(ALL_MINIONS, 3) | Hit(TARGET, 1)


# Resurrect
class BRM_017:
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))
