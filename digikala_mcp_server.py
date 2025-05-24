from mcp.server.fastmcp import FastMCP

from digikala_tools.pydantic_models import (
    DigikalaSearchToolInput,
    DigikalaSearchToolOutput,
)
from digikala_tools.tool_functions import digikala_search_function

mcp = FastMCP("Digikala MCP Server")

digikala_search_tool_description = f"""
Search Digikala using query and optional price filters.

Output is JSON with following schema:

{DigikalaSearchToolOutput.model_json_schema()}
"""


@mcp.tool(name="search_digikala", description=digikala_search_tool_description)
def search_digikala(
    query: str, min_price: int | None = None, max_price: int | None = None
) -> dict:
    """
    Search Digikala using query and optional price filters.

    Parameters:
        query: Keyword or product name to search.
        min_price: Minimum price in Iranian Toman, or None.
        max_price: Maximum price in Iranian Toman, or None.
    """
    try:
        tool_input = DigikalaSearchToolInput(
            query=query, min_price=min_price, max_price=max_price
        )
        tool_output: DigikalaSearchToolOutput = digikala_search_function(tool_input)
        # Indicate failure in case of empty search result
        if len(tool_output.search_results) == 0:
            return -1.0
        output_json = tool_output.model_dump_json(indent=2)
        return output_json

    except Exception:
        # Indicate failure in case of exceptions
        return -1.0


if __name__ == "__main__":
    mcp.run()
