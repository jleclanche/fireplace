from ..utils import *


##
# Druid

class YOD_040:
	"""Steel Beetle"""
	# <b>Battlecry:</b> If you're holding a spell that costs (5) or more, gain 5 Armor.
	powered_up = Find(FRIENDLY_HAND + SPELL + (COST >= 5))
	play = powered_up & GainArmor(FRIENDLY_HERO, 5)


class YOD_001:
	"""Rising Winds"""
	# <b>Twinspell</b> <b>Choose One -</b> Draw a card; or Summon a 3/2_Eagle.
	choose = ("YOD_001b", "YOD_001c")
	play = ChooseBoth(CONTROLLER) & (Draw(CONTROLLER), Summon(CONTROLLER, "YOD_001t"))


class YOD_001b:
	play = Draw(CONTROLLER)


class YOD_001c:
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	play = Summon(CONTROLLER, "YOD_001t")


class YOD_001ts(YOD_001):
	pass


##
# Hunter

class YOD_004:
	"""Chopshop Copter"""
	# After a friendly Mech dies, add a random Mech to your hand.
	events = Death(FRIENDLY + MECH).after(Give(CONTROLLER, RandomMech()))


class YOD_036:
	"""Rotnest Drake"""
	# [x]<b>Battlecry:</b> If you're holding a Dragon, destroy a random enemy minion.
	powered_up = HOLDING_DRAGON
	play = powered_up & Destroy(RANDOM_ENEMY_MINION)


class YOD_005:
	"""Fresh Scent"""
	# <b>Twinspell</b> Give a Beast +2/+2.
	requirements = {
		PlayReq.REQ_TARGET_TO_PLAY: 0,
		PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
	}
	play = Buff(TARGET, "YOD_005e")


class YOD_005ts(YOD_005):
	pass


YOD_005e = buff(+2, +2)


##
# Mage

class YOD_007:
	"""Animated Avalanche"""
	# [x]<b>Battlecry:</b> If you played an Elemental last turn, summon a copy of this.
	powered_up = ELEMENTAL_PLAYED_LAST_TURN
	play = powered_up & Summon(CONTROLLER, ExactCopy(SELF))


class YOD_009:
	"""The Amazing Reno"""
	# <b>Battlecry:</b> Make all minions disappear. <i>*Poof!*</i>
	play = Remove(ALL_MINIONS)


class YOD_009h:
	"""What Does This Do?"""
	# [x]<b>Passive Hero Power</b> At the start of your turn, cast a random spell.
	tags = {enums.PASSIVE_HERO_POWER: True}
	events = OWN_TURN_BEGIN.on(CastSpell(RandomSpell()))


##
# Paladin

class YOD_043:
	"""Scalelord"""
	# <b>Battlecry:</b> Give your Murlocs <b>Divine Shield</b>.
	play = GiveDivineShield(FRIENDLY_MINIONS + MURLOC)


class YOD_012:
	"""Air Raid"""
	# <b>Twinspell</b> Summon two 1/1 Silver_Hand Recruits with <b>Taunt</b>.
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	play = Summon(CONTROLLER, "YOD_012t") * 2


class YOD_012ts(YOD_012):
	pass


##
# Priest

class YOD_013:
	"""Cleric of Scales"""
	# <b>Battlecry:</b> If you're holding a Dragon, <b>Discover</b> a spell from your deck.
	powered_up = HOLDING_DRAGON
	play = powered_up & Choice(
		CONTROLLER, RANDOM(DeDuplicate(FRIENDLY_DECK + SPELL)) * 3
	).then(
		ForceDraw(Choice.CARD)
	)


class YOD_014:
	"""Aeon Reaver"""
	# <b>Battlecry:</b> Deal damage to_a minion equal to its_Attack.
	requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
	play = Hit(TARGET, ATK(SELF))


class YOD_015:
	"""Dark Prophecy"""
	# <b>Discover</b> a 2-Cost minion. Summon it and give it +3 Health.
	play = Discover(CONTROLLER, RandomMinion(cost=2)).then(
		Summon(CONTROLLER, Discover.CARD).then(
			Buff(Summon.CARD, "YOD_015e")
		)
	)


YOD_015e = buff(health=3)


##
# Rogue

class YOD_016:
	"""Skyvateer"""
	# <b>Stealth</b> <b>Deathrattle:</b> Draw a card.
	deathrattle = Draw(CONTROLLER)


class YOD_017:
	"""Shadow Sculptor"""
	# <b>Combo:</b> Draw a card for each card you've played this turn.
	combo = Draw(CONTROLLER) * NUM_CARDS_PLAYED_THIS_TURN


class YOD_018:
	"""Waxmancy"""
	# <b>Discover</b> a <b>Battlecry</b> minion. Reduce its Cost by (2).
	play = Discover(CONTROLLER, RandomMinion(battlecry=True)).then(
		Give(CONTROLLER, Discover.CARD).then(
			Buff(Give.CARD, "YOD_018e")
		)
	)


class YOD_018e:
	tags = {GameTag.COST: -2}
	events = REMOVED_IN_PLAY


##
# Shaman

