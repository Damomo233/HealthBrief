import requests


url = (
    "http://127.0.0.1:8000"
    "/reports/analyze"
)


with open(
    "sample_health_report.pdf",
    "rb"
) as pdf_file:

    files = {
        "file": (
            "sample_health_report.pdf",
            pdf_file,
            "application/pdf"
        )
    }


    response = requests.post(
        url,
        files=files
    )


print("Status code:")
print(response.status_code)


print("\nResponse:")
print(response.json())