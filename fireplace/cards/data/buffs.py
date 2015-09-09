from fireplace.enums import GameTag


# Buff helper
def buff(atk=0, health=0):
	ret = {}
	if atk:
		ret[GameTag.ATK] = atk
	if health:
		ret[GameTag.HEALTH] = health
	return ret


###
# Game/Brawl set
#

TB_006e = buff(+2, +2)

TB_Pilot1 = {
	GameTag.DEATHRATTLE: True,
}

###
# Classic set
#


##
# Druid

# Claws
CS2_017o = buff(atk=1)

# Soul of the Forest
EX1_158e = {
	GameTag.DEATHRATTLE: True,
}

# Rooted (Ancient of War)
EX1_178ae = {
	GameTag.HEALTH: 5,
	GameTag.TAUNT: True,
}

# Uproot (Ancient of War)
EX1_178be = buff(atk=5)

# Claw
CS2_005o = buff(atk=2)

# Mark of the Wild
CS2_009e = {
	GameTag.ATK: 2,
	GameTag.HEALTH: 2,
	GameTag.TAUNT: True,
}

# Savage Roar
CS2_011o = buff(atk=2)

# Mark of Nature (Attack)
EX1_155ae = buff(atk=4)

# Mark of Nature (Health)
EX1_155be = {
	GameTag.HEALTH: 4,
	GameTag.TAUNT: True,
}

# Leader of the Pack (Power of the Wild)
EX1_160be = buff(+1, +1)

# Bite
EX1_570e = buff(atk=4)

# Demigod's Favor (Cenarius)
EX1_573ae = buff(+2, +2)


##
# Hunter

# Master's Presence (Houndmaster)
DS1_070o = {
	GameTag.ATK: 2,
	GameTag.HEALTH: 2,
	GameTag.TAUNT: True,
}

# Furious Howl (Timber Wolf)
DS1_175o = buff(atk=1)

# Charge (Tundra Rhino)
DS1_178e = {
	GameTag.CHARGE: True,
}

# Well Fed (Scavenging Hyena)
EX1_531e = buff(+2, +1)

# Bestial Wrath

EX1_549o = {
	GameTag.ATK: 2,
	GameTag.CANT_BE_DAMAGED: True,
}

# Trapped (Freezing Trap)
EX1_611e = {
	GameTag.COST: 2,
}

# Eye in the Sky (Leokk)
NEW1_033o = buff(atk=1)

# Upgraded (Eaglehorn Bow)
EX1_536e = buff(health=1)


##
# Mage

# Raw Power! (Ethereal Arcanist)
EX1_274e = buff(+2, +2)

# Mana Gorged (Mana Wyrm)
NEW1_012o = buff(atk=1)

# Ice Block
EX1_295o = {
	GameTag.CANT_BE_DAMAGED: True,
}


##
# Paladin

# Blessing of Might
CS2_087e = buff(atk=3)

# Blessing of Kings
CS2_092e = buff(+4, +4)

# Justice Served (Sword of Justice)
EX1_366e = buff(+1, +1)


##
# Priest

# Warded (Lightwarden)
EX1_001e = buff(atk=2)

# Infusion (Temple Enforcer)
EX1_623e = buff(health=3)

# Power Word: Shield
CS2_004e = buff(health=2)

# Shadow Madness
EX1_334e = {
	GameTag.CHARGE: True,
}


##
# Rogue

# VanCleef's Vengeance (Edwin VanCleef)
EX1_613e = buff(+2, +2)

# Cold Blood (+2)
CS2_073e = buff(atk=2)

# Cold Blood (+4)
CS2_073e2 = buff(atk=4)

# Deadly Poison
CS2_074e = buff(atk=2)

# Sharpened (Unused)
CS2_083e = buff(atk=1)


##
# Shaman

# Overloading (Unbound Elemental)
EX1_258e = buff(+1, +1)

# Flametongue (Flametongue Totem)
EX1_565o = buff(atk=2)

# Ancestral Spirit
CS2_038e = {
	GameTag.DEATHRATTLE: True,
}

# Ancestral Infusion (Ancestral Healing)
CS2_041e = {
	GameTag.TAUNT: True,
}

# Rockbiter Weapon
CS2_045e = buff(atk=3)

# Bloodlust
CS2_046e = buff(atk=3)

# Far Sight
CS2_053e = {
	GameTag.COST: -3,
}

# Totemic Might
EX1_244e = buff(health=2)


##
# Warlock

# Blood Pact (Blood Imp)
CS2_059o = buff(health=1)

