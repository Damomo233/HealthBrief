from backend.mcp_client import (
    mcp_find_biomarker,
    mcp_get_abnormal_markers
)


sample_report = {
    "biomarkers": [
        {
            "name": "LDL Cholesterol",
            "value": 168,
            "unit": "mg/dL",
            "lower_bound": 0,
            "upper_bound": 130
        },
        {
            "name": "HDL Cholesterol",
            "value": 42,
            "unit": "mg/dL",
            "lower_bound": 40,
            "upper_bound": 60
        }
    ]
}


print("Find LDL:")

print(
    mcp_find_biomarker(
        sample_report,
        "LDL"
    )
)


print("\nAbnormal:")

print(
    mcp_get_abnormal_markers(
        sample_report
    )
)