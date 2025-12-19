from ..utils import *


##
# Hero Powers


class HERO_05bp:
    """Steady Shot (Rexxar)"""

    requirements = {PlayReq.REQ_MINION_OR_ENEMY_HERO: 0, PlayReq.REQ_STEADY_SHOT: 0}
    powered_up = Find(SELF + EnumSelector(GameTag.STEADY_SHOT_CAN_TARGET))
    activate = powered_up & Hit(TARGET, 2) | Hit(ENEMY_HERO, 2)


class DS1h_292_H1(HERO_05bp):
    """Steady Shot (Alleria Windrunner)"""

    pass


class DS1h_292_H3(HERO_05bp):
    """Steady Shot (Sylvanas Windrunner)"""

    pass


##
# Upgraded Hero Powers


class HERO_05bp2:
    """Ballista Shot"""

    requirements = {PlayReq.REQ_MINION_OR_ENEMY_HERO: 0, PlayReq.REQ_STEADY_SHOT: 0}
    powered_up = Find(SELF + EnumSelector(GameTag.STEADY_SHOT_CAN_TARGET))
    activate = powered_up & Hit(TARGET, 3) | Hit(ENEMY_HERO, 3)


class DS1h_292_H1_AT_132(HERO_05bp2):
    """Ballista Shot (Alleria Windrunner)"""

    pass


class DS1h_292_H3_AT_132(HERO_05bp2):
    """Steady Shot (Sylvanas Windrunner)"""

    pass
