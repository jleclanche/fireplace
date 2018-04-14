from ..utils import *

class LOOT_077:
	"""
	Flanking Strike - (Spell)
	Deal $3 damage to a minion. Summon a 3/3 Wolf.
	https://hearthstone.gamepedia.com/Flanking_Strike
	"""
	play = Hit(TARGET, 3), Summon(CONTROLLER, "LOOT_077t")


class LOOT_078:
	"""
	Cave Hydra - (Minion)
	Also damages the minions next to whomever this attacks.
	https://hearthstone.gamepedia.com/Cave_Hydra
	"""
	events = Attack(SELF).on(CLEAVE)


class LOOT_079:
	"""
	Wandering Monster - (Spell)
	Secret: When an enemy attacks your hero, summon a 3-Cost minion as the new target.
	https://hearthstone.gamepedia.com/Wandering_Monster
	"""
	secret = Attack(ENEMY_CHARACTERS, FRIENDLY_HERO).on(
		Reveal(SELF), Retarget(Attack.ATTACKER, Summon(CONTROLLER, RandomMinion(cost=3)))
	)


class LOOT_080:
	"""
	Lesser Emerald Spellstone - (Spell)
	Summon two 3/3_Wolves.
	https://hearthstone.gamepedia.com/Lesser_Emerald_Spellstone
	"""
	play = Summon("LOOT_077t") * 2
	class Hand:
		events = Play(CONTROLLER, SECRET).after(Morph(SELF, "LOOT_080t2"))

class LOOT_080t2:
	"""
	Emerald Spellstone - (Spell)
	Summon three 3/3_Wolves.
	https://hearthstone.gamepedia.com/Emerald_Spellstone
	"""
	play = Summon("LOOT_077t") * 3
	class Hand:
		events = Play(CONTROLLER, SECRET).after(Morph(SELF, "LOOT_080t3"))


class LOOT_080t3:
	"""
	Greater Emerald Spellstone - (Spell)
	Summon four 3/3_Wolves.
	https://hearthstone.gamepedia.com/Greater_Emerald_Spellstone
	"""
	play = Summon("LOOT_077t") * 4


class LOOT_085:
	"""
	Rhok'delar - (Weapon)
	Battlecry: If your deck has no minions, fill your_hand with Hunter_spells.
	https://hearthstone.gamepedia.com/Rhok%27delar
	"""
	powered_up = -Find(FRIENDLY_DECK + MINION)
	play = powered_up & Give(CONTROLLER, RandomSpell(card_class=CardClass.HUNTER)) * 10


class LOOT_217:
	"""
	To My Side! - (Spell)
	Summon an Animal Companion, or 2 if your deck has no minions.
	https://hearthstone.gamepedia.com/To_My_Side%21
	"""
	powered_up = -Find(FRIENDLY_DECK + MINION)
	play = powered_up & Summon(CONTROLLER, RandomEntourage() * 2) | Summon(CONTROLLER, RandomEntourage())


class LOOT_222:
	"""
	Candleshot - (Weapon)
	Immune while attacking.
	https://hearthstone.gamepedia.com/Candleshot
	"""
	update = Refresh(FRIENDLY_HERO, {GameTag.IMMUNE_WHILE_ATTACKING: True})


class LOOT_511:
	"""
	Kathrena Winterwisp - (Minion)
	Battlecry and Deathrattle: Recruit a Beast.
	https://hearthstone.gamepedia.com/Kathrena_Winterwisp
	"""
	play = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST))
	deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + BEAST))


class LOOT_520:
	"""
	Seeping Oozeling - (Minion)
	Battlecry: Gain the Deathrattle of a random minion in your deck.
	https://hearthstone.gamepedia.com/Seeping_Oozeling
	"""
	play = Find(FRIENDLY_DECK + DEATHRATTLE) & Buff(SELF, "LOOT_520e").then(CopyDeathrattles(Buff.BUFF, RANDOM(FRIENDLY_DECK + DEATHRATTLE)))

LOOT_520e = buff(deathrattle=True)


class LOOT_522:
	"""
	Crushing Walls - (Spell)
	Destroy your opponent's left and right-most minions.
	https://hearthstone.gamepedia.com/Crushing_Walls
	"""
	def play(self):
		yield Destroy([self.controller.opponent.field[0], self.controller.opponent.field[-1]])