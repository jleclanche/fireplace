from ..utils import *


##
# Hero Powers


class HERO_02bp:
    """Totemic Call"""

    requirements = {
        PlayReq.REQ_ENTIRE_ENTOURAGE_NOT_IN_PLAY: 0,
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    entourage = ["CS2_050", "CS2_051", "CS2_052", "NEW1_009"]
    activate = Summon(CONTROLLER, RandomEntourage(exclude=FRIENDLY_MINIONS))


class NEW1_009:
    """Healing Totem"""

    events = OWN_TURN_END.on(Heal(FRIENDLY_MINIONS, 1))


class CS2_049_H1(HERO_02bp):
    """Totemic Call (Morgl the Oracle)"""

    pass


class CS2_049_H2(HERO_02bp):
    """Totemic Call (King Rastakhan)"""

    pass


class CS2_049_H3(HERO_02bp):
    """Totemic Call (The Thunder King)"""

    pass


class CS2_049_H5(HERO_02bp):
    """Totemic Call (Lady Vashj)"""

    pass


##
# Upgraded Hero Powers


class HERO_02bp2:
    """Totemic Slam"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    choose = ("AT_132_SHAMANa", "AT_132_SHAMANb", "AT_132_SHAMANc", "AT_132_SHAMANd")


class AT_132_SHAMANa:
    """Healing Totem"""

    activate = Summon(CONTROLLER, "NEW1_009")


class AT_132_SHAMANb:
    """Searing Totem"""

    activate = Summon(CONTROLLER, "CS2_050")


class AT_132_SHAMANc:
    """Stoneclaw Totem"""

    activate = Summon(CONTROLLER, "CS2_051")


class AT_132_SHAMANd:
    """Wrath of Air Totem"""

    activate = Summon(CONTROLLER, "CS2_052")


class CS2_049_H1_AT_132(HERO_02bp2):
    """Totemic Slam (Morgl the Oracle)"""

    pass


class CS2_049_H2_AT_132(HERO_02bp2):
    """Totemic Slam (King Rastakhan)"""

    pass


class CS2_049_H3_AT_132(HERO_02bp2):
    """Totemic Slam (The Thunder King)"""

    pass


class CS2_049_H4_AT_132(HERO_02bp2):
    """Totemic Slam (Lady Vashj)"""

    pass
