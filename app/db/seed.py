from datetime import datetime
from sqlalchemy.orm import Session

from app.models.lead import Lead


def seed_leads_if_empty(db: Session) -> int:
    """
    Seed mock data if the leads table is empty.
    Returns the number of records inserted.
    """
    existing_count = db.query(Lead).count()
    if existing_count > 0:
        return 0

    mock_leads = [
        Lead(
            name="John Doe",
            email="john.doe@example.com",
            phone="0123456789",
            source="Website",
            created_time=datetime.utcnow(),
        ),
        Lead(
            name="Jane Smith",
            email="jane.smith@example.com",
            phone="0987654321",
            source="Referral",
            created_time=datetime.utcnow(),
        ),
        Lead(
            name="Bob Brown",
            email="bob.brown@example.com",
            phone=None,
            source="Email Campaign",
            created_time=datetime.utcnow(),
        ),
        Lead(
            name="Alice Green",
            email="alice.green@example.com",
            phone="0112233445",
            source="Social Media",
            created_time=datetime.utcnow(),
        ),
        Lead(
            name="Michael White",
            email="michael.white@example.com",
            phone=None,
            source="Cold Call",
            created_time=datetime.utcnow(),
        ),
    ]

    db.add_all(mock_leads)
    db.commit()
    return len(mock_leads)
