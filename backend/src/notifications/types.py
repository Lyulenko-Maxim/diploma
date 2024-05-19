from typing import List, TypedDict

from src.management.models import Task
from src.users.models import Profile


class ProjectDataType(TypedDict):
    name: str


class ProfileDataType(TypedDict):
    profile: Profile


class TaskDataType(TypedDict):
    action: str
    task: Task
    subscribers: List[str]


class ExpelledMemberDataType(TypedDict):
    project: ProjectDataType
    member: ProfileDataType
    actor: ProfileDataType
