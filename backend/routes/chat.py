from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from ..schemas.email import ChatMessage
from ..interactors.email import EmailInteractor

router = APIRouter(prefix="/chat", tags=["chat"])
email_interactor = EmailInteractor()

@router.post("/message")
async def process_chat_message(chat_message: ChatMessage) -> Dict[str, Any]:
    try:
        result = await email_interactor.process_chat_message(
            chat_message.message,
            chat_message.employee_emails
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")