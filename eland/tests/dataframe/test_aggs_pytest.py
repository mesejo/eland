# Licensed to Elasticsearch B.V under one or more agreements.
# Elasticsearch B.V licenses this file to you under the Apache 2.0 License.
# See the LICENSE file in the project root for more information

# File called _pytest for PyCharm compatability

import numpy as np
from pandas.testing import assert_frame_equal

from eland.tests.common import TestData


class TestDataFrameAggs(TestData):
    def test_basic_aggs(self):
        pd_flights = self.pd_flights()
        ed_flights = self.ed_flights()

        pd_sum_min = pd_flights.select_dtypes(include=[np.number]).agg(["sum", "min"])
        ed_sum_min = ed_flights.select_dtypes(include=[np.number]).agg(["sum", "min"])

        # Eland returns all float values for all metric aggs, pandas can return int
        # TODO - investigate this more
        pd_sum_min = pd_sum_min.astype("float64")
        assert_frame_equal(pd_sum_min, ed_sum_min, check_exact=False)

        pd_sum_min_std = pd_flights.select_dtypes(include=[np.number]).agg(
            ["sum", "min", "std"]
        )
        ed_sum_min_std = ed_flights.select_dtypes(include=[np.number]).agg(
            ["sum", "min", "std"]
        )

        print(pd_sum_min_std.dtypes)
        print(ed_sum_min_std.dtypes)

        assert_frame_equal(
            pd_sum_min_std, ed_sum_min_std, check_exact=False, check_less_precise=True
        )

    def test_terms_aggs(self):
        pd_flights = self.pd_flights()
        ed_flights = self.ed_flights()

        pd_sum_min = pd_flights.select_dtypes(include=[np.number]).agg(["sum", "min"])
        ed_sum_min = ed_flights.select_dtypes(include=[np.number]).agg(["sum", "min"])

        # Eland returns all float values for all metric aggs, pandas can return int
        # TODO - investigate this more
        pd_sum_min = pd_sum_min.astype("float64")
        assert_frame_equal(pd_sum_min, ed_sum_min, check_exact=False)

        pd_sum_min_std = pd_flights.select_dtypes(include=[np.number]).agg(
            ["sum", "min", "std"]
        )
        ed_sum_min_std = ed_flights.select_dtypes(include=[np.number]).agg(
            ["sum", "min", "std"]
        )

        print(pd_sum_min_std.dtypes)
        print(ed_sum_min_std.dtypes)

        assert_frame_equal(
            pd_sum_min_std, ed_sum_min_std, check_exact=False, check_less_precise=True
        )

    def test_aggs_median_var(self):
        pd_ecommerce = self.pd_ecommerce()
        ed_ecommerce = self.ed_ecommerce()

        pd_aggs = pd_ecommerce[
            ["taxful_total_price", "taxless_total_price", "total_quantity"]
        ].agg(["median", "var"])
        ed_aggs = ed_ecommerce[
            ["taxful_total_price", "taxless_total_price", "total_quantity"]
        ].agg(["median", "var"])

        print(pd_aggs, pd_aggs.dtypes)
        print(ed_aggs, ed_aggs.dtypes)

        # Eland returns all float values for all metric aggs, pandas can return int
        # TODO - investigate this more
        pd_aggs = pd_aggs.astype("float64")
        assert_frame_equal(pd_aggs, ed_aggs, check_exact=False, check_less_precise=2)
