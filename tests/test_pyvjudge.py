import unittest

from pyvjudge import PyVjudge
from pyvjudge.models.contest import Standing


class TestPyVjudge(unittest.TestCase):
    def __init__(self, *args) -> None:
        self.pv = PyVjudge()
        super().__init__(*args)

    def test_get_standing(self):
        standing = self.pv.get_standing(PyVjudge.find_contest_id("https://vjudge.net/contest/458956#overview"))
        assert isinstance(standing, Standing)

    def test_find_contest_id(self):
        assert PyVjudge.find_contest_id("https://vjudge.net/contest/458956#overview") == 458956
