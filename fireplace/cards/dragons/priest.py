from ..utils import *


##
# Minions


class DRG_090:
    """Murozond the Infinite"""

    # <b>Battlecry:</b> Play all cards your opponent played last_turn.
    play = Replay(Copy(CARDS_OPPONENT_PLAYED_LAST_TURN))


class DRG_300:
    """Fate Weaver"""

    # [x]<b>Battlecry:</b> If you've <b>Invoked</b> twice, reduce the Cost of cards in your
    # hand by (1).
    powered_up = INVOKED_TWICE
    play = powered_up & Buff(FRIENDLY_HAND, "DRG_300e")


class DRG_300e:
    tags = {GameTag.COST: -1}
    events = REMOVED_IN_PLAY


class DRG_303:
    """Disciple of Galakrond"""

    # <b>Battlecry:</b> <b>Invoke</b> Galakrond.
    play = INVOKE


class DRG_304:
    """Chronobreaker"""

    # [x]<b>Deathrattle:</b> If you're holding a Dragon, deal 3 damage to all enemy
    # minions.
    deathrattle = HOLDING_DRAGON & Hit(ENEMY_MINIONS, 3)


class DRG_306:
    """Envoy of Lazul"""

    # [x]<b>Battlecry:</b> Look at 3 cards. Guess which one is in your opponent's hand to
    # get a copy of it.
    class EnvoyOfLazuljAction(TargetedAction):
        def do(self, source, player):
            self.player = player
            self.source = source
            self.min_count = 1
            self.max_count = 1
            # Envoy of Lazul attempts to show three cards:
            # one card in the opponent's hand, and two cards in the opponent's current deck
            # but not in the opponent's hand.
            #
            # For the one card in the opponent's hand:
            # The card being shown in the opponent's hand does not have to be a card that
            # started in the opponent's deck.
            #
            # For the two cards in the opponent's deck but not in the opponent's hand:
            # If the opponent's deck is empty, two cards that had started in the opponent's
            # deck will be shown instead.
            # If the opponent's deck has only one card left, the same thing happens;
            # two cards that had started in the opponent's deck will be shown instead.
            if len(player.opponent.hand) <= 0:
                return
            self.correct_card = player.card(source.game.random.choice(player.opponent.hand).id)
            op_deck = player.opponent.deck.exclude(id=self.correct_card)
            if len(op_deck) <= 1:
                op_deck = player.opponent.starting_deck.exclude(id=self.correct_card)
            if len(op_deck) <= 1:
                return
            self.card_1, self.card_2 = [
                player.card(card.id) for card in source.game.random.sample(op_deck, 2)
            ]
            self.cards = [self.correct_card, self.card_1, self.card_2]
            source.game.random.shuffle(self.cards)
            self.player.choice = self
            source.game.manager.targeted_action(self, source, player)

        def choose(self, card):
            if card not in self.cards:
                raise InvalidAction(
                    "%r is not a valid choice (one of %r)" % (card, self.cards)
                )
            else:
                if card is self.correct_card:
                    if len(self.player.hand) < self.player.max_hand_size:
                        card.zone = Zone.HAND
                else:
                    log.info(
                        "Choose incorrectly, corrent choice is %r", self.correct_card
                    )
                    self.source.game.queue_actions(card, [Reveal(self.correct_card)])
            self.player.choice = None
            self.trigger_choice_callback()

    play = EnvoyOfLazuljAction(CONTROLLER)


class DRG_308:
    """Mindflayer Kaahrj"""

    # <b>Battlecry:</b> Choose an enemy minion. <b>Deathrattle:</b> Summon a new copy of
    # it.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    deathrattle = HAS_TARGET & Summon(CONTROLLER, Copy(TARGET))


##
# Spells


class DRG_246:
    """Time Rip"""

    # Destroy a minion. <b>Invoke</b> Galakrond.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Destroy(TARGET), INVOKE


class DRG_301:
    """Whispers of EVIL"""

    # Add a <b>Lackey</b> to your_hand.
    play = Give(CONTROLLER, RandomLackey())


class DRG_302:
    """Grave Rune"""

    # Give a minion "<b>Deathrattle:</b> Summon 2 copies of this."
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "DRG_302e")


class DRG_302e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, Copy(OWNER)) * 2


class DRG_307:
    """Breath of the Infinite"""

    # Deal $2 damage to all minions. If you're holding a Dragon, only damage enemies.
    powered_up = HOLDING_DRAGON
    play = powered_up & Hit(ENEMY_MINIONS, 2) | Hit(ALL_MINIONS, 2)


##
# Heros


class DRG_660:
    """Galakrond, the Unspeakable"""

    # [x]<b>Battlecry:</b> Destroy 1 random enemy minion. <i>(@)</i>
    progress_total = 2
    play = Destroy(RANDOM_ENEMY_MINION)
    reward = Find(SELF + FRIENDLY_HERO) | (
        Morph(SELF, "DRG_660t2")
    )


class DRG_660t2:
    """Galakrond, the Apocalypse"""

    # [x]<b>Battlecry:</b> Destroy 2 random enemy minions. <i>(@)</i>
    progress_total = 2
    play = Destroy(RANDOM_ENEMY_MINION * 2)
    reward = Find(SELF + FRIENDLY_HERO) | (
        Morph(SELF, "DRG_660t3")
    )


class DRG_660t3:
    """Galakrond, Azeroth's End"""

    # [x]<b>Battlecry:</b> Destroy 4 random enemy minions. Equip a 5/2 Claw.
    play = (Destroy(RANDOM_ENEMY_MINION * 4), Summon(CONTROLLER, "DRG_238ht"))


class DRG_238p5:
    """Galakrond's Wit"""

    # <b>Hero Power</b> Add a random Priest minion to your hand.
    activate = Give(CONTROLLER, RandomMinion(card_class=CardClass.PRIEST))
