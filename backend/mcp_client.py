import asyncio
from typing import Any

from mcp import Client

from backend.mcp_server import mcp

from backend.harness.errors import (
    MCPToolError,
    ToolResultError
)


# =========================================================
# Generic MCP call
# =========================================================

async def _call_mcp_tool(
    tool_name: str,
    arguments: dict[str, Any]
) -> Any:

    try:

        async with Client(mcp) as client:

            result = await client.call_tool(
                tool_name,
                arguments
            )

    except Exception as error:

        raise MCPToolError(
            f"Unable to call MCP tool '{tool_name}'."
        ) from error


    if result.is_error:

        raise MCPToolError(
            f"MCP tool '{tool_name}' returned an execution error."
        )


    structured = (
        result.structured_content
    )


    if structured is None:

        raise MCPToolError(
            f"MCP tool '{tool_name}'returned no structured content."
        )


    if not structured.get(
        "ok",
        False
    ):

        raise ToolResultError(
            structured.get(
                "error",
                (
                    f"Tool '{tool_name}' could not complete the request."
                )
            )
        )


    return structured["result"]


# =========================================================
# Sync wrapper
# =========================================================

def call_mcp_tool(
    tool_name: str,
    arguments: dict[str, Any]
) -> Any:

    return asyncio.run(
        _call_mcp_tool(
            tool_name,
            arguments
        )
    )


# =========================================================
# HealthBrief MCP client helpers
# =========================================================

def mcp_find_biomarker(
    report,
    biomarker_name
):

    return call_mcp_tool(
        "find_biomarker",
        {
            "report": report,
            "biomarker_name": biomarker_name
        }
    )


def mcp_get_abnormal_markers(
    report
):

    return call_mcp_tool(
        "get_abnormal_markers",
        {
            "report": report
        }
    )


def mcp_compare_biomarker(
    current_report,
    previous_report,
    biomarker_name
):

    return call_mcp_tool(
        "compare_biomarker",
        {
            "current_report": current_report,
            "previous_report": previous_report,
            "biomarker_name": biomarker_name
        }
    )


def mcp_prepare_visit_context(
    report
):

    return call_mcp_tool(
        "prepare_visit_context",
        {
            "report": report
        }
    )