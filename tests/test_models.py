import unittest
from datetime import datetime, timedelta

from pyvjudge.models.contest import ContestInfo, Problem, ProblemProperty, Description
from pyvjudge.models.user import User


class TestStandings(unittest.TestCase):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        pass


class TestProblem(unittest.TestCase):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.problem = problem

    def test_problem_attrs(self):
        assert isinstance(self.problem, Problem)
        assert type(self.problem.index) is int


class TestContestInfo(unittest.TestCase):
    def __init__(self, *args) -> None:
        super().__init__(*args)
        self.contest = ContestInfo(
            id=476537, title='Stamford Practice 4', url='/contest/476543',
            created_at=datetime(2022, 1, 13, 19, 10, 25), started_at=datetime(2022, 1, 13, 19, 15),
            ended_at=datetime(2022, 1, 13, 23, 15), manager=User(username="TarifEzaz", id=15155),
            problems=[problem], penalty_second=1200, description=Description(
                format='HTML',
                content="[Cloned from <a href='https://vjudge.net/contest/466932' target='_blank'>DSA - 2021 replay "
                        "jiangxi Province program Contest</a>] "
            ), announcement=''
        )

    def test_contest_is_not_running(self):
        assert self.contest.is_running is False
        assert self.contest.remaining < timedelta(seconds=0)

    def test_contest_is_running(self):
        now = datetime.now()
        self.contest.started_at = now
        self.contest.ended_at = now + timedelta(seconds=2)
        assert self.contest.is_running is True
        assert self.contest.remaining > timedelta(seconds=0)


problem = Problem(
    id=4023801, title='Continued Fraction', oj='Gym', num='B', url='/contest/476543#problem/B', weight=1,
    properties=[ProblemProperty(title='Time limit', content='1000 ms', hint=False),
                ProblemProperty(title='Memory limit', content='262144 kB', hint=False),
                ProblemProperty(title='OS', content='Windows', hint=False), ProblemProperty(
            title='Source', content='2021 Jiangxi Provincial Collegiate Programming Contest', hint=True
        ), ProblemProperty(
            title='Editorial',
            content='<a href="CDN_BASE_URL/51220f59bfa185e39be8d8bc27bd4913?v=1642079398" title="statements.pdf" '
                    'target="_blank">Statements (en)</a>\n<a '
                    'href="CDN_BASE_URL/bf002b18b58f1d4ae30b946f6682a629?v=1642079398" title="tutorials.pdf" '
                    'target="_blank">Tutorial (zh)</a>',
            hint=True
        )],
    languages={'67': 'Ruby 3.0.0', '48': 'Kotlin 1.4.31', '28': 'D DMD32 v2.091.0', '70': 'PyPy 3.7 (7.3.5, 64bit)',
               '50': 'GNU G++14 6.4.0', '72': 'Kotlin 1.5.31', '73': 'GNU G++20 11.2.0 (64 bit, winlibs)',
               }, prob_num='103366B'
)
