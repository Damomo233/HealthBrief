class HealthBriefError(Exception):

    code = "HEALTHBRIEF_ERROR"
    status_code = 500

    def __init__(
        self,
        message: str
    ):
        super().__init__(message)

        self.message = message

        self.request_id = None


class MissingPreviousReportError(
    HealthBriefError
):
    code = "MISSING_PREVIOUS_REPORT"
    status_code = 400


class ToolResultError(
    HealthBriefError
):
    code = "TOOL_RESULT_ERROR"
    status_code = 422


class MCPToolError(
    HealthBriefError
):
    code = "MCP_TOOL_ERROR"
    status_code = 502


class ModelServiceError(
    HealthBriefError
):
    code = "MODEL_SERVICE_ERROR"
    status_code = 502


class ModelResponseError(
    HealthBriefError
):
    code = "MODEL_RESPONSE_ERROR"
    status_code = 502


class ReportReadError(
    HealthBriefError
):
    code = "REPORT_READ_ERROR"
    status_code = 400


class ReportProcessingError(
    HealthBriefError
):
    code = "REPORT_PROCESSING_ERROR"
    status_code = 500


class AgentExecutionError(
    HealthBriefError
):
    code = "AGENT_EXECUTION_ERROR"
    status_code = 500