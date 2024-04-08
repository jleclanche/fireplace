from ..utils import *


##
# Hero Powers


class CS1h_001:
    """Lesser Heal (Anduin Wrynn)"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Heal(TARGET, 2)


class CS1h_001_H1(CS1h_001):
    """Heal (Tyrande Whisperwind)"""

    pass


class CS1h_001_H2(CS1h_001):
    """Heal (Madame Lazul)"""

    pass


##
# Upgraded Hero Powers


class AT_132_PRIEST:
    """Heal"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    activate = Heal(TARGET, 4)


class CS1h_001_H1_AT_132(AT_132_PRIEST):
    """Heal (Tyrande Whisperwind)"""

    pass


class CS1h_001_H2_AT_132(AT_132_PRIEST):
    """Heal (Madame Lazul)"""

    pass
