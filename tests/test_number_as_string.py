"""Number fields with ``as_string=True`` dump strings, so the spec must document them as strings.

apispec maps fields by class and ignores ``as_string``, documenting ``"12.50"`` as a number. Clients that validate
responses against the spec, such as MCP clients checking ``structuredContent`` against ``outputSchema``, reject it.
"""

import json
from typing import Any

import pytest
from aiohttp import web
from apispec import APISpec
from marshmallow import Schema, fields, validate

from aiohttp_apigami import querystring_schema, request_schema, response_schema, setup_aiohttp_apispec
from aiohttp_apigami.constants import SWAGGER_DICT
from aiohttp_apigami.plugin import ApigamiPlugin


@pytest.mark.parametrize(
    ("openapi_version", "field", "expected"),
    [
        ("2.0", fields.Decimal(as_string=True), {"type": "string"}),
        ("2.0", fields.Decimal(as_string=True, allow_none=True), {"type": "string", "x-nullable": True}),
        ("3.0.3", fields.Decimal(as_string=True, allow_none=True), {"type": "string", "nullable": True}),
        ("3.1.0", fields.Decimal(as_string=True, allow_none=True), {"type": ["string", "null"]}),
        (
            "2.0",
            fields.Decimal(as_string=True, validate=validate.Range(min=0, max=100)),
            {"type": "string", "x-minimum": "0", "x-maximum": "100"},
        ),
        ("2.0", fields.Float(as_string=True), {"type": "string"}),
        ("2.0", fields.Integer(as_string=True), {"type": "string"}),
        ("2.0", fields.List(fields.Decimal(as_string=True)), {"type": "array", "items": {"type": "string"}}),
        ("2.0", fields.Decimal(), {"type": "number"}),
        ("2.0", fields.Integer(), {"type": "integer"}),
    ],
)
def test_field_property(openapi_version: str, field: fields.Field, expected: dict[str, Any]) -> None:
    plugin = ApigamiPlugin()
    APISpec(title="Test API", version="1.0.0", openapi_version=openapi_version, plugins=[plugin])

    assert plugin.converter is not None
    assert plugin.converter.field2property(field) == expected


class AmountsSchema(Schema):
    amount = fields.Decimal(as_string=True, required=True)
    fee = fields.Decimal(as_string=True, allow_none=True, validate=validate.Range(min=0))


class FilterSchema(Schema):
    min_amount = fields.Decimal(as_string=True)


@querystring_schema(FilterSchema)
@request_schema(AmountsSchema)
@response_schema(AmountsSchema, 200)
async def amounts_handler(request: web.Request) -> web.Response:
    return web.json_response({})


def _build_spec(openapi_version: str) -> dict[str, Any]:
    app = web.Application()
    app.router.add_post("/amounts", amounts_handler)
    setup_aiohttp_apispec(app=app, openapi_version=openapi_version, in_place=True)
    swagger: dict[str, Any] = json.loads(json.dumps(app[SWAGGER_DICT]))
    return swagger


def test_spec_v2() -> None:
    swagger = _build_spec("2.0")

    assert swagger["definitions"]["Amounts"] == {
        "type": "object",
        "properties": {
            "amount": {"type": "string"},
            "fee": {"type": "string", "x-minimum": "0", "x-nullable": True},
        },
        "required": ["amount"],
        "additionalProperties": False,
    }
    assert swagger["paths"]["/amounts"]["post"]["parameters"] == [
        {"in": "body", "required": False, "name": "body", "schema": {"$ref": "#/definitions/Amounts"}},
        {"in": "query", "name": "min_amount", "type": "string", "required": False},
    ]


def test_spec_v3() -> None:
    swagger = _build_spec("3.0.3")

    assert swagger["components"]["schemas"]["Amounts"] == {
        "type": "object",
        "properties": {
            "amount": {"type": "string"},
            "fee": {"type": "string", "x-minimum": "0", "nullable": True},
        },
        "required": ["amount"],
        "additionalProperties": False,
    }
    assert swagger["paths"]["/amounts"]["post"]["parameters"] == [
        {"in": "query", "name": "min_amount", "schema": {"type": "string"}, "required": False},
    ]
