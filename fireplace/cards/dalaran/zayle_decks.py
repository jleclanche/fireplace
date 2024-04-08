from ..utils import *


# Rastakhan's Rumble
# https://www.youtube.com/watch?v=jlRV-7X0J8A
ZAYLE_DECK_STRINGS = [
    "AAECAaCsAwTtAfgC0P4C65sDDd0E5QT2B9UIpQnRCtIK8gyDlAOHlQOYmwOumwOCnQMA",
    "AAECAaIHCLICzQPtBef6AqCAA7SGA5KXA9KZAwu0Ae0CmwWIB90Ihgmm7wLOjAO0kQOPlwOQlwMA",
    "AAECAaoICrIGp+4C7/cCmfsCoIADwYkD0pgDuZkDxZkDhp0DCoEE9QTeBf4FrZEDtJEDipQDlZQDtJcDxpkDAA==",  # noqa: E501
    "AAECAf0GCtsG8wzC8QKc+ALN/AKggAOPggPShgOXlwOJnQMKkge2B8QIzAjF8wK09gLalgPCmQPamwODoAMA",
    "AAECAQcKuuwCze8Cm/ACkvgCjvsCoIADmocDm5QDkpgDwJgDCp3wApfzAtH1Ap77ArP8AvH8AvWAA5eUA5qUA4OgAwA=",  # noqa: E501
]


if "ZAYLE_DECKS" not in globals():
    ZAYLE_DECKS = [decode_deckstring(code) for code in ZAYLE_DECK_STRINGS]
