from ..utils import *


# Where can I find a list of all the current Whizbang decks?

# The Boomsday Project
# https://www.hearthpwn.com/decks/1163078-all-whizbang-decks-for-your-decktracker
WHIZBANG_DECK_STRINGS = [
    "AAECAQcIqgbTwwKZxwLN7wKb8AKe+AKO+wKggAMLS5EDogT/B5vCAsrDAqLHAsrnAqrsArrsAvLxAgA=",
    "AAECAQcEze8Cm/ACkvgCoIADDZEGzM0CuuwCnfACl/MCn/UCpfUC5PcCjvgCg/sCqPsCs/wCzIEDAA==",
    "AAECAaoICooB7QXAB8/HApvLAsLOAqrsAqfuAoH2Ap79AgqBBPUE/gX/BcfBAvPnApbvAvbwAoqAA5eAAwA=",
    "AAECAaoIBMAH88ICofgCmfsCDb0B+QOGBvAHkwnrwgKw8AL28AKz9wLq+gKP+wKc/wKKgAMA",
    "AAECAaIHBLICgNMC6/ACqPcCDbQBywObBYYJgcIC68ICm8gC5dEC2+MC6vMCt/UCovcCx/gCAA==",
    "AAECAaIHCIwC7QX7BeXRAs/hAvDmAtjpAp/4Agu0AYHCAqvCAuvCAtvjAurmArT2At76Auz8Avb9AtGBAwA=",
    "AAECAZ8FBvoGucEC4fACzfQC6/cC/fsCDNwD9AXPBq8HsQizwQKIxwLZxwKbywK35wL27ALZ/gIA",
    "AAECAZ8FBvQFzwb6BrnBAvH+AqCAAwzcA48Js8EC48sCn/UCpfUC1v4C2f4C4f4CkYAD0YADzIEDAA==",
    "AAECAR8EhwTp0gKG0wLy6gINjQGoArUDyQSXCNsJ/gzd0gLf0gLj0gLh4wLq4wKH+wIA",
    "AAECAR8C4fUCoIADDo0Bigbh4wKf9QLg9QLi9QLv9QKZ9wK5+AKR+wKY+wKE/QL2/QLMgQMA",
    "AAECAZICBMnCAofOAsLOApnTAg1AX8QG5AiU0gKY0gKo0gKL4QKE5gKL5gL15wLf+wLo/AIA",
    "AAECAZICAiTF/QIO/QLtA/cD5gWxCIbBAqTCAuvCAtfvAsHzAt/7AuH7Ar/9AtWDAwA=",
    "AAECAf0GApfTApz4Ag6KAbYHxAjnywLy0AL40AKI0gL85QLq5gLo5wK38QLF8wL8+gKPgAMA",
    "AAECAf0GApfTAo+CAw4w9wTCCPYIm8sC980C8dAC8tAC9PcC0/gCqvkCt/0Cw/0C+v4CAA==",
    "AAECAf0EBNACvwib0wKj6wINTYoByQPsB/sMysMClscCx8cC29MC1eEC1+ECluQC1+sCAA==",
    "AAECAf0EAqLTAu72Ag67ApUDvwOrBLQElgW/wQL77AKS7wK89wKj/QKV/wK5/wLvgAMA",
    "AAECAa0GBMnCApbEAsv4Ao2CAw37AeUE0wryDKvCAubMAvDPAujQAovhAoL3AqH+AvX+AoiCAwA=",
    "AAECAa0GBKIJvsgC2OMCy/gCDfgC5QSNCNEK8gzRwQLYwQLL5gKC9wLl9wL1/gLxgAPeggMA",
]

