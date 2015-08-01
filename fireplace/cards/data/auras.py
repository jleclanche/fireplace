"""
Aura card definitions
"""
from fireplace.enums import AuraType, PlayReq, Race


# Raid Leader
CS2_122 = [{
	"id": "CS2_122e",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_NONSELF_TARGET: True,
	},
}]

# Stormwind Champion
CS2_222 = [{
	"id": "CS2_222o",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_NONSELF_TARGET: True,
	},
}]

# Spiteful Smith
CS2_221 = [{
	"id": "CS2_221e",
	"requirements": {
		PlayReq.REQ_SOURCE_IS_ENRAGED: True,
		PlayReq.REQ_WEAPON_TARGET: True,
	},
}]

# Venture Co. Mercenary
CS2_227 = [{
	"id": "CS2_227a",
	"requirements": {
		PlayReq.REQ_MINION_TARGET: True,
	},
	"type": AuraType.HAND_AURA,
}]

# Timber Wolf
DS1_175 = [{
	"id": "DS1_175o",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_NONSELF_TARGET: True,
		PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
	},
}]

# Tundra Rhino
DS1_178 = [{
	"id": "DS1_178e",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_TARGET_WITH_RACE: Race.BEAST,
	},
}]

# Pint-Sized Summoner
EX1_076 = [{
	"id": "EX1_076a",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_MINION_TARGET: True,
		PlayReq.REQ_NO_MINIONS_PLAYED_THIS_TURN: True,
	},
	"type": AuraType.HAND_AURA,
}]

# Dire Wolf Alpha
EX1_162 = [{
	"id": "EX1_162o",
}]

# Summoning Portal
EX1_315 = [{
	"id": "EX1_315a",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_MINION_TARGET: True,
	},
	"type": AuraType.HAND_AURA,
}]

# Prophet Velen
EX1_350 = [{
	"id": "EX1_350a",
	"type": AuraType.PLAYER_AURA,
}]

# Murloc Warleader
EX1_507 = [{
	"id": "EX1_507e",
	"requirements": {
		PlayReq.REQ_NONSELF_TARGET: True,
		PlayReq.REQ_TARGET_WITH_RACE: Race.MURLOC,
	},
}]

# Grimscale Oracle
EX1_508 = [{
	"id": "EX1_508o",
	"requirements": {
		PlayReq.REQ_NONSELF_TARGET: True,
		PlayReq.REQ_TARGET_WITH_RACE: Race.MURLOC,
	},
}]

# Flametongue Totem
EX1_565 = [{
	"id": "EX1_565o",
}]

# Auchenai Soulpriest
EX1_591 = [{
	"id": "EX1_591a",
	"type": AuraType.PLAYER_AURA,
}]

# Sorcerer's Apprentice
EX1_608 = [{
	"id": "EX1_608a",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_SPELL_TARGET: True,
	},
	"type": AuraType.HAND_AURA,
}]

# Power of the Kirin Tor (Kirin Tor Mage)
EX1_612oa = [{
	"id": "EX1_612o",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_SECRET_TARGET: True,
	},
	"type": AuraType.HAND_AURA,
}]

# Mana Wraith
EX1_616 = [{
	"id": "EX1_616a",
	"requirements": {
		PlayReq.REQ_MINION_TARGET: True,
	},
	"type": AuraType.HAND_AURA,
}]

# Nerub'ar Weblord
FP1_017 = [{
	"id": "FP1_017a",
	"requirements": {
		PlayReq.REQ_MINION_TARGET: True,
		PlayReq.REQ_TARGET_HAS_BATTLECRY: True,
	},
	"type": AuraType.HAND_AURA,
}]

# Necrotic Aura (Loatheb)
FP1_030e = [{
	"id": "FP1_030ea",
	"requirements": {
		PlayReq.REQ_ENEMY_TARGET: True,
		PlayReq.REQ_SPELL_TARGET: True,
	},
	"type": AuraType.HAND_AURA,
}]


# Preparation
EX1_145o = [{
	"id": "EX1_145oa",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_SPELL_TARGET: True,
	},
	"type": AuraType.HAND_AURA,
}]

# Baron Rivendare
FP1_031 = [{
	"id": "FP1_031a",
	"type": AuraType.PLAYER_AURA,
}]

# Mechwarper
GVG_006 = [{
	"id": "GVG_006a",
	"requirements": {
		PlayReq.REQ_MINION_TARGET: True,
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_TARGET_WITH_RACE: Race.MECHANICAL,
	},
	"type": AuraType.HAND_AURA,
}]

# Mal'Ganis
GVG_021 = [{
	"id": "GVG_021e",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_NONSELF_TARGET: True,
		PlayReq.REQ_TARGET_WITH_RACE: Race.DEMON,
	},
}, {
	"id": "GVG_021e2",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_HERO_TARGET: True,
	},
}]

# Steamwheedle Sniper
GVG_087 = [{
	"id": "GVG_087a",
	"type": AuraType.PLAYER_AURA,
}]

# Wee Spellstopper
GVG_122 = [{
	"id": "GVG_122a",
}]

# Southsea Captain
NEW1_027 = [{
	"id": "NEW1_027e",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_NONSELF_TARGET: True,
		PlayReq.REQ_TARGET_WITH_RACE: Race.PIRATE,
	},
}]

# Kill Millhouse!
NEW1_029t = [{
	"id": "NEW1_029ta",
	"requirements": {
		PlayReq.REQ_ENEMY_TARGET: True,
		PlayReq.REQ_SPELL_TARGET: True,
	},
	"type": AuraType.HAND_AURA,
}]

# Leokk
NEW1_033 = [{
	"id": "NEW1_033o",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
		PlayReq.REQ_NONSELF_TARGET: True,
	},
}]

# Free Cards
XXX_022e = [{
	"id": "XXX_022ea",
	"requirements": {
		PlayReq.REQ_FRIENDLY_TARGET: True,
	},
	"type": AuraType.HAND_AURA,
}]
