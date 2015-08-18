from .enums import GameTag


class Manager(object):
	def __init__(self, obj):
		self.obj = obj
		self.observers = []

	def __getitem__(self, tag):
		if self.map.get(tag):
			return getattr(self.obj, self.map[tag], 0)
		raise KeyError

	def __setitem__(self, tag, value):
		setattr(self.obj, self.map[tag], value)

	def __iter__(self):
		for k in self.map:
			if self.map[k]:
				yield k

	def get(self, k, default=None):
		return self[k] if k in self.map else default

	def items(self):
		for k, v in self.map.items():
			if v is not None:
				yield k, self[k]

	def register(self, observer):
		self.observers.append(observer)

	def update(self, tags):
		for k, v in tags.items():
			if self.map.get(k) is not None:
				self[k] = v


class GameManager(Manager):
	map = {
		GameTag.NEXT_STEP: "next_step",
		GameTag.NUM_MINIONS_KILLED_THIS_TURN: "minions_killed_this_turn",
		GameTag.PROPOSED_ATTACKER: "proposed_attacker",
		GameTag.PROPOSED_DEFENDER: "proposed_defender",
		GameTag.STEP: "step",
		GameTag.TURN: "turn",
	}

	def __init__(self, *args):
		super().__init__(*args)
		self.id = 1
		self.counter = self.id + 1

	def action(self, type, *args):
		for observer in self.observers:
			observer.action(type, args)

	def action_end(self, type, *args):
		for observer in self.observers:
			observer.action_end(type, args)

	def new_entity(self, entity):
		for observer in self.observers:
			observer.new_entity(entity)
		entity.manager.id = self.counter
		self.counter += 1


class PlayerManager(Manager):
	map = {
		GameTag.CANT_DRAW: "cant_draw",
		GameTag.CARDTYPE: "type",
		GameTag.COMBO_ACTIVE: "combo",
		GameTag.FATIGUE: "fatigue_counter",
		GameTag.FIRST_PLAYER: "first_player",
		GameTag.HEALING_DOUBLE: "healing_double",
		GameTag.HERO_ENTITY: "hero",
		GameTag.LAST_CARD_PLAYED: "last_card_played",
		GameTag.MAXHANDSIZE: "max_hand_size",
		GameTag.MAXRESOURCES: "max_resources",
		GameTag.NUM_CARDS_DRAWN_THIS_TURN: "cards_drawn_this_turn",
		GameTag.NUM_CARDS_PLAYED_THIS_TURN: "cards_played_this_turn",
		GameTag.NUM_MINIONS_PLAYED_THIS_TURN: "minions_played_this_turn",
		GameTag.NUM_MINIONS_PLAYER_KILLED_THIS_TURN: "minions_killed_this_turn",
		GameTag.NUM_TIMES_HERO_POWER_USED_THIS_GAME: "times_hero_power_used_this_game",
		GameTag.OUTGOING_HEALING_ADJUSTMENT: "outgoing_healing_adjustment",
		GameTag.OVERLOAD_LOCKED: "overload_locked",
		GameTag.PLAYSTATE: "playstate",
		GameTag.CURRENT_SPELLPOWER: "spellpower",
		GameTag.RECALL_OWED: "overloaded",
		GameTag.RESOURCES: "max_mana",
		GameTag.RESOURCES_USED: "used_mana",
		GameTag.SPELLPOWER_DOUBLE: "spellpower_double",
		GameTag.TAG_HERO_POWER_DOUBLE: "hero_power_double",
		GameTag.TEMP_RESOURCES: "temp_mana",
		GameTag.TIMEOUT: "timeout",
		GameTag.TURN_START: "turn_start",
	}


