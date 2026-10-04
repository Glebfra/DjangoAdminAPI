from enum import StrEnum
from typing import Literal


FieldType = Literal[
    "string",
    "text",
    "integer",
    "big_integer",
    "small_integer",
    "positive_integer",
    "positive_small_integer",
    "float",
    "decimal",
    "boolean",
    "date",
    "datetime",
    "time",
    "duration",
    "email",
    "url",
    "slug",
    "uuid",
    "json",
    "binary",
    "file",
    "image",
    "choice",
    "relation",
    "one_to_one",
    "many_to_many",
    "unknown",
]


RelationType = Literal[
    "many_to_one",
    "one_to_one",
    "many_to_many",
]


class AdminAction(StrEnum):
    VIEW = "view"
    ADD = "add"
    CHANGE = "change"
    DELETE = "delete"
