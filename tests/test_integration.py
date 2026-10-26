from backend.harness.runtime import (
    run_healthbrief_agent
)


CURRENT_REPORT = {
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


PREVIOUS_REPORT = {
    "biomarkers": [
        {
            "name": "LDL Cholesterol",
            "value": 180,
            "unit": "mg/dL",
            "lower_bound": 0,
            "upper_bound": 130
        }
    ]
}


def test_compare_trend_integration():

    result = run_healthbrief_agent(
        question=(
            "Has my LDL improved since my previous report?"
        ),
        current_report=CURRENT_REPORT,
        previous_report=PREVIOUS_REPORT
    )


    # Router really ran
    assert (
        result["category"]
        == "COMPARE_TREND"
    )


    # MCP tool really ran
    assert (
        result["tool_result"][
            "current_value"
        ]
        == 168
    )

    assert (
        result["tool_result"][
            "previous_value"
        ]
        == 180
    )


    # Answer model really ran
    assert result["answer"]


    # Harness really ran
    assert result["request_id"]

    assert (
        result["latency_seconds"]
        >= 0
    )


    # Execution trace really exists
    trace = result[
        "execution_trace"
    ]

    assert (
        trace[0]["step"]
        == "router"
    )

    assert (
        trace[0]["category"]
        == "COMPARE_TREND"
    )

    assert (
        trace[1]["step"]
        == "tool"
    )

    assert (
        trace[1]["tool"]
        == "compare_biomarker"
    )

    assert (
        trace[-1]["step"]
        == "answer"
    )