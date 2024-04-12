from ..utils import *


##
# Minions


class ICC_065:
    """Bone Baron"""

    deathrattle = Give(CONTROLLER, "ICC_026t") * 2


class ICC_240:
    """Runeforge Haunter"""

    update = CurrentPlayer(CONTROLLER) & Refresh(
        FRIENDLY_WEAPON, {GameTag.IMMUNE: True}
    )


class ICC_809:
    """Plague Scientist"""

    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
    }
    combo = GivePoisonous(TARGET)


class ICC_811:
    """Lilian Voss"""

    play = Find(ENEMY_HERO - NEUTRAL) & (
        Morph(FRIENDLY_HAND + SPELL, RandomSpell(card_class=ENEMY_CLASS))
    )


class ICC_910:
    """Spectral Pillager"""

    requirements = {
        PlayReq.REQ_TARGET_FOR_COMBO: 0,
    }
    combo = Hit(TARGET, NUM_CARDS_PLAYED_THIS_TURN)


##
# Spells


class ICC_201:
    """Roll the Bones"""

    play = Draw(CONTROLLER).then(Find(Draw.CARD + DEATHRATTLE) & CastSpell("ICC_201"))


class ICC_221:
    """Leeching Poison"""

    requirements = {
        PlayReq.REQ_WEAPON_EQUIPPED: 0,
    }
    play = GiveLifesteal(FRIENDLY_WEAPON)


class ICC_233:
    """Doomerang"""

    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_WEAPON_EQUIPPED: 0,
    }
    play = Hit(TARGET, ATK(FRIENDLY_WEAPON)), Bounce(FRIENDLY_WEAPON)


##
# Weapons


class ICC_850:
    """Shadowblade"""

    play = Buff(FRIENDLY_HERO, "ICC_850e")


ICC_850e = buff(immune=True)


##
# Heros


class ICC_827:
    """Valeera the Hollow"""

    play = (
        Stealth(FRIENDLY_HERO),
        Buff(FRIENDLY_HERO, "ICC_827e3"),
        Give(CONTROLLER, "ICC_827t"),
    )


class ICC_827e3:
    events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class ICC_827p:
    tags = {enums.PASSIVE_HERO_POWER: True}
    events = OWN_TURN_BEGIN.on(Give(CONTROLLER, "ICC_827t"))


class ICC_827t:
    requirements = {
        PlayReq.REQ_MUST_PLAY_OTHER_CARD_FIRST: 0,
    }

    class Hand:
        events = (
            Play(CONTROLLER).on(
                Morph(SELF, ExactCopy(Play.CARD)).then(Buff(Morph.CARD, "ICC_827e"))
            ),
            OWN_TURN_END.on(Destroy(SELF)),
        )
        update = Find(FRIENDLY_HERO_POWER - EXHAUSTED + ID("ICC_827p")) | Destroy(SELF)


class ICC_827e:
    class Hand:
        events = (
            Play(CONTROLLER).on(
                Morph(OWNER, ExactCopy(Play.CARD)).then(Buff(Morph.CARD, "ICC_827e"))
            ),
            OWN_TURN_END.on(Destroy(SELF)),
        )
        update = Find(FRIENDLY_HERO_POWER - EXHAUSTED + ID("ICC_827p")) | Destroy(SELF)

    events = REMOVED_IN_PLAY
