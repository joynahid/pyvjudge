import json
import logging
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Union

from httpx import Client

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(level=logging.DEBUG)


class VjudgeLoginError(Exception):
    def __init__(self, handle: str) -> None:
        super().__init__(f"Couldn't login handle {handle} to vjudge")


class VjudgeContestRegistrationError(Exception):
    def __init__(self, contest_id: str) -> None:
        super().__init__(f"Couldn't register contest with {contest_id}")


@dataclass
class SingleRanklistResponse:
    id: int
    title: str
    begin: int
    length: int
    is_replay: bool
    version: str
    participants: Dict[str, List[str]]
    submissions: List[List[int]]

    def __repr__(self) -> str:
        return f"<SingleRanklistResponse {self.title}>"


class VjudgeClient(Client):
    """Vjudge Client"""

    user_login = "/user/login"
    contest_login_url = "/contest/login/{contest_id}"
    contest_rank_single = "/contest/rank/single/{contest_id}"
    contest_url = "/contest/{contest_id}"

    response_hooks = []
    request_hooks = []

    def __init__(self, *args, **kwargs):
        kwargs["base_url"] = kwargs.get("base_url", os.environ["VJUDGE_BASE_URL"])

        event_hooks = {
            "request": self.register_request_hooks(),
            "response": self.register_response_hooks()
        }

        kwargs["event_hooks"] = event_hooks

        super().__init__(*args, **kwargs)

    def register_request_hooks(self):
        LOGGER.debug(f"Request hooks are set as {self.request_hooks}")
        return self.request_hooks

    def register_response_hooks(self):
        LOGGER.debug(f"Response hooks are set as {self.response_hooks}")
        return self.response_hooks

    def login(self, username: str = None, password: str = None) -> bool:
        """logs in a user with valid credentials. It finds credentials in the environment variables if not provided
        as parameters

        Raises:
            VjudgeLoginError: When credentials are wrong

        Returns:
            bool: True if success
        """

        if (username or password) is None:
            username = os.environ["VJUDGE_USERNAME"]
            password = os.environ["VJUDGE_PASSWORD"]

        payload = {"username": username, "password": password}

        res = self.post(self.user_login, data=payload)

        res.raise_for_status()

        if res.text != "success":
            raise VjudgeLoginError(username)

        return True

    def register_contest(self, contest_id: Union[str, int], contest_password: str) -> bool:
        """Registers contest with password. Required once by a single vjudge account

        Args:
            contest_id (int): Contest ID found as suffix in the contest URL
            contest_password (str): Password set to protect contest

        Returns:
            bool: True if successful or already registered
        """

        res = self.post(
            self.contest_login_url.format(contest_id=contest_id),
            data=dict(password=contest_password),
        )

        if not res:
            logging.info(
                "Contest login failed. Please check your contest password and contest id"
            )
            raise VjudgeContestRegistrationError(contest_id)

        return True

    def get_single_ranklist(self, contest_id: Union[str, int]) -> Optional[SingleRanklistResponse]:
        """Gets ranklist from internal api /contest/rank/single/contestId

        Args:
            contest_id (str or int): Contest ID found in vjudge contest url

        Returns:
            SingleRanklistResponse | None
        """
        req_url = self.contest_rank_single.format(contest_id=contest_id)
        res = self.get(req_url)

        if not res.text:
            return None

        try:
            data: Dict = res.json()
            data.update({"is_replay": data.get("isReplay")})
            del data["isReplay"]

            return SingleRanklistResponse(**data)
        except json.JSONDecodeError as exc:
            logging.error(exc, exc_info=True)
