from ..utils import *


##
# Minions


class BT_008:
    """Rustsworn Initiate"""

    # <b>Deathrattle:</b> Summon a 1/1 Impcaster with <b>Spell Damage +1</b>.
    deathrattle = Summon(CONTROLLER, "BT_008t")


class BT_010:
    """Felfin Navigator"""

    # <b>Battlecry:</b> Give your other Murlocs +1/+1.
    play = Buff(FRIENDLY_MINIONS + MURLOC - SELF, "BT_010e")


BT_010e = buff(+1, +1)


class BT_156:
    """Imprisoned Vilefiend"""

    # <b>Dormant</b> for 2 turns. <b>Rush</b>
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2


class BT_159:
    """Terrorguard Escapee"""

    # <b>Battlecry:</b> Summon three 1/1 Huntresses for your_opponent.
    play = Summon(OPPONENT, "BT_159t")


class BT_160:
    """Rustsworn Cultist"""

    # [x]<b>Battlecry:</b> Give your other minions "<b>Deathrattle:</b> Summon
    # a 1/1 Demon."
    play = Buff(FRIENDLY_MINIONS - SELF, "BT_160e")


class BT_160e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "BT_160t")


class BT_714:
    """Frozen Shadoweaver"""

    # <b>Battlecry:</b> <b>Freeze</b> an_enemy.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }
    play = Freeze(TARGET)


class BT_715:
    """Bonechewer Brawler"""

    # [x]<b>Taunt</b> Whenever this minion takes _damage, gain +2 Attack.
    events = SELF_DAMAGE.on(Buff(SELF, "BT_715e"))


BT_715e = buff(atk=2)


class BT_716:
    """Bonechewer Vanguard"""

    # [x]<b>Taunt</b> Whenever this minion takes damage, gain +2 Attack.
    events = SELF_DAMAGE.on(Buff(SELF, "BT_716e"))


BT_715e = buff(atk=2)


class BT_717:
    """Burrowing Scorpid"""

    # [x]<b>Battlecry:</b> Deal 2 damage. If that kills the target, gain
    # <b>Stealth</b>.
    requirements = {PlayReq.REQ_TARGET_IF_AVAILABLE: 0}
    play = Hit(TARGET, 2), Dead(TARGET) & Stealth(SELF)


class BT_720:
    """Ruststeed Raider"""

    # <b>Taunt</b>, <b>Rush</b> <b>Battlecry:</b> Gain +4 Attack this turn.
    play = Buff(SELF, "BT_720e")


BT_720e = buff(atk=4)


class BT_722:
    """Guardian Augmerchant"""

    # <b>Battlecry:</b> Deal 1 damage to a minion and give it <b>Divine
    # Shield</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), GiveDivineShield(TARGET)


class BT_723:
    """Rocket Augmerchant"""

    # <b>Battlecry:</b> Deal 1 damage to a minion and give it <b>Rush</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), GiveRush(TARGET)


class BT_724:
    """Ethereal Augmerchant"""

    # <b>Battlecry:</b> Deal 1 damage to a minion and give it <b>Spell Damage
    # +1</b>.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 1), Buff(TARGET, "BT_724e")


BT_724e = buff(spellpower=1)


class BT_726:
    """Dragonmaw Sky Stalker"""

    # <b>Deathrattle:</b> Summon a 3/4 Dragonrider.
    deathrattle = Summon(CONTROLLER, "BT_726t")


class BT_727:
    """Soulbound Ashtongue"""

    # Whenever this minion takes damage, also deal that amount to your hero.
    events = SELF_DAMAGE.on(Hit(FRIENDLY_HERO, Damage.AMOUNT))


class BT_728:
    """Disguised Wanderer"""

    # <b>Deathrattle:</b> Summon a 9/1 Inquisitor.
    deathrattle = Summon(CONTROLLER, "BT_728t")


class BT_730:
    """Overconfident Orc"""

    # <b>Taunt</b> While at full Health, this has +2 Attack.
    update = Find(DAMAGED + SELF) | Refresh(SELF, {GameTag.ATK: +2})


class BT_732:
    """Scavenging Shivarra"""

    # <b>Battlecry:</b> Deal 6 damage randomly split among all_other minions.
    play = Hit(RANDOM_OTHER_MINION, 1) * 6


class BT_734:
    """Supreme Abyssal"""

    # Can't attack heroes.
    tags = {GameTag.CANNOT_ATTACK_HEROES: True}
