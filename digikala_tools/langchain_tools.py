from langchain_core.tools import StructuredTool, tool

from .pydantic_models import DigikalaSearchToolInput, DigikalaSearchToolOutput
from .tool_functions import digikala_search_function


def get_digikala_search_tool(return_direct=True) -> StructuredTool:
    digikala_search_tool_description = f"""
    Search Digikala using query. Output is JSON with following schema:

    {DigikalaSearchToolOutput.model_json_schema()}
    """

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
        tool_input = DigikalaSearchToolInput(
            query=query, min_price=min_price, max_price=max_price
        )
        tool_output: DigikalaSearchToolOutput = digikala_search_function(tool_input)
        output_json = tool_output.model_dump_json(indent=2)
        return output_json

    return digikala_search_tool
