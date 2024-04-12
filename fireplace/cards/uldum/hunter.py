from ..utils import *


##
# Minions


class ULD_151:
    """Ramkahen Wildtamer"""

    # <b>Battlecry:</b> Copy a random Beast in your hand.
    play = Give(CONTROLLER, Copy(RANDOM(FRIENDLY_HAND + BEAST)))


class ULD_154:
    """Hyena Alpha"""

    # [x]<b>Battlecry:</b> If you control a <b>Secret</b>, summon two 2/2 Hyenas.
    powered_up = Find(FRIENDLY_SECRETS)
    play = powered_up & Summon(CONTROLLER, "ULD_154t") * 2


class ULD_156:
    """Dinotamer Brann"""

    # <b>Battlecry:</b> If your deck has no duplicates, summon King Krush.
    powered_up = -FindDuplicates(FRIENDLY_DECK)
    play = powered_up & Summon(CONTROLLER, "ULD_156t3")


class ULD_212:
    """Wild Bloodstinger"""

    # <b>Battlecry:</b> Summon a minion from your opponent's hand. Attack it.
    play = Summon(OPPONENT, RANDOM(ENEMY_HAND + MINION)).then(Attack(SELF, Summon.CARD))


class ULD_410:
    """Scarlet Webweaver"""

    # <b>Battlecry:</b> Reduce the Cost of a random Beast in your_hand by (5).
    play = Buff(RANDOM(FRIENDLY_HAND + BEAST), "ULD_410e")


class ULD_410e:
    tags = {GameTag.COST: -5}
    events = REMOVED_IN_PLAY


##
# Spells


class ULD_152:
    """Pressure Plate"""

    # <b>Secret:</b> After your opponent casts a spell, destroy a random enemy_minion.
    secret = Play(OPPONENT, SPELL).after(Reveal(SELF), Destroy(RANDOM_ENEMY_MINION))


class ULD_155:
    """Unseal the Vault"""

    # <b>Quest:</b> Summon 20_minions. <b>Reward:</b> Pharaoh's Warmask.
    progress_total = 20
    quest = Summon(CONTROLLER, MINION).on(AddProgress(SELF, Summon.CARD))
    reward = Summon(CONTROLLER, "ULD_155p")


class ULD_155p:
    """Pharaoh's Warmask"""

    # <b>Hero Power</b> Give your minions +2_Attack.
    activate = Buff(FRIENDLY_MINIONS, "ULD_155e")


ULD_155e = buff(atk=2)


class ULD_429:
    """Hunter's Pack"""

    # Add a random Hunter Beast, <b>Secret</b>, and weapon to your_hand.
    play = (
        Give(CONTROLLER, RandomBeast(card_class=CardClass.HUNTER)),
        Give(CONTROLLER, RandomSpell(secret=True, card_class=CardClass.HUNTER)),
        Give(CONTROLLER, RandomWeapon(card_class=CardClass.HUNTER)),
    )


class ULD_713:
    """Swarm of Locusts"""

    # Summon seven 1/1 Locusts with <b>Rush</b>.
    requirements = {
        PlayReq.REQ_NUM_MINION_SLOTS: 1,
    }
    play = Summon(CONTROLLER, "ULD_430t") * 7


##
# Weapons


class ULD_430:
    """Desert Spear"""

    # After your hero attacks, summon a 1/1 Locust with <b>Rush</b>.
    events = Attack(FRIENDLY_HERO).after(Summon(CONTROLLER, "ULD_430t"))
