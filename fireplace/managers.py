from .enums import CardClass, CardType, GameTag, Race, Rarity


class Manager(object):
	def __init__(self, obj):
		self.obj = obj

	def __getitem__(self, tag):
		return getattr(self.obj, self.map[tag])

	def __setitem__(self, tag, value):
		setattr(self.obj, self.map[tag], value)

	def update(self, tags):
		for k, v in tags.items():
			if self.map[k]:
				self[k] = v


class GameManager(Manager):
	map = {
		GameTag.NUM_MINIONS_KILLED_THIS_TURN: "minionsKilledThisTurn",
		GameTag.PROPOSED_ATTACKER: "proposedAttacker",
		GameTag.PROPOSED_DEFENDER: "proposedDefender",
		GameTag.TURN: "turn",
	}


class PlayerManager(Manager):
	map = {
		GameTag.CARDTYPE: "type",
		GameTag.COMBO_ACTIVE: "combo",
		GameTag.FATIGUE: "fatigueCounter",
		GameTag.FIRST_PLAYER: "firstPlayer",
		GameTag.HERO_ENTITY: "hero",
		GameTag.LAST_CARD_PLAYED: "lastCardPlayed",
		GameTag.MAXHANDSIZE: "maxHandSize",
		GameTag.MAXRESOURCES: "maxResources",
		GameTag.NUM_CARDS_DRAWN_THIS_TURN: "cardsDrawnThisTurn",
		GameTag.NUM_CARDS_PLAYED_THIS_TURN: "cardsPlayedThisTurn",
		GameTag.NUM_MINIONS_PLAYED_THIS_TURN: "minionsPlayedThisTurn",
		GameTag.NUM_MINIONS_PLAYER_KILLED_THIS_TURN: "minionsKilledThisTurn",
		GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME: "timesHeroPowerUsedThisGame",
		GameTag.OUTGOING_HEALING_ADJUSTMENT: "outgoingHealingAdjustment",
		GameTag.CURRENT_SPELLPOWER: "spellpower",
		GameTag.RECALL_OWED: "overloaded",
		GameTag.RESOURCES_USED: "usedMana",
		GameTag.TEMP_RESOURCES: "tempMana",
	}


class CardManager(Manager):
	map = {
		GameTag.AURA: "aura",
		GameTag.CARD_ID: "id",
		GameTag.CONTROLLER: "controller",
		GameTag.CARDNAME: "name",
		GameTag.CARDTYPE: "type",
		GameTag.CLASS: "cardClass",
		GameTag.COST: "cost",
		GameTag.DEATHRATTLE: "hasDeathrattle",
		GameTag.EXHAUSTED: "exhausted",
		GameTag.RARITY: "rarity",
		GameTag.SPELLPOWER: "spellpower",
		GameTag.ARTISTNAME: None,
		GameTag.AttackVisualType: None,
		GameTag.CARD_SET: None,
		GameTag.CARDTEXT_INHAND: None,
		GameTag.CardTextInPlay: None,
		GameTag.DevState: None,
		GameTag.ENCHANTMENT_IDLE_VISUAL: None,
		GameTag.ENCHANTMENT_BIRTH_VISUAL: None,
		GameTag.FACTION: None,
		GameTag.FLAVORTEXT: None,
		GameTag.HealTarget: None,
		GameTag.HOW_TO_EARN: None,
		GameTag.HOW_TO_EARN_GOLDEN: None,
		GameTag.SILENCE: None,
		GameTag.TRIGGER_VISUAL: None,
	}


class PlayableCardManager(Manager):
	map = CardManager.map.copy()
	map.update({
		GameTag.BATTLECRY: "hasBattlecry",
		GameTag.Collectible: "collectible",
		GameTag.CARD_TARGET: "target",
		GameTag.COMBO: "hasCombo",
		GameTag.DEFENDING: "defending",
		GameTag.FREEZE: "freeze",
		GameTag.RECALL: "overload",
		GameTag.WINDFURY: "windfury",
		GameTag.TARGETING_ARROW_TEXT: None,
		GameTag.TOPDECK: None,
	})


class CharacterManager(Manager):
	map = PlayableCardManager.map.copy()
	map.update({
		GameTag.ATK: "atk",
		GameTag.ATTACKING: "attacking",
		GameTag.CANT_ATTACK: "cantAttack",
		GameTag.CANT_BE_DAMAGED: "immune",
		GameTag.CANT_BE_TARGETED_BY_ABILITIES: "cantBeTargetedByAbilities",
		GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: "cantBeTargetedByHeroPowers",
		GameTag.DAMAGE: "damage",
		GameTag.FROZEN: "frozen",
		GameTag.HEALTH: "maxHealth",
		GameTag.NUM_ATTACKS_THIS_TURN: "numAttacks",
		GameTag.SHOULDEXITCOMBAT: "shouldExitCombat",
	})


class HeroManager(Manager):
	map = CharacterManager.map.copy()
	map.update({
		GameTag.ARMOR: "armor",
	})


class MinionManager(Manager):
	map = CharacterManager.map.copy()
	map.update({
		GameTag.ADJACENT_BUFF: "adjacentBuff",
		GameTag.CARDRACE: "race",
		GameTag.CHARGE: "charge",
		GameTag.DIVINE_SHIELD: "divineShield",
		GameTag.ENRAGED: "enrage",
		GameTag.FORGETFUL: "forgetful",
		GameTag.POISONOUS: "poisonous",
		GameTag.SILENCED: "silenced",
		GameTag.STEALTH: "stealthed",
		GameTag.TAUNT: "taunt",
		GameTag.ELITE: None,
	})


class WeaponManager(Manager):
	map = PlayableCardManager.map.copy()
	map.update({
		GameTag.ATK: "atk",
		GameTag.DURABILITY: "durability",
	})


class SpellManager(Manager):
	map = PlayableCardManager.map.copy()
	map.update({
		GameTag.ImmuneToSpellpower: "immuneToSpellpower",
		GameTag.SECRET: "secret",
		GameTag.AFFECTED_BY_SPELL_POWER: None,
	})


class EnchantmentManager(Manager):
	map = CardManager.map.copy()
	map.update({
		GameTag.ATK: "atk",
		GameTag.ATTACHED: "owner",
		GameTag.CANT_BE_DAMAGED: "immune",
		GameTag.CHARGE: "charge",
		GameTag.CREATOR: "creator",
		GameTag.DURABILITY: "durability",
		GameTag.EXTRA_DEATHRATTLES: "extraDeathrattles",
		GameTag.HEALTH: "maxHealth",
		GameTag.HEALTH_MINIMUM: "minHealth",
		GameTag.OneTurnEffect: "oneTurnEffect",
		GameTag.OUTGOING_HEALING_ADJUSTMENT: "outgoingHealingAdjustment",
		GameTag.STEALTH: "stealthed",
		GameTag.TAUNT: "taunt",
	})
