from langchain_core.tools import StructuredTool, tool
from pydantic import BaseModel, Field

from .data_process import SearchResultProduct, process_search_result
from .digikala_api import search_digikala


class DigikalaSearchToolInput(BaseModel):
    query: str = Field(..., description="Keyword or product name to search.")
    min_price: int | None = Field(
        ..., description="Minimum price in Iranian Toman, or None."
    )
    max_price: int | None = Field(
        ..., description="Maximum price in Iranian Toman, or None."
    )


class DigikalaSearchToolOutput(BaseModel):
    search_results: list[SearchResultProduct] = Field(
        ..., description="A list of products"
    )


digikala_search_tool_description = f"""
Search Digikala using query. Output is JSON with following schema:

{DigikalaSearchToolOutput.model_json_schema()}
"""


def get_digikala_search_tool(return_direct=True) -> StructuredTool:
    @tool(
        name_or_callable="digikala-search-tool",
        return_direct=return_direct,
        description=digikala_search_tool_description,
        args_schema=DigikalaSearchToolInput,
        response_format="content",
    )
    def digikala_search_tool(
        query: str,
        min_price: int | None,
        max_price: int | None,
    ) -> list[dict]:
        """Search Digikala"""
        search_result: dict = search_digikala(
            query=query,
            min_price=min_price,
            max_price=max_price,
        )
        search_results: list[SearchResultProduct] = process_search_result(search_result)
        output = DigikalaSearchToolOutput(search_results=search_results)
        output_json = output.model_dump_json(indent=2)
        return output_json

    return digikala_search_tool
