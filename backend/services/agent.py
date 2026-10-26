import os
import json

from dotenv import load_dotenv
from openai import OpenAI
from typing import TypedDict, Any

from langgraph.graph import StateGraph, START, END

from backend.services.router import route_question

from backend.mcp_client import (
    mcp_find_biomarker,
    mcp_get_abnormal_markers,
    mcp_prepare_visit_context,
    mcp_compare_biomarker
)

from backend.harness.logging_config import log_event

from backend.harness.errors import (
    MissingPreviousReportError,
    ModelServiceError,
    ModelResponseError
)



load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


# -----------------------------
# State
# -----------------------------


class HealthState(TypedDict):

    request_id: str

    question: str

    lab_results: dict
    previous_lab_results: dict | None

    category: str | None
    biomarker: str | None

    tool_result: Any

    answer: str | None

    execution_trace: list[dict[str, Any]]


# -----------------------------
# Nodes
# -----------------------------


def router_node(state: HealthState):

    route = route_question(state["question"])

    category = route["category"]

    biomarker = route.get("biomarker")


    log_event(
        "category_selected",
        state["request_id"],
        category=category,
        biomarker=biomarker
    )


    trace = list(
        state["execution_trace"]
    )

    trace.append(
        {
            "step": "router",
            "category": category,
            "biomarker": biomarker
        }
    )


    return {
        "category": category,
        "biomarker": biomarker,
        "execution_trace": trace
    }


def explain_lab_node(state: HealthState):

    biomarker_name = (
        state["biomarker"]
    )


    log_event(
        "tool_called",
        state["request_id"],
        tool="find_biomarker"
    )


    result = mcp_find_biomarker(
        state["lab_results"],
        biomarker_name
    )


    trace = list(
        state["execution_trace"]
    )

    trace.append(
        {
            "step": "tool",
            "tool": "find_biomarker"
        }
    )


    return {
        "tool_result": result,
        "execution_trace": trace
    }


def abnormal_summary_node(state: HealthState):

    log_event(
        "tool_called",
        state["request_id"],
        tool="get_abnormal_markers"
    )


    result = (
        mcp_get_abnormal_markers(
            state["lab_results"]
        )
    )


    trace = list(
        state["execution_trace"]
    )

    trace.append(
        {
            "step": "tool",
            "tool":
                "get_abnormal_markers"
        }
    )


    return {
        "tool_result": result,
        "execution_trace": trace
    }


def visit_prep_node(state: HealthState):

    log_event(
        "tool_called",
        state["request_id"],
        tool="prepare_visit_context"
    )


    result = (
        mcp_prepare_visit_context(
            state["lab_results"]
        )
    )


    trace = list(
        state["execution_trace"]
    )

    trace.append(
        {
            "step": "tool",
            "tool":
                "prepare_visit_context"
        }
    )


    return {
        "tool_result": result,
        "execution_trace": trace
    }


def compare_trend_node(state: HealthState):

    if (state["previous_lab_results"]is None):

        raise MissingPreviousReportError(
        "A previous report is required for trend comparison.")
            

    log_event(
        "tool_called",
        state["request_id"],
        tool="compare_biomarker"
    )


    result = (
        mcp_compare_biomarker(
            state["lab_results"],
            state[
                "previous_lab_results"
            ],
            state["biomarker"]
        )
    )


    trace = list(
        state["execution_trace"]
    )

    trace.append(
        {
            "step": "tool",
            "tool":
                "compare_biomarker"
        }
    )


    return {
        "tool_result": result,
        "execution_trace": trace
    }


def general_node(state: HealthState):

    log_event(
        "no_tool_required",
        state["request_id"]
    )


    trace = list(
        state["execution_trace"]
    )

    trace.append(
        {
            "step": "general",
            "tool": None
        }
    )


    return {
        "tool_result": {
            "message":
                "No specific health-report tool was required."
        },
        "execution_trace": trace
    }


def answer_node(state: HealthState):

    tool_result_json = json.dumps(
        state["tool_result"],
        ensure_ascii=False
    )

    prompt = f"""
You are HealthBrief, an educational health report assistant.

Answer the user's question using ONLY the information provided
in the tool result.

Do not invent laboratory values.
Do not diagnose diseases.
Do not prescribe medication.
If the available information is insufficient, clearly say so.

Keep the answer concise and easy to understand.

User question:
{state["question"]}

category:
{state["category"]}

biomarker:
{state["biomarker"]}

Tool result:
{tool_result_json}
"""
    try:
        response = client.responses.create(
        model="deepseek-flash",
        input=prompt
        )

    except Exception as error:

        raise ModelServiceError(
        "Unable to generate the HealthBrief answer."
    ) from error

    answer = response.output_text

    if not answer:

        raise ModelResponseError(
        "The answer model returned an empty response."
    )


    log_event(
        "answer_generated",
        state["request_id"]
    )


    trace = list(
    state["execution_trace"]
)

    trace.append(
    {
        "step": "answer"
    }
)

    return {
    "answer": answer,
    "execution_trace": trace
}


# -----------------------------
# Routing
# -----------------------------


def choose_route(state: HealthState):

    category = state["category"]

    if category == "EXPLAIN_LAB":
        return "explain_lab"

    if category == "ABNORMAL_SUMMARY":
        return "abnormal_summary"

    if category == "VISIT_PREP":
        return "visit_prep"

    if category == "COMPARE_TREND":
        return "compare_trend"
    
    return "general"


# -----------------------------
# Graph
# -----------------------------


builder = StateGraph(HealthState)


builder.add_node(
    "router",
    router_node
)

builder.add_node(
    "explain_lab",
    explain_lab_node
)

builder.add_node(
    "abnormal_summary",
    abnormal_summary_node
)

builder.add_node(
    "visit_prep",
    visit_prep_node
)

builder.add_node(
    "compare_trend",
    compare_trend_node
)

builder.add_node(
    "general",
    general_node
)

builder.add_node(
    "answer",
    answer_node
)


builder.add_edge(
    START,
    "router"
)


builder.add_conditional_edges(
    "router",
    choose_route,
    {
        "explain_lab": "explain_lab",
        "abnormal_summary": "abnormal_summary",
        "visit_prep": "visit_prep",
        "compare_trend": "compare_trend",
        "general": "general"
    }
)


builder.add_edge(
    "explain_lab",
    "answer"
)

builder.add_edge(
    "abnormal_summary",
    "answer"
)

builder.add_edge(
    "visit_prep",
    "answer"
)

builder.add_edge(
    "compare_trend",
    "answer"
)

builder.add_edge(
    "general",
    "answer"
)


builder.add_edge(
    "answer",
    END
)



health_agent = builder.compile()