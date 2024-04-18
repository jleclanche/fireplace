from ..utils import *


##
# Minions


class OG_109:
    """Darkshire Librarian"""

    play = Discard(RANDOM(FRIENDLY_HAND))
    deathrattle = Draw(CONTROLLER)


class OG_113:
    """Darkshire Councilman"""

    events = Summon(CONTROLLER, MINION).on(Buff(SELF, "OG_113e"))


OG_113e = buff(atk=1)


class OG_121:
    """Cho'gall"""

    play = Buff(CONTROLLER, "OG_121e")


class OG_121e:
    events = OWN_SPELL_PLAY.on(Destroy(SELF))
    update = Refresh(CONTROLLER, {GameTag.SPELLS_COST_HEALTH: True})


class OG_241:
    """Possessed Villager"""

    deathrattle = Summon(CONTROLLER, "OG_241a")


class OG_302:
    """Usher of Souls"""

    events = Death(FRIENDLY_MINIONS).on(Buff(CTHUN, "OG_281e", atk=1, max_health=1))


##
# Spells


class OG_116:
    """Spreading Madness"""

    play = Hit(RANDOM_CHARACTER, 1) * 9


class OG_118:
    """Renounce Darkness"""

    def play(self):
        classes = [
            (CardClass.DEMONHUNTER, "HERO_10bp"),
            (CardClass.DRUID, "HERO_06bp"),
            (CardClass.HUNTER, "HERO_05bp"),
            (CardClass.MAGE, "HERO_08bp"),
            (CardClass.PALADIN, "HERO_04bp"),
            (CardClass.PRIEST, "HERO_09bp"),
            (CardClass.ROGUE, "HERO_03bp"),
            (CardClass.SHAMAN, "HERO_02bp"),
            (CardClass.WARRIOR, "HERO_01bp"),
        ]
        hero_class, hero_power = random.choice(classes)
        yield Summon(CONTROLLER, hero_power)
        yield Morph(
            FRIENDLY + WARLOCK + (IN_HAND | IN_DECK),
            RandomCollectible(card_class=hero_class),
        ).then(Buff(Morph.CARD, "OG_118f"))


class OG_118f:
    events = REMOVED_IN_PLAY
    tags = {GameTag.COST: -1}


class OG_239:
    """DOOM!"""

    def play(self):
        minion_count = Count(ALL_MINIONS).evaluate(self)
        yield Destroy(ALL_MINIONS)
        yield Draw(CONTROLLER) * minion_count


class OG_114:
    """Forbidden Ritual"""

    play = SpendMana(CONTROLLER, CURRENT_MANA(CONTROLLER)).then(
        Summon(CONTROLLER, "OG_114a") * SpendMana.AMOUNT
    )
