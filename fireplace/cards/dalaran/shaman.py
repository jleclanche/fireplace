from ..utils import *


##
# Minions


class DAL_049:
    """Underbelly Angler"""

    # After you play a Murloc, add a random Murloc to your hand.
    events = Play(CONTROLLER, MURLOC).after(
        Give(CONTROLLER, RandomMinion(race=Race.MURLOC))
    )


class DAL_052:
    """Muckmorpher"""

    # [x]<b>Battlecry:</b> Transform into a 4/4 copy of a different minion in your deck.
    play = Find(FRIENDLY_DECK + MINION - ID("DAL_052")) & (
        Morph(SELF, Copy(RANDOM(FRIENDLY_DECK + MINION - ID("DAL_052")))).then(
            Buff(Morph.CARD, "DAL_052e")
        )
    )


class DAL_052e:
    atk = SET(4)
    max_health = SET(4)


class DAL_431:
    """Swampqueen Hagatha"""

    # [x]<b>Battlecry:</b> Add a 5/5 Horror to your hand. Teach it two Shaman spells.
    class SwampqueenHagathaAction(MultipleChoice):
        PLAYER = ActionArg()
        choose_times = 2

        def do(self, source, player):
            self.all_shaman_spells = RandomSpell(
                card_class=CardClass.SHAMAN
            ).find_cards(source)
            self.targeted_spells = []
            self.non_targeted_spells = []
            for id in self.all_shaman_spells:
                if db[id].requirements:
                    self.targeted_spells.append(id)
                else:
                    self.non_targeted_spells.append(id)
            super().do(source, player)

        def do_step1(self):
            self.cards = [
                self.player.card(id)
                for id in self.source.game.random.sample(self.all_shaman_spells, 3)
            ]

        def do_step2(self):
            if self.cards[0] in self.targeted_spells:
                self.cards = [
                    self.player.card(id)
                    for id in self.source.game.random.sample(
                        self.non_targeted_spells, 3
                    )
                ]
            else:
                self.cards = [
                    self.player.card(id)
                    for id in self.source.game.random.sample(self.all_shaman_spells, 3)
                ]

        def done(self):
            card1 = self.choosed_cards[0]
            card2 = self.choosed_cards[1]

            horror = self.player.card("DAL_431t")
            horror.custom_card = True

            def create_custom_card(horror):
                horror.data.scripts.play = (
                    card1.data.scripts.play + card2.data.scripts.play
                )
                horror.requirements = card1.requirements | card2.requirements
                horror.tags[GameTag.CARDTEXT_ENTITY_0] = card1.data.name
                horror.tags[GameTag.CARDTEXT_ENTITY_1] = card2.data.name
                horror.tags[GameTag.OVERLOAD] = (
                    card1.tags[GameTag.OVERLOAD] + card2.tags[GameTag.OVERLOAD]
                )

            horror.create_custom_card = create_custom_card
            horror.create_custom_card(horror)
            self.player.give(horror)

    play = SwampqueenHagathaAction(CONTROLLER)


class DAL_433:
    """Sludge Slurper"""

    # <b>Battlecry:</b> Add a <b>Lackey</b> to your hand. <b>Overload:</b> (1)
    play = Give(CONTROLLER, RandomLackey())


class DAL_726:
    """Scargil"""

    # Your Murlocs cost (1).
    update = Refresh(FRIENDLY_HAND + MURLOC, {GameTag.COST: SET(1)})


##
# Spells


class DAL_009(SchemeUtils):
    """Hagatha's Scheme"""

    # Deal $@ damage to all minions. <i>(Upgrades each turn!)</i>
    play = Hit(ALL_MINIONS, Attr(SELF, GameTag.QUEST_PROGRESS) + 1)


class DAL_071:
    """Mutate"""

    # Transform a friendly minion into a random one that costs (1) more.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Evolve(TARGET, 1)


class DAL_432:
    """Witch's Brew"""

    # Restore #4 Health. Repeatable this turn.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = (
        Heal(TARGET, 4),
        Give(CONTROLLER, "DAL_432").then(Buff(Give.CARD, "GIL_000")),
    )


class DAL_710:
    """Soul of the Murloc"""

    # Give your minions "<b>Deathrattle:</b> Summon a 1/1 Murloc."
    play = Buff(FRIENDLY_MINIONS, "DAL_710e")


class DAL_710e:
    tags = {GameTag.DEATHRATTLE: True}
    deathrattle = Summon(CONTROLLER, "EX1_506a")
