from ..utils import *


##
# Hero Powers


class CS2_101:
    """Reinforce (Uther Lightbringer)"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "CS2_101t")


class CS2_101_H1:
    """Reinforce (Lady Liadrin)"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = CS2_101.activate


class CS2_101_H2:
    """Reinforce (Prince Arthas)"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = CS2_101.activate


class CS2_101_H3(CS2_101):
    """Reinforce (Sir Annoy-O)"""

    pass


##
# Upgraded Hero Powers


class AT_132_PALADIN:
    """The Silver Hand"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    activate = Summon(CONTROLLER, "CS2_101t") * 2


class CS2_101_H1_AT_132(AT_132_PALADIN):
    """The Silver Hand (Lady Liadrin)"""

    pass


class CS2_101_H2_AT_132(AT_132_PALADIN):
    """The Silver Hand (Prince Arthas)"""

    pass


class CS2_101_H3_AT_132(AT_132_PALADIN):
    """The Silver Hand (Sir Annoy-O)"""

    pass
