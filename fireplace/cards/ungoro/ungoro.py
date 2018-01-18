
"""
Card Definitions for Journey to Un'Goro
Part of Fireplace: The Hearthstone simulator in Python
"""

from ..utils import *

###############################################################################
##                                                                           ##
##                                  Neutral                                  ##
##                                                                           ##
###############################################################################

#
# class UNG_001:
# 	"""
# 	Pterrordax Hatchling - (Minion)
# 	Battlecry: Adapt.
# 	https://hearthstone.gamepedia.com/Pterrordax_Hatchling
# 	"""
# 	play = None
#
#
# class UNG_002:
# 	"""
# 	Volcanosaur - (Minion)
# 	Battlecry: Adapt, then_Adapt.
# 	https://hearthstone.gamepedia.com/Volcanosaur
# 	"""
# 	play = None
#
#
# class UNG_009:
# 	"""
# 	Ravasaur Runt - (Minion)
# 	Battlecry: If you control at_least 2 other minions, Adapt.
# 	https://hearthstone.gamepedia.com/Ravasaur_Runt
# 	"""
# 	play = None
#

class UNG_010:
	"""
	Sated Threshadon - (Minion)
	Deathrattle: Summon three 1/1 Murlocs.
	https://hearthstone.gamepedia.com/Sated_Threshadon
	"""
	deathrattle = Summon(CONTROLLER, "UNG_201t") * 3

#
# class UNG_067t1e:
# 	"""
# 	Crystallized - (Enchantment)
# 	Your minions are 5/5.
# 	https://hearthstone.gamepedia.com/Crystallized
# 	"""
# 	pass
#
#
# class UNG_067t1e2:
# 	"""
# 	Crystallized - (Enchantment)
# 	5/5.
# 	https://hearthstone.gamepedia.com/Crystallized
# 	"""
# 	pass
#
#
# class UNG_070:
# 	"""
# 	Tol'vir Stoneshaper - (Minion)
# 	Battlecry: If you played an Elemental last turn, gain _Taunt and Divine_Shield.
# 	https://hearthstone.gamepedia.com/Tol%27vir_Stoneshaper
# 	"""
# 	play = None
#
#
# class UNG_070e:
# 	"""
# 	Stonewall - (Enchantment)
# 	Divine Shield and Taunt.
# 	https://hearthstone.gamepedia.com/Stonewall
# 	"""
# 	pass
#
#
# class UNG_072:
# 	"""
# 	Stonehill Defender - (Minion)
# 	Taunt Battlecry: Discover a Taunt_minion.
# 	https://hearthstone.gamepedia.com/Stonehill_Defender
# 	"""
# 	play = None
#

class UNG_073:
	"""
	Rockpool Hunter - (Minion)
	Battlecry: Give a friendly Murloc +1/+1.
	https://hearthstone.gamepedia.com/Rockpool_Hunter
	"""
	powered_up = Find(FRIENDLY_MINIONS + MURLOC)
	play = Buff(TARGET, "UNG_073e")

UNG_073e = buff(atk=+1, health=+1)

#
# class UNG_075:
# 	"""
# 	Vicious Fledgling - (Minion)
# 	After this minion attacks a_hero, Adapt.
# 	https://hearthstone.gamepedia.com/Vicious_Fledgling
# 	"""
# 	pass
#

class UNG_076:
	"""
	Eggnapper - (Minion)
	Deathrattle: Summon two 1/1 Raptors.
	https://hearthstone.gamepedia.com/Eggnapper
	"""
	deathrattle = Summon(CONTROLLER, "UNG_076t1") * 2


class UNG_079:
	"""
	Frozen Crusher - (Minion)
	After this minion attacks, Freeze it.
	https://hearthstone.gamepedia.com/Frozen_Crusher
	"""
	events = Attack(SELF).on(Freeze(SELF))

#
# class UNG_082:
# 	"""
# 	Thunder Lizard - (Minion)
# 	Battlecry: If you played an_Elemental last turn, Adapt.
# 	https://hearthstone.gamepedia.com/Thunder_Lizard
# 	"""
# 	play = None
#

class UNG_083:
	"""
	Devilsaur Egg - (Minion)
	Deathrattle: Summon a 5/5 Devilsaur.
	https://hearthstone.gamepedia.com/Devilsaur_Egg
	"""
	deathrattle = Summon(CONTROLLER, "EX1_tk29")


class UNG_084:
	"""
	Fire Plume Phoenix - (Minion)
	Battlecry: Deal 2 damage.
	https://hearthstone.gamepedia.com/Fire_Plume_Phoenix
	"""
	play = Hit(TARGET, 2)


class UNG_085:
	"""
	Emerald Hive Queen - (Minion)
	Your minions cost (2) more.
	https://hearthstone.gamepedia.com/Emerald_Hive_Queen
	"""
	update = Refresh(IN_HAND + MINION, {GameTag.COST: +2})


class UNG_087:
	"""
	Bittertide Hydra - (Minion)
	Whenever this minion takes damage, deal 3 damage to_your hero.
	https://hearthstone.gamepedia.com/Bittertide_Hydra
	"""
	events = SELF_DAMAGE.on(Hit(FRIENDLY_HERO, 3))

#
# class UNG_088:
# 	"""
# 	Tortollan Primalist - (Minion)
# 	Battlecry: Discover a spell_and cast it with random targets.
# 	https://hearthstone.gamepedia.com/Tortollan_Primalist
# 	"""
# 	play = None
#
#
# class UNG_089:
# 	"""
# 	Gentle Megasaur - (Minion)
# 	Battlecry: Adapt your_Murlocs.
# 	https://hearthstone.gamepedia.com/Gentle_Megasaur
# 	"""
# 	play = None
#
#
# class UNG_099:
# 	"""
# 	Charged Devilsaur - (Minion)
# 	Charge Battlecry: Can't attack heroes this turn.
# 	https://hearthstone.gamepedia.com/Charged_Devilsaur
# 	"""
# 	play = None
#

