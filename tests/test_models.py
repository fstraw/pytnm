import pytest
import pytnm.utils.stamina as s


class TestRoadwaySeparator:
    def test_returns_header_string(self):
        fixture = "'L' /\n"
        separator = s.roadway_separator()
        assert separator == fixture

class TestBarrierSeparator:
    def test_returns_header_string(self):
        fixture = "'A' /\n"
        separator = s.barrier_separator()
        assert separator == fixture