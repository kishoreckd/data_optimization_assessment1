from fastapi import  Depends, Query,APIRouter, HTTPException, Header, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List
import datetime
import os, json
from math import ceil

# Local imports
from app.utils.logger import get_log_file, log_step
from app.models.record_model import Record
from app.service.clean_records import clean_records
from app.service.ml_refine import refine_records
from app.service.meta_data import extract_metadata
from app.utils.validation.json_validator import JsonResponse
from app.utils.validation.auth import verify_api_key
from app.core.config import settings
from app.service.ml.sentiment import get_sentiment_pipeline


router = APIRouter()

@router.post("/optimize")
async def optimize(records: List[Record], sentiment_pipe=Depends(get_sentiment_pipeline)):
    logfile = get_log_file()  
    log_step(logfile, f"Received {len(records)} records")

    try:
        cleaned, cleaned_file = clean_records([r.model_dump() for r in records])
        log_step(logfile, f"Step1: cleaned data written to {cleaned_file}")

        metadata, metadata_file = extract_metadata(cleaned)
        log_step(logfile, f"Step2: metadata extracted to {metadata_file}")

        final_records = refine_records(cleaned, sentiment_pipe, logfile=logfile)
        log_step(logfile, f"Step3: ML refinement complete and final data written to {settings.FINAL_FILE}")

        return JsonResponse.success(
            message="Workflow completed successfully",
            data={
                "Total records processed": len(final_records),
            }
        )
    except Exception as e:
        log_step(logfile, f"Error: {e}")
        return JsonResponse.error(f"Workflow failed: {e}")

@router.get("/retrieve",dependencies=[Depends(verify_api_key)])
async def retrieve(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(5, ge=1, le=100, description="Records per page")
):
    """
    Retrieve final records with pagination.
    Returns total_records, total_pages, current page, per_page, and the list of records.

    Args:
        page (int): Page number
        per_page (int): Records per page

    Returns:
        JSONResponse: list of records retrieved   
    """
    try:
        if not os.path.exists(settings.FINAL_FILE):
            return JsonResponse.success(message="No records found", data=[])

        with open(settings.FINAL_FILE, "r", encoding="utf-8") as f:
            all_records = json.load(f)

        total = len(all_records)
        total_pages = ceil(total / per_page)

        # Ensure page does not exceed total_pages
        if page > total_pages and total_pages > 0:
            page = total_pages

        start = (page - 1) * per_page
        end = start + per_page
        paginated_records = all_records[start:end]

        return JsonResponse.success(
            message="Final records retrieved",
            data={
                "records": paginated_records,
                "total_records": total,
                "total_pages": total_pages,
                "page": page,
                "per_page": per_page,
            }
        )

    except Exception as e:
        return JsonResponse.error(message=f"Failed to retrieve records: {e}", status_code=500)

@router.get("/health")
def health():
    """
    Health check endpoint.
    Returns the current time in UTC.
    """
    return JsonResponse.success(
        message="Service healthy",
        data={"time": str(datetime.datetime.now(datetime.timezone.utc))}
     )