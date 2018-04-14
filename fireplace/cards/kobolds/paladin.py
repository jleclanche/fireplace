from ..utils import *


class LOOT_088:
	"""
	Potion of Heroism - (Spell)
	Give a minion Divine_Shield. Draw a card.
	https://hearthstone.gamepedia.com/Potion_of_Heroism
	"""
	play = GiveDivineShield(TARGET), Draw(CONTROLLER)


class LOOT_091:
	"""
	Lesser Pearl Spellstone - (Spell)
	Summon a 2/2 Spirit with Taunt. @
	https://hearthstone.gamepedia.com/Lesser_Pearl_Spellstone
	"""
	play = Summon(CONTROLLER, "LOOT_091t")
	reward = Morph(SELF, "LOOT_091t1")
	class Hand:
		event = Heal(FRIENDLY_CHARACTERS).on(UpdateSpellStone(Heal.AMOUNT, 3))


class LOOT_091t1:
	"""
	Pearl Spellstone - (Spell)
	Summon a 4/4 Spirit with Taunt. @
	https://hearthstone.gamepedia.com/Pearl_Spellstone
	"""
	play = Summon(CONTROLLER, "LOOT_091t1t")
	reward = Morph(SELF, "LOOT_091t1")
	class Hand:
		event = Heal(FRIENDLY_CHARACTERS).on(UpdateSpellStone(Heal.AMOUNT, 3))


class LOOT_091t2:
	"""
	Greater Pearl Spellstone - (Spell)
	Summon a 6/6 Spirit with Taunt.
	https://hearthstone.gamepedia.com/Greater_Pearl_Spellstone
	"""
	play = Summon(CONTROLLER, "LOOT_091t2t")


class LOOT_093:
	"""
	Call to Arms - (Spell)
	Recruit 3 minions that  cost (2) or less.
	https://hearthstone.gamepedia.com/Call_to_Arms
	"""
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION + (COST <= 2))) * 3


class LOOT_216:
	"""
	Lynessa Sunsorrow - (Minion)
	Battlecry: Cast each spell you cast on your minions  this game on this one.
	https://hearthstone.gamepedia.com/Lynessa_Sunsorrow
	"""
	def play(self):
		for buff in random.suffle(self.source.spell_cast_on_your_minions):
			yield CastSpell(self, Battlecry(buff, self)) 


class LOOT_286:
	"""
	Unidentified Maul - (Weapon)
	Gains a bonus effect in_your hand.
	https://hearthstone.gamepedia.com/Unidentified_Maul
	"""
	draw = Morph(SELF, RandomID("LOOT_286t2","LOOT_286t3","LOOT_286t1","LOOT_286t4"))


class LOOT_286t1:
	"""
	Champion's Maul - (Weapon)
	Battlecry: Summon two 1/1 Silver Hand Recruits.
	https://hearthstone.gamepedia.com/Champion%27s_Maul
	"""
	play = Summon(CONTROLLER, "CS2_101t") * 2


class LOOT_286t2:
	"""
	Sacred Maul - (Weapon)
	Battlecry: Give your minions Taunt.
	https://hearthstone.gamepedia.com/Sacred_Maul
	"""
	play = Taunt(FRIENDLY_MINIONS)


class LOOT_286t3:
	"""
	Blessed Maul - (Weapon)
	Battlecry: Give your minions +1 Attack.
	https://hearthstone.gamepedia.com/Blessed_Maul
	"""
	play = Buff(FRIENDLY_MINIONS, "LOOT_286t3e")

LOOT_286t3e = buff(atk=1)


class LOOT_286t4:
	"""
	Purifier's Maul - (Weapon)
	Battlecry: Give your minions Divine Shield.
	https://hearthstone.gamepedia.com/Purifier%27s_Maul
	"""
	play = GiveDivineShield(FRIENDLY_MINIONS)


class LOOT_313:
	"""
	Crystal Lion - (Minion)
	Divine Shield Costs (1) less for each Silver Hand Recruit you control.
	https://hearthstone.gamepedia.com/Crystal_Lion
	"""
	cost_mod = -Count(FRIENDLY_MINIONS + ID("CS2_101t"))


class LOOT_333:
	"""
	Level Up! - (Spell)
	Give your Silver Hand Recruits +2/+2 and_Taunt.
	https://hearthstone.gamepedia.com/Level_Up%21
	"""
	play = Buff(FRIENDLY_MINIONS + ID("CS2_101t"), "LOOT_333e")

LOOT_333e = buff(+2, +2, taunt=True)


class LOOT_363:
	"""
	Drygulch Jailor - (Minion)
	Deathrattle: Add 3 Silver_Hand Recruits to_your_hand.
	https://hearthstone.gamepedia.com/Drygulch_Jailor
	"""
	deathrattle = Give(CONTROLLER, "CS2_101t") * 3


class LOOT_398:
	"""
	Benevolent Djinn - (Minion)
	At the end of your turn, restore 3 Health to your_hero.
	https://hearthstone.gamepedia.com/Benevolent_Djinn
	"""
	event = OWN_TURN_END.on(Heal(FRIENDLY_HERO, 3))


class LOOT_500:
	"""
	Val'anyr - (Weapon)
	Deathrattle: Give a minion in your hand +4/+2. When it dies, reequip this.
	https://hearthstone.gamepedia.com/Val%27anyr
	"""
	deathrattle = Buff(RANDOM(FRIENDLY_HAND + MINION), "LOOT_500e")

class LOOT_500e:
	deathrattle = Summon(CONTROLLER, "LOOT_500")
	tag = {
		GameTag.ATK: +4,
		GameTag.HEALTH: +2,
		GameTag.DEATHRATTLE: True
	}