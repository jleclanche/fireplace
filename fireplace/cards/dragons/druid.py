from ..utils import *


##
# Minions


class DRG_312:
    """Shrubadier"""

    # <b>Battlecry:</b> Summon a 2/2_Treant.
    play = Summon(CONTROLLER, "DRG_311t")


class DRG_313:
    """Emerald Explorer"""

    # <b>Taunt</b> <b>Battlecry:</b> <b>Discover</b> a Dragon.
    play = DISCOVER(RandomDragon())


class DRG_319:
    """Goru the Mightree"""

    # [x]<b>Taunt</b> <b>Battlecry:</b> For the rest of the game, your Treants have +1/+1.
    play = Buff(CONTROLLER, "DRG_319e4")


class DRG_319e4:
    update = Refresh(FRIENDLY_MINIONS + TREANT, buff="DRG_319e5")


DRG_319e5 = buff(+1, +1)


class DRG_320:
    """Ysera, Unleashed"""

    # [x]<b>Battlecry:</b> Shuffle 7 Dream Portals into your deck. When drawn, summon a
    # random Dragon.
    play = Shuffle(CONTROLLER, "DRG_320t") * 7


class DRG_320t:
    play = Summon(CONTROLLER, RandomDragon())
    draw = CAST_WHEN_DRAWN


##
# Spells


class DRG_051:
    """Strength in Numbers"""

    # <b>Sidequest:</b> Spend 10 Mana on minions. <b>Reward:</b> Summon a minion from your
    # deck.
    progress_total = 10
    sidequest = SpendMana(CONTROLLER, source=MINION).after(
        AddProgress(SELF, CONTROLLER, SpendMana.AMOUNT)
    )
    reward = Summon(CONTROLLER, RANDOM(FRIENDLY_DECK + MINION))


class DRG_311:
    """Treenforcements"""

    # [x]<b>Choose One -</b> Give a minion +2 Health and <b>Taunt</b>; or Summon a 2/2
    # Treant.
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    choose = ("DRG_311a", "DRG_311b")
    play = ChooseBoth(CONTROLLER) & (
        Buff(TARGET, "DRG_311e"),
        Summon(CONTROLLER, "DRG_311t"),
    )


class DRG_311a:
    requirements = {PlayReq.REQ_NUM_MINION_SLOTS: 1}
    play = Summon(CONTROLLER, "DRG_311t")


class DRG_311b:
    requirements = {PlayReq.REQ_MINION_TARGET: 0, PlayReq.REQ_TARGET_TO_PLAY: 0}
    play = Buff(TARGET, "DRG_311e")


class DRG_314:
    """Aeroponics"""

    # Draw 2 cards. Costs (2) less for each Treant you control.
    cost_mod = -Count(FRIENDLY_MINIONS + TREANT) * 2
    play = Draw(CONTROLLER) * 2


class DRG_315:
    """Embiggen"""

    # Give all minions in your deck +2/+2. They cost (1) more <i>(up to 10)</i>.
    play = MultiBuff(FRIENDLY_DECK + MINION, ["DRG_315e", "DRG_315e2"])


DRG_315e = buff(+2, +2)


class DRG_315e2:
    cost = lambda self, i: i if i >= 10 else i + 1
    events = REMOVED_IN_PLAY


class DRG_317:
    """Secure the Deck"""

    # <b>Sidequest:</b> Attack twice with your hero. <b>Reward:</b> Add 3 'Claw' spells to
    # your hand.
    progress_total = 2
    sidequest = Attack(FRIENDLY_HERO).after(AddProgress(SELF, FRIENDLY_HERO))
    reward = Give(CONTROLLER, "CS2_005") * 3


class DRG_318:
    """Breath of Dreams"""

    # Draw a card. If you're holding a Dragon, gain an empty Mana Crystal.
    powered_up = HOLDING_DRAGON
    play = Draw(CONTROLLER), powered_up & GainEmptyMana(CONTROLLER, 1)