# Rastakhan's Rumble
# https://ds.163.com/article/5c0601af8ec3326ecc6ac82f/
WHIZBANG_DECK_STRINGS = [
    "AAECAZICBpkC/M0CmdMCm+gC9fwCwYYDDEC0BeYFmgjrwgKHzgKY0gKm7wKYhgPAhgPGhgPPiQMA",
    "AAECAZICAiTF/QIO/QLtA/cD5gWxCIbBAqTCAuvCAtfvAsHzAt/7Ar/9AtWDA7SJAwA=",
    "AAECAf0EBNACm9MCo+sCr4cDDU2KAckD7Af7DMrDApbHAtvTAtXhAtfhApbkAtfrAs2JAwA=",
    "AAECAf0ECNACxQT7DNPFApvTAu72Ap74AqiHAwvsB5vCAuvCAsrDAtfhApbkArfxAr36AqSHA6aHA82JAwA=",
    "AAECAaIHBM0D18oCzfQC1owDDbQBiAfnB4YJ3NEC2+MC3+8CovcCqv8CroUDz4kDzowD24wDAA==",
    "AAECAaIHBvYEi+ECz+ECnOICn/gCi4oDDLQBjAKGCYHCAqvCAuvCAtvjArT2At76Auz8AtGBA86MAwA=",
    "AAECAR8IhwTFCN3SAunSAobTAvLqApuFA6KKAwuoArUDyQSXCNsJ/gzf0gLj0gLh4wLq4wKH+wIA",
    "AAECAR8G7QmG0wKA8wLqiQOiigPjiwMMqAK1A+sH2wmBCo7DAtfNAt3SAovlAqCFA7CLA+SLAwA=",
    "AAECAa0GBpvCAsnHAsrLApziAqeHA8CPAwzlBPIM+wzKwwKbywLo0ALL5gKJ8QLeggPqiAOwiQPsiQMA",
    "AAECAa0GAqUJvsgCDvgC5QT2B9EK0gryDPsM0cEC2MEC5fcC5ogDi4kD0okD64oDAA==",
    "AAECAZ8FBuPjApvwAv37Atn+Ar2GA+OGAwzcA/QFrwf2B8rDAojHAuPLAvnsAt6GA+aGA+yGA++GAwA=",
    "AAECAZ8FBvQF+ga5wQLx/gKggAPehgMM3AOPCbPBAuPLAp/1AqX1Atb+Atn+AuH+ApGAA9GAA8yBAwA=",
    "AAECAaoIDN4F7QX/BYoHwAfPxwLCzgLD6gKn7gLv9wLq+gLzigMJgQT1BP4Fx8ECm8sC8+cCm/8CioADl4ADAA==",
    "AAECAaoIBpMJ688CsPAC4vgCmfsCy4UDDPAHkcEC68ICysMCm8sC+9MC3+kCm/8CnP8CvYUD24kD5YkDAA==",
    "AAECAf0GApfTAvKGAw4w9wTCCPYI68ICm8sC980C8dAC8tAC9PcC0/gCw/0C6YYD3YkDAA==",
    "AAECAf0GBJTHArjQAo+CA/CGAw0w0AT3BM4HwgjrwgKRxwKSzQL3zQLx0ALy0ALWhgOvjQMA",
    "AAECAQcGkAf/B6IJ+wz4hgOShwMMogTJxwLMzQKJ8QKb8wL09QKBhwOLhwPoiQPsiQOqiwPolAMA",
    "AAECAQcEze8Cm/ACkvgCoIADDczNArrsAp3wApfzAp/1AqX1AuT3Ao74AoP7Aqj7ArP8AsyBA/iGAwA=",
]

# Rise of Shadows
# https://www.hearthpwn.com/forums/hearthstone-general/general-discussion/232894-whizbang-the-wonderful-rise-of-shadows-deck
WHIZBANG_DECK_STRINGS = [
    "AAEBAZICBpvwAvX8AtOUA8qcA5egBNj2BQxAVvr+ArmUA8+UA7ufA9qfBI+gBJCgBKygBIDUBIPUBAAA",
    "AAEBAZICBMX9AsOUA9efBN6fBA3mBbEI1+8C4fsCv/0C1YMDtIkDzpQDypwD05wD2Z8E3Z8EtaAEAAA=",
    "AAEBAR8C44sDiNQEDqgC3gTrB9sJoooD5IsDnp0Dx50D358E4J8EpKAEv6AEidQEjqQFAAA=",
    "AAEBAR8Em4UD8ZYD+ZYD2PYFDeD1AuL1Au/1ArT2Arn4Aof7Avb9AvKWA7acA6mfBInUBI6kBbmkBgAA",
    "AAEBAf0EBLgI++wCl6AEs54GDbQE5gSWBZX/AqOHA8iHA4mWA5+bA+KbA/+dA/yeBP2eBMKgBAAA",
    "AAEBAf0ECMUEr4cD55UDg5YDlpoD79MEnNQE2PYFC03LBJYFw/gCn5sDoJsD/J4E/Z4E/p4E8dMEndQEAAA=",
    "AAEBAZ8FAq8ElJoDDkaMAZ4BsQit8gLY/gL1iQOOmgOQmgOanwSdnwTqnwSVoATQoAQAAA==",
    "AAEBAZ8FCtIEm/AC/fsChPwCvYYD3oYD44YDzocDnNQE2PYFCvnsAuaGA++GA4qaA7SbA5qfBJyfBO6fBJLUBKHUBAAA",
    "AAEBAa0GBND+AoOgA9j2BbeeBg3tAeUE0QrSCtcK8vEC+/4Cl4cDg5QDmJsDmZsDkKAE9NMEAAA=",
    "AAEBAa0GBqUJ5fcCi4oDgpQD65sD2PYFDO0B5QTSCtz1ArT2AqH+AuuIA++SA4OUA42XA8GfBPTTBAAA",
    "AAEBAaIHCLIC7/MCqPcC5/oCzowDr5EDiJsDi6QFC8f4AqiYA/uaA/6aA5GfBPWfBPefBJWgBIykBb2eBtmiBgAA",
    "AAEBAaIHBrICyAPOjAPWjAPbjAP1nwQM1AXf7wKq/wLPiQORnwT3nwStoASvoASMpAW/+AW9ngbZogYAAA==",
    "AAEBAaoIBKIJp+4CgKAE2PYFDZQDn/0Cm/8CioUDvYUD84oDrZEDipQDj5QDxJkDr58E/Z8EhdQEAAA=",
    "AAEBAaoIArWYA5ybAw6/Af4D4wXw8wLeggPiiQOMlAPGmQP0mQO1nwSioASroATu0wTy3QQAAA==",
    "AAEBAf0GCPIFkgec+AKXlwOsnwSDoASsoATY9gUL+wbhB4+AA8KZA4+fBLGfBIKgBI+gBJ3UBKXUBNWeBgAA",
    "AAEBAf0GAA/VA84HsQie8QL09wLD/QKrkQO/mAOAmgOHnQOEoASkoATmoAT50wSi1AQAAA==",
    "AAEBAQcIuPYCkvgCmocDm4oD9pYDtJ8Ei6AE2PYFC/LxApvzAo77AtiMA5aUA5mUA5+fBIagBIigBImgBI7UBAAA",
    "AAEBAQcIkAeiCd6CA/iGA5KHA72ZA47UBJzUBAuJ8QKb8wL09QKBhwOLhwPoiQPsiQOqiwPolAPCmQOJoAQAAA==",
]

