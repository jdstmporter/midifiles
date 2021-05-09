# Parser for MIDI (and similar formats) binary files

This package defines some basic Python3 classes for parsing MIDI (and MIDI-like) binary files.  At the moment, this means:

* MIDI binary files (`.mid`)
* FL Studio project files (`.flp`)

In the current version, tere are two separate packages: `MIDI`  and `PL`, one for each format.  However, as the two formats are more or less identical, we intend to merge the two in future, providing a dimple mechanism to automatically discriminate between formats.

Detailed documentation can be found below:

* MIDI: [README.rst](./py/README.rst)
* FL: *none yet - nearly identical to MIDI*