# Power Overwhelming
EX1_316e = buff(+4, +4)


# Demonfire
EX1_596e = buff(+2, +2)


##
# Warrior

# Charge (Warsong Commander)
EX1_084e = {
	GameTag.CHARGE: True,
}

# Berserk (Frothing Berserker)
EX1_604o = buff(atk=1)

# Whipped Into Shape (Cruel Taskmaster)
EX1_603e = buff(atk=2)

# Charge
CS2_103e2 = {
	GameTag.ATK: 2,
	GameTag.CHARGE: True,
}

# Rampage
CS2_104e = buff(+3, +3)

# Heroic Strike
CS2_105e = buff(atk=4)

# Upgraded (Upgrade!)
EX1_409e = buff(+1, +1)

# Inner Rage
EX1_607e = buff(atk=2)

# Commanding Shout
NEW1_036e = {
	GameTag.HEALTH_MINIMUM: 1,
}


##
# Neutral common

# Enhanced (Raid Leader)
CS2_122e = buff(atk=1)

# Might of Stormwind (Stormwind Champion)
CS2_222o = buff(+1, +1)

# Frostwolf Banner (Frostwolf Warlord)
CS2_226e = buff(+1, +1)

# Berserking (Gurubashi Berserker)
EX1_399e = buff(atk=3)

# Sharp! (Spiteful Smith)
CS2_221e = buff(atk=2)

# Full Strength (Unused)
CS2_181e = buff(atk=2)

# 'Inspired' (Abusive Seargent)
CS2_188o = buff(atk=2)

# Cleric's Blessing (Shattered Sun Cleric)
EX1_019e = buff(+1, +1)

# Tempered (Dark Iron Dwarf)
EX1_046e = buff(atk=2)

# Strength of the Pack (Dire Wolf Alpha)
EX1_162o = buff(atk=1)

# Mlarggragllabl! (Grimscale Oracle)
EX1_508o = buff(atk=1)

# Cannibalize (Flesheating Ghoul)
tt_004o = buff(atk=1)


##
# Neutral rare

# Elune's Grace (Young Priestess)
EX1_004e = buff(health=1)

# Hour of Twilight (Twilight Drake)
EX1_043e = buff(health=1)

# Level Up! (Questing Adventurer)
EX1_044e = buff(+1, +1)

# Empowered (Mana Addict)
EX1_055o = buff(atk=2)

# Keeping Secrets (Secretkeeper)
EX1_080o = buff(+1, +1)

# Hand of Argus (Defender of Argus)
EX1_093e = {
	GameTag.ATK: 1,
	GameTag.HEALTH: 1,
	GameTag.TAUNT: True,
}

# Mrghlglhal (Coldlight Seer)
EX1_103e = buff(health=2)

# Blarghghl (Murloc Tidecaller)
EX1_509e = buff(atk=1)

# Equipped (Master Swordsmith)
NEW1_037e = buff(atk=1)


##
# Neutral epic

# Shadows of M'uru (Blood Knight)
EX1_590e = buff(+3, +3)

# Mrgglaargl! (Murloc Warleader)
EX1_507e = buff(+2, +1)

# Full Belly (Hungry Crab)
NEW1_017e = buff(+2, +2)

# Yarrr! (Southsea Captain)
NEW1_027e = buff(+1, +1)


##
# Neutral legendary

# Bananas (King Mukla)
EX1_014te = buff(+1, +1)

# Greenskin's Command (Captain Greenskin)
NEW1_024o = buff(+1, +1)

# Growth (Gruul)
NEW1_038o = buff(+1, +1)

# Emboldened! (Emboldener 3000)
Mekka3e = buff(+1, +1)


##
# Curse of Naxxramas set
#

# Consume (Shade of Naxxramas)
FP1_005e = buff(+1, +1)

# Vengeance (Avenge)
FP1_020e = buff(+3, +2)

# Power of the Ziggurat (Dark Cultist)
FP1_023e = buff(health=3)

# Darkness Calls (Undertaker)
FP1_028e = buff(atk=1)


##
# Naxxramas Adventure

# Fungal Growth (Spore)
NAX6_03te = buff(atk=8)

# Mark of the Horsement
NAX9_07e = buff(+1, +1)

# Mutating Injection
NAX11_04e = {
	GameTag.ATK: 4,
	GameTag.HEALTH: 4,
	GameTag.TAUNT: True,
}

# Extra Teeth (Jaws)
NAX12_03e = buff(atk=2)

