# mypy: disable-error-code="attr-defined"
from importlib import metadata

from .compat import flat_error_handler
from .core import AiohttpApiSpec, OpenApiVersion, setup_aiohttp_apispec
from .decorators import (
    cookies_schema,
    docs,
    form_schema,
    headers_schema,
    json_schema,
    marshal_with,
    match_info_schema,
    querystring_schema,
    request_schema,
    response_schema,
    use_kwargs,
)
from .middlewares import validation_middleware

__all__ = [
    "AiohttpApiSpec",
    "OpenApiVersion",
    "__version__",
    "cookies_schema",
    "docs",
    "flat_error_handler",
    "form_schema",
    "headers_schema",
    "json_schema",
    "marshal_with",
    "match_info_schema",
    "querystring_schema",
    "request_schema",
    "response_schema",
    "setup_aiohttp_apispec",
    "use_kwargs",
    "validation_middleware",
]

__version__ = metadata.version(__package__)
