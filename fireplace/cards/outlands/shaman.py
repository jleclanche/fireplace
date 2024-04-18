from ..utils import *


##
# Minions


class BT_106:
    """Bogstrok Clacker"""

    # <b>Battlecry:</b> Transform adjacent minions into random minions that
    # cost (1) more.
    play = Evolve(SELF_ADJACENT, 1)


class BT_109:
    """Lady Vashj"""

    # [x]<b>Spell Damage +1</b> <b>Deathrattle:</b> Shuffle 'Vashj Prime' into
    # your deck.
    deathrattle = Shuffle(CONTROLLER, "BT_109t")


class BT_109t:
    """Vashj Prime"""

    # [x]<b>Spell Damage +1</b> <b>Battlecry:</b> Draw 3 spells. ___Reduce
    # their Cost by (3).___
    play = Draw(CONTROLLER).then(Buff(Draw.CARD, "BT_109te"))


class BT_109te:
    tags = {GameTag.COST: -3}
    events = REMOVED_IN_PLAY


class BT_114:
    """Shattered Rumbler"""

    # <b>Battlecry:</b> If you cast a spell last turn, deal 2 damage to all
    # other minions.
    powered_up = Find(CARDS_PLAYED_LAST_TURN + SPELL)
    play = powered_up & Hit(ALL_MINIONS - SELF, 2)


class BT_115:
    """Marshspawn"""

    # <b>Battlecry:</b> If you cast a spell last turn, <b>Discover</b> a spell.
    powered_up = Find(CARDS_PLAYED_LAST_TURN + SPELL)
    play = powered_up & DISCOVER(RandomSpell())


class BT_230:
    """The Lurker Below"""

    # [x]<b>Battlecry:</b> Deal 3 damage to an enemy minion. If it dies, repeat
    # on one of its neighbors.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    def play(self):
        target = self.target
        yield Hit(target, 3)
        while Dead(SELF).check(target) and target.adjacent_minions:
            target = random.choice(target.adjacent_minions)
            yield Deaths()
            yield Hit(target, 3)


##
# Spells


class BT_100:
    """Serpentshrine Portal"""

    # Deal $3 damage. Summon a random 3-Cost minion. <b>Overload:</b> (1)
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 3), Summon(CONTROLLER, RandomMinion(cost=3))


class BT_101:
    """Vivid Spores"""

    # Give your minions "<b>Deathrattle:</b> Resummon this minion."
    play = Buff(FRIENDLY_MINIONS, "BT_101e")


class BT_101e:
    deathrattle = Summon(CONTROLLER, Copy(OWNER))
    tags = {GameTag.DEATHRATTLE: True}


class BT_110:
    """Torrent"""

    # [x]Deal $8 damage to a minion. Costs (3) less if you cast a spell last
    # turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    cost_mod = Find(CARDS_PLAYED_LAST_TURN + SPELL) & -3
    play = Hit(TARGET, 8)


class BT_113:
    """Totemic Reflection"""

    # Give a minion +2/+2. If it's a Totem, summon a copy of it.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = (
        Buff(TARGET, "BT_113e"),
        Find(TARGET + TOTEM) & Summon(CONTROLLER, ExactCopy(TARGET)),
    )


BT_113e = buff(+2, +2)


##
# Weapons


class BT_102:
    """Boggspine Knuckles"""

    # After your hero attacks, transform your minions into random ones that
    # cost (1) more.
    events = Attack(FRIENDLY_HERO).after(Evolve(FRIENDLY_MINIONS, 1))
