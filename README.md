# <img src="/logo.png" height="32" width="32"/> Fireplace
[![Build Status](https://travis-ci.org/jleclanche/fireplace.svg?branch=master)](https://travis-ci.org/jleclanche/fireplace)

## Overview
A Hearthstone simulator and implementation, written in Python.


## Requirements

* Python 3.6+


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