class UNG_113:
	"""
	Bright-Eyed Scout - (Minion)
	Battlecry: Draw a card. Change its Cost to (5).
	https://hearthstone.gamepedia.com/Bright-Eyed_Scout
	"""
	play = Draw(CONTROLLER).then(
		Buff(Draw.CARD, "UNG_113e")
	)


class UNG_113e:
	cost = SET(5)

#
# class UNG_202e:
# 	"""
# 	Fiery - (Enchantment)
# 	Costs (1) less.
# 	https://hearthstone.gamepedia.com/Fiery
# 	"""
# 	pass
#

class UNG_205:
	"""
	Glacial Shard - (Minion)
	Battlecry: Freeze an_enemy.
	https://hearthstone.gamepedia.com/Glacial_Shard
	"""
	play = Freeze(TARGET)


class UNG_801:
	"""
	Nesting Roc - (Minion)
	Battlecry: If you control at_least 2 other minions, gain Taunt.
	https://hearthstone.gamepedia.com/Nesting_Roc
	"""
	powered_up = Count(FRIENDLY_MINIONS - SELF) >= 2
	play = powered_up & Taunt(SELF)


class UNG_803:
	"""
	Emerald Reaver - (Minion)
	Battlecry: Deal 1 damage to each hero.
	https://hearthstone.gamepedia.com/Emerald_Reaver
	"""
	play = Hit(FRIENDLY_HERO, 1), Hit(ENEMY_HERO, 1)


class UNG_807:
	"""
	Golakka Crawler - (Minion)
	Battlecry: Destroy a Pirate and gain +1/+1.
	https://hearthstone.gamepedia.com/Golakka_Crawler
	"""
	play = Destroy(TARGET), Buff(SELF, "UNG_807e")

UNG_807e=buff(atk=+1, health=+1)


class UNG_809:
	"""
	Fire Fly - (Minion)
	Battlecry: Add a 1/2 Elemental to your hand.
	https://hearthstone.gamepedia.com/Fire_Fly
	"""
	play = Give(CONTROLLER, "UNG_809t1")

#
# class UNG_816:
# 	"""
# 	Servant of Kalimos - (Minion)
# 	Battlecry: If you played an Elemental last turn, _Discover an Elemental.
# 	https://hearthstone.gamepedia.com/Servant_of_Kalimos
# 	"""
# 	play = None
#

class UNG_818:
	"""
	Volatile Elemental - (Minion)
	Deathrattle: Deal 3 damage to a random enemy minion.
	https://hearthstone.gamepedia.com/Volatile_Elemental
	"""
	deathrattle = Hit(RANDOM_ENEMY_MINION, 3)

#
# class UNG_832e:
# 	"""
# 	Dark Power - (Enchantment)
# 	Your next spell costs Health instead of Mana.
# 	https://hearthstone.gamepedia.com/Dark_Power
# 	"""
# 	pass
#

class UNG_840:
	"""
	Hemet, Jungle Hunter - (Minion)
	Battlecry: Destroy all cards in your deck that cost (3)_or less.
	https://hearthstone.gamepedia.com/Hemet%2C_Jungle_Hunter
	"""
	play = Destroy(FRIENDLY_DECK + (COST <= 3))

#
# class UNG_843:
# 	"""
# 	The Voraxx - (Minion)
# 	After you cast a spell on this minion, summon a 1/1 Plant and cast another copy on it.
# 	https://hearthstone.gamepedia.com/The_Voraxx
# 	"""
# 	pass
#

class UNG_845:
	"""
	Igneous Elemental - (Minion)
	Deathrattle: Add two 1/2 Elementals to your hand.
	https://hearthstone.gamepedia.com/Igneous_Elemental
	"""
	deathrattle = Give(CONTROLLER, "UNG_809t1") * 2

#
# class UNG_847:
# 	"""
# 	Blazecaller - (Minion)
# 	Battlecry: If you played an_Elemental last turn, deal 5 damage.
# 	https://hearthstone.gamepedia.com/Blazecaller
# 	"""
# 	play = None
#

class UNG_848:
	"""
	Primordial Drake - (Minion)
	Taunt Battlecry: Deal 2 damage to all other minions.
	https://hearthstone.gamepedia.com/Primordial_Drake
	"""
	play = Hit(ALL_MINIONS - SELF, 2)


class UNG_851:
	"""
	Elise the Trailblazer - (Minion)
	Battlecry: Shuffle a sealed_Un'Goro pack into_your deck.
	https://hearthstone.gamepedia.com/Elise_the_Trailblazer
	"""
	play = Shuffle(CONTROLLER, "UNG_851t1")

#
# class UNG_851t1:
# 	"""
# 	Un'Goro Pack - (Spell)
# 	Add 5 Journey to Un'Goro cards to your hand.
# 	https://hearthstone.gamepedia.com/Un%27Goro_Pack
# 	"""
# 	pass
#
#
# class UNG_900:
# 	"""
# 	Spiritsinger Umbra - (Minion)
# 	After you summon a minion, trigger its Deathrattle effect.
# 	https://hearthstone.gamepedia.com/Spiritsinger_Umbra
# 	"""
# 	pass
#
#
# class UNG_907:
# 	"""
# 	Ozruk - (Minion)
# 	Taunt Battlecry: Gain +5 Health for each Elemental you played last turn.
# 	https://hearthstone.gamepedia.com/Ozruk
# 	"""
# 	play = None
#
#
# class UNG_907e:
# 	"""
# 	Just Blaze - (Enchantment)
# 	+5 Health
# 	https://hearthstone.gamepedia.com/Just_Blaze
# 	"""
# 	pass
#
#
# class UNG_928:
# 	"""
# 	Tar Creeper - (Minion)
# 	Taunt Has +2 Attack during your opponent's turn.
# 	https://hearthstone.gamepedia.com/Tar_Creeper
# 	"""
# 	pass
#
#
# class UNG_934t2:
# 	"""
# 	DIE, INSECT! - (HeroPower)
# 	Hero Power Deal $8 damage to a random enemy.
# 	https://hearthstone.gamepedia.com/DIE%2C_INSECT%21
# 	"""
# 	pass
#

