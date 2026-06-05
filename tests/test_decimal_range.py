"""Regression tests for https://github.com/anna-money/aiohttp-apigami/issues/115.

``fields.Decimal`` combined with ``validate.Range`` made apispec serialize the
``min``/``max`` bounds back through the field, producing ``Decimal`` values in
the spec dict. ``json.dumps`` cannot serialize ``Decimal``, so the
``swagger.json`` endpoint returned a 500.
"""

import json
from decimal import Decimal
from typing import Any

from aiohttp import web
from aiohttp.test_utils import TestClient
from marshmallow import Schema, fields, validate
from pytest_aiohttp.plugin import AiohttpClient

from aiohttp_apigami import request_schema, setup_aiohttp_apispec
from aiohttp_apigami.constants import SWAGGER_DICT


class DecimalSchema(Schema):
    amount = fields.Decimal(
        required=True,
        validate=validate.Range(min=0, max=100, min_inclusive=False),
    )


@request_schema(DecimalSchema)
async def decimal_handler(request: web.Request) -> web.Response:
    return web.json_response({"msg": "done"})


def _build_app() -> web.Application:
    app = web.Application()
    app.router.add_post("/decimal", decimal_handler)
    setup_aiohttp_apispec(app=app, url="/api/docs/api-docs", in_place=True)
    return app


def test_swagger_dict_is_json_serializable() -> None:
    app = _build_app()
    # Should not raise "Object of type Decimal is not JSON serializable".
    json.dumps(app[SWAGGER_DICT])

    amount = app[SWAGGER_DICT]["definitions"]["Decimal"]["properties"]["amount"]
    assert amount["minimum"] == 0
    assert amount["maximum"] == 100
    assert not isinstance(amount["minimum"], Decimal)
    assert not isinstance(amount["maximum"], Decimal)


async def test_swagger_json_endpoint_returns_200(aiohttp_client: AiohttpClient) -> None:
    client: TestClient[web.Request, web.Application] = await aiohttp_client(_build_app())
    resp = await client.get("/api/docs/api-docs")
    assert resp.status == 200
    docs: dict[str, Any] = await resp.json()
    amount = docs["definitions"]["Decimal"]["properties"]["amount"]
    assert amount["minimum"] == 0
    assert amount["maximum"] == 100
