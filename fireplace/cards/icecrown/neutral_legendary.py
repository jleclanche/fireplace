from ..utils import *


##
# Minions


class ICC_314:
    """The Lich King"""

    entourage = LICH_KING_CARDS
    events = OWN_TURN_END.on(Give(CONTROLLER, RandomEntourage()))


class ICC_314t1:
    """Frostmourne"""

    events = Attack(FRIENDLY_HERO, ALL_MINIONS).after(
        Dead(Attack.DEFENDER) & StoringBuff(SELF, "ICC_314t1e", Attack.DEFENDER)
    )


class ICC_314t1e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, Copy(STORE_CARD))


class ICC_314t2:
    """Army of the Dead"""

    play = (Mill(CONTROLLER) * 5).then(
        Find(MINION + Mill.CARD) & Summon(CONTROLLER, Mill.CARD)
    )


class ICC_314t3:
    """Doom Pact"""

    def play(self):
        minion_count = len(self.controller.field) + len(self.controller.opponent.field)
        yield Destroy(ALL_MINIONS)
        yield Mill(CONTROLLER) * minion_count


class ICC_314t4:
    """Death Grip"""

    play = Steal(RANDOM(ENEMY_DECK + MINION)).then(Give(CONTROLLER, Steal.TARGET))


class ICC_314t5:
    """Death Coil"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Find(TARGET + ENEMY) & Hit(TARGET, 5) | Heal(TARGET, 5)


class ICC_314t6:
    """Obliterate"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Destroy(TARGET).then(Hit(FRIENDLY_HERO, ATK(TARGET)))


class ICC_314t7:
    """Anti-Magic Shell"""

    play = Buff(FRIENDLY_MINIONS, "ICC_314t7e")


ICC_314t7e = buff(
    atk=2,
    health=2,
    cant_be_targeted_by_spells=True,
    cant_be_targeted_by_hero_powers=True,
)


class ICC_314t8:
    """Death and Decay"""

    play = Hit(ENEMY_CHARACTERS, 3)


class ICC_851:
    """Prince Keleseth"""

    play = Find(FRIENDLY_DECK + (COST == 2)) | Buff(FRIENDLY_DECK + MINION, "ICC_851e")


ICC_851e = buff(+1, +1)


class ICC_852:
    """Prince Taldaram"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_IF_AVAILABLE_AND_NO_3_COST_CARD_IN_DECK: 0,
    }
    play = Morph(SELF, ExactCopy(TARGET)).then(Buff(Morph.CARD, "ICC_852e"))


class ICC_852e:
    atk = SET(3)
    max_health = SET(3)


class ICC_853:
    """Prince Valanar"""

    play = Find(FRIENDLY_DECK + (COST == 2)) | (Taunt(SELF), GiveLifesteal(SELF))


class ICC_854:
    """Arfus"""

    entourage = LICH_KING_CARDS
    deathrattle = Give(CONTROLLER, RandomEntourage())