class UNG_937:
	"""
	Primalfin Lookout - (Minion)
	Battlecry: If you control another Murloc, Discover a_Murloc.
	https://hearthstone.gamepedia.com/Primalfin_Lookout
	"""
	powered_up = Find(FRIENDLY_MINIONS + MURLOC - SELF)
	play = powered_up & Give(CONTROLLER, RandomMurloc())


class UNG_946:
	"""
	Gluttonous Ooze - (Minion)
	Battlecry: Destroy your opponent's weapon and gain Armor equal to its Attack.
	https://hearthstone.gamepedia.com/Gluttonous_Ooze
	"""
	play = (
		GainArmor(FRIENDLY_HERO, 1) * Attr(ENEMY_WEAPON, GameTag.ATK),
		Destroy(ENEMY_WEAPON)
	)

#
# class UNG_999t10:
# 	"""
# 	Shrouding Mist - (Spell)
# 	Stealth until your next turn.
# 	https://hearthstone.gamepedia.com/Shrouding_Mist
# 	"""
# 	pass
#
#
# class UNG_999t10e:
# 	"""
# 	Shrouding Mist - (Enchantment)
# 	Stealthed until your next turn.
# 	https://hearthstone.gamepedia.com/Shrouding_Mist
# 	"""
# 	pass
#
#
# class UNG_999t14:
# 	"""
# 	Volcanic Might - (Spell)
# 	+1/+1
# 	https://hearthstone.gamepedia.com/Volcanic_Might
# 	"""
# 	pass
#
#
# class UNG_999t14e:
# 	"""
# 	Volcanic Might - (Enchantment)
# 	+1/+1.
# 	https://hearthstone.gamepedia.com/Volcanic_Might
# 	"""
# 	pass
#
#
# class UNG_999t2:
# 	"""
# 	Living Spores - (Spell)
# 	Deathrattle: Summon two 1/1 Plants.
# 	https://hearthstone.gamepedia.com/Living_Spores
# 	"""
# 	pass
#
#
# class UNG_999t2e:
# 	"""
# 	Living Spores - (Enchantment)
# 	Deathrattle: Summon two 1/1 Plants.
# 	https://hearthstone.gamepedia.com/Living_Spores
# 	"""
# 	pass
#
#
# class UNG_999t3:
# 	"""
# 	Flaming Claws - (Spell)
# 	+3 Attack
# 	https://hearthstone.gamepedia.com/Flaming_Claws
# 	"""
# 	pass
#
#
# class UNG_999t3e:
# 	"""
# 	Flaming Claws - (Enchantment)
# 	+3 Attack.
# 	https://hearthstone.gamepedia.com/Flaming_Claws
# 	"""
# 	pass
#
#
# class UNG_999t4:
# 	"""
# 	Rocky Carapace - (Spell)
# 	+3 Health
# 	https://hearthstone.gamepedia.com/Rocky_Carapace
# 	"""
# 	pass
#
#
# class UNG_999t4e:
# 	"""
# 	Rocky Carapace - (Enchantment)
# 	+3 Health.
# 	https://hearthstone.gamepedia.com/Rocky_Carapace
# 	"""
# 	pass
#
###############################################################################
##                                                                           ##
##                                  Warrior                                  ##
##                                                                           ##
###############################################################################

#
# class UNG_838:
# 	"""
# 	Tar Lord - (Minion)
# 	Taunt Has +4 Attack during your opponent’s turn.
# 	https://hearthstone.gamepedia.com/Tar_Lord
# 	"""
# 	pass
#
#
# class UNG_922:
# 	"""
# 	Explore Un'Goro - (Spell)
# 	Replace your deck with_copies of "Discover a card."
# 	https://hearthstone.gamepedia.com/Explore_Un%27Goro
# 	"""
# 	pass
#
#
# class UNG_922t1:
# 	"""
# 	Choose Your Path - (Spell)
# 	Discover a card.
# 	https://hearthstone.gamepedia.com/Choose_Your_Path
# 	"""
# 	pass
#
#
# class UNG_923:
# 	"""
# 	Iron Hide - (Spell)
# 	Gain 5 Armor.
# 	https://hearthstone.gamepedia.com/Iron_Hide
# 	"""
# 	pass
#
#
# class UNG_925:
# 	"""
# 	Ornery Direhorn - (Minion)
# 	Taunt Battlecry: Adapt.
# 	https://hearthstone.gamepedia.com/Ornery_Direhorn
# 	"""
# 	play = None
#
#
# class UNG_926:
# 	"""
# 	Cornered Sentry - (Minion)
# 	Taunt. Battlecry: Summon three 1/1 Raptors for your_opponent.
# 	https://hearthstone.gamepedia.com/Cornered_Sentry
# 	"""
# 	play = None
#
#
# class UNG_927:
# 	"""
# 	Sudden Genesis - (Spell)
# 	Summon copies of your damaged minions.
# 	https://hearthstone.gamepedia.com/Sudden_Genesis
# 	"""
# 	pass
#
#
# class UNG_929:
# 	"""
# 	Molten Blade - (Weapon)
# 	Each turn this is in your hand, transform it into a new weapon.
# 	https://hearthstone.gamepedia.com/Molten_Blade
# 	"""
# 	pass
#
#
# class UNG_929e:
# 	"""
# 	Magmic - (Enchantment)
# 	Transforming into random weapons.
# 	https://hearthstone.gamepedia.com/Magmic
# 	"""
# 	pass
#
#
# class UNG_933:
# 	"""
# 	King Mosh - (Minion)
# 	Battlecry: Destroy all damaged minions.
# 	https://hearthstone.gamepedia.com/King_Mosh
# 	"""
# 	play = None
#
#
# class UNG_934:
# 	"""
# 	Fire Plume's Heart - (Spell)
# 	Quest: Play 7 Taunt minions. Reward: Sulfuras.
# 	https://hearthstone.gamepedia.com/Fire_Plume%27s_Heart
# 	"""
# 	pass
#
#
# class UNG_934t1:
# 	"""
# 	Sulfuras - (Weapon)
# 	Battlecry: Your Hero Power becomes 'Deal 8_damage to a random enemy.'
# 	https://hearthstone.gamepedia.com/Sulfuras
# 	"""
# 	play = None


