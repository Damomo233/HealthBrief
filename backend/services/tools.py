# Tool 1: Find certain biomarker

def classify_status(value, lower_bound, upper_bound):

    if lower_bound is not None and value < lower_bound:
        return "LOW"

    if upper_bound is not None and value > upper_bound:
        return "HIGH"

    return "NORMAL"


def find_biomarker(lab_results, biomarker_name):

    for item in lab_results["biomarkers"]:

        if biomarker_name.lower() in item["name"].lower():

            status = classify_status(
                item["value"],
                item["lower_bound"],
                item["upper_bound"]
            )

            return {
                "name": item["name"],
                "value": item["value"],
                "unit": item["unit"],
                "lower_bound": item["lower_bound"],
                "upper_bound": item["upper_bound"],
                "status": status
            }

    return None



# Tool 2: Find all abnormal biomarkers

def get_abnormal_markers(lab_results):

    abnormal_markers = []

    for item in lab_results["biomarkers"]:

        status = classify_status(
            item["value"],
            item["lower_bound"],
            item["upper_bound"]
        )

        if status != "NORMAL":

            abnormal_markers.append(
                {
                    "name": item["name"],
                    "value": item["value"],
                    "unit": item["unit"],
                    "lower_bound": item["lower_bound"],
                    "upper_bound": item["upper_bound"],
                    "status": status
                }
            )

    return abnormal_markers


# Tool3: Prepare abnormal biomarkers for visit preparation

def prepare_visit_context(lab_results):

    abnormal_markers = get_abnormal_markers(lab_results)

    return {
        "abnormal_markers": abnormal_markers,
        "total_abnormal": len(abnormal_markers)
    }


# Tool4: Compare biomarker values across two reports


def compare_biomarker(current_results, previous_results, biomarker_name):

    current = find_biomarker(
        current_results,
        biomarker_name
    )

    previous = find_biomarker(
        previous_results,
        biomarker_name
    )

    if current is None or previous is None:
        return None


    old_value = previous["value"]
    new_value = current["value"]


    absolute_change = new_value - old_value


    if old_value != 0:
        percent_change = (absolute_change / old_value) * 100

    else:
        percent_change = None


    return {
        "name": current["name"],

        "previous_value": old_value,
        "current_value": new_value,

        "unit": current["unit"],

        "absolute_change": round(absolute_change,2),

        "percent_change": (
            round(percent_change, 2)
            if percent_change is not None
            else None
        ),

        "previous_status": previous["status"],
        "current_status": current["status"]
    }