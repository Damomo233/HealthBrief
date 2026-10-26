import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from backend.harness.errors import (
    ModelServiceError,
    ModelResponseError
)

import re
from datetime import date



load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def extract_lab_results(report_text):

    prompt = f"""
You are extracting laboratory test results from a health report.

Return ONLY valid JSON.
Do not include markdown.
Do not include explanations.


Also extract the laboratory examination date if it is explicitly present.

Prior order of preference for the check-up date if there are multiple dates mentioned:
1. specimen/collection date
2. examination/test date
3. report date

Return the date in YYYY-MM-DD format when possible.
If no reliable date is explicitly available, return null.
Do not infer or invent a date.


Use this exact structure:

{{
    "report_date": "YYYY-MM-DD" or null,
    "biomarkers": [
        {{
            "name": "HbA1c",
            "value": 5.9,
            "unit": "%",
            "lower_bound": 4.0,
            "upper_bound": 5.6
        }}
    ]
}}

Rules:
1. Extract only biomarkers that actually appear in the report.
2. value, lower_bound, and upper_bound must be numbers when available.
3. If a lower or upper reference bound is missing, set "report_date" to null.
4. Do not guess missing values.
5. Preserve the unit shown in the report.

Health report:

{report_text}
"""

    try:

        response = (
        client.chat.completions.create(
            model = "deepseek-flash",
            messages=[
    {
        "role": "user",
        "content": prompt
    }
]
        )
    )

    except Exception as error:

     raise ModelServiceError(
        "The laboratory extraction model could not be reached."
    ) from error

    result_text = response.choices[0].message.content


    try:
        result = json.loads(result_text)

    except json.JSONDecodeError as error:
        
        raise ModelResponseError(
        "The laboratory extraction model returned invalid JSON."
    ) from error
    

    return result



def parse_report_date(
    report_date
):

    if not report_date:
        return None

    try:
        return date.fromisoformat(
            report_date.strip()
        )

    except (ValueError, AttributeError):
        return None


def extract_report_date_from_filename(
    filename
):

    patterns = [
        r"(?<!\d)(20\d{2})[-_](0[1-9]|1[0-2])[-_](0[1-9]|[12]\d|3[01])(?!\d)",
        r"(?<!\d)(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])(?!\d)"
    ]


    for pattern in patterns:

        match = re.search(
            pattern,
            filename
        )

        if match:

            year = int(
                match.group(1)
            )

            month = int(
                match.group(2)
            )

            day = int(
                match.group(3)
            )

            try:
                return date(
                    year,
                    month,
                    day
                )

            except ValueError:
                return None


    return None