import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from typing import List, Dict

load_dotenv()

class EmailService:
    def __init__(self):
        self.api_key = os.environ.get('SENDGRID_API_KEY')
        if not self.api_key:
            raise ValueError('SENDGRID_API_KEY environment variable must be set')
        self.client = SendGridAPIClient(self.api_key)
        self.from_email = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@company.com')
        self.from_name = "TechFlow Solutions"
    
    async def send_email_to_employee(self, employee_email: str, subject: str, content: str) -> bool:
        try:
            if not content.strip().startswith('<!DOCTYPE html>') and not content.strip().startswith('<html'):
                content = self.create_professional_html_email(subject, content)
            
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(employee_email),
                subject=subject,
                html_content=Content("text/html", content)
            )
            
            response = self.client.send(message)
            return response.status_code == 202
        except Exception as e:
            return False
    
    async def send_email_to_employees(self, employee_emails: List[str], subject: str, content: str) -> Dict[str, bool]:
        results = {}
        for email in employee_emails:
            results[email] = await self.send_email_to_employee(email, subject, content)
        return results
    
    def create_professional_html_email(self, subject: str, plain_content: str) -> str:
        paragraphs = plain_content.strip().split('\n\n')
        html_paragraphs = []
        
        for paragraph in paragraphs:
            if paragraph.strip():
                formatted_paragraph = paragraph.replace('\n', '<br>')
                html_paragraphs.append(f'<p style="color: #555555; font-size: 16px; line-height: 1.7; margin: 0 0 20px 0;">{formatted_paragraph}</p>')
        
        content_html = '\n'.join(html_paragraphs)
        
        return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{subject}</title>
</head>
<body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; max-width: 650px; margin: 0 auto; padding: 20px; background-color: #f4f6f9;">
    
    <!-- Main Container -->
    <div style="background-color: #ffffff; border-radius: 12px; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1); overflow: hidden; border: 1px solid #e1e8ed;">
        
        <!-- Company Header -->
        <div style="background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%); padding: 35px 40px; text-align: center; position: relative;">
            <div style="background: rgba(255,255,255,0.1); border-radius: 50px; display: inline-block; padding: 8px 20px; margin-bottom: 15px;">
                <h1 style="color: #ffffff; margin: 0; font-size: 28px; font-weight: 700; letter-spacing: 1.5px;">
                    TechFlow Solutions
                </h1>
            </div>
            <p style="color: #b8d4f0; margin: 0; font-size: 15px; font-weight: 400;">
                Enterprise Software & Cloud Solutions
            </p>
            <div style="margin-top: 12px;">
                <span style="color: #ffffff; font-size: 12px; background: rgba(255,255,255,0.15); padding: 4px 12px; border-radius: 15px;">
                    🚀 Innovation • 🔒 Security • ⚡ Performance
                </span>
            </div>
        </div>
        
        <!-- Content Section -->
        <div style="padding: 40px;">
            <h2 style="color: #1e3c72; margin: 0 0 25px 0; font-size: 24px; font-weight: 600; border-bottom: 3px solid #2a5298; padding-bottom: 12px; display: inline-block;">
                {subject}
            </h2>
            
            {content_html}
            
            <div style="margin-top: 35px; padding: 25px; background: linear-gradient(135deg, #f8fbff 0%, #e8f4fd 100%); border-radius: 10px; border-left: 4px solid #2a5298;">
                <p style="color: #1e3c72; font-size: 15px; line-height: 1.6; margin: 0 0 8px 0; font-weight: 500;">
                    Best regards,
                </p>
                <p style="color: #2a5298; font-size: 16px; font-weight: 600; margin: 0 0 5px 0;">
                    TechFlow Solutions Team
                </p>
                <p style="color: #6b7280; font-size: 13px; margin: 0;">
                    Customer Success Department
                </p>
            </div>
        </div>
        
        <!-- Company Information Footer -->
        <div style="background: linear-gradient(135deg, #f8fbff 0%, #e8f4fd 100%); padding: 30px 40px; border-top: 1px solid #e1e8ed;">
            <div style="text-align: center; margin-bottom: 25px;">
                <h3 style="color: #1e3c72; margin: 0 0 15px 0; font-size: 18px; font-weight: 600;">
                    TechFlow Solutions Inc.
                </h3>
                <div style="color: #6b7280; font-size: 14px; line-height: 1.6;">
                    <p style="margin: 0 0 8px 0;">
                        <strong>📍 Headquarters:</strong> 1250 Innovation Drive, Suite 400<br>
                        San Francisco, CA 94107, United States
                    </p>
                    <p style="margin: 0 0 8px 0;">
                        <strong>📞 Phone:</strong> +1 (555) 123-4567 | <strong>📧 Email:</strong> support@techflowsolutions.com
                    </p>
                    <p style="margin: 0 0 15px 0;">
                        <strong>🌐 Website:</strong> www.techflowsolutions.com
                    </p>
                </div>
            </div>
            
            <!-- Action Links -->
            <div style="text-align: center; margin-bottom: 20px;">
                <a href="#" style="display: inline-block; background-color: #2a5298; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 25px; font-size: 13px; font-weight: 500; margin: 0 8px;">
                    🏠 Customer Portal
                </a>
                <a href="#" style="display: inline-block; background-color: #1e3c72; color: #ffffff; padding: 10px 20px; text-decoration: none; border-radius: 25px; font-size: 13px; font-weight: 500; margin: 0 8px;">
                    📞 Contact Support
                </a>
            </div>
            
            <!-- Legal Links -->
            <div style="text-align: center; border-top: 1px solid #d1d5db; padding-top: 20px;">
                <div style="margin-bottom: 15px;">
                    <a href="#" style="color: #2a5298; text-decoration: none; font-size: 12px; margin: 0 15px; font-weight: 500;">Privacy Policy</a>
                    <a href="#" style="color: #2a5298; text-decoration: none; font-size: 12px; margin: 0 15px; font-weight: 500;">Terms of Service</a>
                    <a href="#" style="color: #2a5298; text-decoration: none; font-size: 12px; margin: 0 15px; font-weight: 500;">Unsubscribe</a>
                    <a href="#" style="color: #2a5298; text-decoration: none; font-size: 12px; margin: 0 15px; font-weight: 500;">Security Center</a>
                </div>
                <p style="color: #9ca3af; font-size: 11px; margin: 0; line-height: 1.5;">
                    This email was sent by TechFlow Solutions Inc. to keep you informed about your account and services.<br>
                    If you received this email in error, please contact us immediately.
                </p>
            </div>
        </div>
        
    </div>
    
    <!-- Legal Footer -->
    <div style="text-align: center; margin-top: 20px; padding: 15px;">
        <p style="color: #9ca3af; font-size: 11px; margin: 0 0 5px 0; line-height: 1.4;">
            © 2024 TechFlow Solutions Inc. All rights reserved. | NASDAQ: TFLOW
        </p>
        <p style="color: #d1d5db; font-size: 10px; margin: 0; line-height: 1.3;">
            TechFlow Solutions is a registered trademark. Enterprise software solutions trusted by 10,000+ companies worldwide.
        </p>
    </div>
    
</body>
</html>
"""
