from ..utils import *


##
# Minions


class BOT_020:
    """Skaterbot"""

    # <b>Magnetic</b> <b>Rush</b>
    magnetic = MAGNETIC("BOT_020e")


BOT_020e = buff(rush=True)


class BOT_021:
    """Bronze Gatekeeper"""

    # <b>Magnetic</b> <b>Taunt</b>
    magnetic = MAGNETIC("BOT_021e")


BOT_021e = buff(taunt=True)


class BOT_031:
    """Goblin Bomb"""

    # [x]<b>Deathrattle:</b> Deal 2 damage to the enemy hero.
    deathrattle = Hit(ENEMY_HERO, 2)


class BOT_079:
    """Faithful Lumi"""

    # <b>Battlecry:</b> Give a friendly Mech +1/+1.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
        PlayReq.REQ_TARGET_WITH_RACE: 17,
        PlayReq.REQ_FRIENDLY_TARGET: 0,
        PlayReq.REQ_MINION_TARGET: 0,
    }
    play = Buff(TARGET, "BOT_079e")


BOT_079e = buff(+1, +1)


class BOT_083:
    """Toxicologist"""

    # <b>Battlecry:</b> Give your weapon +1 Attack.
    play = Buff(FRIENDLY_WEAPON, "BOT_083e")


BOT_083e = buff(atk=1)


class BOT_267:
    """Piloted Reaper"""

    # <b>Deathrattle:</b> Summon a random minion from your hand that costs (2) or less.
    deathrattle = Summon(CONTROLLER, RANDOM(FRIENDLY_HAND + MINION + (COST <= 2)))


class BOT_308:
    """Spring Rocket"""

    # <b>Battlecry:</b> Deal 2 damage.
    requirements = {
        PlayReq.REQ_TARGET_IF_AVAILABLE: 0,
    }
    play = Hit(TARGET, 2)


class BOT_413:
    """Brainstormer"""

    # [x]<b>Battlecry:</b> Gain +1 Health for each spell in your hand.
    play = Buff(SELF, "BOT_413e") * Count(FRIENDLY_HAND + SPELL)


BOT_413e = buff(health=1)


class BOT_431:
    """Whirliglider"""

    # <b>Battlecry:</b> Summon a 0/2_Goblin Bomb.
    play = Summon(CONTROLLER, "BOT_031")


class BOT_445:
    """Mecharoo"""

    # <b>Deathrattle:</b> Summon a 1/1 Jo-E Bot.
    deathrattle = Summon(CONTROLLER, "BOT_445t")


class BOT_448:
    """Damaged Stegotron"""

    # <b>Taunt</b> <b>Battlecry:</b> Deal 6 damage to this minion.
    play = Hit(SELF, 6)


class BOT_532:
    """Explodinator"""

    # <b>Battlecry:</b> Summon two 0/2 Goblin Bombs.
    play = SummonBothSides(CONTROLLER, "BOT_031") * 2


class BOT_535:
    """Microtech Controller"""

    # <b>Battlecry:</b> Summon two 1/1 Microbots.
    play = SummonBothSides(CONTROLLER, "BOT_312t") * 2


class BOT_550:
    """Electrowright"""

    # <b>Battlecry:</b> If you're holding a spell that costs (5) or more, gain +1/+1.
    play = Find(FRIENDLY_HAND + SPELL + (COST >= 5)) & Buff(SELF, "BOT_550e")


BOT_550e = buff(+1, +1)


class BOT_562:
    """Coppertail Imposter"""

    # <b>Battlecry:</b> Gain <b>Stealth</b> until your next turn.
    play = Stealth(SELF), Buff(SELF, "BOT_562e")


class BOT_562e:
    events = OWN_TURN_BEGIN.on(Unstealth(OWNER), Destroy(SELF))


class BOT_563:
    """Wargear"""

    # <b>Magnetic</b>
    magnetic = MAGNETIC("BOT_563e")


class BOT_606:
    """Kaboom Bot"""

    # <b>Deathrattle:</b> Deal 4_damage to a random enemy minion.
    deathrattle = Hit(RANDOM_ENEMY_MINION, 4)
