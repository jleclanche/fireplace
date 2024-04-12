from ..utils import *


##
# Minions


class ICC_018:
    """Phantom Freebooter"""

    play = Find(FRIENDLY_WEAPON) & Buff(
        SELF,
        "ICC_018e",
        atk=ATK(FRIENDLY_WEAPON),
        max_health=CURRENT_DURABILITY(FRIENDLY_WEAPON),
    )


class ICC_027:
    """Bone Drake"""

    deathrattle = Give(CONTROLLER, RandomDragon())


class ICC_099:
    """Ticking Abomination"""

    deathrattle = Hit(FRIENDLY_MINIONS, 5)


class ICC_257:
    """Corpse Raiser"""

    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "ICC_257e")


class ICC_257e:
    deathrattle = Summon(CONTROLLER, Copy(OWNER))
    tags = {GameTag.DEATHRATTLE: True}


class ICC_466:
    """Saronite Chain Gang"""

    play = Summon(CONTROLLER, ExactCopy(SELF))


class ICC_700:
    """Happy Ghoul"""

    class Hand:
        events = Heal(FRIENDLY_HERO).on(Buff(SELF, "ICC_700e"))


@custom_card
class ICC_700e:
    tags = {
        GameTag.CARDNAME: "Happy Ghoul Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
        GameTag.TAG_ONE_TURN_EFFECT: True,
    }
    cost = SET(0)
    events = REMOVED_IN_PLAY


class ICC_702:
    """Shallow Gravedigger"""

    deathrattle = Give(CONTROLLER, RandomMinion(deathrattle=True))


class ICC_902:
    """Mindbreaker"""

    update = Refresh(ALL_HERO_POWERS, {enums.HEROPOWER_DISABLED: True})


class ICC_911:
    """Keening Banshee"""

    events = Play(CONTROLLER).on(Mill(CONTROLLER) * 3)
