import utils
import pytest
from hearthstone.enums import CardType, GameTag, Rarity


CARDS = utils.fireplace.cards.db


# def test_all_tags_known():
#     """
#     Iterate through the card database and check that all specified GameTags
#     are known in hearthstone.enums.GameTag
#     """
#     unknown_tags = set()
#     known_tags = list(GameTag)
#     known_rarities = list(Rarity)
#
#     # Check the db loaded correctly
#     assert utils.fireplace.cards.db
#
#     for card in CARDS.values():
#         for tag in card.tags:
#             # We have fake tags in fireplace.enums which are always negative
#             if tag not in known_tags and tag > 0:
#                 unknown_tags.add(tag)
#
#         # Test rarities as well (cf. TB_BlingBrawl_Blade1e in 10956...)
#         assert card.rarity in known_rarities
#
#     assert not unknown_tags


def test_play_scripts():
    for card in CARDS.values():
        if card.scripts.activate:
            assert card.type in (CardType.HERO_POWER, CardType.SPELL, CardType.MINION)
        elif card.scripts.play:
            assert card.type not in (CardType.HERO_POWER, CardType.ENCHANTMENT)


def test_battlecry_scripts():
    for card in CARDS.values():
        if card.battlecry and card.collectible:
            if card.id in ["DRG_308", "GIL_614", "ULD_003"]:
                continue
            assert card.scripts.play


def test_deathrattle_scripts():
    for card in CARDS.values():
        if card.deathrattle and card.collectible:
            if card.id in ["BOT_558", "DRG_086", "ULD_163", "UNG_953", "BT_126"]:
                continue
            assert card.scripts.deathrattle


def test_card_docstrings():
    for card in CARDS.values():
        if card.locale != "enUS":
            continue
        c = utils.fireplace.cards.get_script_definition(card.id)
        name = c.__doc__
        if name is not None:
            if name.endswith(")"):
                continue
            assert name == card.name
