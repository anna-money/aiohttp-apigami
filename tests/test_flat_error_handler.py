"""Tests for the built-in aiohttp-apispec flat error format adapter."""

import json
from typing import Any

import pytest
from aiohttp import web
from marshmallow import ValidationError
from pytest_aiohttp.plugin import AiohttpClient

from aiohttp_apigami import flat_error_handler, request_schema, setup_aiohttp_apispec, validation_middleware
from tests.fixtures.schemas import RequestSchema


class TestUnit:
    def _call(self, messages: Any) -> web.HTTPUnprocessableEntity:
        with pytest.raises(web.HTTPUnprocessableEntity) as exc_info:
            flat_error_handler(
                ValidationError(messages),
                req=None,  # type: ignore[arg-type]
                schema=None,  # type: ignore[arg-type]
                error_status_code=422,
                error_headers=None,
            )
        return exc_info.value

    def test_strips_location_level(self) -> None:
        exc = self._call({"json": {"id": ["Not a valid integer."]}})
        assert json.loads(exc.text or "") == {"id": ["Not a valid integer."]}

    def test_merges_multiple_locations_and_logs(self, caplog: pytest.LogCaptureFixture) -> None:
        exc = self._call({"json": {"a": ["x"]}, "querystring": {"b": ["y"]}})
        assert json.loads(exc.text or "") == {"a": ["x"], "b": ["y"]}
        assert "flattening may overwrite same-named fields" in caplog.text

    def test_non_nested_messages_kept_as_is(self) -> None:
        exc = self._call(["plain error"])
        assert json.loads(exc.text or "") == ["plain error"]


async def test_response_body_is_flat(aiohttp_client: AiohttpClient) -> None:
    @request_schema(RequestSchema)
    async def handler(request: web.Request) -> web.Response:
        return web.json_response({})

    app = web.Application()
    app.router.add_post("/test", handler)
    setup_aiohttp_apispec(app, error_callback=flat_error_handler)
    app.middlewares.append(validation_middleware)

    client = await aiohttp_client(app)
    res = await client.post("/test", json={"id": "not-an-int"})

    assert res.status == 422
    assert await res.json() == {"id": ["Not a valid integer."]}
