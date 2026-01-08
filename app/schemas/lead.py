from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, ConfigDict


class LeadBase(BaseModel):
    """
    Shared properties for Lead.
    """
    name: str
    email: EmailStr
    phone: Optional[str] = None
    source: Optional[str] = None


class LeadCreate(LeadBase):
    """
    Properties required when creating a Lead.
    """
    pass


class LeadUpdate(BaseModel):
    """
    Properties allowed when updating a Lead.
    All fields are optional to support partial updates.
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    source: Optional[str] = None


class LeadResponse(LeadBase):
    """
    Properties returned to the client.
    """
    id: int
    created_time: datetime

    model_config = ConfigDict(from_attributes=True)
