from ..utils import *


##
# Minions


class BT_120:
    """Warmaul Challenger"""

    # <b>Battlecry:</b> Choose an enemy minion. Battle it to the death!
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    def play(self):
        yield Attack(SELF, TARGET)
        for _ in range(29):
            if not Dead(SELF | TARGET).check(self):
                yield Attack(SELF, TARGET)
            else:
                break


class BT_121:
    """Imprisoned Gan'arg"""

    # <b>Dormant</b> for 2 turns. When this awakens, equip a 3/2 Axe.
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2
    awaken = Summon(CONTROLLER, "CS2_106")


class BT_123:
    """Kargath Bladefist"""

    # [x]<b>Rush</b> <b>Deathrattle:</b> Shuffle 'Kargath Prime' into your
    # deck.
    deathrattle = Shuffle(CONTROLLER, "BT_123t")


class BT_123t:
    """Kargath Prime"""

    # <b>Rush</b>. Whenever this attacks and kills a minion, gain 10 Armor.
    events = Attack(SELF, ALL_MINIONS).after(
        Dead(ALL_MINIONS + Attack.DEFENDER) & GainArmor(FRIENDLY_HERO, 10)
    )


class BT_138:
    """Bloodboil Brute"""

    # <b>Rush</b> Costs (1) less for each damaged minion.
    cost_mod = -Count(DAMAGED_CHARACTERS)


class BT_140:
    """Bonechewer Raider"""

    # <b>Battlecry:</b> If there is a damaged minion, gain +1/+1 and
    # <b>Rush</b>.
    powered_up = Find(ALL_MINIONS + DAMAGED)
    play = powered_up & Buff(SELF, "BT_140e")


BT_140e = buff(+1, +1, rush=True)


class BT_249:
    """Scrap Golem"""

    # <b>Taunt</b>. <b>Deathrattle</b>: Gain Armor equal to this minion's
    # Attack.
    deathrattle = GainArmor(FRIENDLY_HERO, ATK(SELF))


##
# Spells


class BT_117:
    """Bladestorm"""

    # Deal $1 damage to all minions. Repeat until one dies.
    def play(self):
        yield Hit(ALL_MINIONS, 1)
        for _ in range(29):
            if not Dead(ALL_MINIONS).check(self):
                yield Hit(ALL_MINIONS, 1)
            else:
                break


class BT_124:
    """Corsair Cache"""

    # Draw a weapon. Give it +1 Durability.
    play = ForceDraw(RANDOM(FRIENDLY_HAND + WEAPON)).then(
        Buff(ForceDraw.TARGET, "BT_124e")
    )


BT_124e = buff(health=1)


class BT_233:
    """Sword and Board"""

    # Deal $2 damage to a minion. Gain 2 Armor.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Hit(TARGET, 2), GainArmor(FRIENDLY_HERO, 2)


##
# Weapons


class BT_781:
    """Bulwark of Azzinoth"""

    # [x]Whenever your hero would take damage, this loses _1 Durability
    # instead.
    events = Predamage(FRIENDLY_HERO).on(Predamage(FRIENDLY_HERO, 0), Hit(SELF, 1))
