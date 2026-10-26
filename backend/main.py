from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from backend.services.pdf_reader import extract_text_from_pdf

from backend.services.lab_extractor import (
    extract_lab_results,
    parse_report_date,
    extract_report_date_from_filename
)

from backend.harness.runtime import run_healthbrief_agent

from backend.schemas import (
    AgentQueryRequest,
    AgentQueryResponse,
    ReportAnalysisResponse,
    SaveReportRequest,
    SavedReportSummary,
    SavedReportResponse
)

from fastapi import Request

from fastapi.responses import (
    JSONResponse
)


from backend.harness.errors import (
    HealthBriefError,
    ReportReadError,
    ReportProcessingError
)

from backend.database import (
    save_report as save_report_to_db,
    list_saved_reports as list_saved_reports_from_db,
    get_saved_report as get_saved_report_from_db,
    delete_saved_report as delete_saved_report_from_db
)


app = FastAPI(
    title="HealthBrief API",
    version="1.0.0"
)


@app.exception_handler(
    HealthBriefError
)
async def healthbrief_error_handler(
    request: Request,
    error: HealthBriefError
):

    return JSONResponse(
        status_code=error.status_code,
        content={
            "detail": {
                "code": error.code,
                "message": error.message,
                "request_id":
                    error.request_id
            }
        }
    )


@app.get("/health")
def health_check():

    return {
        "status": "ok",
        "service": "HealthBrief API"
    }


@app.post(
    "/agent/query",
    response_model=AgentQueryResponse
)
def agent_query(request: AgentQueryRequest):

    result = run_healthbrief_agent(
    question=request.question,
    current_report=request.current_report,
    previous_report=request.previous_report
)


    return {
        "category": result["category"],
        "biomarker": result["biomarker"],
        "answer": result["answer"],
        "tool_result": result["tool_result"]
    }


@app.post(
    "/reports/analyze",     # Endpoint for analyzing uploaded PDF
    response_model=ReportAnalysisResponse
)


def analyze_report(file: UploadFile = File(...)):

    # Check file type
    if not file.filename.lower().endswith(".pdf"):

        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )


    # Extract text from PDF

    try:

        pdf_text = extract_text_from_pdf(file.file)


    except Exception as error:

        raise ReportReadError(
        "Unable to read the uploaded PDF."
    ) from error
  

    # Check whether readable text exists
    if not pdf_text.strip():

        raise HTTPException(
            status_code=400,
            detail=(
                "No readable text was found in the PDF. "
                "Please upload a text-based PDF."
            )
        )


    # Extract structured biomarkers
    try:
        extraction_result = extract_lab_results(
            pdf_text
        )

        report_date = parse_report_date(
            extraction_result.get(
                "report_date"
            )
        )

        if report_date is None:
            report_date = (
                extract_report_date_from_filename(
                    file.filename
                )
            )

        lab_results = {
            "biomarkers":
                extraction_result["biomarkers"]
        }


    except HealthBriefError:
        raise


    except Exception as error:
        raise ReportProcessingError(
            "Unable to process the laboratory report."
        ) from error


    return {
        "lab_results": lab_results,
        "report_date": report_date,
        "extracted_text": pdf_text
        
    }



@app.post(
    "/reports/save",
    response_model=SavedReportResponse
)
def save_report(
    request: SaveReportRequest
):

    return save_report_to_db(
        filename=request.filename,
        report_date=request.report_date,
        lab_results=(
            request.lab_results.model_dump()
        )
    )



@app.get(
    "/reports/saved",
    response_model=list[SavedReportSummary]
)
def get_saved_reports():

    return list_saved_reports_from_db()



@app.get(
    "/reports/saved/{report_id}",
    response_model=SavedReportResponse
)
def get_saved_report(
    report_id: int
):

    report = get_saved_report_from_db(
        report_id
    )

    if report is None:

        raise HTTPException(
            status_code=404,
            detail="Saved report not found."
        )

    return report


# remove a saved report by its ID
@app.delete(
    "/reports/saved/{report_id}"
)
def delete_saved_report(
    report_id: int
):

    deleted = delete_saved_report_from_db(
        report_id
    )

    if not deleted:

        raise HTTPException(
            status_code=404,
            detail="Saved report not found."
        )

    return {
        "status": "deleted",
        "report_id": report_id
    }