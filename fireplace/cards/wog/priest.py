from ..utils import *


##
# Minions

class OG_096:
	"Twilight Darkmender"
	play = CTHUN_CHECK & Heal(FRIENDLY_HERO, 10)

class OG_234:
	"Darkshire Alchemist"
	play = Heal(TARGET, 5)


class OG_316:
	"Herald Volazj"
	def play(self):
		for i in self.controller.field:
			if i!=self:
				card = Buff(ExactCopy(i).evaluate(self), "OG_316k").evaluate(self)
				self.game.cheat_action(i, [Summon(CONTROLLER, card)])

class OG_316k:
	atk = SET(1)
	max_health = SET(1)


class OG_334:
	"Hooded Acolyte"
	events = Heal(ALL_CHARACTERS).on(Buff(CTHUN, "OG_334e"))

OG_334e = buff(+1, +1)

class OG_335:
	"Shifting Shade"
	deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


##
# Spells

class OG_094:
	"Power Word: Tentacles"
	play = Buff(TARGET, "OG_094e")

OG_094e = buff(+2, +6)


class OG_100:
	"Shadow Word: Horror"
	play = Destroy(ALL_MINIONS + (ATK <= 2))


class OG_101:
	"Forbidden Shaping"
	play = (
		Summon(CONTROLLER, RandomMinion(cost=Attr(CONTROLLER, "mana"))),
		SpendMana(CONTROLLER, Attr(CONTROLLER, "mana")),
	)


class OG_104:
	"Embrace the Shadow"
	play = Buff(CONTROLLER, "OG_104e")

class OG_104e:
	update = Refresh(CONTROLLER, {
		GameTag.EMBRACE_THE_SHADOW: True,
	})
