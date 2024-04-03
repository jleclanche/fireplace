from ..utils import *


##
# Minions

class DRG_019:
	"""Scion of Ruin"""
	# <b>Rush</b>. <b>Battlecry:</b> If you've <b>Invoked</b> twice, summon 2_copies of
	# this.
	play = INVOKED_TWICE & SummonBothSides(SELF, ExactCopy(SELF))


class DRG_020:
	"""EVIL Quartermaster"""
	# <b>Battlecry:</b> Add a <b>Lackey</b> to your hand. Gain 3 Armor.
	play = Give(CONTROLLER, RandomLackey()), GainArmor(FRIENDLY_HERO, 3)


class DRG_023:
	"""Skybarge"""
	# [x]After you summon a Pirate, deal 2 damage to a random enemy.
	events = Summon(CONTROLLER, PIRATE).after(
		Hit(RANDOM_ENEMY_CHARACTER, 2)
	)


class DRG_024:
	"""Sky Raider"""
	# <b>Battlecry:</b> Add a random Pirate to your hand.
	play = Give(CONTROLLER, RandomMinion(race=Race.PIRATE))


class DRG_026:
	"""Deathwing, Mad Aspect"""
	# <b>Battlecry:</b> Attack ALL other minions.
	def play(self):
		entities = (ALL_MINIONS - SELF - DEAD).eval(self.game.live_entities, self)
		random.shuffle(entities)
		for entity in entities:
			if not self.dead and not entity.dead:
				yield Attack(self, entity)
				yield Deaths()


##
# Spells

class DRG_022:
	"""Ramming Speed"""
	# Force a minion to attack one of its neighbors.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0
	}
	play = Attack(TARGET, RANDOM(TARGET_ADJACENT))


class DRG_249:
	"""Awaken!"""
	# <b>Invoke</b> Galakrond. Deal_$1 damage to all_minions.
	play = INVOKE, Hit(ALL_MINIONS, 1)


class DRG_500:
	"""Molten Breath"""
	# [x]Deal $5 damage to a minion. If you're holding a Dragon, gain 5 Armor.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0
	}
	powered_up = HOLDING_DRAGON
	play = Hit(TARGET, 5), powered_up & GainArmor(FRIENDLY_HERO, 5)


##
# Weapons

class DRG_021:
	"""Ritual Chopper"""
	# <b>Battlecry:</b> <b>Invoke</b> Galakrond.
	play = INVOKE


class DRG_025:
	"""Ancharrr"""
	# After your hero attacks, draw a Pirate from your_deck.
	events = Attack(FRIENDLY_HERO).after(ForceDraw(RANDOM(FRIENDLY_DECK + PIRATE)))


##
# Heros

class DRG_650:
	"""Galakrond, the Unbreakable"""
	# [x]<b>Battlecry:</b> Draw 1 minion. Give it +4/+4. <i>(@)</i>
	progress_total = 2
	play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION)).then(
		Buff(ForceDraw.TARGET, "DRG_650e")
	)
	reward = Find(SELF + FRIENDLY_HERO) | (
		Morph(SELF, "DRG_650t2").then(
			SetAttribute(CONTROLLER, "_galakrond", Morph.CARD),
		)
	)


DRG_650e = buff(+4, +4)


class DRG_650t2:
	"""Galakrond, the Apocalypse"""
	# [x]<b>Battlecry:</b> Draw 2 minions. Give them +4/+4. <i>(@)</i>
	progress_total = 2
	play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION)).then(
		Buff(ForceDraw.TARGET, "DRG_650e2")
	) * 2
	reward = Find(SELF + FRIENDLY_HERO) | (
		Morph(SELF, "DRG_650t3").then(
			SetAttribute(CONTROLLER, "_galakrond", Morph.CARD),
		)
	)


DRG_650e2 = buff(+4, +4)


class DRG_650t3:
	"""Galakrond, Azeroth's End"""
	# [x]<b>Battlecry:</b> Draw 4 minions. Give them +4/+4. Equip a 5/2 Claw.
	play = (
		ForceDraw(RANDOM(FRIENDLY_DECK + MINION)).then(
			Buff(ForceDraw.TARGET, "DRG_650e3")
		) * 4,
		Summon(CONTROLLER, "DRG_238ht")
	)


DRG_650e3 = buff(+4, +4)


class DRG_238p:
	"""Galakrond's Might"""
	# <b>Hero Power</b> Give your hero +3_Attack this turn.
	activate = Buff(FRIENDLY_HERO, "DRG_238t10e")


DRG_238t10e = buff(atk=3)
