from ..utils import *


@custom_card
class VAN_NEW1_008:
    tags = {
        GameTag.CARDNAME: "Ancient of Lore (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.DRUID,
        GameTag.RARITY: Rarity.EPIC,
        GameTag.COST: 7,
        GameTag.ATK: 5,
        GameTag.HEALTH: 5,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    choose = ("VAN_NEW1_008a", "NEW1_008b")
    play = ChooseBoth(CONTROLLER) & (Draw(CONTROLLER) * 2, Heal(TARGET, 5))


@custom_card
class VAN_NEW1_008a:
    tags = {
        GameTag.CARDNAME: "Ancient Teachings (Old)",
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.CLASS: CardClass.DRUID,
    }
    play = Draw(CONTROLLER) * 2


@custom_card
class VAN_EX1_571:
    tags = {
        GameTag.CARDNAME: "Force of Nature (Old)",
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.CLASS: CardClass.DRUID,
        GameTag.RARITY: Rarity.EPIC,
        GameTag.COST: 6,
    }
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "VAN_EX1_tk9b") * 3


@custom_card
class VAN_EX1_tk9b:
    tags = {
        GameTag.CARDNAME: "Treant (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.DRUID,
        GameTag.COST: 1,
        GameTag.ATK: 2,
        GameTag.HEALTH: 2,
        GameTag.CHARGE: True,
    }
    events = OWN_TURN_END.on(Destroy(SELF))


@custom_card
class VAN_EX1_166:
    tags = {
        GameTag.CARDNAME: "Keeper of the Grove (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.DRUID,
        GameTag.RARITY: Rarity.RARE,
        GameTag.COST: 4,
        GameTag.ATK: 2,
        GameTag.HEALTH: 4,
    }
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    choose = ("EX1_166a", "EX1_166b")
    play = ChooseBoth(CONTROLLER) & (Hit(TARGET, 2), Silence(TARGET))


@custom_card
class VAN_CS2_203:
    tags = {
        GameTag.CARDNAME: "Ironbeak Owl (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.NEUTRAL,
        GameTag.RARITY: Rarity.COMMON,
        GameTag.COST: 2,
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
        GameTag.CARDRACE: Race.BEAST,
    }
    play = Silence(TARGET)


@custom_card
class VAN_EX1_005:
    tags = {
        GameTag.CARDNAME: "Big Game Hunter (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.NEUTRAL,
        GameTag.RARITY: Rarity.EPIC,
        GameTag.COST: 3,
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
    }
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_MIN_ATTACK: 7,
    }
    play = Destroy(TARGET)


@custom_card
class VAN_CS2_084:
    tags = {
        GameTag.CARDNAME: "Hunter's Mark (Old)",
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.CLASS: CardClass.HUNTER,
        GameTag.COST: 0,
    }
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_084e")


@custom_card
class VAN_CS2_233:
    tags = {
        GameTag.CARDNAME: "Blade Flurry (Old)",
        GameTag.CARDTYPE: CardType.SPELL,
        GameTag.CLASS: CardClass.ROGUE,
        GameTag.RARITY: Rarity.RARE,
        GameTag.COST: 2,
    }
    requirements = {PlayReq.REQ_WEAPON_EQUIPPED: 0}
    play = Hit(ENEMY_CHARACTERS, ATK(FRIENDLY_WEAPON)), Destroy(FRIENDLY_WEAPON)


@custom_card
class VAN_NEW1_019:
    tags = {
        GameTag.CARDNAME: "Knife Juggler (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.NEUTRAL,
        GameTag.RARITY: Rarity.RARE,
        GameTag.COST: 2,
        GameTag.ATK: 3,
        GameTag.HEALTH: 2,
    }
    """Knife Juggler"""
    events = Summon(CONTROLLER, MINION - SELF).after(Hit(RANDOM_ENEMY_CHARACTER, 1))


@custom_card
class VAN_EX1_029:
    tags = {
        GameTag.CARDNAME: "Leper Gnome (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.NEUTRAL,
        GameTag.RARITY: Rarity.COMMON,
        GameTag.COST: 1,
        GameTag.ATK: 2,
        GameTag.HEALTH: 1,
    }
    deathrattle = Hit(ENEMY_HERO, 2)


@custom_card
class VAN_EX1_089:
    tags = {
        GameTag.CARDNAME: "Arcane Golem (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.NEUTRAL,
        GameTag.RARITY: Rarity.RARE,
        GameTag.COST: 3,
        GameTag.ATK: 4,
        GameTag.HEALTH: 2,
        GameTag.CHARGE: True,
    }
    play = GainMana(OPPONENT, 1)


@custom_card
class VAN_EX1_620:
    tags = {
        GameTag.CARDNAME: "Molten Giant (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.NEUTRAL,
        GameTag.RARITY: Rarity.EPIC,
        GameTag.COST: 20,
        GameTag.ATK: 8,
        GameTag.HEALTH: 8,
    }
    cost_mod = -DAMAGE(FRIENDLY_HERO)


@custom_card
class VAN_NEW1_014:
    tags = {
        GameTag.CARDNAME: "Master of Disguise (Old)",
        GameTag.CARDTYPE: CardType.MINION,
        GameTag.CLASS: CardClass.ROGUE,
        GameTag.RARITY: Rarity.RARE,
        GameTag.COST: 4,
        GameTag.ATK: 4,
        GameTag.HEALTH: 4,
    }
    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_NONSELF_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Buff(TARGET - STEALTH, "VAN_NEW1_014e")


@custom_card
class VAN_NEW1_014e:
    tags = {
        GameTag.CARDNAME: "Disguised (Old)",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.STEALTH: True,
    }
