import os
from dotenv import load_dotenv
from groq import Groq
from typing import List
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langchain_core.messages.tool import ToolCall

load_dotenv()

class LLMService:
    def __init__(self):
        self.api_key = os.environ.get("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("GROQ_API_KEY environment variable must be set")
        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-8b-instant"
    
    async def generate_email(self, topic: str, context: str = "") -> str:
        from datetime import datetime
        today_date = datetime.now().strftime("%B %d, %Y")
        
        prompt = f"""
        You are a professional email assistant for the CEO of TechFlow Solutions. Generate a professional, well-structured email about the following topic:
        
        Topic: {topic}
        Additional Context: {context}
        Today's Date: {today_date}
        
        IMPORTANT REQUIREMENTS:
        - Write complete, specific content - NO placeholder text like [Insert location] or [Your Name]
        - For meetings, provide specific details like conference room locations, actual meeting links
        - End the email with the signature: "CEO\\nTechFlow\\nDated: {today_date}"
        - Do NOT use placeholder signatures like [Your Name] [Your Title] [Company Name]
        - Be professional and appropriate for company-wide communication
        - Clear and concise with specific actionable information
        - Include proper subject line
        
        CRITICAL: You MUST respond with ONLY valid JSON. Use proper JSON escaping for newlines.
        For line breaks in the email body, use \\n (escaped newline characters).
        
        Format your response exactly like this:
        {{"subject": "Your subject here", "body": "Your email body here with \\n for line breaks"}}
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional email writing assistant for corporate communications. Always respond with ONLY valid JSON containing 'subject' and 'body' fields. Use \\n for line breaks in the body. Example: {\"subject\": \"Subject Here\", \"body\": \"Body text here\\nWith line breaks\"}"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            content = response.choices[0].message.content
            
            if content is None:
                return '{"subject": "", "body": ""}'
            
            import re
            import json
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                json_content = json_match.group(0)
                try:
                    fixed_content = json_content.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t')
                    parsed = json.loads(fixed_content)
                    return json.dumps(parsed, ensure_ascii=False)
                except json.JSONDecodeError:
                    return json_content
            
            def escape_json_string(s):
                return (s.replace('\\', '\\\\')
                        .replace('"', '\\"')
                        .replace('\n', '\\n')
                        .replace('\r', '\\r')
                        .replace('\t', '\\t')
                        .replace('\b', '\\b')
                        .replace('\f', '\\f'))
            
            escaped_content = escape_json_string(content)
            return f'{{"subject": "Company Communication", "body": "{escaped_content}"}}'
            
        except Exception as e:
            raise Exception(f"Failed to generate email: {e}")
    
    async def generate_response_with_tools(self, messages: List[BaseMessage], employee_emails: List[str] = None) -> AIMessage:
        if employee_emails is None:
            employee_emails = []
        
        last_user_message = ""
        for msg in reversed(messages):
            if isinstance(msg, HumanMessage):
                last_user_message = msg.content
                break
        
        if any(phrase in last_user_message.lower() for phrase in 
               ["generate email", "write email", "create email", "email about", "write an email", "make email",
                "compose email", "draft email", "email on", "create a", "write a", "send a", "make a",
                "announcement", "meeting", "holiday", "greeting", "update", "invite", "inform", "notify"]):
            
            topic = self._extract_topic_from_message(last_user_message)
            
            tool_calls = [
                ToolCall(
                    name="generate_professional_email",
                    args={"topic": topic, "context": ""},
                    id="generate_email_call"
                )
            ]
            
            return AIMessage(
                content="I'll help you generate a professional email. Let me create that for you.",
                tool_calls=tool_calls
            )
            
        elif any(phrase in last_user_message.lower() for phrase in 
                ["send email", "send it", "send the email"]):
            
            return AIMessage(
                content="I'll send the email to all employees now.",
                tool_calls=[
                    ToolCall(
                        name="send_email_to_employees",
                        args={
                            "employee_emails": employee_emails,
                            "subject": "Email Subject",
                            "email_body": "Email Body"
                        },
                        id="send_email_call"
                    )
                ]
            )
        else:
            return AIMessage(
                content="I am an email agent specialized in writing and sending professional emails. I can help you:\n\n• Generate professional emails for company communications\n• Write emails about meetings, announcements, holidays, etc.\n• Send emails to your employees\n\nPlease ask me to write or send an email, and I'll be happy to help!"
            )
    
    def extract_topic_from_message(self, message: str) -> str:
        message_lower = message.lower()
        
        patterns = [
            "write an email about", "write email about", "email about",
            "write an email on", "write email on", "email on",
            "create email about", "create email on",
            "make email about", "make email on",
            "compose email about", "compose email on",
            "draft email about", "draft email on",
            "generate email about", "generate email on"
        ]
        
        for pattern in patterns:
            if pattern in message_lower:
                topic = message_lower.split(pattern)[-1].strip()
                if topic:  
                    return topic
        
        fallback_patterns = ["write email", "create email", "make email", "compose email", "draft email", "generate email"]
        for pattern in fallback_patterns:
            if pattern in message_lower:
                topic = message_lower.split(pattern)[-1].strip()
                if topic:
                    return topic
        
        natural_patterns = [
            "create a", "write a", "send a", "make a", "make an", "create an", "write an"
        ]
        
        for pattern in natural_patterns:
            if pattern in message_lower:
                topic = message_lower.split(pattern)[-1].strip()
                if topic:
                    return topic
        
        if "announce" in message_lower:
            if "announce that" in message_lower:
                topic = message_lower.split("announce that")[-1].strip()
            else:
                topic = message_lower.split("announce")[-1].strip()
            if topic:
                return topic
        
        return message_lower if message_lower else "General company communication"
