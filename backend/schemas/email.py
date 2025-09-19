from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from datetime import datetime

class EmailSendRequest(BaseModel):
    subject: str = Field(..., min_length=1, max_length=200)
    body: str = Field(..., min_length=1)
    employee_emails: List[EmailStr]

class ChatMessage(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    employee_emails: Optional[List[EmailStr]] = None

class EmailSendResult(BaseModel):
    success: bool
    sent_count: int
    total_count: int
    results: dict
    message: str
    timestamp: Optional[datetime] = None

class RecentEmail(BaseModel):
    id: Optional[int] = None
    subject: str
    body: str
    recipients: List[str]
    sent_at: datetime
    success_count: int
    total_count: int