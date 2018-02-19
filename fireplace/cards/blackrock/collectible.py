from ..utils import *


##
# Minions

class BRM_002:
	"Flamewaker"
	events = OWN_SPELL_PLAY.after(Hit(RANDOM_ENEMY_MINION, 1) * 2)


class BRM_004:
	"Twilight Whelp"
	powered_up = HOLDING_DRAGON
	play = powered_up & Buff(SELF, "BRM_004e")

BRM_004e = buff(health=2)


class BRM_006:
	"Imp Gang Boss"
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_006t"))


class BRM_008:
	"Dark Iron Skulker"
	play = Hit(ENEMY_MINIONS - DAMAGED, 2)


class BRM_009:
	"Volcanic Lumberer"
	cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


class BRM_010:
	"Druid of the Flame"
	choose = ("BRM_010a", "BRM_010b")
	play = ChooseBoth(CONTROLLER) & Morph(SELF, "OG_044b")

class BRM_010a:
	play = Morph(SELF, "BRM_010t")

class BRM_010b:
	play = Morph(SELF, "BRM_010t2")


class BRM_012:
	"Fireguard Destroyer"
	play = Buff(SELF, "BRM_012e") * RandomNumber(1, 2, 3, 4)

BRM_012e = buff(atk=1)


class BRM_014:
	"Core Rager"
	powered_up = Count(FRIENDLY_HAND - SELF) == 0
	play = EMPTY_HAND & Buff(SELF, "BRM_014e")

BRM_014e = buff(+3, +3)


class BRM_016:
	"Axe Flinger"
	events = SELF_DAMAGE.on(Hit(ENEMY_HERO, 2))


class BRM_018:
	"Dragon Consort"
	play = Buff(CONTROLLER, "BRM_018e")

BRM_018e = buff(cost=-3)


class BRM_018e:
	events = Play(CONTROLLER, DRAGON).on(Destroy(SELF))


class BRM_019:
	"Grim Patron"
	events = SELF_DAMAGE.on(Dead(SELF) | Summon(CONTROLLER, "BRM_019"))


class BRM_020:
	"Dragonkin Sorcerer"
	events = Play(CONTROLLER, SPELL, SELF).on(Buff(SELF, "BRM_020e"))

BRM_020e = buff(+1, +1)


class BRM_022:
	"Dragon Egg"
	events = SELF_DAMAGE.on(Summon(CONTROLLER, "BRM_022t"))


class BRM_024:
	"Drakonid Crusher"
	powered_up = CURRENT_HEALTH(ENEMY_HERO) <= 15
	play = powered_up & Buff(SELF, "BRM_024e")

BRM_024e = buff(+3, +3)


class BRM_025:
	"Volcanic Drake"
	cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


class BRM_026:
	"Hungry Dragon"
	play = Summon(OPPONENT, RandomMinion(cost=1))


class BRM_027:
	"Majordomo Executus"
	deathrattle = Summon(CONTROLLER, "BRM_027h")

class BRM_027p:
	"DIE, INSECT!"
	activate = Hit(RANDOM_ENEMY_CHARACTER, 8)

class BRM_027pH:
	"DIE, INSECTS!"
	activate = Hit(RANDOM_ENEMY_CHARACTER, 8) * 2


class BRM_028:
	"Emperor Thaurissan"
	events = OWN_TURN_END.on(Buff(FRIENDLY_HAND, "BRM_028e"))

class BRM_028e:
	events = REMOVED_IN_PLAY
	tags = {GameTag.COST: -1}


class BRM_029:
	"Rend Blackhand"
	powered_up = HOLDING_DRAGON, Find(ENEMY_MINIONS + LEGENDARY)
	play = HOLDING_DRAGON & Destroy(TARGET)


class BRM_030:
	"Nefarian"
	play = Find(ENEMY_HERO + CLASS_CARD) & (
		Give(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS)) * 2
	) | (
		Give(CONTROLLER, "BRM_030t") * 2
	)

class BRM_030t:
	"Tail Swipe"
	play = Hit(TARGET, 4)


class BRM_031:
	"Chromaggus"
	events = Draw(CONTROLLER).on(Give(CONTROLLER, Copy(Draw.CARD)))


class BRM_033:
	"Blackwing Technician"
	powered_up = HOLDING_DRAGON
	play = powered_up & Buff(SELF, "BRM_033e")

BRM_033e = buff(+1, +1)


class BRM_034:
	"Blackwing Corruptor"
	powered_up = HOLDING_DRAGON
	play = powered_up & Hit(TARGET, 3)


##
# Spells

class BRM_001:
	"Solemn Vigil"
	play = Draw(CONTROLLER) * 2
	cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)


class BRM_001e:
	"Melt (Unused)"
	atk = SET(0)


class BRM_003:
	"Dragon's Breath"
	play = Hit(TARGET, 4)
	cost_mod = -Attr(GAME, GameTag.NUM_MINIONS_KILLED_THIS_TURN)

# Dragon's Might (Unused)
BRM_003e = buff(cost=-3)


class BRM_005:
	"Demonwrath"
	play = Hit(ALL_MINIONS - DEMON, 2)


class BRM_007:
	"Gang Up"
	play = Shuffle(CONTROLLER, Copy(TARGET)) * 3


class BRM_011:
	"Lava Shock"
	play = Hit(TARGET, 2), UnlockOverload(CONTROLLER)

class BRM_011t:
	"Lava Shock (Unused)"
	tags = {enums.CANT_OVERLOAD: True}


class BRM_013:
	"Quick Shot"
	powered_up = Count(FRIENDLY_HAND - SELF) == 0
	play = Hit(TARGET, 3), EMPTY_HAND & Draw(CONTROLLER)


class BRM_015:
	"Revenge"
	powered_up = CURRENT_HEALTH(FRIENDLY_HERO) <= 12
	play = powered_up & Hit(ALL_MINIONS, 3) | Hit(ALL_MINIONS, 1)


class BRM_017:
	"Resurrect"
	play = Summon(CONTROLLER, Copy(RANDOM(FRIENDLY + KILLED + MINION)))