# Enrage
NAX12_04e = buff(atk=6)

# Supercharge
NAX13_03e = buff(health=2)


##
# Goblins vs. Gnomes set
#

##
# Druid

# Attack Mode (Anodized Robo Cub)
GVG_030ae = buff(atk=1)

# Tank Mode (Anodized Robo Cub)
GVG_030be = buff(health=1)

# Dark Wispers
GVG_041c = {
	GameTag.ATK: 5,
	GameTag.HEALTH: 5,
	GameTag.TAUNT: True,
}

##
# Hunter

# The King (King of Beasts)
GVG_046e = buff(atk=1)

# Metal Teeth (Metaltooth Leaper)
GVG_048e = buff(atk=2)

# Glaivezooka
GVG_043e = buff(atk=1)


##
# Paladin

# Well Equipped (Quartermaster)
GVG_060e = buff(+2, +2)

# Retribution (Bolvar Fordragon)
GVG_063a = buff(atk=1)

# Seal of Light
GVG_057a = buff(atk=2)


##
# Priest

# Repairs! (Upgraded Repair Bot)
GVG_069a = buff(health=4)

# Velen's Chosen
GVG_010b = {
	GameTag.ATK: 2,
	GameTag.HEALTH: 4,
	GameTag.SPELLPOWER: 1,
}

# Shrink Ray (Shrinkmeister)
GVG_011a = buff(atk=-2)


##
# Rogue

# Tinker's Sharpsword Oil
GVG_022a = buff(atk=3)  # Weapon
GVG_022b = buff(atk=3)  # Minion

# Extra Sharp (Goblin Auto-Barber)
GVG_023a = buff(atk=1)

# Ironed Out (Iron Sensei)
GVG_027e = buff(+2, +2)


##
# Shaman

# Powered (Powermace)
GVG_036e = buff(+2, +2)


##
# Warlock

# Demonheart
GVG_019e = buff(+5, +5)

# Grasp of Mal'Ganis (Mal'Ganis)
GVG_021e = buff(+2, +2)

# Brow Furrow (Floating Watcher)
GVG_100e = buff(+2, +2)


##
# Warrior

# Armor Plated (Siege Engine)
GVG_086e = buff(atk=1)


##
# Neutral common

# Metabolized Magic (Stonesplinter Trogg)
GVG_067a = buff(atk=1)

# Metabolized Magic (Burly Rockjaw Trogg)
GVG_068a = buff(atk=2)

# Pistons (Micro Machine)
GVG_076a = buff(atk=1)

# Might of Tinkertown (Tinkertown Technician)
GVG_102e = buff(+1, +1)

##
# Neutral rare

# Screwy Jank (Screwjank Clunker)
GVG_055e = buff(+2, +2)

# Pure (Lil' Exorcist)
GVG_101e = buff(+1, +1)


##
# Neutral epic

# HERE, TAKE BUFF. (Hobgoblin)
GVG_104a = buff(+2, +2)

# Junked Up (Junkbot)
GVG_106e = buff(+2, +2)


##
# Spare parts

# Armor Plating
PART_001e = buff(health=1)

# Whirling Blades
PART_007e = buff(atk=1)


###
# Blackrock Mountain set
#

# Dragon's Might (Unused)
BRM_003e = {
	GameTag.COST: -3,
}

# Twilight Endurance (Twilight Whelp)
BRM_004e = buff(health=2)

# On Fire! (Fireguard Destroyer)
BRM_012e = buff(atk=1)

# Power Rager (Core Rager)
BRM_014e = buff(+3, +3)

# Unchained! (Dragon Consort)
BRM_018e = {
	GameTag.COST: -3,
}

# Draconic Power (Dragonkin Sorcerer)
BRM_020e = buff(+1, +1)

# Large Talons (Drakonid Crusher)
BRM_024e = buff(+3, +3)

# Imperial Favor (Emperor Thaurissan)
BRM_028e = {
	GameTag.COST: -1,
}

# Dragon Blood (Blackwing Technician)
BRM_033e = buff(+1, +1)


##
# Blackrock Adventure

# Incubation (The Rookery)
BRMA10_3e = buff(health=1)

# Blind With Rage (Razorgore's Claws)
BRMA10_6e = buff(atk=1)

# Potion of Might (The Alchemist)
BRMA15_2He = buff(+2, +2)

# Sonic Breath
BRMA16_3e = buff(atk=3)

# I hear you... (Dragonteeth)
BRMA16_5e = buff(atk=1)


##
# Blackrock Brawl

