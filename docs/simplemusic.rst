.. _simplemusic:

==================================
 Simplemusic and Pitch Class Sets
==================================

Simplemusic
===========

.. autofunction:: simplemusic.mod12

    Return `n % 12`.

>>> simplemusic.mod12(13)
1

.. autofunction:: simplemusic.interval

    Return the numeric interval between two notes. Exchanging notes gives the complement adding up to 12.

>>> simplemusic.interval(2, 0)
2
>>> simplemusic.interval(0, 2)
10

.. autofunction:: simplemusic.transposition

    Transpose a set of notes by a number of half-steps. Notes are limited to values 0 to 11.

>>> notes = [0, 2, 4, 6, 8, 10]
[0, 2, 4, 6, 8, 10]
>>> simplemusic.transposition(notes, 3)
[3, 5, 7, 9, 11, 1]


.. autofunction:: simplemusic.transposition_startswith

    Transpose a set of notes so it begins with `start` note.

>>> simplemusic.transposition_startswith([0, 1, 2, 3], 3)
[3, 4, 5, 6]
>>> simplemusic.transposition_startswith([0, 1, 2, 3], 10)
[10, 11, 0, 1]


.. autofunction:: simplemusic.is_related_by_transposition

    Return True if a `notes1` can be transposed to match `notes2`.

    We use brute force here; the best way is to check for the normal or prime forms.

>>> simplemusic.is_related_by_transposition([0,1,2,3], [1,2,3,4])
True
>>> simplemusic.is_related_by_transposition([0,1,2,3], [4,1,2,3])
True
>>> simplemusic.is_related_by_transposition([0,1,2,3], [2,3,4,7])
False
>>> simplemusic.is_related_by_transposition([0,1,2,3], [3,4,5])
False

.. autofunction:: simplemusic.inversion

    Invert a set of notes using `index` as the pivot point. Notes originally above `index` will be below it (wrapping at 12), and vice versa.

>>> simplemusic.inversion([0, 1, 2, 3])
[0, 11, 10, 9]
>>> simplemusic.inversion([0, 1, 2, 3], 2)
[2, 1, 0, 11]
>>> simplemusic.inversion([0, 1, 2, 3], 3)
[3, 2, 1, 0]
>>> simplemusic.inversion([0, 1, 2, 3], 4)
[4, 3, 2, 1]
>>> simplemusic.inversion([0, 1, 2, 3], 5)
[5, 4, 3, 2]

    The inversion index pivot point is not very musical.
    The function :func:`inversion_startswith` is probably more useful.

.. autofunction:: simplemusic.inversion_startswith

    Invert and transpose a set of notes so it begins with `start` note.

>>> simplemusic.inversion_startswith([0, 4, 7], 2)
[2, 10, 7]

.. autofunction:: simplemusic.rotate

    Return `notes` with the contents rotated by `n` positions.

>>> simplemusic.rotate([1,2,3,4])
[2, 3, 4, 1]
>>> simplemusic.rotate([1,2,3,4], 3)
[4, 1, 2, 3]

.. autofunction:: simplemusic.rotate_set

    Return a list of all rotations of a collection.

>>> simplemusic.rotate_set([1, 2, 3, 4])
[[1, 2, 3, 4], [2, 3, 1, 4], [3, 4, 1, 2], [4, 1, 2, 3]]


Pitch Class Set
===============


.. autofunction:: simplemusic.name_to_diatonic

    Return a number from 0 to 6 for the note name without the accidental.

.. autofunction:: simplemusic.dotted_duration

    Sn = a(1 - r^n)/1 - r where a is the first term, r is the common
    ration (1/2 in our case) and n is the number of terms.
