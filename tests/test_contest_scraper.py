import os
import unittest
from dataclasses import dataclass
from unittest import mock

from bs4 import BeautifulSoup

from pyvjudge.models.contest import ContestInfo
from pyvjudge.vjudge.api_client import VjudgeClient
from pyvjudge.vjudge.contest_scraper import ContestScraper
from tests.conftest import ENV_VARS

BASE_URL = "https://vjudge.net"

TEST_CONTEST_IDS = [476543, 502668]

class TestContestScraper(unittest.TestCase):
    def __init__(self, *args) -> None:
        with mock.patch.dict(os.environ, ENV_VARS):
            client = VjudgeClient(base_url=BASE_URL)
            self.scraper = ContestScraper(client)
            super().__init__(*args)

    def test_scraper_instance(self):
        assert isinstance(self.scraper, ContestScraper)

    def test_find_data_json(self):
        with open("tests/data/sample_contest_page.html", "r") as f:
            html = f.read()
            soup = BeautifulSoup(html, "html.parser")
            data_json = self.scraper.find_data_json(soup)
            assert isinstance(data_json, dict)

    def test_scrape_contest_info(self):
        with open("tests/data/sample_contest_page.html", "r") as f:
            html = f.read()

            @dataclass
            class Response:
                status_code = 200
                text = html

            self.scraper.client.get = lambda *args, **kwargs: Response()

        for c_id in TEST_CONTEST_IDS:
            contest_info = self.scraper.scrape_contest_info(c_id)
            assert isinstance(contest_info, ContestInfo)
