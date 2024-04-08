from ..utils import *


##
# Minions


class ULD_174:
    """Serpent Egg"""

    # <b>Deathrattle:</b> Summon a 3/4 Sea Serpent.
    deathrattle = Summon(CONTROLLER, "ULD_174t")


class ULD_179:
    """Phalanx Commander"""

    # Your <b>Taunt</b> minions have +2 Attack.
    update = Refresh(FRIENDLY_MINIONS + TAUNT, {GameTag.ATK: +2})


class ULD_182:
    """Spitting Camel"""

    # [x]At the end of your turn, __deal 1 damage to another__ random friendly minion.
    events = OWN_TURN_END.on(Hit(RANDOM_OTHER_FRIENDLY_MINION, 1))


class ULD_183:
    """Anubisath Warbringer"""

    # <b>Deathrattle:</b> Give all minions in your hand +3/+3.
    deathrattle = Buff(FRIENDLY_HAND + MINION, "ULD_183e")


ULD_183e = buff(+3, +3)


class ULD_184:
    """Kobold Sandtrooper"""

    # <b>Deathrattle:</b> Deal 3 damage to the enemy_hero.
    deathrattle = Hit(ENEMY_HERO, 3)


class ULD_185:
    """Temple Berserker"""

    # <b>Reborn</b> Has +2 Attack while damaged.
    enrage = Refresh(SELF, buff="ULD_185e")


ULD_185e = buff(atk=2)


class ULD_188:
    """Golden Scarab"""

    # <b><b>Battlecry:</b> Discover</b> a 4-Cost card.
    play = DISCOVER(RandomCollectible(cost=4))


class ULD_189:
    """Faceless Lurker"""

    # <b>Taunt</b> <b>Battlecry:</b> Double this minion's Health.
    play = Buff(SELF, "ULD_189e")


class ULD_189e:
    def apply(self, target):
        self._xhealth = target.health * 2

    max_health = lambda self, _: self._xhealth


class ULD_190:
    """Pit Crocolisk"""

    # <b>Battlecry:</b> Deal 5 damage.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 5)


class ULD_191:
    """Beaming Sidekick"""

    # <b>Battlecry:</b> Give a friendly minion +2 Health.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ULD_191e")


ULD_191e = buff(health=2)


class ULD_271:
    """Injured Tol'vir"""

    # <b>Taunt</b> <b>Battlecry:</b> Deal 3 damage to this minion.
    play = Hit(SELF, 3)


class ULD_282:
    """Jar Dealer"""

    # [x]<b>Deathrattle:</b> Add a random 1-Cost minion to your hand.
    deathrattle = Give(CONTROLLER, RandomMinion(cost=1))


class ULD_289:
    """Fishflinger"""

    # <b>Battlecry:</b> Add a random Murloc to each player's_hand.
    play = Give(ALL_PLAYERS, RandomMurloc())


class ULD_712:
    """Bug Collector"""

    # <b>Battlecry:</b> Summon a 1/1 Locust with <b>Rush</b>.
    play = Summon(CONTROLLER, "ULD_430t")


class ULD_719:
    """Desert Hare"""

    # <b>Battlecry:</b> Summon two 1/1 Desert Hares.
    play = SummonBothSides(CONTROLLER, "ULD_719")
