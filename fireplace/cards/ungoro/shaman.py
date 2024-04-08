from ..utils import *


##
# Minions


class UNG_201:
    """Primalfin Totem"""

    events = OWN_TURN_END.on(Summon(CONTROLLER, "UNG_201t"))


class UNG_202:
    """Fire Plume Harbinger"""

    play = Buff(FRIENDLY_HAND + ELEMENTAL, "GBL_003e")


class UNG_208:
    """Stone Sentinel"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_WITH_DEATHRATTLE: 0,
    }
    play = ELEMENTAL_PLAYED_LAST_TURN & (SummonBothSides(CONTROLLER, "UNG_208t") * 2)


class UNG_211:
    """Kalimos, Primal Lord"""

    play = ELEMENTAL_PLAYED_LAST_TURN & Choice(
        CONTROLLER, ["UNG_211a", "UNG_211b", "UNG_211c", "UNG_211d"]
    ).then(Battlecry(Choice.CARD, None))


class UNG_211a:
    play = (Summon(CONTROLLER, "UNG_211aa") * 7,)


class UNG_211b:
    play = (Heal(FRIENDLY_HERO, 12),)


class UNG_211c:
    play = (Hit(ENEMY_HERO, 6),)


class UNG_211d:
    play = (Hit(ENEMY_MINIONS, 3),)


class UNG_938:
    """Hot Spring Guardian"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Heal(TARGET, 3)


##
# Spells


class UNG_025:
    """Volcano"""

    play = Hit(RANDOM_MINION, 1) * SPELL_DAMAGE(15)


class UNG_817:
    """Tidal Surge"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Hit(TARGET, 4), Heal(FRIENDLY_HERO, 4)


class UNG_942:
    """Unite the Murlocs"""

    progress_total = 10
    quest = Summon(CONTROLLER, MURLOC).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "UNG_942t")


class UNG_942t:
    play = Give(CONTROLLER, RandomMurloc()) * (
        MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
    )


class UNG_956:
    """Spirit Echo"""

    play = Buff(FRIENDLY_MINIONS, "UNG_956e")


class UNG_956e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Give(CONTROLLER, SELF)
