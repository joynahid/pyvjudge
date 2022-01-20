import datetime
import json
from typing import Dict, List

from bs4 import BeautifulSoup

from pyvjudge.models.contest import ContestInfo, Problem, ProblemProperty, Description
from pyvjudge.models.user import User
from pyvjudge.vjudge.api_client import VjudgeClient

CONTEST_URL: str = "/contest/{contest_id}"


class ContestScraper:
    def __init__(
            self, client: VjudgeClient
    ) -> None:
        """
        This scraper will scrape contest from the contest url. It leverages the dataJson hidden inside the html

        Args:
            client (VjudgeClient): Vjudge APIClient
        """
        self.client = client

    def scrape_contest_info(self, contest_id) -> ContestInfo:
        req_url = CONTEST_URL.format(contest_id=contest_id)
        resp = self.client.get(req_url)

        if resp.status_code != 200:
            raise BadVjudgeResponse()

        html = resp.text

        soup = BeautifulSoup(html, "html.parser")

        data = self.find_data_json(soup)

        self.is_contest_accessible(data.get("openness"))

        return ContestInfo(
            id=data['id'],
            title=data['title'],
            url=req_url,
            started_at=datetime.datetime.fromtimestamp(data['begin'] // 1000),
            ended_at=datetime.datetime.fromtimestamp(data['end'] // 1000),
            created_at=datetime.datetime.fromtimestamp(data['createTime'] // 1000),
            announcement=data['announcement'],
            description=Description(**data['description']),
            penalty_second=data['penalty'],
            manager=User(username=data['managerName'], id=data["managerId"]),
            problems=list(self.parse_problems_from_data_json(data['problems'], contest_id))
        )

    @staticmethod
    def is_contest_accessible(openness: int) -> bool:
        if openness == 0:
            return True
        raise ContestNotAccessible()

    @staticmethod
    def parse_problems_from_data_json(problems: List, contest_id: int) -> List[Problem]:
        problem_uri = CONTEST_URL.format(contest_id=contest_id) + "#problem/{}"

        for p in problems:
            yield Problem(
                id=p['pid'],
                num=p['num'],
                title=p['title'],
                oj=p['oj'],
                prob_num=p.get('probNum'),
                weight=p['weight'],
                languages=p.get('languages'),
                properties=[ProblemProperty(**x) for x in p['properties']],
                url=problem_uri.format(p["num"])
            )

    @staticmethod
    def find_data_json(soup: BeautifulSoup) -> Dict:
        """Extracts json data from html returned by vjudge contest_url

        Args:
            soup (BeautifulSoup): Html soup
        """
        assert isinstance(soup, BeautifulSoup)

        data = soup.find("textarea", {"name": "dataJson"})

        if not data:
            raise ValueError("HTML doesn't contain any \"dataJson\" named attribute")

        return json.loads(data.text)


class BadVjudgeResponse(Exception):
    pass


class ContestNotAccessible(Exception):
    def __init__(self):
        super().__init__(
            "Contest isn't directly accessible. "
            "Make sure the account has access to the contest directly. "
            "If necessary, login or register the contest first with valid password."
        )
