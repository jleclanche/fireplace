from ..utils import *


##
# Minions

class DRG_102:
	"""Azure Explorer"""
	# <b>Spell Damage +2</b> <b>Battlecry:</b> <b>Discover</b> a Dragon.
	play = DISCOVER(RandomDragon())


class DRG_104:
	"""Chenvaala"""
	# After you cast three spells in a turn, summon a 5/5_Elemental.
	progress_total = 3
	reward = Summon(CONTROLLER, "DRG_104t2"), ClearProgress(SELF)
	events = (
		Play(CONTROLLER, SPELL).after(AddProgress(SELF, Play.CARD)),
		TURN_BEGIN.on(ClearProgress(SELF))
	)


class DRG_107:
	"""Violet Spellwing"""
	# <b>Deathrattle:</b> Add an 'Arcane Missiles' spell to_your hand.
	deathrattle = Give(CONTROLLER, "EX1_277")


class DRG_109:
	"""Mana Giant"""
	# [x]Costs (1) less for each card you've played this game that didn't start in your
	# deck.
	cost_mod = -Count(CARDS_PLAYED_THIS_GAME - STARTING_DECK)


class DRG_270:
	"""Malygos, Aspect of Magic"""
	# [x]<b>Battlecry:</b> If you're holding a Dragon, <b>Discover</b> an upgraded Mage
	# spell.
	powered_up = HOLDING_DRAGON
	entourage = [
		"DRG_270t1", "DRG_270t2", "DRG_270t4",
		"DRG_270t5", "DRG_270t6", "DRG_270t7",
		"DRG_270t8", "DRG_270t9", "DRG_270t11"]
	play = powered_up & DISCOVER(RandomEntourage())


class DRG_270t1:
	"""Malygos's Intellect"""
	# Draw 4 cards.
	play = Draw(CONTROLLER) * 4


class DRG_270t2:
	"""Malygos's Tome"""
	# Add 3 random Mage spells to your hand.
	play = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE)) * 3


class DRG_270t4:
	"""Malygos's Explosion"""
	# Deal $2 damage to all enemy minions.
	play = Hit(ENEMY_MINIONS, 2)


class DRG_270t5:
	"""Malygos's Nova"""
	# <b>Freeze</b> all enemy minions.
	play = Freeze(ENEMY_MINIONS)


class DRG_270t6:
	"""Malygos's Polymorph"""
	# Transform a minion into a 1/1 Sheep.
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Morph(TARGET, "DRG_270t6t")


class DRG_270t7:
	"""Malygos's Flamestrike"""
	# Deal $8 damage to all enemy minions.
	play = Hit(ENEMY_MINIONS, 8)


class DRG_270t8:
	"""Malygos's Frostbolt"""
	# Deal $3 damage to a_character and <b>Freeze</b> it.
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 3), Freeze(TARGET)


class DRG_270t9:
	"""Malygos's Fireball"""
	# Deal $8 damage.
	requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
	play = Hit(TARGET, 8)


class DRG_270t11:
	"""Malygos's Missiles"""
	# Deal $6 damage randomly split among all enemies.
	play = Hit(RANDOM_ENEMY_CHARACTER, 1) * SPELL_DAMAGE(6)


class DRG_322:
	"""Dragoncaster"""
	# <b>Battlecry:</b> If you're holding a Dragon, your next spell this turn costs (0).
	powered_up = HOLDING_DRAGON
	play = powered_up & Buff(CONTROLLER, "DRG_322e")


class DRG_322e:
	update = Refresh(FRIENDLY_HAND + SPELL, {GameTag.COST: SET(0)})
	events = OWN_SPELL_PLAY.on(Destroy(SELF))


##
# Spells

class DRG_106:
	"""Arcane Breath"""
	# Deal $2 damage to a minion. If you're holding a Dragon, <b>Discover</b> a spell.
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
	powered_up = HOLDING_DRAGON
	play = Hit(TARGET, 2), powered_up & DISCOVER(RandomDragon())


class DRG_321:
	"""Rolling Fireball"""
	# Deal $8 damage to a minion. Any excess damage continues to the left or right.
	requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}

	def play(self):
		class Direction(IntEnum):
			LEFT = 1
			RIGHT = 2

		target = self.target
		left_minion = target.left_minion
		right_minion = target.right_minion
		direction = None
		if left_minion and right_minion:
			direction = random.choice([Direction.LEFT, Direction.RIGHT])
		elif left_minion:
			direction = Direction.LEFT
		elif right_minion:
			direction = Direction.RIGHT
		damage = self.controller.get_spell_damage(8)
		action = HitExcessDamage(target, damage)
		if direction == Direction.LEFT:
			while left_minion:
				action = HitExcessDamage(left_minion[0], action)
				left_minion = left_minion[0].left_minion
		elif direction == Direction.RIGHT:
			while right_minion:
				action = HitExcessDamage(right_minion[0], action)
				right_minion = right_minion[0].right_minion
		yield action
		return


class DRG_323:
	"""Learn Draconic"""
	# [x]<b>Sidequest:</b> Spend 8 Mana on spells. <b>Reward:</b> Summon a 6/6 Dragon.
	progress_total = 8
	sidequest = SpendMana(CONTROLLER, source=SPELL).after(
		AddProgress(SELF, CONTROLLER, SpendMana.AMOUNT)
	)
	reward = Summon(CONTROLLER, "DRG_323t")


class DRG_324:
	"""Elemental Allies"""
	# [x]<b>Sidequest:</b> Play an Elemental 2 turns in a row. <b>Reward:</b> Draw 3 spells
	# from your deck.
	progress_total = 2
	sidequest = (
		Play(CONTROLLER, ELEMENTAL).after(
			Find(CARDS_PLAYED_THIS_TURN + ELEMENTAL - Play.CARD) | AddProgress(SELF, Play.CARD)
		),
		OWN_TURN_END.on(Find(CARDS_PLAYED_THIS_TURN + ELEMENTAL) | ClearProgress(SELF))
	)
	reward = ForceDraw(RANDOM(FRIENDLY_DECK + SPELL)) * 3