class UNG_957:
	"""
	Direhorn Hatchling - (Minion)
	Taunt Deathrattle: Shuffle a 6/9 Direhorn with Taunt into your deck.
	https://hearthstone.gamepedia.com/Direhorn_Hatchling
	"""
	deathrattle = Shuffle(CONTROLLER, "UNG_957t1")

###############################################################################
##                                                                           ##
##                                  Warlock                                  ##
##                                                                           ##
###############################################################################

#
# class UNG_047:
# 	"""
# 	Ravenous Pterrordax - (Minion)
# 	Battlecry: Destroy a friendly minion to Adapt_twice.
# 	https://hearthstone.gamepedia.com/Ravenous_Pterrordax
# 	"""
# 	play = None
#
#
# class UNG_049:
# 	"""
# 	Tar Lurker - (Minion)
# 	Taunt Has +3 Attack during your opponent's turn.
# 	https://hearthstone.gamepedia.com/Tar_Lurker
# 	"""
# 	pass
#
#
# class UNG_829:
# 	"""
# 	Lakkari Sacrifice - (Spell)
# 	Quest: Discard 6 cards. Reward: Nether Portal.
# 	https://hearthstone.gamepedia.com/Lakkari_Sacrifice
# 	"""
# 	pass
#
#
# class UNG_829t1:
# 	"""
# 	Nether Portal - (Spell)
# 	Open a permanent portal that summons 3/2 Imps.
# 	https://hearthstone.gamepedia.com/Nether_Portal
# 	"""
# 	pass
#
#
# class UNG_829t2:
# 	"""
# 	Nether Portal - (Minion)
# 	At the end of your turn, summon two 3/2 Imps.
# 	https://hearthstone.gamepedia.com/Nether_Portal
# 	"""
# 	pass
#
#
# class UNG_830:
# 	"""
# 	Cruel Dinomancer - (Minion)
# 	Deathrattle: Summon a random minion you discarded this game.
# 	https://hearthstone.gamepedia.com/Cruel_Dinomancer
# 	"""
# 	deathrattle = None
#
#
# class UNG_831:
# 	"""
# 	Corrupting Mist - (Spell)
# 	Corrupt every minion. Destroy them at the start of your next turn.
# 	https://hearthstone.gamepedia.com/Corrupting_Mist
# 	"""
# 	pass
#
#
# class UNG_831e:
# 	"""
# 	Corrupting Mist - (Enchantment)
# 	At the start of the corrupting player's turn, destroy this minion.
# 	https://hearthstone.gamepedia.com/Corrupting_Mist
# 	"""
# 	pass


class UNG_832:
	"""
	Bloodbloom - (Spell)
	The next spell you cast this turn costs Health instead of Mana.
	https://hearthstone.gamepedia.com/Bloodbloom
	"""
	play = Buff(CONTROLLER, "UNG_832e")


class UNG_832e:
	events = OWN_SPELL_PLAY.on(Destroy(SELF))
	update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})


# class UNG_833:
# 	"""
# 	Lakkari Felhound - (Minion)
# 	Taunt Battlecry: Discard two random cards.
# 	https://hearthstone.gamepedia.com/Lakkari_Felhound
# 	"""
# 	play = None
#
#
# class UNG_834:
# 	"""
# 	Feeding Time - (Spell)
# 	Deal $3 damage to a minion. Summon three 1/1 Pterrordaxes.
# 	https://hearthstone.gamepedia.com/Feeding_Time
# 	"""
# 	pass
#
#
# class UNG_835:
# 	"""
# 	Chittering Tunneler - (Minion)
# 	Battlecry: Discover a spell. Deal damage to your hero equal to its Cost.
# 	https://hearthstone.gamepedia.com/Chittering_Tunneler
# 	"""
# 	play = None
#
#
# class UNG_836:
# 	"""
# 	Clutchmother Zavas - (Minion)
# 	Whenever you discard this, give it +2/+2 and return it to your hand.
# 	https://hearthstone.gamepedia.com/Clutchmother_Zavas
# 	"""
# 	pass
#
#
# class UNG_836e:
# 	"""
# 	Remembrance - (Enchantment)
# 	+2/+2 each time this is discarded.
# 	https://hearthstone.gamepedia.com/Remembrance
# 	"""
# 	pass
#
###############################################################################
##                                                                           ##
##                                  Shaman                                   ##
##                                                                           ##
###############################################################################

