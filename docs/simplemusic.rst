.. _simplemusic:

==================================
 Simplemusic and Pitch Class Sets
==================================

Simplemusic
===========

.. autofunction:: simplemusic.mod12

>>> simplemusic.mod12(13)
1

.. autofunction:: simplemusic.interval

   Return the numeric interval between two notes.

.. autofunction:: simplemusic.transposition

    Transpose a set of notes by a numerical index.

.. autofunction:: simplemusic.transposition_startswith

    Transpose a set of notes so it begins with `start` note.

.. autofunction:: simplemusic.is_related_by_transposition

    Check if two groups of notes are related by transposition.

    We use brute force here; the best way is to check for the normal
    or prime forms.

.. autofunction:: simplemusic.inversion

    Invert a set of notes though an inversion index.

    The inversion index is not very musical. the function
    :func:`inversion_startswith` is probably more useful.
 
 .. autofunction:: simplemusic.inversion_startswith

    Invert a set of notes so it begins with `start` note.

>>> simplemusic.inversion_startswith([0, 4, 7], 2)
[2, 10, 7]

.. autofunction:: simplemusic.rotate_set

   Return all rotations of a collection of notes.


Pitch Class Set
===============


.. autofunction:: simplemusic.name_to_diatonic

   Return a number from 0 to 6 for the note name without the accidental.

.. autofunction:: simplemusic.dotted_duration

    Sn = a(1 - r^n)/1 - r where a is the first term, r is the common
    ration (1/2 in our case) and n is the number of terms.
