from ..utils import *


##
# Minions

# Flamewaker
class BRM_002:
	events = OWN_SPELL_PLAY.after(Hit(RANDOM_ENEMY_MINION, 1) * 2)


# Twilight Whelp
class BRM_004:
	play = HOLDING_DRAGON & Buff(SELF, "BRM_004e")

BRM_004e = buff(health=2)


# Imp Gang Boss
class BRM_006:
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_006t"))


# Dark Iron Skulker
class BRM_008:
	play = Hit(ENEMY_MINIONS - DAMAGED, 2)


# Volcanic Lumberer
class BRM_009:
	cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


# Druid of the Flame
class BRM_010:
	choose = ("BRM_010a", "BRM_010b")

class BRM_010a:
	play = Morph(SELF, "BRM_010t")

class BRM_010b:
	play = Morph(SELF, "BRM_010t2")


# Fireguard Destroyer
class BRM_012:
	play = Buff(SELF, "BRM_012e") * RandomNumber(1, 2, 3, 4)

BRM_012e = buff(atk=1)


# Core Rager
class BRM_014:
	powered_up = Count(FRIENDLY_HAND - SELF) == 0
	play = EMPTY_HAND & Buff(SELF, "BRM_014e")

BRM_014e = buff(+3, +3)


# Axe Flinger
class BRM_016:
	events = SELF_DAMAGE.on(Hit(ENEMY_HERO, 2))


# Dragon Consort
class BRM_018:
	play = Buff(CONTROLLER, "BRM_018e")

BRM_018e = buff(cost=-3)


class BRM_018e:
	events = Play(CONTROLLER, DRAGON).on(Destroy(SELF))


# Grim Patron
class BRM_019:
	events = SELF_DAMAGE.on(Dead(SELF) | Summon(CONTROLLER, "BRM_019"))


# Dragonkin Sorcerer
class BRM_020:
	events = Play(CONTROLLER, SPELL, SELF).on(Buff(SELF, "BRM_020e"))

BRM_020e = buff(+1, +1)


# Dragon Egg
class BRM_022:
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_022t"))


# Drakonid Crusher
class BRM_024:
	powered_up = Attr(ENEMY_HERO, "health") <= 15
	play = powered_up & Buff(SELF, "BRM_024e")

BRM_024e = buff(+3, +3)


# Volcanic Drake
class BRM_025:
	cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


# Hungry Dragon
class BRM_026:
	play = Summon(OPPONENT, RandomMinion(cost=1))


# Majordomo Executus
class BRM_027:
	deathrattle = Summon(CONTROLLER, "BRM_027h")

# DIE, INSECT!
class BRM_027p:
	activate = Hit(RANDOM_ENEMY_CHARACTER, 8)

# DIE, INSECTS!
class BRM_027pH:
	activate = Hit(RANDOM_ENEMY_CHARACTER, 8) * 2


# Emperor Thaurissan
class BRM_028:
	events = OWN_TURN_END.on(Buff(FRIENDLY_HAND, "BRM_028e"))

class BRM_028e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -1}


# Rend Blackhand
class BRM_029:
	powered_up = HOLDING_DRAGON, Find(ENEMY_MINIONS + LEGENDARY)
	play = HOLDING_DRAGON & Destroy(TARGET)


# Nefarian
class BRM_030:
	play = Find(ENEMY_HERO + CLASS_CARD) & (
		Give(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS)) * 2
	) | (
		Give(CONTROLLER, "BRM_030t") * 2
	)

# Tail Swipe
class BRM_030t:
	play = Hit(TARGET, 4)


# Chromaggus
class BRM_031:
	events = Draw(CONTROLLER).on(Give(CONTROLLER, Copy(Draw.CARD)))


# Blackwing Technician
class BRM_033:
	powered_up = HOLDING_DRAGON
	play = HOLDING_DRAGON & Buff(SELF, "BRM_033e")

BRM_033e = buff(+1, +1)


# Blackwing Corruptor
class BRM_034:
	powered_up = HOLDING_DRAGON
	play = HOLDING_DRAGON & Hit(TARGET, 3)


##
# Spells

# Solemn Vigil
class BRM_001:
	play = Draw(CONTROLLER) * 2
	cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


# Melt (Unused)
class BRM_001e:
	atk = SET(0)


# Dragon's Breath
class BRM_003:
	play = Hit(TARGET, 4)
	cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)

# Dragon's Might (Unused)
BRM_003e = buff(cost=-3)


# Demonwrath
class BRM_005:
	play = Hit(ALL_MINIONS - DEMON, 2)


# Gang Up
class BRM_007:
	play = Shuffle(CONTROLLER, Copy(TARGET)) * 3


# Lava Shock
class BRM_011:
	play = Hit(TARGET, 2), UnlockOverload(CONTROLLER)

# Lava Shock (Unused)
class BRM_011t:
	tags = {enums.CANT_OVERLOAD: True}


# Quick Shot
class BRM_013:
	powered_up = Count(FRIENDLY_HAND - SELF) == 0
	play = Hit(TARGET, 3), EMPTY_HAND & Draw(CONTROLLER)


# Revenge
class BRM_015:
	powered_up = Attr(FRIENDLY_HERO, "health") <= 12
	play = powered_up & Hit(ALL_MINIONS, 3) | Hit(ALL_MINIONS, 1)


# Resurrect
class BRM_017:
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))
