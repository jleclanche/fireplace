from ..utils import *


##
# Minions


class UNG_020:
    """Arcanologist"""

    play = ForceDraw(RANDOM(FRIENDLY_DECK + SECRET))


class UNG_021:
    """Steam Surger"""

    play = ELEMENTAL_PLAYED_LAST_TURN & Give(CONTROLLER, "UNG_018")


class UNG_027:
    """Pyros"""

    deathrattle = Give(CONTROLLER, SELF).then(Morph(SELF, "UNG_027t2"))


class UNG_027t2:
    deathrattle = Give(CONTROLLER, SELF).then(Morph(SELF, "UNG_027t4"))


class UNG_846:
    """Shimmering Tempest"""

    deathrattle = Give(CONTROLLER, RandomSpell(card_class=CardClass.MAGE))


##
# Spells


class UNG_018:
    """Flame Geyser"""

    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 2), Give(CONTROLLER, "UNG_809t1")


class UNG_024:
    """Mana Bind"""

    secret = Play(OPPONENT, SPELL).after(
        Reveal(SELF),
        Give(CONTROLLER, Copy(Play.CARD)).then(Buff(Give.CARD, "UNG_024e")),
    )


@custom_card
class UNG_024e:
    tags = {
        GameTag.CARDNAME: "Mana Bind Buff",
        GameTag.CARDTYPE: CardType.ENCHANTMENT,
    }
    cost = SET(0)
    events = REMOVED_IN_PLAY


class UNG_028:
    """Open the Waygate"""

    progress_total = 8
    quest = Play(CONTROLLER, SPELL - STARTING_DECK).after(AddProgress(SELF, Play.CARD))
    reward = Give(CONTROLLER, "UNG_028t")


class UNG_028t:
    def play(self):
        self.game.next_players.insert(0, self.controller)


class UNG_941:
    """Primordial Glyph"""

    play = Discover(CONTROLLER, RandomSpell()).then(
        Give(CONTROLLER, Discover.CARD), Buff(Discover.CARD, "UNG_941e")
    )


class UNG_941e:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -2}


class UNG_948:
    """Molten Reflection"""

    requirements = {
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Summon(CONTROLLER, ExactCopy(TARGET))


class UNG_955:
    """Meteor"""

    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Hit(TARGET, 15), Hit(TARGET_ADJACENT, 3)
