from ..utils import *


##
# Hero Powers


class HERO_09bp:
    """Lesser Heal (Anduin Wrynn)"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Heal(TARGET, 2)


class CS1h_001_H1(HERO_09bp):
    """Heal (Tyrande Whisperwind)"""

    pass


class CS1h_001_H2(HERO_09bp):
    """Heal (Madame Lazul)"""

    pass


##
# Upgraded Hero Powers


class HERO_09bp2:
    """Heal"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Heal(TARGET, 4)


class CS1h_001_H1_AT_132(HERO_09bp2):
    """Heal (Tyrande Whisperwind)"""

    pass


class CS1h_001_H2_AT_132(HERO_09bp2):
    """Heal (Madame Lazul)"""

    pass
