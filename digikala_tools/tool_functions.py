"""Framework agnostic tools as simple python functions."""

from .data_process import process_search_result
from .digikala_api import search_digikala
from .pydantic_models import (
    DigikalaSearchToolInput,
    DigikalaSearchToolOutput,
    SearchResultProduct,
)


def digikala_search_function(
    tool_input: DigikalaSearchToolInput,
) -> DigikalaSearchToolOutput:
    """Digikala Search Function"""
    search_result: dict = search_digikala(
        query=tool_input.query,
        min_price=tool_input.min_price,
        max_price=tool_input.max_price,
    )
    search_results: list[SearchResultProduct] = process_search_result(search_result)
    output = DigikalaSearchToolOutput(search_results=search_results)
    return output
