from ..utils import *


##
# Minions


class ULD_195:
    """Frightened Flunky"""

    # <b>Taunt</b> <b>Battlecry:</b> <b>Discover</b> a <b>Taunt</b>_minion.
    play = DISCOVER(RandomMinion(taunt=True))


class ULD_253:
    """Tomb Warden"""

    # <b>Taunt</b> <b>Battlecry:</b> Summon a copy of this minion.
    play = Summon(CONTROLLER, ExactCopy(SELF))


class ULD_258:
    """Armagedillo"""

    # [x]<b>Taunt</b> At the end of your turn, give all <b>Taunt</b> minions in your hand
    # +2/+2.
    events = OWN_TURN_END.on(Buff(FRIENDLY_HAND + MINION + TAUNT, "ULD_258e"))


ULD_258e = buff(+2, +2)


class ULD_709:
    """Armored Goon"""

    # Whenever your hero attacks, gain 5 Armor.
    events = Attack(FRIENDLY_HERO).on(GainArmor(FRIENDLY_HERO, 5))


class ULD_720:
    """Bloodsworn Mercenary"""

    # [x]<b>Battlecry</b>: Choose a damaged friendly minion. Summon a copy of it.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_DAMAGED_TARGET: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET))


##
# Spells


class ULD_256:
    """Into the Fray"""

    # Give all <b>Taunt</b> minions in your hand +2/+2.
    play = Buff(FRIENDLY_HAND + MINION + TAUNT, "ULD_256e")


ULD_256e = buff(+2, +2)


class ULD_707:
    """Plague of Wrath"""

    # Destroy all damaged minions.
    play = Destroy(ALL_MINIONS + DAMAGED)


class ULD_711:
    """Hack the System"""

    # [x]<b>Quest:</b> Attack 5 times with your hero. <b>Reward:</b> Anraphet's Core.
    progress_total = 5
    quest = Attack(FRIENDLY_HERO).after(AddProgress(SELF, Attack.ATTACKER))
    reward = Summon(CONTROLLER, "ULD_711p3")


class ULD_711p3:
    """Anraphet's Core"""

    # [x]<b>Hero Power</b> Summon a 4/3 Golem. After your hero attacks, refresh this.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    activate = Summon(CONTROLLER, "ULD_711t")
    events = Attack(FRIENDLY_HERO).after(RefreshHeroPower(SELF))


##
# Weapons


class ULD_708:
    """Livewire Lance"""

    # After your Hero attacks, add a <b>Lackey</b> to your_hand.
    events = Attack(FRIENDLY_HERO).after(Give(CONTROLLER, RandomLackey()))
