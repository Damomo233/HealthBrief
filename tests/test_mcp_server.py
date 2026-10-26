import anyio

from mcp import Client

from backend.mcp_server import mcp


sample_report = {
    "biomarkers": [
        {
            "name": "LDL Cholesterol",
            "value": 168,
            "unit": "mg/dL",
            "lower_bound": 0,
            "upper_bound": 130
        }
    ]
}


async def main():

    async with Client(mcp) as client:

        tools = await client.list_tools()

        print("Available MCP tools:")

        for tool in tools.tools:
            print("-", tool.name)


        result = await client.call_tool(
            "find_biomarker",
            {
                "report": sample_report,
                "biomarker_name": "LDL"
            }
        )


        print("\nStructured result:")

        print(
            result.structured_content
        )


if __name__ == "__main__":
    anyio.run(main)