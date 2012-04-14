from pyknon.pc_sets import PC_SETS
from pyknon.simplemusic import (mod12, interval, rotate, all_intervals, rotate_set,
                                inversion, transposition_startswith,
                                inversion_first_note)


def set_sizes(pset):
    return [interval(x, y) for x,y in zip(rotate(pset, len(pset) - 1), pset)]


def set_size(pset):
    ## pset must be sorted
    return mod12(pset[-1] - pset[0])


def interval_vector(notes):
    vector = [0, 0, 0, 0, 0, 0]

    for i in all_intervals(notes):
        vector[i-1] += 1

    return vector


def order_set(notes):
    # it doesn't eliminate repetition
    return sorted([mod12(n) for n in notes])


def interval_tie(pset):
    # return interval of between second-to-last and first, according to Straus.
    return interval(pset[-2], pset[0])


def normal_form(notes):
    oset = order_set(notes)
    rotations = rotate_set(oset)
    min_size = min(set_sizes(oset))
    smallest_sets = [x for x in rotations if set_size(x) == min_size]

    if len(smallest_sets) == 1:
        return smallest_sets[0]
    else:
        min_pack_size = min([interval_tie(x) for x in smallest_sets])
        packed_sets = [x for x in smallest_sets if interval_tie(x) == min_pack_size]

        return packed_sets[0]


def prime_form(notes):
    set_zero = transposition_startswith(normal_form(notes), 0)
    set_inv = transposition_startswith(normal_form(inversion(set_zero)), 0)
    if interval_tie(set_zero) <= interval_tie(set_inv):
        return set_zero
    else:
        return set_inv


def matrix(row):
    return [transposition_startswith(row, n) for n in inversion_first_note(row)]


def row_matrix_search(matrix, notes):
    # return positions
    return [[row.index(note) for note in notes] for row in matrix]


def column_matrix_search(matrix, notes):
    return [[row.index(note) for note in notes] for row in zip(*matrix)]