class YOD_020:
	"""Explosive Evolution"""
	# Transform a minion into a random one that costs (3) more.
	requirements = {
		PlayReq.REQ_MINION_TARGET: 0,
		PlayReq.REQ_TARGET_TO_PLAY: 0,
	}
	play = Evolve(TARGET, 3)


class YOD_041:
	"""Eye of the Storm"""
	# Summon three 5/6 Elementals with <b>Taunt</b>. <b>Overload:</b> (3)
	requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
	play = Summon(CONTROLLER, "YOD_041t") * 3


class YOD_042:
	"""The Fist of Ra-den"""
	# [x]After you cast a spell, summon a <b>Legendary</b> minion of that Cost. Lose 1
	# Durability.
	events = OWN_SPELL_PLAY.after(
		Summon(CONTROLLER, RandomLegendaryMinion(cost=COST(Play.CARD))),
		Hit(SELF, 1)
	)


##
# Warlock

class YOD_026:
	"""Fiendish Servant"""
	# [x]<b>Deathrattle:</b> Give this minion's Attack to a random friendly minion.
	deathrattle = Buff(RANDOM_OTHER_FRIENDLY_MINION, "YOD_026e", atk=ATK(SELF))


@custom_card
class YOD_026e:
	tags = {
		GameTag.CARDNAME: "Fiendish Servant Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
	}


class YOD_027:
	"""Chaos Gazer"""
	# [x]<b>Battlecry:</b> Corrupt a playable card in your opponent's hand. They have 1
	# turn to play it!
	play = Buff(RANDOM(ENEMY_HAND + (COST <= (MANA(OPPONENT) + Number(1)))), "YOD_027e")


class YOD_027e:
	events = REMOVED_IN_PLAY

	class Hand:
		events = OWN_TURN_END.on(Destroy(OWNER))


class YOD_025:
	"""Twisted Knowledge"""
	# <b>Discover</b> 2 Warlock cards.
	play = DISCOVER(RandomCollectible(card_class=CardClass.WARLOCK)) * 2


##
# Warrior

class YOD_022:
	"""Risky Skipper"""
	# After you play a minion, deal 1 damage to all_minions.
	events = Play(CONTROLLER, MINION).after(Hit(ALL_MINIONS, 1))


class YOD_024:
	"""Bomb Wrangler"""
	# Whenever this minion takes damage, summon a_1/1 Boom Bot.
	events = Attack(SELF).on(Summon(CONTROLLER, "GVG_110t"))


class YOD_023:
	"""Boom Squad"""
	# <b>Discover</b> a <b>Lackey</b>, Mech, or Dragon.
	play = GenericChoice(CONTROLLER, [
		RandomLackey(), RandomMech(), RandomDragon()
	])


##
# Neutral

class YOD_028:
	"""Skydiving Instructor"""
	# [x]<b>Battlecry:</b> Summon a 1-Cost minion from your deck.
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST == 1)))


class YOD_029:
	"""Hailbringer"""
	# [x]<b>Battlecry:</b> Summon two 1/1 Ice Shards that <b>Freeze</b>.
	play = Summon(CONTROLLER, "YOD_029t") * 2


class YOD_029t:
	events = Damage(CHARACTER, None, SELF).on(Freeze(Damage.TARGET))


class YOD_030:
	"""Licensed Adventurer"""
	# [x]<b>Battlecry:</b> If you control a <b>Quest</b>, add a Coin to your hand.
	play = Find(FRIENDLY_QUEST) & Give(CONTROLLER, THE_COIN)


class YOD_032:
	"""Frenzied Felwing"""
	# Costs (1) less for each damage dealt to your opponent this turn.
	cost_mod = -DAMAGED_THIS_TURN(ENEMY_HERO)


class YOD_006:
	"""Escaped Manasaber"""
	# [x]<b>Stealth</b> Whenever this attacks, gain 1 Mana Crystal this turn only.
	events = Attack(SELF).on(ManaThisTurn(CONTROLLER, 1))


class YOD_033:
	"""Boompistol Bully"""
	# <b>Battlecry:</b> Enemy <b>Battlecry</b>_cards cost (5)_more next turn.
	play = Buff(OPPONENT, "YOD_033e")


class YOD_033e:
	update = CurrentPlayer(OWNER) & Refresh(ENEMY_HAND + BATTLECRY, {GameTag.COST: +5})
	events = OWN_TURN_BEGIN.on(Destroy(SELF))


class YOD_035:
	"""Grand Lackey Erkh"""
	# After you play a <b>Lackey</b>, add a <b>Lackey</b> to your hand.
	events = Play(CONTROLLER, LACKEY).after(Give(CONTROLLER, RandomLackey()))


class YOD_038:
	"""Sky Gen'ral Kragg"""
	# [x]<b>Taunt</b> <b>Battlecry:</b> If you've played a <b>Quest</b> this game, summon a
	# 4/2 Parrot with <b>Rush</b>.
	powered_up = Find(CARDS_PLAYED_THIS_GAME + QUEST)
	play = powered_up & Summon(CONTROLLER, "YOD_038t")
