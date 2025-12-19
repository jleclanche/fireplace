from ..utils import *


##
# Minions


class ULD_157:
    """Questing Explorer"""

    # <b>Battlecry:</b> If you control a <b>Quest</b>, draw a card.
    play = Find(FRIENDLY_QUEST) & Draw(CONTROLLER)


class ULD_180:
    """Sunstruck Henchman"""

    # At the start of your turn, this has a 50% chance to_fall asleep.
    events = OWN_TURN_BEGIN.on(
        COINFLIP & SetTags(SELF, {GameTag.NUM_TURNS_IN_PLAY: -1})
    )


class ULD_196:
    """Neferset Ritualist"""

    # <b>Battlecry:</b> Restore adjacent minions to full_Health.
    play = FullHeal(SELF_ADJACENT)


class ULD_197:
    """Quicksand Elemental"""

    # <b>Battlecry:</b> Give all enemy minions -2 Attack this_turn.
    play = Buff(ENEMY_MINIONS, "ULD_197e")


ULD_197e = buff(atk=-2)


class ULD_198:
    """Conjured Mirage"""

    # <b>Taunt</b> At the start of your turn, shuffle this minion into your deck.
    events = OWN_TURN_BEGIN.on(Shuffle(CONTROLLER, SELF))


class ULD_208:
    """Khartut Defender"""

    # [x]<b>Taunt</b>, <b>Reborn</b> <b>Deathrattle:</b> Restore #3 Health to your hero.
    deathrattle = Heal(FRIENDLY_HERO, 3)


class ULD_214:
    """Generous Mummy"""

    # <b>Reborn</b> Your opponent's cards cost (1) less.
    update = Refresh(ENEMY_HAND, {GameTag.COST: -1})


class ULD_215:
    """Wrapped Golem"""

    # [x]<b>Reborn</b> At the end of your turn, summon a 1/1 Scarab with <b>Taunt</b>.
    events = OWN_TURN_END.on(Summon(CONTROLLER, "ULD_215t"))


class ULD_250:
    """Infested Goblin"""

    # <b>Taunt</b> <b>Deathrattle:</b> Add two 1/1 Scarabs with <b>Taunt</b> to your hand.
    deathrattle = Give(CONTROLLER, "ULD_215t") * 2
