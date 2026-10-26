from typing import Any

from pydantic import BaseModel

from datetime import date


class AgentQueryRequest(BaseModel):
    question: str
    current_report: dict
    previous_report: dict | None = None     # Historical report is optional.


class AgentQueryResponse(BaseModel):
    category: str
    biomarker: str | None
    answer: str
    tool_result: Any


class Biomarker(BaseModel):
    name: str
    value: float
    unit: str | None = None
    lower_bound: float | None = None
    upper_bound: float | None = None


class LabResults(BaseModel):
    biomarkers: list[Biomarker]


class ReportAnalysisResponse(BaseModel):
    lab_results: LabResults
    report_date: date | None = None
    extracted_text: str


class SaveReportRequest(BaseModel):
    filename: str
    report_date: date | None = None
    lab_results: LabResults


class SavedReportSummary(BaseModel):
    id: int
    filename: str
    report_date: date | None = None


class SavedReportResponse(BaseModel):
    id: int
    filename: str
    report_date: date | None = None
    lab_results: LabResults