CARD_ATTRIBUTE_MAP = {
	GameTag.ADJACENT_BUFF: "adjacent_buff",
	GameTag.ALWAYS_WINS_BRAWLS: "always_wins_brawls",
	GameTag.ARMOR: "armor",
	GameTag.ATK: "atk",
	GameTag.ATTACKING: "attacking",
	GameTag.ATTACHED: "owner",
	GameTag.AURA: "aura",
	GameTag.BATTLECRY: "has_battlecry",
	GameTag.CANT_ATTACK: "cant_attack",
	GameTag.CANT_BE_ATTACKED: "cant_be_attacked",
	GameTag.CANT_BE_DAMAGED: "immune",
	GameTag.CANT_BE_TARGETED_BY_ABILITIES: "cant_be_targeted_by_abilities",
	GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: "cant_be_targeted_by_hero_powers",
	GameTag.CANT_BE_TARGETED_BY_OPPONENTS: "cant_be_targeted_by_opponents",
	GameTag.CANT_PLAY: "cant_play",
	GameTag.CARD_ID: "id",
	GameTag.CARD_TARGET: "target",
	GameTag.CARDNAME: "name",
	GameTag.CARDRACE: "race",
	GameTag.CARDTYPE: "type",
	GameTag.CHARGE: "charge",
	GameTag.CLASS: "card_class",
	GameTag.COMBO: "has_combo",
	GameTag.CONTROLLER: "controller",
	GameTag.COST: "cost",
	GameTag.CREATOR: "creator",
	GameTag.DAMAGE: "damage",
	GameTag.DEATHRATTLE: "has_deathrattle",
	GameTag.DEFENDING: "defending",
	GameTag.DIVINE_SHIELD: "divine_shield",
	GameTag.DURABILITY: "max_durability",
	GameTag.ENRAGED: "enrage",
	GameTag.EXHAUSTED: "exhausted",
	GameTag.EXTRA_DEATHRATTLES: "extra_deathrattles",
	GameTag.FORGETFUL: "forgetful",
	GameTag.FROZEN: "frozen",
	GameTag.HEALING_DOUBLE: "healing_double",
	GameTag.HEALTH: "max_health",
	GameTag.HEALTH_MINIMUM: "min_health",
	GameTag.HEROPOWER_DAMAGE: "heropower_damage",
	GameTag.ImmuneToSpellpower: "immune_to_spellpower",
	GameTag.INSPIRE: "has_inspire",
	GameTag.NUM_ATTACKS_THIS_TURN: "num_attacks",
	GameTag.NUM_TURNS_IN_PLAY: "turns_in_play",
	GameTag.OneTurnEffect: "one_turn_effect",
	GameTag.OUTGOING_HEALING_ADJUSTMENT: "outgoing_healing_adjustment",
	GameTag.POISONOUS: "poisonous",
	GameTag.RARITY: "rarity",
	GameTag.RECALL: "overload",
	GameTag.RECEIVES_DOUBLE_SPELLDAMAGE_BONUS: "receives_double_spelldamage_bonus",
	GameTag.SECRET: "secret",
	GameTag.SHOULDEXITCOMBAT: "should_exit_combat",
	GameTag.SILENCED: "silenced",
	GameTag.SPELLPOWER: "spellpower",
	GameTag.SPELLPOWER_DOUBLE: "spellpower_double",
	GameTag.STEALTH: "stealthed",
	GameTag.TAG_AI_MUST_PLAY: "autocast",
	GameTag.TAG_HERO_POWER_DOUBLE: "hero_power_double",
	GameTag.TAUNT: "taunt",
	GameTag.WINDFURY: "windfury",
	GameTag.ZONE: "zone",
	GameTag.ATTACK_HEALTH_SWAP: "attack_health_swap",
	GameTag.AFFECTED_BY_SPELL_POWER: None,
	GameTag.ARTISTNAME: None,
	GameTag.AttackVisualType: None,
	GameTag.CARD_SET: None,
	GameTag.CARDTEXT_INHAND: None,
	GameTag.CardTextInPlay: None,
	GameTag.Collectible: None,
	GameTag.DevState: None,
	GameTag.ELITE: None,
	GameTag.ENCHANTMENT_IDLE_VISUAL: None,
	GameTag.ENCHANTMENT_BIRTH_VISUAL: None,
	GameTag.EVIL_GLOW: None,
	GameTag.FACTION: None,
	GameTag.FLAVORTEXT: None,
	GameTag.FREEZE: None,
	GameTag.HealTarget: None,
	GameTag.HIDE_COST: None,
	GameTag.HOW_TO_EARN: None,
	GameTag.HOW_TO_EARN_GOLDEN: None,
	GameTag.InvisibleDeathrattle: None,
	GameTag.MORPH: None,
	GameTag.SILENCE: None,
	GameTag.SUMMONED: None,
	GameTag.SPARE_PART: None,
	GameTag.SHOWN_HERO_POWER: None,
	GameTag.TARGETING_ARROW_TEXT: None,
	GameTag.TOPDECK: None,
	GameTag.TAG_AI_MUST_PLAY: None,
	GameTag.TRIGGER_VISUAL: None,
}


class CardManager(Manager):
	map = CARD_ATTRIBUTE_MAP
