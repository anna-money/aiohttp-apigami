from dataclasses import is_dataclass
from decimal import Decimal
from inspect import isclass
from string import Formatter
from typing import Any, TypeVar, cast, get_origin

import marshmallow as m
from aiohttp import web
from aiohttp.abc import AbstractView
from aiohttp.typedefs import Handler

from .constants import API_SPEC_ATTR, SCHEMAS_ATTR
from .typedefs import IDataclass, SchemaBuilder, SchemaType
from .validation import ValidationSchema

try:
    import marshmallow_recipe as mr

except ImportError:  # pragma: no cover
    mr = None  # type: ignore

T = TypeVar("T")
TDataclass = TypeVar("TDataclass", bound=IDataclass)


def get_path(route: web.AbstractRoute) -> str | None:
    """Get path string from a route."""
    if route.resource is None:
        return None
    return route.resource.canonical


def get_path_keys(path: str) -> list[str]:
    """Get path keys from a path string."""
    return [i[1] for i in Formatter().parse(path) if i[1]]


def is_class_based_view(handler: Handler | type[AbstractView]) -> bool:
    """Check if the handler is a class-based view."""
    if not isclass(handler):
        return False

    return issubclass(handler, web.View)


def get_or_set_apispec(func: T) -> dict[str, Any]:
    func_apispec: dict[str, Any]
    if hasattr(func, API_SPEC_ATTR):
        func_apispec = getattr(func, API_SPEC_ATTR)
    else:
        func_apispec = {"schemas": [], "responses": {}, "parameters": []}
        setattr(func, API_SPEC_ATTR, func_apispec)
    return func_apispec


def get_or_set_schemas(func: T) -> list[ValidationSchema]:
    func_schemas: list[ValidationSchema]
    if hasattr(func, SCHEMAS_ATTR):
        func_schemas = getattr(func, SCHEMAS_ATTR)
    else:
        func_schemas = []
        setattr(func, SCHEMAS_ATTR, func_schemas)
    return func_schemas


def _resolve_schema_class(schema: type[m.Schema]) -> m.Schema:
    """Instantiate a marshmallow Schema class."""
    return schema()


def _resolve_dataclass(schema: type[TDataclass]) -> m.Schema:
    """Build a Schema from a dataclass (or a generic alias of one)."""
    if mr is None:
        raise RuntimeError(
            "marshmallow-recipe is required for dataclass support. "
            "Install it with `pip install aiohttp-apigami[dataclass]`."
        )
    return mr.schema(schema)


def _resolve_schema_builder(schema: SchemaBuilder) -> m.Schema:
    """Invoke a callable schema builder and validate its result."""
    built = schema()
    if not isinstance(built, m.Schema):
        raise ValueError(f"Schema builder must return a marshmallow Schema instance, got {type(built).__name__}")
    return built


def _is_dataclass_schema(schema: Any) -> bool:
    """Check if schema is a dataclass or a generic alias of one.

    For generic aliases like ``MyClass = MyBaseClass[InnerType]``,
    ``get_origin()`` returns ``MyBaseClass``.
    """
    origin = get_origin(schema)
    return bool(is_dataclass(origin if origin is not None else schema))


def resolve_schema_instance(schema: SchemaType | type[TDataclass] | SchemaBuilder) -> m.Schema:
    # Dataclass types and callables (Schema classes, builders) all overlap, so
    # order matters: dedicated types first, the generic callable builder last.
    match schema:
        case type() as cls if issubclass(cls, m.Schema):
            return _resolve_schema_class(cls)
        case m.Schema():
            return schema
        case _ if _is_dataclass_schema(schema):
            return _resolve_dataclass(cast("type[TDataclass]", schema))
        case _ if callable(schema):
            return _resolve_schema_builder(cast("SchemaBuilder", schema))
        case _:
            raise ValueError(f"Invalid schema type: {schema}")


def make_json_serializable(value: Any) -> Any:
    """Recursively convert spec values into JSON-serializable types.

    apispec serializes ``validate.Range`` bounds back through the field they are
    attached to (see ``FieldConverterMixin.field2range``). For a ``fields.Decimal``
    field this yields ``Decimal`` ``minimum``/``maximum`` values, which the stdlib
    ``json`` encoder used by ``web.json_response`` cannot serialize.

    Decimals are converted to ``int`` when integral and ``float`` otherwise.
    See https://github.com/anna-money/aiohttp-apigami/issues/115.
    """
    if isinstance(value, dict):
        return {k: make_json_serializable(v) for k, v in value.items()}
    if isinstance(value, list):
        return [make_json_serializable(v) for v in value]
    if isinstance(value, Decimal):
        return int(value) if value == value.to_integral_value() else float(value)
    return value