# Saviours of Uldum
# https://www.hearthpwn.com/decks/1299114-uldum-whizbang-all-codes-for-hearthstone-deck
WHIZBANG_DECK_STRINGS = [
    "AAECAZICBiRfrtIC9fwCyZwD+KEDDEBWigH3A8QGi+4C4fsCypwDr6IDyKID3KID2akDAA==",
    "AAECAZICBpvwAvX8AqCAA9OUA8mcA9ulAwxAVpMExAaYB+QI6PwCuZQDypwDu58Dr6IDyKIDAA==",
    "AAECAR8GuwXtCcn4AuOLA+aWA6SlAwy1A94E2wmBCvbsAqCFA6SIA9ePA56dA8edA+SkA5ipAwA=",
    "AAECAR8Gh/sCoIADm4UD8ZYD+ZYDn7cDDLUDlwjg9QLi9QLv9QLw9QK09gK5+AKY+wL2/QLylgO2nAMA",
    "AAECAf0EHk2KAbsCiwPJA6sEywSWBd4F8gWKB+wH+wzL7AKe8AK38QLF8wLG+AKggAOvhwPsiQPnlQO9mQOfmwOKngOhoQP8owOSpAO/pAOEpwMAAA==",
    "AAECAf0EBO0FuAju9gKJlgMNuwKrBLQE5gSWBZX/Arn/AqOHA8iHA5+bA+KbA/+dA4ipAwA=",
    "AAECAZ8FHooB3APSBN4F8gX0Bc8G+gaKB68H9gf+B48J+wz57AKb8AL9+wKE/ALd/gKggAO9hgPjhgPshgPsiQODoQOhoQP8owPDpAOEpwOWrAMAAA==",
    "AAECAZ8FBowBrwTIBMD9AqeCA5SaAwyeAc8G7gavB63yAtj+AvWJA/mTA76YA46aA5CaA8OkAwA=",
    "AAECAa0GBqCAA4OUA6mlA7ulA9OlA92rAwz4AuUE9gfVCNEK0gryDPsMvfMC5fcC0qUDhKgDAA==",
    "AAECAa0GCNcKvfMC+/4CoIAD1pkDk5sDg6ADn6kDC/gC5QTRCtMK8vECl4cD/okDgpQDmJsDmZsD0qUDAA==",
    "AAECAaIHBLIC6/ACtIYDp6gDDbQBmwWIB90IhgnH+AKPlwOQlwP7mgP+mgO7pQOqqAOtqAMA",
    "AAECAaIHBrICyAPdCKbvAtaMA9uMAwy0AagF1AWIB+cHhgnf7wKq/wLVjAOPlwOQlwP/pQMA",
    "AAECAaoICqbwAu/3AqH4Aur6ArmZA72ZA8WZA9qdA4SnA+GoAwr1BN4F/gWyBu/xAq2RA7SRA8aZA7ulA8+lAwA=",
    "AAECAaoIAt6CA5ybAw7FA9sD/gPjBdAHpwiTCeKJA4yUA7WYA8aZA/SZA6+nA8qrAwA=",
    "AAECAf0GCtsGxAjMCMLxApz4AqCAA4+CA5eXA4mdA+ujAwowtgfzDMXzAtqWA8KZA9qbA6GhA7ulA9KlAwA=",
    "AAECAf0GAA8w0wHOB9kHsQjCCJDuAp7xAvT3AquRA7+YA4CaA4edA4idA/qkAwA=",
    "AAECAQcES6CAA/KoA/eoAw3/A6IE/wf7DJ3wApvzAvT1Ap77ArP8AoiHA5+hA/WoA/aoAwA=",
    "AAECAQcK0gL8BLj2ApL4AoP7AqCAA5qHA5uKA/aWA9+pAwpLogSRBv8Hsgjy8QKb8wKO+wLYjAOWlAMA",
]

if "WHIZBANG_DECKS" not in globals():
    WHIZBANG_DECKS = [decode_deckstring(code) for code in WHIZBANG_DECK_STRINGS]
