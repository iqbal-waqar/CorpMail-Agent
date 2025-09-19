from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
from ..schemas.email import EmailSendRequest, EmailSendResult, RecentEmail
from ..interactors.email import EmailInteractor

router = APIRouter(prefix="/email", tags=["email"])
email_interactor = EmailInteractor()

@router.post("/send", response_model=EmailSendResult)
async def send_email_to_employees(send_request: EmailSendRequest) -> EmailSendResult:
    try:
        result = await email_interactor.send_email_to_employees(send_request)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/recent", response_model=List[RecentEmail])
async def get_recent_emails(limit: int = 10) -> List[RecentEmail]:
    try:
        result = email_interactor.get_recent_emails(limit)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")