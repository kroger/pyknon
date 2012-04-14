import unittest
from pyknon import pcset


class PcSetTest(unittest.TestCase):
    def test_set_sizes(self):
        self.assertEqual(pcset.set_sizes([0, 4, 8, 9, 11]), [11, 8, 8, 11, 10])

    def test_set_size(self):
        self.assertEqual(pcset.set_size([0, 3, 11]), 11)
        self.assertEqual(pcset.set_size([3, 4, 11]), 8)
        self.assertEqual(pcset.set_size([4, 5, 10]), 6)

    def test_interval_vector(self):
        self.assertEqual(pcset.interval_vector([0, 4, 7]), [0, 0, 1, 1, 1, 0])

    def test_order_set(self):
        self.assertEqual(pcset.order_set([13, 14, 1, 3, 4]), [1, 1, 2, 3, 4])

    def test_interval_tie(self):
        self.assertEqual(pcset.interval_tie([0, 1, 4, 7]), 4)

    def test_normal_form(self):
        self.assertEqual(pcset.normal_form([9, 8, 11, 4, 0]), [8, 9, 11, 0, 4])
        self.assertEqual(pcset.normal_form([0, 1, 6]), [0, 1, 6])
        self.assertEqual(pcset.normal_form([3, 6, 9, 0]), [0, 3, 6, 9])
        self.assertEqual(pcset.normal_form([4, 8, 0]), [0, 4, 8])

    def test_prime_form(self):
        self.assertEqual(pcset.prime_form([0, 4, 7]), [0, 3, 7])
        # those are from previous bugs, keep'em
        self.assertEqual(pcset.prime_form([0, 1, 2, 4, 5]), [0, 1, 2, 4, 5])
        self.assertEqual(pcset.prime_form([0, 2, 3, 6, 7, 9]), [0, 2, 3, 6, 7, 9])


class MatrixTest(unittest.TestCase):
    def setUp(self):
        self.webern_row = [4, 5, 7, 1, 6, 3, 8, 2, 11, 0, 9, 10]
        self.webern_matrix = [[4, 5, 7, 1, 6, 3, 8, 2, 11, 0, 9, 10],
            [3, 4, 6, 0, 5, 2, 7, 1, 10, 11, 8, 9],
            [1, 2, 4, 10, 3, 0, 5, 11, 8, 9, 6, 7],
            [7, 8, 10, 4, 9, 6, 11, 5, 2, 3, 0, 1],
            [2, 3, 5, 11, 4, 1, 6, 0, 9, 10, 7, 8],
            [5, 6, 8, 2, 7, 4, 9, 3, 0, 1, 10, 11],
            [0, 1, 3, 9, 2, 11, 4, 10, 7, 8, 5, 6],
            [6, 7, 9, 3, 8, 5, 10, 4, 1, 2, 11, 0],
            [9, 10, 0, 6, 11, 8, 1, 7, 4, 5, 2, 3],
            [8, 9, 11, 5, 10, 7, 0, 6, 3, 4, 1, 2],
            [11, 0, 2, 8, 1, 10, 3, 9, 6, 7, 4, 5],
            [10, 11, 1, 7, 0, 9, 2, 8, 5, 6, 3, 4]]

    def test_matrix(self):
        self.assertEqual(pcset.matrix(self.webern_row), self.webern_matrix)

    def test_row_matrix_search(self):
        result = [[9, 3, 5], [3, 7, 0], [5, 0, 4], [10, 11, 9],
                  [7, 5, 1], [8, 9, 7], [0, 1, 2], [11, 8, 3],
                  [2, 6, 11], [6, 10, 8], [1, 4, 6], [4, 2, 10]]

        self.assertEqual(pcset.row_matrix_search(self.webern_matrix, [0, 1, 3]), result)

    def test_column_matrix_search(self):
        result = [[6, 2, 1], [10, 6, 4], [8, 11, 6], [1, 0, 7],
                  [11, 10, 2], [2, 4, 0], [9, 8, 10], [4, 1, 5],
                  [5, 7, 9], [0, 5, 3], [3, 9, 11], [7, 3, 8]]
        self.assertEqual(pcset.column_matrix_search(self.webern_matrix, [0, 1, 3]), result)
