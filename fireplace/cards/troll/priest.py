from ..utils import *


##
# Minions


class TRL_131:
    """Sand Drudge"""

    # Whenever you cast a spell, summon a 1/1 Zombie with <b>Taunt</b>.
    events = Play(CONTROLLER, SPELL).on(Summon(CONTROLLER, "TRL_131t"))


class TRL_259:
    """Princess Talanji"""

    # <b>Battlecry:</b> Summon all minions from your hand that_didn't start in your_deck.
    play = Summon(CONTROLLER, FRIENDLY_HAND + MINION - STARTING_DECK)


class TRL_260:
    """Bwonsamdi, the Dead"""

    # [x]<b>Battlecry:</b> Draw 1-Cost minions from your deck until your hand is full.
    play = ForceDraw(RANDOM(FRIENDLY_DECK + MINION + (COST == 1))) * (
        MAX_HAND_SIZE(CONTROLLER) - Count(FRIENDLY_HAND)
    )


class TRL_408:
    """Grave Horror"""

    # [x]<b>Taunt</b> Costs (1) less for each spell you've cast this game.
    cost_mod = -Count(CARDS_PLAYED_THIS_GAME + SPELL)


class TRL_501:
    """Auchenai Phantasm"""

    # <b>Battlecry:</b> This turn, your healing effects deal damage instead.
    play = Buff(CONTROLLER, "TRL_501e")


TRL_501e = buff(embrace_the_shadow=True)


class TRL_502:
    """Spirit of the Dead"""

    # [x]<b>Stealth</b> for 1 turn. After a friendly minion dies, shuffle a 1-Cost copy of
    # it into your deck.
    events = (
        OWN_TURN_BEGIN.on(Unstealth(SELF)),
        Death(FRIENDLY_MINIONS).on(
            Shuffle(CONTROLLER, Buff(Copy(Death.ENTITY), "TRL_502e"))
        ),
    )


class TRL_502e:
    cost = SET(1)
    events = REMOVED_IN_PLAY


##
# Spells


class TRL_097:
    """Seance"""

    # Choose a minion. Add_a copy of it to your hand.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Give(CONTROLLER, Copy(TARGET))


class TRL_128:
    """Regenerate"""

    # Restore #3 Health.
    requirements = {
        PlayReq.REQ_TARGET_TO_PLAY: 0,
    }
    play = Heal(TARGET, 3)


class TRL_258:
    """Mass Hysteria"""

    # Force each minion to_attack another random minion.
    requirements = {
        PlayReq.REQ_MINION_TARGET: 0,
        PlayReq.REQ_ENEMY_TARGET: 0,
    }

    def play(self):
        board = ALL_MINIONS.eval(self.game, self)
        self.game.random.shuffle(board)
        for attacker in board:
            if attacker.dead:
                continue
            defenders = RANDOM(ALL_MINIONS - DEAD - SELF).eval(self.game, attacker)
            if defenders:
                defender = self.game.random.choice(defenders)
                yield Attack(attacker, defender)


class TRL_500:
    """Surrender to Madness"""

    # [x]Destroy 3 of your Mana Crystals. Give all minions in your deck +2/+2.
    play = (GainEmptyMana(CONTROLLER, -3), Buff(FRIENDLY_DECK + MINION, "TRL_500e"))


TRL_500e = buff(+2, +2)
