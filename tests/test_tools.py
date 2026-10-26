from backend.services.tools import (
    classify_status,
    find_biomarker,
    get_abnormal_markers,
    compare_biomarker
)


sample_results = {
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


def test_classify_high():

    assert classify_status(
        168,
        0,
        130
    ) == "HIGH"


def test_classify_normal():

    assert classify_status(
        42,
        40,
        60
    ) == "NORMAL"


def test_find_ldl():

    result = find_biomarker(
        sample_results,
        "LDL"
    )

    assert result["value"] == 168

    assert result["status"] == "HIGH"


def test_abnormal_markers():

    result = get_abnormal_markers(
        sample_results
    )

    assert len(result) == 1

    assert result[0]["name"] == "LDL Cholesterol"