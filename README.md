# <img src="/logo.png" height="32" width="32"/> Fireplace
[![Build Status](https://travis-ci.org/jleclanche/fireplace.svg?branch=master)](https://travis-ci.org/jleclanche/fireplace)

## Overview
A Hearthstone simulator and implementation, written in Python.

<<<<<<< HEAD
<target>

### State Of Implementation (59.5% of Standard Card Sets)

| Card Set      | Implemented |       |
| ------------- |    :---:    | :---: |
| **Basic** | 209/209 | **100.0%**
| **Classic** | 383/386 | **99.2%**
| **Whispers of the Old Gods** | 162/218 | **74.3%**
| **One Night in Karazhan** | 108/220 | **49.1%**
| **Mean Streets of Gadgetzan** | 233/257 | **90.7%**
| **Journey to Un'Goro** | 72/225 | **32.0%**
| **Knights of the Frozen Throne** | 51/297 | **17.2%**
| **Kobolds & Catacombs** | 181/541 | **33.5%**


</target>

## Requirements
=======
>>>>>>> 52f42338fecc529dcf89c4ab4db55684122eb884

## Requirements

<<<<<<< HEAD
## Installation
=======
* Python 3.6+
>>>>>>> 52f42338fecc529dcf89c4ab4db55684122eb884


<<<<<<< HEAD
## Contribute

Help us improve fireplace and extend how many cards we have implemented.
There's even a script that helps you:

* `cd scripts`
* `python card_implementer.py`

The script will find cards that seem easy to implement! E.g.
```
Searching for easy cards (might take a while)...
The following cards might be easy to implement due to high similarity with existing implementations:

CFM_095: Deathrattle Shuffle this minion into your opponents deck
CFM_316: x Deathrattle Summon a number of 1/1 Rats equal  to this minions Attack
CFM_699: x Battlecry The next Murloc you play this turn costs  Health instead of Mana
```
And will also output code that will probably help you!
```
Enter a card ID: CFM_095
We found: CFM_095!
Description:
Deathrattle Shuffle this minion into your opponents deck

Some cards and their implementations that are quite similar:

GVG_035: Deathrattle Shuffle this minion into your deck    <---- See? Almost the same effect!
class GVG_035:
        "Malorne"
        deathrattle = Shuffle(CONTROLLER, SELF)

GVG_031: Shuffle an enemy minion into your opponents deck
class GVG_031:
        "Recycle"
        play = Shuffle(OPPONENT, TARGET)                   <---- This also helps!

UNG_914: Deathrattle Shuffle a 4/3 Raptor into your deck
class UNG_914:
        "Raptor Hatchling"
        deathrattle = Shuffle(CONTROLLER, "UNG_914t1")

```
Now you can easily implement it!
```
class CFM_095:
        "Weasel Tunneler"
        deathrattle = Shuffle(OPPONENT, SELF)
```

And don't forget to write tests!
=======
## Installation

* `pip install .`
>>>>>>> 52f42338fecc529dcf89c4ab4db55684122eb884


## Documentation

The [Fireplace Wiki](https://github.com/jleclanche/fireplace/wiki) is the best
source of documentation, along with the actual code.

<<<<<<< HEAD
=======

>>>>>>> 52f42338fecc529dcf89c4ab4db55684122eb884
## License

[![AGPLv3](https://www.gnu.org/graphics/agplv3-88x31.png)](http://choosealicense.com/licenses/agpl-3.0/)

Fireplace is licensed under the terms of the
[Affero GPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html) or any later version.

<<<<<<< HEAD
## Community
=======
>>>>>>> 52f42338fecc529dcf89c4ab4db55684122eb884

## Community

Fireplace is a [HearthSim](http://hearthsim.info/) project.
Join the community: <https://hearthsim.info/join/>
