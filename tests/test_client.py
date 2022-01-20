import os
import unittest
from unittest import mock

from pyvjudge.vjudge.api_client import VjudgeClient, SingleRanklistResponse
from tests.conftest import ENV_VARS

BASE_URL = "https://vjudge.net"
TEST_CONTEST_ID = 476543


class TestVjudgeClient(unittest.TestCase):
    def __init__(self, *args) -> None:
        with mock.patch.dict(os.environ, ENV_VARS):
            self.client = VjudgeClient(base_url=BASE_URL)
            assert self.client.base_url == BASE_URL
            super().__init__(*args)

    def test_initiate_client(self):
        assert isinstance(self.client, VjudgeClient)

    def test_single_ranklist_public_contest(self):
        data = self.client.get_single_ranklist(TEST_CONTEST_ID)
        assert isinstance(data, SingleRanklistResponse)
        assert data.id == TEST_CONTEST_ID

    def test_single_ranklist_private_contest(self):
        # login to the account
        self.client.login()

        # Register, should return True if already registered!
        registered = self.client.register_contest(462682, "udif")

        assert registered

        data = self.client.get_single_ranklist(462682)
        assert isinstance(data, SingleRanklistResponse)
        assert data.id == 462682
