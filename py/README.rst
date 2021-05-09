MIDIFile
========

A simple Python3 MIDI File / stream parser / decoder

Introduction
------------

API
---
The top-level namespace is **MIDI**, which contains two classese: **MIDI.MIDIFile** and **MIDI.Track**.

Class **MIDI.MIDIFile**
^^^^^^^^^^^^^^^^^^^^^^^

Represents a file of Standard Midi Format (SMF) data, as defined by the `MIDI Association`_.  **MIDI.MIDIFile** objects are iterable and array-like.

Constructor
"""""""""""

**MIDI.MIDIFile**.__init__(*self*, ``filename``)

    .. list-table::

        * - ``filename`` 
          - the name of an SMF file to read and parse.  Raises an exception if the file does not exist / cannot be read.

Methods
"""""""

    .. list-table::

        * - **MIDI.MIDIFile**.readHeader(*self*)
          - Determine whether the file starts with a MIDI header; returns **True** if it does, **False** otherwise.
        * - **MIDI.MIDIFile**.parse(*self*)
          - Parse the file.  Determines the file's type and populates an array of content tracks, each of which contains one track from the file and is represented by a **MIDI.Track** instance.
        * - **MIDI.MIDIFile**.__len__(*self*)
          - The number of tracks in the file (0 if ``parse`` has not yet been invoked).
        * - **MIDI.MIDIFile**.__iter__(*self*) 
          - Iterates over the tracks in the file
        * - **MIDI.MIDIFile**.__get_item__(*self*, ``n``)
          - A **MIDI.Track** object, representing the ``n``'th track in the file (or throws a **RangeError** if ``n`` is out of range)
        * - **MIDI.MIDIFile**.__str__(*self*)
          - Useful information about the file as a whole, number of tracks and their sizes

Properties
""""""""""

If *self* is an **MIDI.MIDIFile** instance then

    .. list-table::

        * - *self*.format
          - int
          - The MIDI format of the loaded file.  Possible values are `0`, `1` and `2` (or **None** if the ``parse`` method has not yet been invoked).  See page 134 of the `MIDI Specification v1.0`_.
        * - *self*.division
          - uint16
          - Time quantum of the MIDI data encoded in the file (or ``None`` if the ``parse`` method has not yet been invoked).  Interpretation depends on the value: 

            - `< 32768` : equals number of ticks per quarter-note; often equal to ``960``
            - `>=32786` : number of subdivisions of a second as defined in the `SMTPE Standard`_ and on pages 116- of the `MIDI Specification v1.0`_.  Equals `32768 + 256 f + t`  where `f` identifies one of the standard MIDI time code formats, and signifies the number of frames per second, while `f` is the numbef of subdivisions within a frame (common values are `4`, `8`, `10`, `80` and `100`).


Class **MIDI.Track**
^^^^^^^^^^^^^^^^^^^^
Class representing a single track from an SMF file, or a collection of MIDI events.  **MIDI.Track** objects are iterable and array-like.

Constructor
"""""""""""

**MIDI.Track**.__init__(*self*, ``data``, ``containsTiming = True``)

Arguments:


    .. list-table::

        * - ``data``
          - binary string or array 
          - data comprising one track from an SMF file, or a sequence of MIDI messages
        * - ``containsTiming``
          - boolean
          - **True** if ``data`` consists of MIDI events interleaved with timestamps (as in an SMF file); **False** if it is a sequence of MIDI messages


So, for example

    .. code-block:: python

        track = Track(data,containsTiming=True)

    initialises ``track`` for parsing ``data`` representing a track taken from an SMF file; while

    .. code-block:: python

        track = Track(data,containsTiming=False)

    initialises ``track`` for parsing ``data`` consisting of a sequence of one or more raw MIDI events, e.g. captured from an observed MIDI stream, or sent to the application by a MIDI controller.

Methods
"""""""

    .. list-table::

        * - **MIDI.Track**.parse(*self*)
          - Parse the track into an array of events, ordered based on their appearance in the track.  Events are represented by instances of **MIDI.Events.Event**.
        * - **MIDI.Track**.__len__(*self*)
          - Returns the number of messages in the track (0 if ``parse`` has not yet been invoked).
        * - **MIDI.Track**.__iter__(*self*)
          - Iterates over the events / messages in the track, in the order in which they appeared.
        * - **MIDI.Track**.__get_item__(*self*, ``n``)
          - Returns a **MIDI.Events.Event** instance representing  the ``n``'th event in the track (or throws a **RangeError** if ``n`` is out of range).
        * - **MIDI.Track**.__str__(*self*)
          - Returns string representations of all the track's events, concatenated and separated by newline ``'\n'``.


Class **MIDI.Events.Event**
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Represents a general event as found in SMF files, or streams of MIDI messages.  Specific kinds of event are represented by subclasses (for which, see below).

Constructor
"""""""""""
    **MIDI.Events.Event**.__init__(*self*, ``time``, ``buffer``)

    Arguments:

    .. list-table::

      * - ``time`` 
        - uint64 
        - MIDI timestamp for the time of the event's occurrence, relative to some arbitrary zero.
      * -  ``buffer`` 
        -  binary string or array 
        -  bytes making up the event.

