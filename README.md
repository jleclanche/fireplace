# <img src="/logo.png" height="32" width="32"/> Fireplace
[![](https://img.shields.io/badge/python-3.10+-blue.svg)](https://peps.python.org/pep-0619/)
[![](https://img.shields.io/github/license/jleclanche/fireplace.svg)](https://github.com/jleclanche/fireplace/blob/master/LICENSE.md)
[![](https://github.com/jleclanche/fireplace/actions/workflows/build.yml/badge.svg)](https://github.com/jleclanche/fireplace/actions/workflows/build.yml)
[![codecov](https://codecov.io/github/jleclanche/fireplace/graph/badge.svg?token=FXDTJSKZL9)](https://codecov.io/github/jleclanche/fireplace)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Hearthstone simulator and implementation, written in Python.


## Cards Implementation

Now updated to [Patch 17.6.0.53261](https://hearthstone.wiki.gg/wiki/Patch_17.6.0.53261)
* **100%** Basic (153 of 153 cards)
* **100%** Classic (240 of 240 cards)
* **100%** Hall of Fame (35 of 35 cards)
* **100%** Curse of Naxxramas (30 of 30 cards)
* **100%** Goblins vs Gnomes (123 of 123 cards)
* **100%** Blackrock Mountain (31 of 31 cards)
* **100%** The Grand Tournament (132 of 132 cards)
* **100%** Hero Skins (33 of 33 cards)
* **100%** The League of Explorers (45 of 45 cards)
* **100%** Whispers of the Old Gods (134 of 134 cards)
* **100%** One Night in Karazhan (45 of 45 cards)
* **100%** Mean Streets of Gadgetzan (132 of 132 cards)
* **100%** Journey to Un'Goro (135 of 135 cards)
* **100%** Knights of the Frozen Throne (135 of 135 cards)
* **100%** Kobolds & Catacombs (135 of 135 cards)
* **100%** The Witchwood (129 of 129 cards)
* **100%** The Boomsday Project (136 of 136 cards)
* **100%** Rastakhan's Rumble (135 of 135 cards)
* **100%** Rise of Shadows (136 of 136 cards)
* **99%** Saviours of Uldum (134 of 135 cards)
* **100%** Descent of Dragons (140 of 140 cards)
* **100%** Galakrond's Awakening (35 of 35 cards)
* **34%** Ashes of Outlands (47 of 135 cards)
* **100%** Scholomance Academy (1 of 1 card)
* **100%** Demon Hunter Initiate (20 of 20 cards)

Not Implemented
* Zephrys the Great (ULD_003)
* Rustsworn Initiate (BT_008)
* Imprisoned Sungill (BT_009)
* Felfin Navigator (BT_010)
* Libram of Justice (BT_011)
* Underlight Angling Rod (BT_018)
* Murgur Murgurgle (BT_019)
* Aldor Attendant (BT_020)
* Libram of Hope (BT_024)
* Libram of Wisdom (BT_025)
* Aldor Truthseeker (BT_026)
* Bamboozle (BT_042)
* Serpentshrine Portal (BT_100)
* Vivid Spores (BT_101)
* Boggspine Knuckles (BT_102)
* Bogstrok Clacker (BT_106)
* Lady Vashj (BT_109)
* Torrent (BT_110)
* Totemic Reflection (BT_113)
* Shattered Rumbler (BT_114)
* Marshspawn (BT_115)
* Bladestorm (BT_117)
* Warmaul Challenger (BT_120)
* Imprisoned Gan'arg (BT_121)
* Kargath Bladefist (BT_123)
* Corsair Cache (BT_124)
* Teron Gorefiend (BT_126)
* Bloodboil Brute (BT_138)
* Bonechewer Raider (BT_140)
* Scrapyard Colossus (BT_155)
* Imprisoned Vilefiend (BT_156)
* Terrorguard Escapee (BT_159)
* Rustsworn Cultist (BT_160)
* Shadowjeweler Hanar (BT_188)
* Replicat-o-tron (BT_190)
* Keli'dan the Breaker (BT_196)
* Reliquary of Souls (BT_197)
* Soul Mirror (BT_198)
* Unstable Felbolt (BT_199)
* The Lurker Below (BT_230)
* Sword and Board (BT_233)
* Scrap Golem (BT_249)
* Renew (BT_252)
* Psyche Split (BT_253)
* Sethekk Veilweaver (BT_254)
* Dragonmaw Overseer (BT_256)
* Apotheosis (BT_257)
* Imprisoned Homunculus (BT_258)
* Dragonmaw Sentinel (BT_262)
* Hand of A'dal (BT_292)
* Hand of Gul'dan (BT_300)
* Nightshade Matron (BT_301)
* The Dark Portal (BT_302)
* Enhanced Dreadlord (BT_304)
* Imprisoned Scrap Imp (BT_305)
* Shadow Council (BT_306)
* Darkglare (BT_307)
* Kanrethad Ebonlocke (BT_309)
* Lady Liadrin (BT_334)
* Skeletal Dragon (BT_341)
* Ashtongue Slayer (BT_702)
* Cursed Vagrant (BT_703)
* Ambush (BT_707)
* Dirty Tricks (BT_709)
* Greyheart Sage (BT_710)
* Blackjack Stunner (BT_711)
* Akama (BT_713)
* Frozen Shadoweaver (BT_714)
* Bonechewer Brawler (BT_715)
* Bonechewer Vanguard (BT_716)
* Burrowing Scorpid (BT_717)
* Ruststeed Raider (BT_720)
* Blistering Rot (BT_721)
* Guardian Augmerchant (BT_722)
* Rocket Augmerchant (BT_723)
* Ethereal Augmerchant (BT_724)
* Dragonmaw Sky Stalker (BT_726)
* Soulbound Ashtongue (BT_727)
* Disguised Wanderer (BT_728)
* Waste Warden (BT_729)
* Overconfident Orc (BT_730)
* Infectious Sporeling (BT_731)
* Scavenging Shivarra (BT_732)
* Mo'arg Artificer (BT_733)
* Supreme Abyssal (BT_734)
* Al'ar (BT_735)
* Maiev Shadowsong (BT_737)
* Bulwark of Azzinoth (BT_781)
* Magtheridon (BT_850)

## Requirements

* Python 3.10+


## Installation

* `pip install .`


## Documentation

The [Fireplace Wiki](https://github.com/jleclanche/fireplace/wiki) is the best
source of documentation, along with the actual code.


## License

[![AGPLv3](https://www.gnu.org/graphics/agplv3-88x31.png)](http://choosealicense.com/licenses/agpl-3.0/)

Fireplace is licensed under the terms of the
[Affero GPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html) or any later version.


## Community

Fireplace is a [HearthSim](http://hearthsim.info/) project.
Join the community: <https://hearthsim.info/join/>
