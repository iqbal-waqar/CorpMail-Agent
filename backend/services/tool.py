from langchain.tools import tool
from typing import List
import json
from .llm import LLMService
from .sendgrid import EmailService

llm_service = LLMService()
email_service = EmailService()

@tool
async def generate_professional_email(topic: str, context: str = "") -> str:
    """
    Generate a professional email for company communications.
    
    Args:
        topic: The main topic or subject of the email
        context: Additional context or details for the email
    
    Returns:
        JSON string with 'subject' and 'body' fields
    """
    try:
        email_content = await llm_service.generate_email(topic, context)
        return email_content
    except Exception as e:
        return json.dumps({"error": f"Failed to generate email: {str(e)}"})

@tool
async def send_email_to_employees(employee_emails: List[str], subject: str, email_body: str) -> str:
    """
    Send the generated email to all employees.
    
    Args:
        employee_emails: List of employee email addresses
        subject: Email subject line
        email_body: Email body content
        
    Returns:
        JSON string with sending results
    """
    try:
        results = await email_service.send_email_to_employees(employee_emails, subject, email_body)
        success_count = sum(1 for success in results.values() if success)
        total_count = len(employee_emails)
        
        return json.dumps({
            "success": True,
            "sent_count": success_count,
            "total_count": total_count,
            "results": results,
            "message": f"Email sent successfully to {success_count} out of {total_count} employees"
        })
    except Exception as e:
        return json.dumps({
            "success": False,
            "error": f"Failed to send emails: {str(e)}"
        })

AGENT_TOOLS = [
    generate_professional_email,
    send_email_to_employees
]
