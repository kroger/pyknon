Introduction
============



Implementation
==============

.. testsetup:: *

   import pyknon


Integer notation
----------------

    In music Set Theory we represent each note in the chromatic scale as an integer. C is represented as 0, C# as 1, D
    as 2, until B as 11.

Octave equivalence
------------------

    We represent numbers using integers from 0 to 11 which completes an octave. The integers 12, 24 and 36
    all refer to the pitch class C, and can be simplified to 0. Therefore we'll take the mod 12 of any
    number greater than 12. In Python we can just say `n % 12`, but musiclib has a utility function
    :func:`simplemusic.mod12`.

    .. autofunction:: simplemusic.mod12

        >>> simplemusic.mod12(13)
        1


Intervals
---------

    A interval is a subtraction of two notes (using integer notation). The result will be an integer
    that indicates the number of semitones between two notes:

    .. math::
        \{ a - b \pmod{12} \mid n \in \mathbb{N} \}

    For instance, the interval between the notes E and C is 4, (4 - 0 = 4). On the other hand, the interval
    between C and E is -4 (0 - 4 = -4). A negative interval shows that an interval is descendant. But often,
    it's useful to have the smallest interval (which is called `interval class`).

    .. autofunction:: simplemusic.interval_class

        The function :func:`interval_class` will return the interval class between two notes.
        For example, the interval between 1 and 9 is -8, and -8 mod 12 is 4. So the interval
        class between 1 and 9 is the same of 9 and 1.

        >>> simplemusic.interval_class(1, 9)
        4
        >>> simplemusic.interval_class(9, 1)
        4

Transposition
-------------

    Music transposition is the modulo 12 of the sum of every element `n`
    in a set to a transposition index `i`:

        .. math::
            \{ n + i \pmod{12} \mid n \in \mathbb{N} \}


    This translates into the following python code (we use the
    :func:`simplemusic.mod12` function for readability)::

        [mod12(n + index) for n in notes]

    .. autofunction:: simplemusic.transposition

        Transpose a list of notes (in integer notation) to a
        transposition index.

        >>> simplemusic.transposition([1, 3, 7], 5)
        [6, 8, 0]

    .. autofunction:: simplemusic.transposition_startswith

        Transpose a list of notes in a way that the transposed list
        will start with the note `start`.  This is useful when you
        don't have the transposition index, but know the first note of
        the transposed set. (see :func:`simplemusic.matrix` for an
        example)

        >>> simplemusic.transposition_startswith([3, 5, 6], 7)
        [7, 9, 10]


Inversion
---------

    .. autofunction:: simplemusic.inversion


    .. autofunction:: simplemusic.inversion_first_note

        Use 1st note as index


index number


Normal form
-----------

    To calculate the normal form we use the following algorithm:

    1.

    The auxiliary function :func:`simplemusic.set_sizes`

Tn-Form
-------


Prime form
----------

http://www.mta.ca/faculty/arts-letters/music/pc-set_project/pc-set_new/pages/pc-table/packed.html

Common tones under transposition
--------------------------------



Common tones under inversion
----------------------------


Transpositional symmetry
------------------------


Inversional symmetry
--------------------


Complement
----------


Subset and supersets
--------------------


12-tone matrix
--------------

    .. autofunction:: simplemusic.matrix
