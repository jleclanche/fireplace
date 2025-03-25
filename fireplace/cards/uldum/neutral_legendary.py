from ..utils import *


##
# Minions


class ULD_003:
    """Zephrys the Great"""

    # <b>Battlecry:</b> If your deck has no duplicates, wish for the perfect card.
    # powered_up = -FindDuplicates(FRIENDLY_DECK)
    # play = powered_up & ZephrysAction(CONTROLLER)
    pass


class ULD_177:
    """Octosari"""

    # <b>Deathrattle:</b> Draw 8 cards.
    deathrattle = Draw(CONTROLLER) * 8


class ULD_178:
    """Siamat"""

    # [x]<b>Battlecry:</b> Gain 2 of <b>Rush</b>, <b>Taunt</b>, <b>Divine Shield</b>, or
    # <b>Windfury</b> <i>(your choice).</i>
    class SiamatAction(MultipleChoice):
        PLAYER = ActionArg()
        choose_times = 2
        siamat_ids = ["ULD_178a", "ULD_178a2", "ULD_178a3", "ULD_178a4"]

        def do_step1(self):
            self.cards = [self.player.card(id) for id in self.siamat_ids]

        def do_step2(self):
            self.cards.remove(self.choosed_cards[0])

        def done(self):
            for card in self.choosed_cards:
                self.source.game.queue_actions(card, [Battlecry(card, self.source)])

    play = SiamatAction(CONTROLLER)


class ULD_178a:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = GiveWindfury(TARGET)


class ULD_178a2:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = GiveDivineShield(TARGET)


class ULD_178a3:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
    }
    play = Taunt(TARGET)


class ULD_178a4:
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = GiveRush(TARGET)


class ULD_304:
    """King Phaoris"""

    # [x]<b>Battlecry:</b> For each spell in your hand, summon a random minion of the same
    # Cost.
    def play(self):
        cards = (FRIENDLY_HAND + SPELL).eval(self.controller.hand, self)
        for card in cards:
            yield Summon(CONTROLLER, RandomMinion(cost=card.cost))
