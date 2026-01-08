from typing import List, Optional
from datetime import date, datetime, time
import csv
import io

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.db.session import get_db
from app.models.lead import Lead
from app.schemas.lead import LeadCreate, LeadUpdate, LeadResponse

router = APIRouter(prefix="/leads", tags=["Leads"])


@router.get("/report")
def leads_report(
    db: Session = Depends(get_db),
    from_date: Optional[date] = Query(None, description="Filter from date (YYYY-MM-DD)"),
    to_date: Optional[date] = Query(None, description="Filter to date (YYYY-MM-DD)"),
    name: Optional[str] = Query(None, description="Filter by name (contains)"),
    email: Optional[str] = Query(None, description="Filter by exact email"),
    source: Optional[str] = Query(None, description="Filter by source (contains)"),
):
    """
    Generate and download a CSV report of leads with optional filters.

    Filters:
    - from_date/to_date apply to created_time
    - name/source use case-insensitive 'contains'
    - email uses exact match
    """
    query = db.query(Lead)

    filters = []

    if from_date:
        start_dt = datetime.combine(from_date, time.min)
        filters.append(Lead.created_time >= start_dt)

    if to_date:
        end_dt = datetime.combine(to_date, time.max)
        filters.append(Lead.created_time <= end_dt)

    if name:
        filters.append(Lead.name.ilike(f"%{name}%"))

    if email:
        filters.append(Lead.email == email)

    if source:
        filters.append(Lead.source.ilike(f"%{source}%"))

    if filters:
        query = query.filter(and_(*filters))

    leads = query.order_by(Lead.created_time.desc()).all()

    def generate():
        buffer = io.StringIO()
        writer = csv.writer(buffer)

        # Header
        writer.writerow(["id", "name", "email", "phone", "source", "created_time"])

        # Rows
        for lead in leads:
            created = lead.created_time.isoformat(sep=" ") if lead.created_time else ""
            writer.writerow([lead.id, lead.name, lead.email, lead.phone or "", lead.source or "", created])

        yield buffer.getvalue()

    filename = f"leads_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}

    return StreamingResponse(generate(), media_type="text/csv", headers=headers)


@router.post(
    "",
    response_model=LeadResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_lead(
    lead_in: LeadCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(Lead).filter(Lead.email == lead_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Lead with this email already exists",
        )

    lead = Lead(**lead_in.model_dump())
    db.add(lead)
    db.commit()
    db.refresh(lead)
    return lead


@router.get("", response_model=List[LeadResponse])
def get_leads(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    name: Optional[str] = None,
    email: Optional[str] = None,
    source: Optional[str] = None,
):
    """
    Get leads with pagination and optional filtering.
    """
    query = db.query(Lead)

    filters = []

    if name:
        filters.append(Lead.name.ilike(f"%{name}%"))

    if email:
        filters.append(Lead.email == email)

    if source:
        filters.append(Lead.source.ilike(f"%{source}%"))

    if filters:
        query = query.filter(and_(*filters))

    return query.offset(skip).limit(limit).all()


@router.get("/{lead_id}", response_model=LeadResponse)
def get_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )
    return lead


@router.put("/{lead_id}", response_model=LeadResponse)
def update_lead(
    lead_id: int,
    lead_in: LeadUpdate,
    db: Session = Depends(get_db),
):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )

    for field, value in lead_in.model_dump(exclude_unset=True).items():
        setattr(lead, field, value)

    db.commit()
    db.refresh(lead)
    return lead


@router.delete("/{lead_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lead(lead_id: int, db: Session = Depends(get_db)):
    lead = db.query(Lead).filter(Lead.id == lead_id).first()
    if not lead:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lead not found",
        )

    db.delete(lead)
    db.commit()
