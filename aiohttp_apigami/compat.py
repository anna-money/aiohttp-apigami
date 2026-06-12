"""Helpers for code migrating from aiohttp-apispec."""

import json
import logging
from typing import Any, NoReturn

import marshmallow as m
from aiohttp import web

logger = logging.getLogger(__name__)


def flat_error_handler(
    error: m.ValidationError,
    req: web.Request,
    schema: m.Schema,
    *args: Any,
    error_status_code: int | None = None,
    error_headers: dict[str, str] | None = None,
) -> NoReturn:
    """
    Error callback restoring the flat aiohttp-apispec 2.x error format.

    webargs 8 nests ``ValidationError.messages`` under the request location,
    e.g. ``{"json": {"field": ["Not a valid integer."]}}``. This handler
    strips the location level, so API clients keep receiving the flat
    ``{"field": ["Not a valid integer."]}`` body with a 422 response,
    exactly like aiohttp-apispec 2.x.

    If validation fails in several locations at once, flattening may
    overwrite same-named fields; an error is logged when that risk exists.

    Usage:

    .. code-block:: python

        from aiohttp_apigami import (
            flat_error_handler,
            setup_aiohttp_apispec,
        )

        setup_aiohttp_apispec(
            app, error_callback=flat_error_handler
        )
    """
    messages = error.messages
    if isinstance(messages, dict):
        if len(messages) > 1:
            logger.error(
                "Validation errors in multiple locations %s; flattening may overwrite same-named fields",
                sorted(messages),
            )
        # Strip the location level (e.g. {"json": {...}} -> {...})
        flat = {
            field: field_errors
            for location_errors in messages.values()
            if isinstance(location_errors, dict)
            for field, field_errors in location_errors.items()
        }
        messages = flat or messages

    raise web.HTTPUnprocessableEntity(
        text=json.dumps(messages),
        headers=error_headers,
        content_type="application/json",
    )
