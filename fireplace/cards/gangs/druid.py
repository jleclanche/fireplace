from ..utils import *


##
# Minions

class CFM_343:
    """Jade Behemoth"""
    play = SummonJadeGolem(CONTROLLER)


##
# Spells

class CFM_602:
    """Jade Idol"""
    choose = ("CFM_602a", "CFM_602b")
    play = ChooseBoth(CONTROLLER) & (SummonJadeGolem(CONTROLLER), Shuffle(CONTROLLER, "CFM_602") * 3)


class CFM_602a:
    play = SummonJadeGolem(CONTROLLER)


class CFM_602b:
    play = Shuffle(CONTROLLER, "CFM_602") * 3


class CFM_713:
    """Jade Blossom"""
    play = SummonJadeGolem(CONTROLLER), GainEmptyMana(CONTROLLER, 1)
