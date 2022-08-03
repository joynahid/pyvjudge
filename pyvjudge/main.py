import datetime
import logging
import re
from typing import Union, List, Dict

from pyvjudge.models.contest import Submission, Verdict, Standing
from pyvjudge.models.user import User
from pyvjudge.vjudge.api_client import VjudgeClient
from pyvjudge.vjudge.contest_scraper import ContestScraper

logging.basicConfig()
LOGGER = logging.getLogger("PyVjudge")


class PyVjudge:
    def __init__(self, vjudge_client: VjudgeClient = None):
        self.client = vjudge_client or VjudgeClient()
        self.contest_scraper = ContestScraper(self.client)

    def get_standing(self, contest_id: Union[str, int], contest_password: str = None) -> Standing:
        if not (contest_password is None):
            LOGGER.info("Password was provided, registering the contest...")
            self.client.register_contest(contest_id, contest_password)

        LOGGER.info(f"Scraping contest info")
        contest_info = self.contest_scraper.scrape_contest_info(contest_id)

        LOGGER.info(f"Fetching standing ({contest_id})")
        single_ranklist = self.client.get_single_ranklist(contest_id)
        submissions = self.build_submissions(contest_info, single_ranklist)
        return Standing(contest=contest_info, submissions=submissions)

    def __del__(self):
        self.client.close()

    @staticmethod
    def build_submissions(contest_info, single_ranklist) -> List[Submission]:
        problem_hashtable = dict()
        for p in contest_info.problems:
            problem_hashtable[p.index] = p

        users_hashtable: Dict[str, List[str]] = single_ranklist.participants

        submissions: List[Submission] = []
        for s in single_ranklist.submissions:
            cur_user = users_hashtable[str(s[0])]
            sub = Submission(
                contest=contest_info,
                problem=problem_hashtable[s[1]],
                verdict=Verdict.ACCEPTED if s[2] else Verdict.REJECTED,
                submitted_at=contest_info.started_at + datetime.timedelta(seconds=s[3]),
                submitted_by=User(id=s[0], username=cur_user[0], nickname=cur_user[1], avatar=cur_user[2])
            )
            submissions.append(sub)
        return submissions

    @staticmethod
    def find_contest_id(url: str) -> int:
        """Finds Contest ID from vjudge contest url"""
        m = re.match(r'.*/contest/(\d+).+$', url, re.I)
        groups = m.groups()

        if len(groups) > 0:
            return int(groups[0])
