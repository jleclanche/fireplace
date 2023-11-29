from collections import defaultdict

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
	deathrattle = Find(FRIENDLY_MINIONS + SELF) & (
		Morph(SELF, "UNG_065t")
	) | (
		Summon(CONTROLLER, "UNG_065t")
	)


class UNG_065t:
	progress_total = 4
	events = [
		Play(CONTROLLER).after(AddProgress(SELF, Play.CARD)),
		TURN_BEGIN.on(ClearProgress(SELF))
	]
	reward = Morph(SELF, "UNG_065")


##
# Spells

class UNG_057:
	"""Razorpetal Volley"""
	play = Give(CONTROLLER, "UNG_057t1") * 2


class UNG_057t1:
	play = Hit(TARGET, 1)


class UNG_060:
	"""Mimic Pod"""
	play = Draw(CONTROLLER).then(Give(CONTROLLER, Copy(Draw.CARD)))


class UNG_067:
	"""The Caverns Below"""
	progress_total = 5
	quest = Play(CONTROLLER, MINION).after(AddProgress(SELF, Play.CARD))
	reward = Give(CONTROLLER, "UNG_067t1")

	def add_progress(self, card):
		if not hasattr(self, "card_name_counter"):
			self.card_name_counter = defaultdict(int)
		# 炉石简中汉化组一点都不用心
		# 存在部分英文同名但简中不同名的现象
		# * NEW1_040t: Gnoll 豺狼人
		# * OG_318t: Gnoll 腐化豺狼人
		# * TU4a_003: Gnoll 豺狼人
		name = card.data.strings[GameTag.CARDNAME]["enUS"]
		self.card_name_counter[name] += 1


class UNG_067t1:
	play = Buff(CONTROLLER, "UNG_067t1e")


class UNG_067t1e:
	update = Refresh(
		(IN_DECK | IN_HAND | IN_PLAY) + FRIENDLY + MINION,
		buff="UNG_067t1e2"
	)


class UNG_067t1e2:
	atk = SET(5)
	max_health = SET(5)


class UNG_823:
	"""Envenom Weapon"""
	play = SetTag(FRIENDLY_WEAPON, (GameTag.POISONOUS, ))


class UNG_856:
	"""Hallucination"""
	play = Find(ENEMY_HERO - NEUTRAL) & (
		GenericChoice(CONTROLLER, RandomSpell(card_class=ENEMY_CLASS) * 3)
	) | (
		GenericChoice(CONTROLLER, RandomSpell(card_class=CardClass.ROGUE) * 3)
	)


##
# Weapons

class UNG_061:
	"""Obsidian Shard"""
	cost_mod = -Count(CARDS_PLAYED_THIS_GAME + OTHER_CLASS_CHARACTER)
