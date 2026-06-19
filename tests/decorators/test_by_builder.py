from dataclasses import dataclass

import marshmallow as m
import marshmallow_recipe as mr
import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient
from pytest_aiohttp.plugin import AiohttpClient

from aiohttp_apigami import request_schema, response_schema, setup_aiohttp_apispec, validation_middleware
from aiohttp_apigami.typedefs import IDataclass, SchemaBuilder
from aiohttp_apigami.validation import ValidationSchema


@dataclass
class RequestData:
    id: int
    name: str


class CapitalCamelCaseSchemaBuilder:
    """A callable object that builds a marshmallow Schema (issue #41)."""

    def __init__(self, data_cls: type[IDataclass]) -> None:
        self._data_cls = data_cls

    def __call__(self) -> m.Schema:
        return mr.schema(self._data_cls, naming_case=mr.CAPITAL_CAMEL_CASE)


def test_request_schema_with_builder() -> None:
    """request_schema resolves a SchemaBuilder into a Schema instance at decoration time."""

    @request_schema(CapitalCamelCaseSchemaBuilder(RequestData))
    async def index(request: web.Request) -> web.Response:
        return web.json_response({})

    assert hasattr(index, "__schemas__")
    assert len(index.__schemas__) == 1
    schema = index.__schemas__[0]
    assert isinstance(schema, ValidationSchema)
    assert isinstance(schema.schema, m.Schema)
    # The builder applied CapitalCamelCase naming: attribute names stay snake,
    # the serialized data_key is CapitalCamelCase.
    assert set(schema.schema.fields) == {"id", "name"}
    assert {f.data_key for f in schema.schema.fields.values()} == {"Id", "Name"}


def test_response_schema_with_builder() -> None:
    """response_schema resolves a SchemaBuilder into a Schema instance."""

    @response_schema(CapitalCamelCaseSchemaBuilder(RequestData), 200)
    async def index(request: web.Request) -> web.Response:
        return web.json_response({})

    response_spec = index.__apispec__["responses"]["200"]
    assert isinstance(response_spec["schema"], m.Schema)
    assert set(response_spec["schema"].fields) == {"id", "name"}


def test_builder_satisfies_schema_builder_protocol() -> None:
    """The builder is structurally a SchemaBuilder."""
    builder: SchemaBuilder = CapitalCamelCaseSchemaBuilder(RequestData)
    assert isinstance(builder(), m.Schema)


@pytest.fixture
async def builder_app(aiohttp_client: AiohttpClient) -> TestClient[web.Request, web.Application]:
    @request_schema(CapitalCamelCaseSchemaBuilder(RequestData))
    async def handler(request: web.Request) -> web.Response:
        data: RequestData = request["data"]
        return web.json_response({"id": data.id, "name": data.name})

    app = web.Application()
    setup_aiohttp_apispec(app=app)
    app.middlewares.append(validation_middleware)
    app.router.add_post("/builder", handler)
    return await aiohttp_client(app)


@pytest.mark.asyncio
async def test_builder_end_to_end_ok(builder_app: TestClient[web.Request, web.Application]) -> None:
    """Valid CapitalCamelCase payload is parsed into a dataclass instance."""
    res = await builder_app.post("/builder", json={"Id": 1, "Name": "max"})
    assert res.status == 200
    assert await res.json() == {"id": 1, "name": "max"}


@pytest.mark.asyncio
async def test_builder_end_to_end_validation_error(builder_app: TestClient[web.Request, web.Application]) -> None:
    """Invalid payload through a builder-produced schema is rejected with 422."""
    res = await builder_app.post("/builder", json={"Id": "not-an-int", "Name": "max"})
    assert res.status == 422
