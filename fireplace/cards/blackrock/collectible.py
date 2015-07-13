from ..utils import *


##
# Minions

# Flamewaker
class BRM_002:
	events = [
		OWN_SPELL_PLAY.after(Hit(RANDOM_ENEMY_MINION, 1) * 2)
	]


# Imp Gang Boss
class BRM_006:
	events = [
		SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_006t"))
	]


# Dark Iron Skulker
class BRM_008:
	action = [Hit(ENEMY_MINIONS - DAMAGED, 2)]


# Volcanic Lumberer
class BRM_009:
	def cost(self, value):
		return value - len(self.game.minions_killed_this_turn)


# Druid of the Flame (Firecat Form)
class BRM_010a:
	action = [Morph(SELF, "BRM_010t")]

# Druid of the Flame (Firehawk Form)
class BRM_010b:
	action = [Morph(SELF, "BRM_010t2")]


# Axe Flinger
class BRM_016:
	events = [
		SELF_DAMAGE.on(Hit(ENEMY_HERO, 2))
	]


# Dragon Egg
class BRM_022:
	events = [
		SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_022t"))
	]


# Volcanic Drake
class BRM_025:
	def cost(self, value):
		return value - len(self.game.minions_killed_this_turn)


# Hungry Dragon
class BRM_026:
	action = [Summon(OPPONENT, RandomMinion(cost=1))]


# Majordomo Executus
class BRM_027:
	deathrattle = [Summon(CONTROLLER, "BRM_027h"), Summon(CONTROLLER, "BRM_027p")]

# DIE, INSECT!
class BRM_027p:
	activate = [Hit(RANDOM_ENEMY_CHARACTER, 8)]


# Emperor Thaurissan
class BRM_028:
	events = [
		OWN_TURN_END.on(Buff(CONTROLLER_HAND, "BRM_028e"))
	]

##
# Spells

# Solemn Vigil
class BRM_001:
	action = [Draw(CONTROLLER) * 2]

	def cost(self, value):
		return value - len(self.game.minions_killed_this_turn)


# Dragon's Breath
class BRM_003:
	action = [Hit(TARGET, 4)]

	def cost(self, value):
		return value - len(self.game.minions_killed_this_turn)


# Demonwrath
class BRM_005:
	action = [Hit(ALL_MINIONS - DEMON, 2)]


# Gang Up
class BRM_007:
	action = [Shuffle(CONTROLLER, Copy(TARGET)) * 3]


# Quick Shot
class BRM_013:
	action = [Hit(TARGET, 3), Find(CONTROLLER_HAND) | Draw(CONTROLLER)]


# Resurrect
class BRM_017:
	def action(self):
		minions = self.game.minions_killed.filter(controller=self.controller)
		if minions:
			return [Summon(CONTROLLER, random.choice(minions).id)]
