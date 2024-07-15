# Verity Triumph Instructor

Very simplistic commandline tool, allowing for quick and easy input of observed shapes in the 4th encounter of Destiny 2's *Salvation's Edge*, and for near-guaranteed flawless execution of the encounter and the associated triumph.

Note, that this tool is by no means perfect, and can probably contain bugs. If so, you may choose to open an **Issue tab** on GitHub at your own convenience.

# Requirements
This tool has no requirements whatsoever, besides installing Python 3 for the Developer Setup (see at the end).

Requirements of the Developer Setup:\
The tool only uses base-python libraries, thereby necessitating no further steps (technically it doesn't even require pip).

# Quick Setup
Choose any of the attached releases according to your platform, and follow the given steps [here](https://github.com/Nightknight3000/Verity-Triumph-Instructor/releases).


# Execution

## Step 1: Initial symbols
Upon starting the tool, it asks the user for the symbols held by the statues in the **inside** rooms (left to right).
Use one letter for each shape (and no spaces) like this:
```
Initial statue inputs: tsc
```

## Step 2: Inside room walls
Afterwards, the tool will do the same for the symbols on the wall of each inside room (auto-filling the third one):
```
Left inside room wall: ts
Middle inside room wall: sc
Right inside room wall: tc   <- auto-filled
```

## Step 3: Outside room bodies/shapes
And finally, it will, again, do the same for the outside room (auto-filling the third one).
Here, you may choose to enter the 3D bodies' names like this *(takes longer, but easier)*:
```
Left outside statue: cone
Middle outside statue: prism
Right outside statue: sc   <- auto-filled
```
or you can enter the letters for its defining 2D-shapes *(faster, but you need to know the shapes)*:
```
Left outside statue: tc
Middle outside statue: st
Right outside statue: sc   <- auto-filled
```
*Hint: For all 2-letter-inputs inside and outside, the sequence does not matter (ex. 'st' = 'ts').*

---
---

### Optional: Developer Setup
Download or clone this repository in order to execute it locally on your machine.\
You may execute the tool via this call on your commandline:
```
python verity_triumph.py
```
Or directly from within a python shell:
```
from verity_triumph import main
main()
```
*Hint: Of course, you need to navigate to the directory containing the script for each.*

## Authors
* **Nightknight3000** (Bungie-Name: HawkS0UL#2153)
