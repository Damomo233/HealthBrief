from backend.harness.runtime import (
    run_healthbrief_agent
)


current_report = {
    "biomarkers": [
        {
            "name":
                "LDL Cholesterol",

            "value": 168,

            "unit": "mg/dL",

            "lower_bound": 0,

            "upper_bound": 130
        }
    ]
}


previous_report = {
    "biomarkers": [
        {
            "name":
                "LDL Cholesterol",

            "value": 180,

            "unit": "mg/dL",

            "lower_bound": 0,

            "upper_bound": 130
        }
    ]
}


result = run_healthbrief_agent(
    question=(
        "Has my LDL improved?"
    ),

    current_report=current_report,

    previous_report=previous_report
)


print("\nRequest ID:")

print(
    result["request_id"]
)


print("\nCategory:")

print(
    result["category"]
)


print("\nExecution Trace:")

print(
    result["execution_trace"]
)


print("\nLatency:")

print(
    result["latency_seconds"]
)