#
# class UNG_025:
# 	"""
# 	Volcano - (Spell)
# 	Deal $15 damage randomly split among all_minions. Overload: (2)
# 	https://hearthstone.gamepedia.com/Volcano
# 	"""
# 	pass
#
#
# class UNG_201:
# 	"""
# 	Primalfin Totem - (Minion)
# 	At the end of your turn, summon a 1/1 Murloc.
# 	https://hearthstone.gamepedia.com/Primalfin_Totem
# 	"""
# 	pass
#
#
# class UNG_202:
# 	"""
# 	Fire Plume Harbinger - (Minion)
# 	Battlecry: Reduce the Cost of Elementals in your hand_by (1).
# 	https://hearthstone.gamepedia.com/Fire_Plume_Harbinger
# 	"""
# 	play = None
#
#
# class UNG_208:
# 	"""
# 	Stone Sentinel - (Minion)
# 	Battlecry: If you played an Elemental last turn, summon two 2/3 Elementals with Taunt.
# 	https://hearthstone.gamepedia.com/Stone_Sentinel
# 	"""
# 	play = None
#
#
# class UNG_211:
# 	"""
# 	Kalimos, Primal Lord - (Minion)
# 	Battlecry: If you played an Elemental last turn, cast an Elemental Invocation.
# 	https://hearthstone.gamepedia.com/Kalimos%2C_Primal_Lord
# 	"""
# 	play = None
#
#
# class UNG_211a:
# 	"""
# 	Invocation of Earth - (Spell)
# 	Fill your board with 1/1 Elementals.
# 	https://hearthstone.gamepedia.com/Invocation_of_Earth
# 	"""
# 	pass
#
#
# class UNG_211b:
# 	"""
# 	Invocation of Water - (Spell)
# 	Restore 12 Health to your hero.
# 	https://hearthstone.gamepedia.com/Invocation_of_Water
# 	"""
# 	pass
#
#
# class UNG_211c:
# 	"""
# 	Invocation of Fire - (Spell)
# 	Deal 6 damage to the enemy hero.
# 	https://hearthstone.gamepedia.com/Invocation_of_Fire
# 	"""
# 	pass
#
#
# class UNG_211d:
# 	"""
# 	Invocation of Air - (Spell)
# 	Deal 3 damage to all enemy minions.
# 	https://hearthstone.gamepedia.com/Invocation_of_Air
# 	"""
# 	pass
#
#
# class UNG_817:
# 	"""
# 	Tidal Surge - (Spell)
# 	Deal $4 damage to a minion. Restore #4 Health to your hero.
# 	https://hearthstone.gamepedia.com/Tidal_Surge
# 	"""
# 	pass
#
#
# class UNG_938:
# 	"""
# 	Hot Spring Guardian - (Minion)
# 	Taunt Battlecry: Restore 3_Health.
# 	https://hearthstone.gamepedia.com/Hot_Spring_Guardian
# 	"""
# 	play = None
#
#
# class UNG_942:
# 	"""
# 	Unite the Murlocs - (Spell)
# 	Quest: Summon 10 Murlocs. Reward: Megafin.
# 	https://hearthstone.gamepedia.com/Unite_the_Murlocs
# 	"""
# 	pass
#
#
# class UNG_942t:
# 	"""
# 	Megafin - (Minion)
# 	Battlecry: Fill your hand with random Murlocs.
# 	https://hearthstone.gamepedia.com/Megafin
# 	"""
# 	play = None
#
#
# class UNG_956:
# 	"""
# 	Spirit Echo - (Spell)
# 	Give your minions "Deathrattle: Return _this to your hand."
# 	https://hearthstone.gamepedia.com/Spirit_Echo
# 	"""
# 	pass
#
#
# class UNG_956e:
# 	"""
# 	Echoed Spirit - (Enchantment)
# 	Deathrattle: Return to your hand.
# 	https://hearthstone.gamepedia.com/Echoed_Spirit
# 	"""
# 	pass
#
###############################################################################
##                                                                           ##
##                                   Rogue                                   ##
##                                                                           ##
###############################################################################


class UNG_057:
	"""
	Razorpetal Volley - (Spell)
	Add two Razorpetals to_your hand that deal_1 damage.
	https://hearthstone.gamepedia.com/Razorpetal_Volley
	"""
	play = Give(CONTROLLER, "UNG_057t1") * 2



class UNG_057t1:
	"""
	Razorpetal - (Spell)
	Deal $1 damage.
	https://hearthstone.gamepedia.com/Razorpetal
	"""
	play = Hit(TARGET, 1)


class UNG_058:
	"""
	Razorpetal Lasher - (Minion)
	Battlecry: Add a Razorpetal to your hand that deals 1 damage.
	https://hearthstone.gamepedia.com/Razorpetal_Lasher
	"""
	play = Give(CONTROLLER, "UNG_057t1")

##
# Spells

#
# class UNG_060:
# 	"""
# 	Mimic Pod - (Spell)
# 	Draw a card, then add a copy of it to your hand.
# 	https://hearthstone.gamepedia.com/Mimic_Pod
# 	"""
# 	pass
#
#
# class UNG_061:
# 	"""
# 	Obsidian Shard - (Weapon)
# 	Costs (1) less for each card you've played from another class.
# 	https://hearthstone.gamepedia.com/Obsidian_Shard
# 	"""
# 	pass


class UNG_063:
	"""
	Biteweed - (Minion)
	Combo: Gain +1/+1 for each other card you've played this turn.
	https://hearthstone.gamepedia.com/Biteweed
	"""
	combo = Buff(SELF, "UNG_063e") * Attr(CONTROLLER, GameTag.NUM_CARDS_PLAYED_THIS_TURN)

UNG_063e = buff(+1, +1)


# class UNG_063e:
# 	"""
# 	Sprout - (Enchantment)
# 	Increased stats.
# 	https://hearthstone.gamepedia.com/Sprout
# 	"""
# 	pass
#
#
# class UNG_064:
# 	"""
# 	Vilespine Slayer - (Minion)
# 	Combo: Destroy a minion.
# 	https://hearthstone.gamepedia.com/Vilespine_Slayer
# 	"""
# 	pass
#
#
# class UNG_065:
# 	"""
# 	Sherazin, Corpse Flower - (Minion)
# 	Deathrattle: Go dormant. Play 4 cards in a turn to revive this minion.
# 	https://hearthstone.gamepedia.com/Sherazin%2C_Corpse_Flower
# 	"""
# 	deathrattle = None
#
#
# class UNG_065t:
# 	"""
# 	Sherazin, Seed - (Minion)
# 	When you play 4 cards in a_turn, revive this minion.
# 	https://hearthstone.gamepedia.com/Sherazin%2C_Seed
# 	"""
# 	pass
#
#
# class UNG_067:
# 	"""
# 	The Caverns Below - (Spell)
# 	Quest: Play five minions with the same name. Reward: Crystal Core.
# 	https://hearthstone.gamepedia.com/The_Caverns_Below
# 	"""
# 	pass
#
#
# class UNG_067t1:
# 	"""
# 	Crystal Core - (Spell)
# 	For the rest of the game, your minions are 5/5.
# 	https://hearthstone.gamepedia.com/Crystal_Core
# 	"""
# 	pass
#
#
# class UNG_823:
# 	"""
# 	Envenom Weapon - (Spell)
# 	Give your weapon Poisonous.
# 	https://hearthstone.gamepedia.com/Envenom_Weapon
# 	"""
# 	pass
#
#
# class UNG_856:
# 	"""
# 	Hallucination - (Spell)
# 	Discover a card from your opponent's class.
# 	https://hearthstone.gamepedia.com/Hallucination
# 	"""
# 	pass
#
###############################################################################
##                                                                           ##
##                                  Priest                                   ##
##                                                                           ##
###############################################################################

