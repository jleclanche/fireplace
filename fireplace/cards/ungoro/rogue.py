from ..utils import *


##
# Minions

class UNG_058:
	"""Razorpetal Lasher"""
	play = Give(CONTROLLER, "UNG_057t1")


class UNG_063:
	"""Biteweed"""
	combo = Buff(SELF, "UNG_063e") * Attr(CONTROLLER, GameTag.NUM_CARDS_PLAYED_THIS_TURN)


UNG_063e = buff(+1, +1)


class UNG_064:
	"""Vilespine Slayer"""
	combo = Destroy(TARGET)


class UNG_065:
	"""Sherazin, Corpse Flower"""
	deathrattle = Morph(SELF, "UNG_065t").then(Summon(CONTROLLER, Morph.CARD))


##
# Spells

class UNG_057:
	"""Razorpetal Volley"""
	play = Give(CONTROLLER, "UNG_057t1") * 2


class UNG_060:
	"""Mimic Pod"""
	play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)))


class UNG_067:
	"""The Caverns Below"""
	events = Play(CONTROLLER, MINION).after(CompleteRogueQuest(SELF, Play.CARD))
	reward = Destroy(SELF), Give(CONTROLLER, "UNG_067t1")


class UNG_067t1:
	play = Buff(CONTROLLER, "UNG_067t1e")


class UNG_067t1e:
	update = Refresh(FRIENDLY + MINION, buff="UNG_067t1e2")


class UNG_067t1e2:
	atk = SET(4)
	max_health = SET(4)


class UNG_823:
	"""Envenom Weapon"""
	play = Buff(FRIENDLY_WEAPON, "UNG_823e")


UNG_823e = buff(poisonous=True)


class UNG_856:
	"""Hallucination"""
	play = DISCOVER(RandomCollectible(card_class=ENEMY_CLASS))


##
# Weapons

class UNG_061:
	"""Obsidian Shard"""
	def Hand(self):
		events = Play(CONTROLLER, -FRIENDLY_CLASS).then(Buff(SELF, "UNG_061e"))


@custom_card
class UNG_061e:
	events = REMOVED_IN_PLAY
	tags = {
		GameTag.CARDNAME: "Obsidian Shard Buff",
		GameTag.COST: -1
	}
