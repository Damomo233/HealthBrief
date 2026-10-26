import time
import uuid

from backend.services.agent import health_agent

from backend.harness.logging_config import log_event

from backend.harness.errors import (
    HealthBriefError,
    AgentExecutionError
)

def run_healthbrief_agent(
    question,
    current_report,
    previous_report=None
):

    request_id = str(uuid.uuid4())

    start_time = time.perf_counter()

    log_event(
    "agent_started",
    request_id,
    has_previous_report=(
        previous_report is not None
    )
)

    initial_state = {
        "request_id": request_id,
        "question": question,
        "lab_results": current_report,
        "previous_lab_results": previous_report,

        "category": None,
        "biomarker": None,

        "tool_result": None,
        "answer": None,
        "execution_trace": []
    }

    try:

        result = health_agent.invoke(initial_state)

        end_time = time.perf_counter()
        
        latency_seconds = end_time - start_time

    except HealthBriefError as error:
        log_event(
        "agent_finished",
        request_id,
        error_code=error.code,
        latency_seconds=round(latency_seconds,2)
    )

        raise

    except Exception as error:

        end_time = time.perf_counter()

        latency_seconds = end_time - start_time

        log_event(
        "agent_failed",
        request_id,
        error_code="AGENT_EXECUTION_ERROR",
        latency_seconds=round(latency_seconds,2)
    )

        wrapped_error = (
        AgentExecutionError(
            "An unexpected error occurred while running HealthBrief."
        )
    )

        raise wrapped_error from error


    return {
        "request_id": request_id,

        "category": result["category"],
        "biomarker": result["biomarker"],

        "tool_result": result["tool_result"],
        "answer": result["answer"],

        "execution_trace":result["execution_trace"],
        "latency_seconds": round(latency_seconds,2)
    }