#
# class UNG_022:
# 	"""
# 	Mirage Caller - (Minion)
# 	Battlecry: Choose a friendly minion. Summon a 1/1 copy of it.
# 	https://hearthstone.gamepedia.com/Mirage_Caller
# 	"""
# 	play = None
#
#
# class UNG_022e:
# 	"""
# 	Mirage - (Enchantment)
# 	1/1.
# 	https://hearthstone.gamepedia.com/Mirage
# 	"""
# 	pass
#
#
# class UNG_029:
# 	"""
# 	Shadow Visions - (Spell)
# 	Discover a copy of a spell in your deck.
# 	https://hearthstone.gamepedia.com/Shadow_Visions
# 	"""
# 	pass
#
#
# class UNG_030:
# 	"""
# 	Binding Heal - (Spell)
# 	Restore #5 Health to a minion and your hero.
# 	https://hearthstone.gamepedia.com/Binding_Heal
# 	"""
# 	pass
#
#
class UNG_032:
	"""
	Crystalline Oracle - (Minion)
	Deathrattle: Copy a card from your opponent's deck _and add it to your hand.
	https://hearthstone.gamepedia.com/Crystalline_Oracle
	"""
	deathrattle = Give(CONTROLLER, Copy(RANDOM(ENEMY_DECK)))


# class UNG_034:
# 	"""
# 	Radiant Elemental - (Minion)
# 	Your spells cost (1) less.
# 	https://hearthstone.gamepedia.com/Radiant_Elemental
# 	"""
# 	pass
#
#
# class UNG_035:
# 	"""
# 	Curious Glimmerroot - (Minion)
# 	Battlecry: Look at 3 cards. Guess which one started in your opponent's deck to get a copy of it.
# 	https://hearthstone.gamepedia.com/Curious_Glimmerroot
# 	"""
# 	play = None
#
#
# class UNG_037:
# 	"""
# 	Tortollan Shellraiser - (Minion)
# 	Taunt Deathrattle: Give a random _friendly minion +1/+1.
# 	https://hearthstone.gamepedia.com/Tortollan_Shellraiser
# 	"""
# 	deathrattle = None
#
#
# class UNG_037e:
# 	"""
# 	Shellshield - (Enchantment)
# 	+1/+1.
# 	https://hearthstone.gamepedia.com/Shellshield
# 	"""
# 	pass
#
#
# class UNG_854:
# 	"""
# 	Free From Amber - (Spell)
# 	Discover a minion that costs (8) or more. Summon it.
# 	https://hearthstone.gamepedia.com/Free_From_Amber
# 	"""
# 	pass
#
#
# class UNG_940:
# 	"""
# 	Awaken the Makers - (Spell)
# 	Quest: Summon 7 Deathrattle minions. Reward: Amara, Warden of Hope.
# 	https://hearthstone.gamepedia.com/Awaken_the_Makers
# 	"""
# 	pass
#
#
# class UNG_940t8:
# 	"""
# 	Amara, Warden of Hope - (Minion)
# 	Taunt Battlecry: Set your hero's Health to 40.
# 	https://hearthstone.gamepedia.com/Amara%2C_Warden_of_Hope
# 	"""
# 	play = None
#
#
class UNG_963:
	"""
	Lyra the Sunshard - (Minion)
	Whenever you cast a spell, add a random Priest spell to your hand.
	https://hearthstone.gamepedia.com/Lyra_the_Sunshard
	"""
	events = OWN_SPELL_PLAY.on(Give(CONTROLLER, RandomSpell(card_class=CardClass.PRIEST)))

###############################################################################
##                                                                           ##
##                                  Paladin                                  ##
##                                                                           ##
###############################################################################

#
# class UNG_004:
# 	"""
# 	Dinosize - (Spell)
# 	Set a minion's Attack and Health to 10.
# 	https://hearthstone.gamepedia.com/Dinosize
# 	"""
# 	pass
#
#
# class UNG_004e:
# 	"""
# 	RAAAAR! - (Enchantment)
# 	Stats changed to 10/10.
# 	https://hearthstone.gamepedia.com/RAAAAR%21
# 	"""
# 	pass
#
#
# class UNG_011:
# 	"""
# 	Hydrologist - (Minion)
# 	Battlecry: Discover a Secret.
# 	https://hearthstone.gamepedia.com/Hydrologist
# 	"""
# 	play = None
#
#
# class UNG_015:
# 	"""
# 	Sunkeeper Tarim - (Minion)
# 	Taunt Battlecry: Set all other minions' Attack and Health to 3.
# 	https://hearthstone.gamepedia.com/Sunkeeper_Tarim
# 	"""
# 	play = None
#
#
# class UNG_015e:
# 	"""
# 	Watched - (Enchantment)
# 	Stats changed to 3/3.
# 	https://hearthstone.gamepedia.com/Watched
# 	"""
# 	pass
#
#
# class UNG_950:
# 	"""
# 	Vinecleaver - (Weapon)
# 	After your hero attacks, summon two 1/1 Silver Hand Recruits.
# 	https://hearthstone.gamepedia.com/Vinecleaver
# 	"""
# 	pass
#
#
# class UNG_952:
# 	"""
# 	Spikeridged Steed - (Spell)
# 	Give a minion +2/+6 and Taunt. When it dies, summon a Stegodon.
# 	https://hearthstone.gamepedia.com/Spikeridged_Steed
# 	"""
# 	pass
#
#
# class UNG_952e:
# 	"""
# 	On a Stegodon - (Enchantment)
# 	+2/+6 and Taunt. Deathrattle: Summon a Stegodon.
# 	https://hearthstone.gamepedia.com/On_a_Stegodon
# 	"""
# 	pass
#
#
# class UNG_953:
# 	"""
# 	Primalfin Champion - (Minion)
# 	Deathrattle: Return any spells you cast on this minion to your hand.
# 	https://hearthstone.gamepedia.com/Primalfin_Champion
# 	"""
# 	deathrattle = None
#
#
# class UNG_953e:
# 	"""
# 	Inspired - (Enchantment)
# 	Storing spell.
# 	https://hearthstone.gamepedia.com/Inspired
# 	"""
# 	pass
#
#
# class UNG_954:
# 	"""
# 	The Last Kaleidosaur - (Spell)
# 	Quest: Cast 6 spells on your minions. Reward: Galvadon.
# 	https://hearthstone.gamepedia.com/The_Last_Kaleidosaur
# 	"""
# 	pass
#
#
# class UNG_954t1:
# 	"""
# 	Galvadon - (Minion)
# 	Battlecry: Adapt 5 times.
# 	https://hearthstone.gamepedia.com/Galvadon
# 	"""
# 	play = None
#
#
# class UNG_960:
# 	"""
# 	Lost in the Jungle - (Spell)
# 	Summon two 1/1 Silver Hand Recruits.
# 	https://hearthstone.gamepedia.com/Lost_in_the_Jungle
# 	"""
# 	pass
#
#
# class UNG_961:
# 	"""
# 	Adaptation - (Spell)
# 	Adapt a friendly minion.
# 	https://hearthstone.gamepedia.com/Adaptation
# 	"""
# 	pass
#
#
# class UNG_962:
# 	"""
# 	Lightfused Stegodon - (Minion)
# 	Battlecry: Adapt your Silver_Hand Recruits.
# 	https://hearthstone.gamepedia.com/Lightfused_Stegodon
# 	"""
# 	play = None
#
###############################################################################
##                                                                           ##
##                                   Mage                                    ##
##                                                                           ##
###############################################################################

