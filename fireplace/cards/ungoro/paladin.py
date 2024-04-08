from ..utils import *


##
# Minions


class UNG_011:
    """Hydrologist"""

    play = WITH_SECRECTS & (DISCOVER(RandomSpell(secret=True))) | (
        DISCOVER(RandomSpell(secret=True, card_class=CardClass.PALADIN))
    )


class UNG_015:
    """Sunkeeper Tarim"""

    play = Buff(ALL_MINIONS - SELF, "UNG_015e")


class UNG_015e:
    atk = SET(3)
    max_health = SET(3)


class UNG_953:
    """Primalfin Champion"""

    events = Play(CONTROLLER, SPELL, SELF).on(StoringBuff(SELF, "UNG_953e", Play.CARD))


class UNG_953e:
    tags = {GameTag.DEATHRATTLE: True}

    def deathrattle(self):
        yield Give(CONTROLLER, self.store_card.id)


class UNG_962:
    """Lightfused Stegodon"""

    play = Adapt(FRIENDLY_MINIONS + ID("CS2_101t"))


##
# Spells


class UNG_004:
    """Dinosize"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "UNG_004e")


class UNG_004e:
    atk = SET(10)
    max_health = SET(10)


class UNG_952:
    """Spikeridged Steed"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "UNG_952e")


class UNG_952e:
    tags = {
        GameTag.ATK: 2,
        GameTag.HEALTH: 6,
        GameTag.TAUNT: True,
        GameTag.DEATHRATTLE: True,
    }

    deathrattle = Summon(CONTROLLER, "UNG_810")


class UNG_954:
    """The Last Kaleidosaur"""

    progress_total = 6
    quest = Play(CONTROLLER, SPELL, FRIENDLY_MINIONS).after(
        AddProgress(SELF, Play.CARD)
    )
    reward = Give(CONTROLLER, "UNG_954t1")


class UNG_954t1:
    play = Adapt(SELF) * 5


class UNG_960:
    """Lost in the Jungle"""

    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "CS2_101t") * 2


class UNG_961:
    """Adaptation"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Adapt(TARGET)


##
# Weapons


class UNG_950:
    """Vinecleaver"""

    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "CS2_101t") * 2)
