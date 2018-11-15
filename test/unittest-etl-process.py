#!/usr/bin/env python3
from .fakesparksession import PySparkTest
from etl import extract


class SimpleTest(PySparkTest):
    """
    Will perform test on the functions used within the ETL process with a fake spark session
    """
    def test_basic(self):
        expected_df = extract(self.spark)

        self.assertEquals(expected_df.schema.names, ["date", "time", "user_id", "url", "ip", "user_agent_string"])
