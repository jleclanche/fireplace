from ..utils import *


##
# Druid

class YOD_040:
	"""Steel Beetle"""
	# <b>Battlecry:</b> If you're holding a spell that costs (5) or more, gain 5 Armor.
	powered_up = Find(FRIENDLY_HAND + SEPLL + (COST >= 5))
	play = powered_up & GainArmor(FRIENDLY_HERO, 5)


class YOD_001:
	"""Rising Winds"""
	# <b>Twinspell</b> <b>Choose One -</b> Draw a card; or Summon a 3/2_Eagle.
	choose = ("YOD_001a", "YOD_001b")


##
# Hunter

class YOD_004:
	"""Chopshop Copter"""
	# After a friendly Mech dies, add a random Mech to your hand.
	pass


class YOD_036:
	"""Rotnest Drake"""
	# [x]<b>Battlecry:</b> If you're holding a Dragon, destroy a random enemy minion.
	pass


class YOD_005:
	"""Fresh Scent"""
	# <b>Twinspell</b> Give a Beast +2/+2.
	pass


##
# Mage

class YOD_007:
	"""Animated Avalanche"""
	# [x]<b>Battlecry:</b> If you played an Elemental last turn, summon a copy of this.
	pass


class YOD_009:
	"""The Amazing Reno"""
	# <b>Battlecry:</b> Make all minions disappear. <i>*Poof!*</i>
	pass


##
# Paladin

class YOD_043:
	"""Scalelord"""
	# <b>Battlecry:</b> Give your Murlocs <b>Divine Shield</b>.
	pass


class YOD_012:
	"""Air Raid"""
	# <b>Twinspell</b> Summon two 1/1 Silver_Hand Recruits with <b>Taunt</b>.
	pass


##
# Priest

class YOD_013:
	"""Cleric of Scales"""
	# <b>Battlecry:</b> If you're holding a Dragon, <b>Discover</b> a spell from your deck.
	pass


class YOD_014:
	"""Aeon Reaver"""
	# <b>Battlecry:</b> Deal damage to_a minion equal to its_Attack.
	pass


class YOD_015:
	"""Dark Prophecy"""
	# <b>Discover</b> a 2-Cost minion. Summon it and give it +3 Health.
	pass


##
# Rogue

class YOD_016:
	"""Skyvateer"""
	# <b>Stealth</b> <b>Deathrattle:</b> Draw a card.
	pass


class YOD_017:
	"""Shadow Sculptor"""
	# <b>Combo:</b> Draw a card for each card you've played this turn.
	pass


class YOD_018:
	"""Waxmancy"""
	# <b>Discover</b> a <b>Battlecry</b> minion. Reduce its Cost by (2).
	pass


##
# Shaman

class YOD_020:
	"""Explosive Evolution"""
	# Transform a minion into a random one that costs (3) more.
	pass


class YOD_041:
	"""Eye of the Storm"""
	# Summon three 5/6 Elementals with <b>Taunt</b>. <b>Overload:</b> (3)
	pass


class YOD_042:
	"""The Fist of Ra-den"""
	# [x]After you cast a spell, summon a <b>Legendary</b> minion of that Cost. Lose 1
	# Durability.
	pass


##
# Warlock

class YOD_026:
	"""Fiendish Servant"""
	# [x]<b>Deathrattle:</b> Give this minion's Attack to a random friendly minion.
	pass


class YOD_027:
	"""Chaos Gazer"""
	# [x]<b>Battlecry:</b> Corrupt a playable card in your opponent's hand. They have 1
	# turn to play it!
	pass


class YOD_025:
	"""Twisted Knowledge"""
	# <b>Discover</b> 2 Warlock cards.
	pass


##
# Warrior

class YOD_022:
	"""Risky Skipper"""
	# After you play a minion, deal 1 damage to all_minions.
	pass


class YOD_024:
	"""Bomb Wrangler"""
	# Whenever this minion takes damage, summon a_1/1 Boom Bot.
	pass


class YOD_023:
	"""Boom Squad"""
	# <b>Discover</b> a <b>Lackey</b>, Mech, or Dragon.
	pass


##
# Neutral

class YOD_028:
	"""Skydiving Instructor"""
	# [x]<b>Battlecry:</b> Summon a 1-Cost minion from your deck.
	pass


class YOD_029:
	"""Hailbringer"""
	# [x]<b>Battlecry:</b> Summon two 1/1 Ice Shards that <b>Freeze</b>.
	pass


class YOD_030:
	"""Licensed Adventurer"""
	# [x]<b>Battlecry:</b> If you control a <b>Quest</b>, add a Coin to your hand.
	pass


class YOD_032:
	"""Frenzied Felwing"""
	# Costs (1) less for each damage dealt to your opponent this turn.
	pass


class YOD_006:
	"""Escaped Manasaber"""
	# [x]<b>Stealth</b> Whenever this attacks, gain 1 Mana Crystal this turn only.
	pass


class YOD_033:
	"""Boompistol Bully"""
	# <b>Battlecry:</b> Enemy <b>Battlecry</b>_cards cost (5)_more next turn.
	pass


class YOD_035:
	"""Grand Lackey Erkh"""
	# After you play a <b>Lackey</b>, add a <b>Lackey</b> to your hand.
	pass


class YOD_038:
	"""Sky Gen'ral Kragg"""
	# [x]<b>Taunt</b> <b>Battlecry:</b> If you've played a <b>Quest</b> this game, summon a
	# 4/2 Parrot with <b>Rush</b>.
	pass
