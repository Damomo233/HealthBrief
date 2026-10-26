import os
import json

from dotenv import load_dotenv
from openai import OpenAI

from backend.harness.errors import (
    ModelServiceError,
    ModelResponseError
)


load_dotenv()


client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)


def route_question(question):
    prompt = f"""
Classify the user's question into exactly one of these categories:

EXPLAIN_LAB
ABNORMAL_SUMMARY
VISIT_PREP
COMPARE_TREND
GENERAL

Definitions:

EXPLAIN_LAB:
The users' question mentioned about one or more specific laboratory biomarkers,
such as LDL, HbA1c, ALT, glucose, or HDL.

ABNORMAL_SUMMARY:
The user wants to know which test results are abnormal,
important, high, low, or need attention.Questions did not mention 
specific one or more laboratory biomarkers.

VISIT_PREP:
The user wants help preparing questions for a doctor visit.

COMPARE_TREND:
The user wants to compare a biomarker across two reports,
for example whether LDL improved or HbA1c increased.

GENERAL:
Anything that does not fit the categories above.

Return ONLY valid JSON in this format:

{{
    "category": "EXPLAIN_LAB",
    "biomarker": "LDL"
}}

If there is no specific biomarker, set biomarker to null.

User question:

{question}
"""

    try:
        response = client.chat.completions.create(
            model="deepseek-flash",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

    except Exception as error:
        raise ModelServiceError(
        "The category router model could not be reached."
    ) from error

    result_text = response.choices[0].message.content
    
    try:

        result = json.loads(result_text)

    except json.JSONDecodeError as error:

        raise ModelResponseError(
        "The category router returned invalid JSON."
    ) from error

    return result