from ..utils import *


class CS2_004_Puzzle:
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "CS2_004e"), Draw(CONTROLLER)