Methods
"""""""

   .. list-table::


    * - **MIDI.Events.Event**.__len__(*self*)
      - The total length of the event.
    * - **MIDI.Events.Event**.__str__(*self*)
      - String representation of the event.  By default, a representation of the raw bytes as a binary string.

Properties
""""""""""

If *self* is an **MIDI.Events.Event** instance then

    .. list-table::

        * - *self*.time
          -  the timestamp with which the event instance was initialised; measured in units of the quantum of time defined by the value of the ``division`` property of the **MIDI.MIDIFile** instance containing the track of which this event forms a part.
        * - *self*.header
          - the event's initial byte, which serves to identify its kind.
        * - *self*.data
          - binary string or array containing the event's *body*, i.e. its data content, with the header byte and other formatting removed

Specialisations of this class, describing specific kinds of SMF event, offer various dynamically generated read-only properties, describing properties specific to them.  This is described below: 


**Meta Events**

Provide information about the track, e.g. lyrics, tempo, etc, are represented by the type **MIDI.Events.MetaEvent**, which has the following additional properties:


    .. list-table::
    
     * - ``ev.message`` 
       - is the meta event's kind, expressed as a member of the enumeration **MIDI.Events.meta.MetaEventKinds** for defined message types (see pages 137-139 of the `MIDI Specification v1.0`_ for a complete list) , and **None** otherwise 

Other parameters exist only for specific event kinds as follows:


   .. list-table::
     :header-rows: 1

     * - Property
       - Description
       - Meta Event Type(s)
     * - ``ev.text`` 
       -  general text
       - Text, Copyright_Notice, Track_Name, Instrument_Name, Lyric, Marker, Cue_Point
     * - ``ev.number`` 
       - sequence number
       - Sequence_Number
     * - ``ev.channel`` 
       - channel number
       - MIDI_Channel_Prefix
     * - ``ev.tempo``
       -  tempo
       -  Set_Tempo
     * - ``ev.hh``
       -  hours
       -  SMTPE_Offset 
     * - ``ev.mm``
       -  minutes
       -  SMTPE_Offset
     * - ``ev.ss``
       -  seconds
       -  SMTPE_Offset 
     * - ``ev.frame``
       -  frames
       -  SMTPE_Offset 
     * - ``ev.numerator`` 
       - time signature top number
       - Time_Signature
     * - ``ev.denominator``
       - time signature bottom number
       - Time_Signature
     * - ``ev.clocksPerTick``
       - number of MIDI clocks per tick
       - Time_Signature
     * - ``ev.demisemiquaverPer24Clocks``
       - what it says
       - Time_Signature

**System Events**

Tell MIDI instruments how to perform the track, and are represented by the type **MIDI.Events.SysExEvent**.  Each System event consists of a single MIDI **System** message.  If ``self`` is an instance of **MIDI.Events.SysExEvent** then:

    .. list-table::
    
     * - ``ev.type`` 
       - uint8
       - is the MIDI system message's kind, expressed as an integer 0 - 15;  it is equal to ``ev.header & 15``

**MIDI Events**

Tell MIDI instruments what to play when performing the track, and are represented by the type **MIDI.Events.MIDIEvent**.  All instances have the following fields:

    .. list-table::

        * - ``ev.command``
          - uint8
          - The message command type, as defined in the `MIDI Specification v1.0`_.  Equal to ``ev.header & 240``
        * - ``ev.channel``
          - uint8
          - The channel that the message relates to.  Equal to ``ev.header & 15``
        * - ``ev.message``
          - message type specific
          - Instance of a class representing this particular kind of MIDI message; depending on ``ev.command`` 

The value of ``ev.message`` is as follows, depending on the message type:

    **NOTE-OFF** or **NOTE-ON** (``command = 0x80 or 0x90``)

        .. list-table::

            * - ``ev.onOff``
              - **ON** if this is a **NOTE-ON** message;  **OFF** if it is a **NOTE-OFF** message
            * - ``ev.note``
              - The note to which the message refers
            * - ``ev.velocity``
              - The velocity with which the note is applied

    **KEY PRESSURE** (``command = 0xa0``)

        .. list-table::

            * - ``ev.note``
              - The note to which the message refers
            * - ``ev.pressure``
              - The pressure with which the note is applied

    **CONTROL CHANGE** (``command = 0xb0``)

        .. list-table::

            * - ``ev.command``
              - The control that should be changed; represented either as a named object, for known controls, or as an unsigned integer for others
            * - ``ev.pressure``
              - The new value of the control; converted to **ON** / **OFF**, etc for known controls, left as an unsigned integer for others

    **PROGRAM CHANGE** (``command = 0xc0``)

        .. list-table::

            * - ``ev.name``
              - always equal to **"Program"**
            * - ``ev.value``
              - The new program number

    **CHANNEL PRESSURE** (``command = 0xd0``)

        .. list-table::

            * - ``ev.name``
              - always equal to **"Pressure"**
            * - ``ev.value``
              - The new pressure value for the channel as an unsigned integer

    **PITCH BEND CHANGE** (``command = 0xe0``)

        .. list-table::

            * - ``ev.name``
              - always equal to **"BEND"**
            * - ``ev.value``
              - The new pitch bend for the channel as a signed integer `b` such that `-2048 <= b <= 2047`
         

    





Examples
--------

Included in the package is the following simple test script:

    .. code-block:: python

        from MIDI import MIDIFile
        from sys import argv

        def parse(file):
            c=MIDIFile(file)
            c.parse()
            print(str(c))
            for idx, track in enumerate(c):
                track.parse()
                print(f'Track {idx}:')
                print(str(track))


        parse(argv[1])  

The first few lines of the output from applying this to a SMF file are as follows: ::

    Format 1 nTracks 4 division 960
	   Track 0 of length 0
	   Track 1 of length 0
	   Track 2 of length 0
	   Track 3 of length 0
    Track 0:
    META@0 Key Signature -> key=C mode=major
    META@0 Set Tempo -> tempo=128.57136
    META@0 Track Name -> text=b'It was a punter and a pro'
    META@0 Text -> text=b'Julian Porter'
    META@0 Copyright Notice -> text=b'Copyright \xa9 Julian Porter'
    META@1 End Of Track -> 
    Track 1:
    MIDI@6336 0[0] 
    MIDI@6336 CONTROL_CHANGE[1] Pan := 16
    MIDI@6336 CONTROL_CHANGE[1] Channel Volume := 112
    META@6336 Track Name -> text=b'Soprano'
    META@10656 Lyric -> text=b'It '
    MIDI@10656 NOTE_ON[1] E5 ON velocity := 36
    MIDI@11136 NOTE_OFF[1] E5 OFF velocity := 0
    META@11136 Lyric -> text=b'was '
    MIDI@11136 NOTE_ON[1] G#5 ON velocity := 36
    MIDI@11616 NOTE_OFF[1] G#5 OFF velocity := 0
    META@11616 Lyric -> text=b'a '
    MIDI@11616 NOTE_ON[1] C6 ON velocity := 36
    MIDI@12096 NOTE_OFF[1] C6 OFF velocity := 0
    META@12096 Lyric -> text=b'pun'
    MIDI@12096 NOTE_ON[1] A#5 ON velocity := 36
    MIDI@12576 NOTE_OFF[1] A#5 OFF velocity := 0
    META@12576 Lyric -> text=b'ter '
    MIDI@12576 CONTROL_CHANGE[1] RPN MSB := 0
    MIDI@12576 CONTROL_CHANGE[1] RPN LSB := 0
    MIDI@12576 CONTROL_CHANGE[1] Data Entry MSB := 4
    MIDI@12576 CONTROL_CHANGE[1] Data Entry LSB := 0
    MIDI@12576 PITCH_BEND[1] Bend := -8192
    MIDI@12576 PITCH_BEND[1] Bend := 8191
    MIDI@12591 PITCH_BEND[1] Bend := 7927
    MIDI@12606 PITCH_BEND[1] Bend := 7663
    MIDI@12621 PITCH_BEND[1] Bend := 7399
    MIDI@12636 PITCH_BEND[1] Bend := 7134
    MIDI@12651 PITCH_BEND[1] Bend := 6870
    MIDI@12651 NOTE_ON[1] C#6 ON velocity := 36
    MIDI@12666 PITCH_BEND[1] Bend := 6606
    MIDI@12681 PITCH_BEND[1] Bend := 6342
    MIDI@12696 PITCH_BEND[1] Bend := 6077
    MIDI@12711 PITCH_BEND[1] Bend := 5813

This clearly shows the overall structure of the file (with four tracks), the content of the initial metadata track, which specifies tempo, key, etc, and the start of the second track, which mixes MIDI messages specifying what an instrument should play, with metadata  providing lyrics, etc. 


Requirements
------------

MIDIFile is a pure python module requiring Python 3.6 or later to run (this could be reduced by using more long-winded equivalents to Python 3.6's ``f'...{x}'`` string interpolation syntax).

It is known to run on MacOS and Linux.  It should run on Windows, but then, nothing is certain when Windows is involved, is it?  Attempts to make it run on Windows are at your own risk.


.. _MIDI Association: https://www.midi.org/specifications-old/category/smf-specifications
.. _SMF Standard: MIDI Association_
.. _MIDI Specification v1.0: https://www.midi.org/downloads?task=callelement&format=raw&item_id=92&element=f85c494b-2b32-4109-b8c1-083cca2b7db6&method=download
.. _SMTPE Standard: https://ieeexplore.ieee.org/document/7291029

