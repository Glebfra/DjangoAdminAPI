from dataclasses import dataclass
from decimal import Decimal

from .literals import FieldType, RelationType

@dataclass(frozen=True, slots=True)
class ChoiceMetadata:
    value: str | int | float | bool
    label: str


@dataclass(frozen=True, slots=True)
class RelationMetadata:
    type: RelationType
    app_label: str
    model_name: str
    verbose_name: str
    verbose_name_plural: str
    related_name: str | None = None


@dataclass(frozen=True, slots=True)
class FieldMetadata:
    name: str
    type: FieldType
    label: str

    required: bool
    editable: bool
    readonly: bool
    nullable: bool

    primary_key: bool = False
    unique: bool = False

    help_text: str = ""

    default: object | None = None

    max_length: int | None = None

    choices: tuple[ChoiceMetadata, ...] = ()

    relation: RelationMetadata | None = None

    min_value: int | float | Decimal | None = None
    max_value: int | float | Decimal | None = None

    max_digits: int | None = None
    decimal_places: int | None = None

    upload_to: str | None = None

    auto_now: bool = False
    auto_now_add: bool = False


@dataclass(frozen=True, slots=True)
class ModelMetadata:
    app_label: str
    model_name: str

    verbose_name: str
    verbose_name_plural: str

    fields: tuple[FieldMetadata, ...]

    list_display: tuple[str, ...]
    list_filter: tuple[str, ...]
    search_fields: tuple[str, ...]
    ordering: tuple[str, ...]

    can_view: bool
    can_add: bool
    can_change: bool
    can_delete: bool
