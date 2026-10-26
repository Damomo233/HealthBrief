from typing import Any

from mcp.server import MCPServer
from mcp.types import ToolAnnotations

from backend.services.tools import (
    find_biomarker as find_biomarker_service,
    get_abnormal_markers as get_abnormal_markers_service,
    compare_biomarker as compare_biomarker_service,
    prepare_visit_context as prepare_visit_context_service
)


# =========================================================
# MCP Server
# =========================================================

mcp = MCPServer(
    "HealthBrief Tools"
)


# =========================================================
# Tool 1: Find Biomarker
# =========================================================

@mcp.tool(
    name="find_biomarker",
    title="Find a biomarker",
    annotations=ToolAnnotations(
        read_only_hint=True,
        open_world_hint=False
    )
)

def find_biomarker_tool(
    report: dict[str, Any],
    biomarker_name: str
) -> dict[str, Any]:


    result = find_biomarker_service(
        report,
        biomarker_name
    )

    if result is None:

        return {
            "ok": False,
            "result": None,
            "error": (
                f"Biomarker '{biomarker_name}' was not found in the report."
            )
        }

    return {
        "ok": True,
        "result": result,
        "error": None
    }


# =========================================================
# Tool 2: Get Abnormal Markers
# =========================================================

@mcp.tool(
    name="get_abnormal_markers",
    title="Get abnormal biomarkers",
    annotations=ToolAnnotations(
        read_only_hint=True,
        open_world_hint=False
    )
)
def get_abnormal_markers_tool(
    report: dict[str, Any]
) -> dict[str, Any]:


    result = get_abnormal_markers_service(
        report
    )

    return {
        "ok": True,
        "result": result,
        "error": None
    }


# =========================================================
# Tool 3: Compare Biomarker
# =========================================================

@mcp.tool(
    name="compare_biomarker",
    title="Compare a biomarker across two reports",
    annotations=ToolAnnotations(
        read_only_hint=True,
        open_world_hint=False
    )
)
def compare_biomarker_tool(
    current_report: dict[str, Any],
    previous_report: dict[str, Any],
    biomarker_name: str
) -> dict[str, Any]:

    result = compare_biomarker_service(
        current_report,
        previous_report,
        biomarker_name
    )

    if result is None:

        return {
            "ok": False,
            "result": None,
            "error": (
                f"Biomarker '{biomarker_name}' was not found in both reports."
            )
        }

    return {
        "ok": True,
        "result": result,
        "error": None
    }


# =========================================================
# Tool 4: Prepare Visit Context
# =========================================================

@mcp.tool(
    name="prepare_visit_context",
    title="Prepare doctor visit context",
    annotations=ToolAnnotations(
        read_only_hint=True,
        open_world_hint=False
    )
)
def prepare_visit_context_tool(
    report: dict[str, Any]
) -> dict[str, Any]:


    result = prepare_visit_context_service(
        report
    )

    return {
        "ok": True,
        "result": result,
        "error": None
    }


# =========================================================
# Run server directly if needed
# =========================================================

if __name__ == "__main__":
    mcp.run()