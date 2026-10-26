from datetime import date
from typing import Any

from sqlalchemy import (
    JSON,
    Date,
    Integer,
    String,
    create_engine,
    select
)

from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    sessionmaker
)


# =========================================================
# Database
# =========================================================

DATABASE_URL = "sqlite:///./healthbrief.db"


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


SessionLocal = sessionmaker(
    bind=engine
)


class Base(DeclarativeBase):
    pass


# =========================================================
# Saved report table
# =========================================================

class SavedReport(Base):

    __tablename__ = "saved_reports"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    filename: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    report_date: Mapped[date | None] = mapped_column(
        Date,
        nullable=True
    )

    lab_results: Mapped[dict[str, Any]] = mapped_column(
        JSON,
        nullable=False
    )


Base.metadata.create_all(
    bind=engine
)


# =========================================================
# Create
# =========================================================

def save_report(
   filename: str,
    report_date: date | None,
    lab_results: dict
):

    with SessionLocal() as db:

        report = SavedReport(
            filename=filename,
            report_date=report_date,
            lab_results=lab_results
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return {
            "id": report.id,
            "filename": report.filename,
            "report_date": report.report_date,
            "lab_results": report.lab_results
        }


# =========================================================
# Read all
# =========================================================

def list_saved_reports():

    with SessionLocal() as db:

        statement = (
            select(SavedReport)
            .order_by(
                SavedReport.report_date.desc()
            )
        )

        reports = (
            db.scalars(statement)
            .all()
        )

        return [
            {
                "id": report.id,
                "filename": report.filename,
                "report_date": report.report_date
            }
            for report in reports
        ]


# =========================================================
# Read one
# =========================================================

def get_saved_report(
    report_id: int
):

    with SessionLocal() as db:

        report = db.get(
            SavedReport,
            report_id
        )

        if report is None:
            return None

        return {
            "id": report.id,
            "filename": report.filename,
            "report_date": report.report_date,
            "lab_results": report.lab_results
        }


# =========================================================
# Delete
# =========================================================

def delete_saved_report(
    report_id: int
):

    with SessionLocal() as db:

        report = db.get(
            SavedReport,
            report_id
        )

        if report is None:
            return False

        db.delete(report)
        db.commit()

        return True