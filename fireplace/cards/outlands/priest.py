from ..utils import *


##
# Minions


class BT_197:
    """Reliquary of Souls"""

    # [x]<b>Lifesteal</b> <b>Deathrattle:</b> Shuffle 'Reliquary Prime' into
    # your deck.
    deathrattle = Shuffle(CONTROLLER, "BT_197t")


class BT_197t:
    """Reliquary Prime"""

    # [x]<b><b>Taunt</b>, Lifesteal</b> Only you can target this with spells
    # and Hero Powers.
    update = CurrentPlayer(OPPONENT) & Refresh(
        SELF,
        {
            GameTag.CANT_BE_TARGETED_BY_HERO_POWERS: True,
            GameTag.CANT_BE_TARGETED_BY_ABILITIES: True,
        },
    )


class BT_254:
    """Sethekk Veilweaver"""

    # [x]After you cast a spell on a minion, add a Priest spell to your hand.
    events = Play(CONTROLLER, SPELL, MINION).after(
        Give(CONTROLLER, RandomSpell(card_class=CardClass.PRIEST))
    )


class BT_256:
    """Dragonmaw Overseer"""

    # At the end of your turn, give another friendly minion +2/+2.
    events = OWN_TURN_END.on(Buff(RANDOM_OTHER_FRIENDLY_MINION, "BT_256e"))


BT_256e = buff(+2, +2)


class BT_258:
    """Imprisoned Homunculus"""

    # <b>Dormant</b> for 2 turns. <b>Taunt</b>
    tags = {GameTag.DORMANT: True}
    dormant_turns = 2


class BT_262:
    """Dragonmaw Sentinel"""

    # <b>Battlecry:</b> If you're holding a Dragon, gain +1 Attack and
    # <b>Lifesteal</b>.
    powered_up = HOLDING_DRAGON
    play = powered_up & Buff(SELF, "BT_262e")


BT_262e = buff(atk=1, lifesteal=True)


class BT_341:
    """Skeletal Dragon"""

    # [x]<b>Taunt</b> At the end of your turn, add a Dragon to your hand.
    events = OWN_TURN_END.on(Give(CONTROLLER, RandomDragon()))


##
# Spells


class BT_198:
    """Soul Mirror"""

    # Summon copies of enemy minions. They attack their copies.
    def play(self):
        for entity in ENEMY_MINIONS.eval(self.game, self):
            yield Summon(CONTROLLER, ExactCopy(SELF).evaluate(entity)).then(
                Attack(Summon.CARD, entity)
            )


class BT_252:
    """Renew"""

    # Restore #3 Health. <b>Discover</b> a spell.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Heal(TARGET, 3), DISCOVER(RandomSpell())


class BT_253:
    """Psyche Split"""

    # Give a minion +1/+2. Summon a copy of it.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "BT_253e"), Summon(CONTROLLER, ExactCopy(TARGET))


class BT_257:
    """Apotheosis"""

    # Give a minion +2/+3 and <b>Lifesteal</b>.
    requirements = {PlayReq.REQ_TARGET_TO_PLAY: 0, PlayReq.REQ_MINION_TARGET: 0}
    play = Buff(TARGET, "BT_257e")


BT_257e = buff(+2, +3, lifesteal=True)
