"""Backward compatibility shims for code migrating from aiohttp-apispec."""

import pytest
from aiohttp import web

from aiohttp_apigami import marshal_with, request_schema, response_schema, use_kwargs
from tests.fixtures.schemas import RequestSchema


class TestAliases:
    def test_use_kwargs_is_request_schema(self) -> None:
        assert use_kwargs is request_schema

    def test_marshal_with_is_response_schema(self) -> None:
        assert marshal_with is response_schema


class TestLocationsShim:
    def test_single_location_list_is_accepted_with_deprecation_warning(self) -> None:
        with pytest.warns(DeprecationWarning, match="`locations` argument is deprecated"):

            @request_schema(RequestSchema, locations=["querystring"])
            async def handler(request: web.Request) -> web.Response:
                return web.json_response({})

        assert handler.__schemas__[0].location == "querystring"  # type: ignore[attr-defined]
        assert handler.__apispec__["schemas"][0]["location"] == "querystring"  # type: ignore[attr-defined]

    @pytest.mark.parametrize("bad_locations", [["querystring", "form"], []])
    def test_non_single_locations_raise_value_error(self, bad_locations: list[str]) -> None:
        with (
            pytest.warns(DeprecationWarning),
            pytest.raises(ValueError, match="must contain exactly one location"),
        ):

            @request_schema(RequestSchema, locations=bad_locations)
            async def handler(request: web.Request) -> web.Response:
                return web.json_response({})

    @pytest.mark.parametrize("explicit_location", ["form", "json"])
    def test_location_and_locations_together_raise_value_error(self, explicit_location: str) -> None:
        with (
            pytest.warns(DeprecationWarning),
            pytest.raises(ValueError, match="not both"),
        ):

            @request_schema(RequestSchema, location=explicit_location, locations=["querystring"])  # type: ignore[arg-type]
            async def handler(request: web.Request) -> web.Response:
                return web.json_response({})

    def test_non_list_locations_raise_type_error(self) -> None:
        with (
            pytest.warns(DeprecationWarning),
            pytest.raises(TypeError, match="`locations` must be a list, got str"),
        ):

            @request_schema(RequestSchema, locations="querystring")
            async def handler(request: web.Request) -> web.Response:
                return web.json_response({})


class TestUnknownKwargs:
    def test_unexpected_keyword_argument_raises_type_error(self) -> None:
        with pytest.raises(TypeError, match="unexpected keyword arguments: \\['foo'\\]"):

            @request_schema(RequestSchema, foo=1)
            async def handler(request: web.Request) -> web.Response:
                return web.json_response({})

    def test_required_kwarg_still_accepted(self) -> None:
        @request_schema(RequestSchema, required=True)
        async def handler(request: web.Request) -> web.Response:
            return web.json_response({})

        assert handler.__apispec__["schemas"][0]["options"] == {"required": True}  # type: ignore[attr-defined]
