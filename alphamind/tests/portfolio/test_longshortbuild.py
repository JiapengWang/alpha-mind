# -*- coding: utf-8 -*-
"""
Created on 2017-5-9

@author: cheng.li
"""

import unittest
import numpy as np
import pandas as pd
from alphamind.portfolio.longshortbulder import long_short_build


class TestLongShortBuild(unittest.TestCase):

    def setUp(self):
        self.x = np.random.randn(3000, 10)
        self.groups = np.random.randint(10, 40, size=3000)

    def test_long_short_build(self):
        x = self.x[:, 0].flatten()
        calc_weights = long_short_build(x).flatten()
        expected_weights = x / np.abs(x).sum()
        np.testing.assert_array_almost_equal(calc_weights, expected_weights)

        calc_weights = long_short_build(self.x, leverage=2)
        expected_weights = self.x / np.abs(self.x).sum(axis=0) * 2
        np.testing.assert_array_almost_equal(calc_weights, expected_weights)

    def test_long_short_build_with_group(self):
        x = self.x[:, 0].flatten()
        calc_weights = long_short_build(x, groups=self.groups).flatten()
        expected_weights = pd.Series(x).groupby(self.groups).apply(lambda s: s / np.abs(s).sum())
        np.testing.assert_array_almost_equal(calc_weights, expected_weights)

        calc_weights = long_short_build(self.x, groups=self.groups)
        expected_weights = pd.DataFrame(self.x).groupby(self.groups).apply(lambda s: s / np.abs(s).sum(axis=0))
        np.testing.assert_array_almost_equal(calc_weights, expected_weights)


if __name__ == '__main__':
    unittest.main()