#
# class UNG_018:
# 	"""
# 	Flame Geyser - (Spell)
# 	Deal $2 damage. Add a 1/2 Elemental to_your hand.
# 	https://hearthstone.gamepedia.com/Flame_Geyser
# 	"""
# 	pass
#
#
# class UNG_020:
# 	"""
# 	Arcanologist - (Minion)
# 	Battlecry: Draw a Secret from your deck.
# 	https://hearthstone.gamepedia.com/Arcanologist
# 	"""
# 	play = None
#
#
# class UNG_021:
# 	"""
# 	Steam Surger - (Minion)
# 	Battlecry: If you played an Elemental last turn, add a 'Flame Geyser' to your hand.
# 	https://hearthstone.gamepedia.com/Steam_Surger
# 	"""
# 	play = None


class UNG_024:
	"""
	Mana Bind - (Spell)
	Secret: When your opponent casts a spell, add a copy to your hand that costs (0).
	https://hearthstone.gamepedia.com/Mana_Bind
	"""
	secret = Play(ENEMY, SPELL).on(Give(CONTROLLER, Copy(Play.CARD)).then(Buff(Give.CARD, "UNG_024e")))

@custom_card
class UNG_024e:
	tags = {
		GameTag.CARDNAME: "Mana Bind Buff",
		GameTag.CARDTYPE: CardType.ENCHANTMENT,
	}
	cost = SET(0)
	events = REMOVED_IN_PLAY


# class UNG_027:
# 	"""
# 	Pyros - (Minion)
# 	Deathrattle: Return this to_your hand as a 6/6 that costs (6).
# 	https://hearthstone.gamepedia.com/Pyros
# 	"""
# 	deathrattle = None
#
#
# class UNG_027t2:
# 	"""
# 	Pyros - (Minion)
# 	Deathrattle: Return this to_your hand as a 10/10 that costs (10).
# 	https://hearthstone.gamepedia.com/Pyros
# 	"""
# 	deathrattle = None
#
#
# class UNG_028:
# 	"""
# 	Open the Waygate - (Spell)
# 	Quest: Cast 6 spells that didn't start in your deck. Reward: Time Warp.
# 	https://hearthstone.gamepedia.com/Open_the_Waygate
# 	"""
# 	pass
#
#
# class UNG_028e:
# 	"""
# 	Insightful - (Enchantment)
# 	Take an extra turn.
# 	https://hearthstone.gamepedia.com/Insightful
# 	"""
# 	pass
#
#
# class UNG_028t:
# 	"""
# 	Time Warp - (Spell)
# 	Take an extra turn.
# 	https://hearthstone.gamepedia.com/Time_Warp
# 	"""
# 	pass
#
#
# class UNG_846:
# 	"""
# 	Shimmering Tempest - (Minion)
# 	Deathrattle: Add a random Mage spell to your hand.
# 	https://hearthstone.gamepedia.com/Shimmering_Tempest
# 	"""
# 	deathrattle = None
#
#
# class UNG_941:
# 	"""
# 	Primordial Glyph - (Spell)
# 	Discover a spell. Reduce its Cost by (2).
# 	https://hearthstone.gamepedia.com/Primordial_Glyph
# 	"""
# 	pass
#
#
# class UNG_941e:
# 	"""
# 	Primal Magic - (Enchantment)
# 	Cost reduced.
# 	https://hearthstone.gamepedia.com/Primal_Magic
# 	"""
# 	pass


class UNG_948:
	"""
	Molten Reflection - (Spell)
	Choose a friendly minion. Summon a copy of it.
	https://hearthstone.gamepedia.com/Molten_Reflection
	"""
	play = Summon(CONTROLLER, ExactCopy(TARGET))


# class UNG_955:
# 	"""
# 	Meteor - (Spell)
# 	Deal $15 damage to a minion and $3 damage to adjacent ones.
# 	https://hearthstone.gamepedia.com/Meteor
# 	"""
# 	pass
#
###############################################################################
##                                                                           ##
##                                  Hunter                                   ##
##                                                                           ##
###############################################################################


class UNG_800:
	"""
	Terrorscale Stalker - (Minion)
	Battlecry: Trigger a friendly minion's Deathrattle.
	https://hearthstone.gamepedia.com/Terrorscale_Stalker
	"""
	play = Deathrattle(TARGET)


class UNG_910:
	"""
	Grievous Bite - (Spell)
	Deal $2 damage to a minion and $1 damage to adjacent ones.
	https://hearthstone.gamepedia.com/Grievous_Bite
	"""
	play = Hit(TARGET, 2), Hit(TARGET_ADJACENT, 1)


class UNG_912:
	"""
	Jeweled Macaw - (Minion)
	Battlecry: Add a random Beast to your hand.
	https://hearthstone.gamepedia.com/Jeweled_Macaw
	"""
	play = Give(CONTROLLER, RandomBeast())


