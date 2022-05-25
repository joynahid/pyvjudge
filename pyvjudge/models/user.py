from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    id: int
    username: str
    nickname: Optional[str] = ""
    avatar: str = None
    email: Optional[str] = None
    school: Optional[str] = None

    def __repr__(self) -> str:
        return f"<User {self.username}>"

    def __hash__(self):
        return self.id


@dataclass
class Team:
    members: List[User]
