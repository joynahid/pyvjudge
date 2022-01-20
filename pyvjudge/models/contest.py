import datetime as dt
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto
from typing import Dict, List, Generator, Union

from pyvjudge.models.user import User


class Verdict(Enum):
    ACCEPTED = auto()
    REJECTED = auto()


@dataclass
class ProblemProperty:
    title: str
    content: str
    hint: bool


@dataclass
class Problem:
    id: int
    title: str
    oj: str
    num: str
    url: str
    weight: int
    properties: List[ProblemProperty]
    languages: Dict[str, str] = None
    prob_num: str = None

    @property
    def index(self):
        return ord(self.num) - ord('A')

    def __repr__(self):
        return f"<Problem {self.num} {self.title}>"


@dataclass
class Description:
    format: str
    content: str


@dataclass
class ContestInfo:
    id: int
    title: str
    url: str
    created_at: datetime
    started_at: datetime
    ended_at: datetime
    manager: User
    problems: List[Problem]
    penalty_second: int = 1200
    description: Description = None
    announcement: str = None

    @property
    def elapsed(self) -> dt.timedelta:
        return dt.datetime.now() - self.started_at

    @property
    def remaining(self) -> dt.timedelta:
        return self.ended_at - dt.datetime.now()

    @property
    def is_running(self) -> bool:
        """As the name suggests, checks if the contest is running or not"""
        return self.remaining.total_seconds() > 0


@dataclass
class Submission:
    problem: Problem
    verdict: Verdict
    submitted_by: User
    submitted_at: datetime
    contest: ContestInfo = None

    @property
    def relative_submission_seconds(self) -> float:
        """Calculates how many seconds of contest time elapsed when the submission was made"""
        if self.contest is None:
            return 0
        return (self.submitted_at - self.contest.started_at).total_seconds()

    def is_successful(self) -> bool:
        """Returns true if the submission is OK/Accepted in the judge"""
        return self.verdict is Verdict.ACCEPTED

    def is_submitted_in_contest_time(self) -> bool:
        """
        Checks if it's official or unofficial submission. If it is submitted during contest time, then it will
        return true which makes it official submission.
        """
        return self.contest.started_at <= self.submitted_at <= self.contest.ended_at

    def __repr__(self):
        return f"<Submission submitted_by={self.submitted_by} problem={self.problem.prob_num} verdict={self.verdict}>"


@dataclass
class ProblemResult:
    problem: Problem
    best_submission: Union[Submission, None] = None
    attempts: int = 0
    penalty_seconds: float = 0


@dataclass
class Row:
    user: User
    score: int
    attempts: int
    total_penalty_seconds: float
    submissions: List[Submission]
    problem_results: List[ProblemResult]

    def __repr__(self):
        return f"<Row of={self.user.username} scored={self.score} penalty={self.total_penalty_seconds}>"


@dataclass
class Standing:
    contest: ContestInfo
    submissions: List[Submission]

    @property
    def problem_set(self):
        return self.contest.problems

    def rows_unofficial(self):
        return self.__get_rows(unofficial=True)

    @property
    def rows(self):
        """
        Each row of official participants. Official simply depicts,
        if the participant made submission during contest time
        """
        return self.__get_rows()

    def __get_rows(self, unofficial: bool = False) -> Generator[List[Row], None, None]:
        user_based_submissions = defaultdict(lambda: [])

        for submission in self.submissions:
            user_based_submissions[submission.submitted_by].append(submission)

        for user, submissions in user_based_submissions.items():
            penalty_secs = defaultdict(lambda: 0)
            attempts = defaultdict(lambda: 0)
            solved = defaultdict(lambda: None)
            problems = list(self.contest.problems)
            score = 0

            for submission in submissions:
                if (submission.is_successful() and submission.is_submitted_in_contest_time()) or unofficial:
                    penalty_secs[submission.problem.index] += \
                        attempts[submission.problem.index] \
                        * self.contest.penalty_second \
                        + submission.relative_submission_seconds

                    solved[submission.problem.index] = submission
                    score += problems[submission.problem.index].weight
                    continue
                attempts[submission.problem.index] += 1

            total_penalty = sum([p for (_, p) in penalty_secs.items()])

            problem_results: List[ProblemResult] = []
            for p in problems:
                problem_results.append(
                    ProblemResult(
                        problem=p,
                        best_submission=solved[p.index],
                        penalty_seconds=penalty_secs[p.index],
                        attempts=attempts[p.index]
                    )
                )

            yield Row(
                user=user, attempts=len(submissions),
                total_penalty_seconds=total_penalty, submissions=submissions, score=score,
                problem_results=problem_results
            )