class UNG_913:
	"""
	Tol'vir Warden - (Minion)
	Battlecry: Draw two 1-Cost minions from your deck.
	https://hearthstone.gamepedia.com/Tol%27vir_Warden
	"""
	play = ForceDraw( RANDOM(FRIENDLY_DECK + MINION + (COST == 1)) ) * 2


class UNG_914:
	"""
	Raptor Hatchling - (Minion)
	Deathrattle: Shuffle a 4/3 Raptor into your deck.
	https://hearthstone.gamepedia.com/Raptor_Hatchling
	"""
	deathrattle = Shuffle(CONTROLLER, "UNG_914t1")

#
# class UNG_915:
# 	"""
# 	Crackling Razormaw - (Minion)
# 	Battlecry: Adapt a friendly_Beast.
# 	https://hearthstone.gamepedia.com/Crackling_Razormaw
# 	"""
# 	play = None
#

class UNG_916:
	"""
	Stampede - (Spell)
	Each time you play a Beast this turn, add_a_random Beast to_your hand.
	https://hearthstone.gamepedia.com/Stampede
	"""
	play = Buff(CONTROLLER, "UNG_916e")


class UNG_916e:
	events = Play(CONTROLLER, FRIENDLY_MINIONS + BEAST).after(
		Give(CONTROLLER, RandomBeast())
	)


class UNG_917:
	"""
	Dinomancy - (Spell)
	Your Hero Power becomes 'Give a Beast +2/+2.'
	https://hearthstone.gamepedia.com/Dinomancy
	"""
	play = Switch(FRIENDLY_HERO_POWER, {
		None: Summon(CONTROLLER, "UNG_917t1"),
	})


class UNG_917t1:
	"""
	Dinomancy - (HeroPower)
	Hero Power Give a Beast +2/+2.
	https://hearthstone.gamepedia.com/Dinomancy
	"""
	activate = Buff(TARGET, "UNG_917e")

UNG_917e = buff(+2, +2)


#
# class UNG_919:
# 	"""
# 	Swamp King Dred - (Minion)
# 	After your opponent plays a minion, attack_it.
# 	https://hearthstone.gamepedia.com/Swamp_King_Dred
# 	"""
# 	pass
#
#
# class UNG_920:
# 	"""
# 	The Marsh Queen - (Spell)
# 	Quest: Play seven 1-Cost minions. Reward: Queen Carnassa.
# 	https://hearthstone.gamepedia.com/The_Marsh_Queen
# 	"""
# 	pass
#
#
# class UNG_920t1:
# 	"""
# 	Queen Carnassa - (Minion)
# 	Battlecry: Shuffle 15 Raptors into your deck.
# 	https://hearthstone.gamepedia.com/Queen_Carnassa
# 	"""
# 	play = None
#
#
# class UNG_920t2:
# 	"""
# 	Carnassa's Brood - (Minion)
# 	Battlecry: Draw a card.
# 	https://hearthstone.gamepedia.com/Carnassa%27s_Brood
# 	"""
# 	play = None
#
###############################################################################
##                                                                           ##
##                                   Druid                                   ##
##                                                                           ##
###############################################################################

#
# class UNG_078:
# 	"""
# 	Tortollan Forager - (Minion)
# 	Battlecry: Add a random minion with 5 or more Attack to your hand.
# 	https://hearthstone.gamepedia.com/Tortollan_Forager
# 	"""
# 	play = None
#

class UNG_086:
	"""
	Giant Anaconda - (Minion)
	Deathrattle: Summon a minion from your hand with 5 or more Attack.
	https://hearthstone.gamepedia.com/Giant_Anaconda
	"""
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION + (ATK >= 5)))

#
# class UNG_100:
# 	"""
# 	Verdant Longneck - (Minion)
# 	Battlecry: Adapt.
# 	https://hearthstone.gamepedia.com/Verdant_Longneck
# 	"""
# 	play = None
#

class UNG_101:
	"""
	Shellshifter - (Minion)
	Choose One - Transform into a 5/3 with Stealth; or a 3/5 with Taunt.
	https://hearthstone.gamepedia.com/Shellshifter
	"""
	choose = ("UNG_101a", "UNG_101b")

#
# class UNG_103:
# 	"""
# 	Evolving Spores - (Spell)
# 	Adapt your minions.
# 	https://hearthstone.gamepedia.com/Evolving_Spores
# 	"""
# 	pass
#

class UNG_108:
	"""
	Earthen Scales - (Spell)
	Give a friendly minion +1/+1, then gain Armor equal to its Attack.
	https://hearthstone.gamepedia.com/Earthen_Scales
	"""
	play = Buff(TARGET, "UNG_108e"), GainArmor(FRIENDLY_HERO, ATK(TARGET))

UNG_108e = buff(+1, +1)

#
# class UNG_109:
# 	"""
# 	Elder Longneck - (Minion)
# 	Battlecry: If you're holding a minion with 5 or more Attack, Adapt.
# 	https://hearthstone.gamepedia.com/Elder_Longneck
# 	"""
# 	play = None
#
#
# class UNG_111:
# 	"""
# 	Living Mana - (Spell)
# 	Transform your Mana Crystals into 2/2 minions. Recover the mana when they die.
# 	https://hearthstone.gamepedia.com/Living_Mana
# 	"""
# 	pass
#
#
# class UNG_116:
# 	"""
# 	Jungle Giants - (Spell)
# 	Quest: Summon 5 minions with 5 or more Attack. Reward: Barnabus.
# 	https://hearthstone.gamepedia.com/Jungle_Giants
# 	"""
# 	pass
#
#
# class UNG_116t:
# 	"""
# 	Barnabus the Stomper - (Minion)
# 	Battlecry: Reduce the Cost of minions in your deck to (0).
# 	https://hearthstone.gamepedia.com/Barnabus_the_Stomper
# 	"""
# 	play = None
#
#
# class UNG_116te:
# 	"""
# 	Romper Stompers - (Enchantment)
# 	Costs (0).
# 	https://hearthstone.gamepedia.com/Romper_Stompers
# 	"""
# 	pass
#
