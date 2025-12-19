from ..utils import *


##
# Hero Powers


class HERO_04bp:
    """Reinforce (Uther Lightbringer)"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "CS2_101t")


class CS2_101_H1(HERO_04bp):
    """Reinforce (Lady Liadrin)"""

    pass


class CS2_101_H2(HERO_04bp):
    """Reinforce (Prince Arthas)"""

    pass


class CS2_101_H3(HERO_04bp):
    """Reinforce (Sir Annoy-O)"""

    pass


##
# Upgraded Hero Powers


class HERO_04bp2:
    """The Silver Hand"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "CS2_101t") * 2


class CS2_101_H1_AT_132(HERO_04bp2):
    """The Silver Hand (Lady Liadrin)"""

    pass


class CS2_101_H2_AT_132(HERO_04bp2):
    """The Silver Hand (Prince Arthas)"""

    pass


class CS2_101_H3_AT_132(HERO_04bp2):
    """The Silver Hand (Sir Annoy-O)"""

    pass