# I Hear You... (Atramedes)
BRMC_86e = buff(atk=2)

# Dragonlust (Razorgore)
BRMC_98e = buff(atk=3)


##
# The Grand Tournament set

# Power of Dalaran (Dalaran Aspirant)
AT_006e = {
	GameTag.SPELLPOWER: 1,
}

# Light's Blessing (Holy Champion)
AT_011e = buff(atk=2)

# Shadowfiended (Shadowfiend)
AT_014e = {
	GameTag.COST: -1,
}

# Twilight's Embrace (Twilight Guardian)
AT_017e = {
	GameTag.ATK: 1,
	GameTag.TAUNT: True,
}

# Felrage (Tiny Knight of Evil)
AT_021e = buff(+1, +1)

# Dark Fusion (Demonfuse)
AT_024e = buff(+3, +3)

# Chi Lance (Shado-Pan Rider)
AT_028e = buff(atk=3)

# Extra Stabby (Buccaneer)
AT_029e = buff(atk=1)

# Shady Deals (Shady Dealer)
AT_032e = buff(+1, +1)

# Laced (Poisoned Blade)
AT_034e = buff(atk=1)

# Savage (Savage Combatant)
AT_039e = buff(atk=2)

# Kindred Spirit (Wildwalker)
AT_040e = buff(health=3)

# Call of the Wild (Knight of the Wild)
AT_041e = {
	GameTag.COST: -1,
}

# Empowering Mist (The Mistcaller)
AT_045e = buff(+1, +1)

# Experienced (Draenei Totemcarver)
AT_047e = buff(+1, +1)

# Power of the Bluff (Thunder Bluff Valiant)
AT_049e = buff(+1, +1)

# Groomed (Stablemaster)
AT_057o = {
	GameTag.CANT_BE_DAMAGED: True,
}

# King's Defender
AT_065e = buff(health=1)

# Forges of Orgrimmar (Orgrimmar Aspirant)
AT_066e = buff(atk=1)

# Bolstered (Bolster)
AT_068e = buff(+2, +2)

# Alexstrasza's Boon (Alexstrasza's Champion)
AT_071e = {
	GameTag.ATK: 1,
	GameTag.CHARGE: True,
}

# Competitive Spirit
AT_073e = buff(+1, +1)

# Seal of Champions
AT_074e2 = {
	GameTag.ATK: 3,
	GameTag.DIVINE_SHIELD: True,
}

# Might of the Hostler (Warhorse Trainer)
AT_075e = buff(atk=1)

# Extra Poke (Argent Lance)
AT_077e = buff(health=1)

# Training (Lowly Squire)
AT_082e = buff(atk=1)

# Dragonhawkery (Dragonhawk Rider)
AT_083e = {
	GameTag.WINDFURY: True,
}

# Equipped (Lance Carrier)
AT_084e = buff(atk=2)

# Villainy (Saboteur)
AT_086e = {
	GameTag.COST: 5,
}

# Boneguarded (Boneguard Lieutenant)
AT_089e = buff(health=1)

# Might of the Monkey (Mukla's Champion)
AT_090e = buff(+1, +1)

# Wound Up (Clockwork Knight)
AT_096e = buff(+1, +1)

# Argent Watchman
AT_109e = {
	GameTag.CANT_ATTACK: False,
}

# Bring It On! (Wyrmrest Agent)
AT_116e = {
	GameTag.ATK: 1,
	GameTag.TAUNT: True,
}

# Ceremony (Master of Ceremonies)
AT_117e = buff(+2, +2)

# Inspired (Kvaldir Raider)
AT_119e = buff(+2, +2)

# Huge Ego (Crowd Favorite)
AT_121e = buff(+1, +1)

# Victory! (Gadgetzan Jouster)
AT_133e = buff(+1, +1)

# Dire Claws (Dire Shapeshift) (Justicar Trueheart)
AT_132_DRUIDe = buff(atk=2)


###
# Tutorial set
#

# Might of Mukla (Unused)
TU4c_008e = buff(atk=8)

# Legacy of the Emperor
TU4f_004o = buff(+2, +2)

# Bananas
TU4c_006e = buff(+1, +1)

# Transcendence
TU4f_006o = {
	GameTag.CANT_BE_ATTACKED: True,
	GameTag.CANT_BE_TARGETED_BY_OPPONENTS: True,
}

###
# Debug set
#

# Weapon Buff Enchant
XXX_054e = buff(+100, +100)

# 1000 Stats Enchant
XXX_055e = buff(+1000, +1000)
