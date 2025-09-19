import streamlit as st
import requests
import json
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = "http://localhost:8000"

def get_email_counts(email_list):
    gmail_count = sum(1 for email in email_list if email.lower().endswith('@gmail.com'))
    total_count = len(email_list)
    other_count = total_count - gmail_count
    return gmail_count, total_count, other_count

st.set_page_config(
    page_title="AI Email Sender - CEO Dashboard", 
    page_icon="📧", 
    layout="wide",
    initial_sidebar_state="expanded"
)

if "messages" not in st.session_state:
    st.session_state.messages = []
if "employee_emails" not in st.session_state:
    st.session_state.employee_emails = []
if "email_draft" not in st.session_state:
    st.session_state.email_draft = ""
if "pending_send" not in st.session_state:
    st.session_state.pending_send = False

def main():
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styling */
    .main {
        font-family: 'Inter', sans-serif !important;
        background-color: #fafafa !important;
    }
    
    /* Main title styling */
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        padding: 1rem 0;
        letter-spacing: -0.02em;
    }
    
    /* Emoji in title */
    .title-emoji {
        font-size: 3.5rem;
        margin-right: 0.5rem;
        vertical-align: middle;
    }
    
    /* Subtitle styling */
    .main-subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #7f8c8d;
        font-weight: 400;
        margin-bottom: 2rem;
        letter-spacing: 0.01em;
    }
    
    /* Status card styling */
    .status-card {
        background: #ffffff;
        padding: 1.8rem;
        border-radius: 12px;
        border: 1px solid #e8e8e8;
        margin: 1.5rem 0;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    /* Status emoji styling */
    .status-emoji {
        font-size: 2rem;
        margin-right: 0.5rem;
        vertical-align: middle;
    }
    
    /* Fix chat input at bottom */
    .stChatInput {
        position: sticky !important;
        bottom: 0 !important;
        background: #ffffff !important;
        z-index: 999 !important;
        padding: 15px 0 !important;
        border-top: 1px solid #e8e8e8 !important;
        box-shadow: 0 -1px 3px rgba(0,0,0,0.05) !important;
    }
    
    /* Chat container styling */
    .stChatMessage {
        margin-bottom: 1rem !important;
        border-radius: 12px !important;
    }
    
    /* Chat message emoji styling */
    .stChatMessage [data-testid="chatAvatarIcon-assistant"] {
        background-color: #f8f9fa !important;
        color: #2c3e50 !important;
    }
    
    .stChatMessage [data-testid="chatAvatarIcon-user"] {
        background-color: #2c3e50 !important;
        color: #ffffff !important;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: #ffffff !important;
        border-right: 1px solid #e8e8e8 !important;
    }
    
    /* Button styling */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 500 !important;
        transition: all 0.2s ease !important;
        border: 1px solid #e8e8e8 !important;
        background-color: #ffffff !important;
        color: #2c3e50 !important;
    }
    
    .stButton > button:hover {
        background-color: #f8f9fa !important;
        border-color: #d0d0d0 !important;
    }
    
    /* Ensure proper scrolling */
    .main .block-container {
        padding-bottom: 120px !important;
        max-width: 1200px !important;
    }
    
    /* Header spacing */
    .block-container {
        padding-top: 1rem !important;
    }
    
    /* Reduce spacing between elements */
    .element-container {
        margin-bottom: 0.5rem !important;
    }
    
    /* Compact metrics */
    [data-testid="metric-container"] {
        background: #ffffff !important;
        border: 1px solid #e8e8e8 !important;
        border-radius: 8px !important;
        padding: 0.8rem !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }
    
    /* Input field styling */
    .stTextInput > div > div > input {
        border-radius: 8px !important;
        border: 1px solid #e8e8e8 !important;
    }
    
    /* Remove default streamlit styling */
    .stApp {
        background-color: #fafafa !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="text-align: center; padding: 1.2rem 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 12px; margin-bottom: 1.5rem; color: white; box-shadow: 0 3px 10px rgba(0,0,0,0.1);">
        <h1 style="font-size: 2.5rem; margin: 0; font-weight: 600; text-shadow: 1px 1px 3px rgba(0,0,0,0.3);">
            📧 CorpMail AI
        </h1>
        <p style="font-size: 1rem; margin: 0.3rem 0 0 0; opacity: 0.9; font-weight: 300;">
            🚀 Professional Email Assistant for Executive Communication
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.employee_emails:
        gmail_count, total_count, other_count = get_email_counts(st.session_state.employee_emails)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(
                label="📧 Gmail Recipients", 
                value=gmail_count,
                delta="Ready to send" if gmail_count > 0 else None
            )
        with col2:
            st.metric(
                label="📮 Other Recipients", 
                value=other_count,
                delta="Various providers" if other_count > 0 else None
            )
        with col3:
            st.metric(
                label="📊 Total Recipients", 
                value=total_count,
                delta="All configured"
            )
        
        st.success(f"🎉 **System Ready!** You have {total_count} recipients configured and ready for email campaigns.")
        
    else:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%); 
                    padding: 1.2rem; border-radius: 12px; text-align: center; margin: 0.8rem 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="color: #2d3436; margin: 0 0 0.5rem 0; font-size: 1.4rem;">
                🚀 Welcome to CorpMail AI!
            </h3>
            <p style="color: #636e72; font-size: 0.95rem; margin: 0;">
                Get started by adding email recipients in the sidebar, then chat with our AI to create and send professional emails.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.header("📧 Recipients")
        
        if st.session_state.employee_emails:
            gmail_count, total_count, other_count = get_email_counts(st.session_state.employee_emails)
            st.metric("Total Recipients", total_count, delta=f"{gmail_count} Gmail")
        else:
            st.info("💡 Add email addresses to get started")
        
        st.divider()
        
        tab1, tab2 = st.tabs(["➕ Add", "📋 Manage"])
        
        with tab1:
            new_email = st.text_input("Email Address", placeholder="user@gmail.com")
            if st.button("Add Email", use_container_width=True) and new_email:
                if '@' not in new_email or '.' not in new_email.split('@')[1]:
                    st.error("❌ Invalid email format")
                elif new_email not in st.session_state.employee_emails:
                    st.session_state.employee_emails.append(new_email)
                    st.success(f"✅ Added")
                    st.rerun()
                else:
                    st.warning("⚠️ Already exists")
            
            st.divider()
            
            with st.expander("📝 Bulk Add"):
                bulk_emails = st.text_area("One email per line", height=100, placeholder="user1@gmail.com\nuser2@yahoo.com")
                if st.button("Add All", use_container_width=True) and bulk_emails:
                    emails = [email.strip() for email in bulk_emails.split('\n') if email.strip()]
                    valid_emails = []
                    invalid_count = 0
                    
                    for email in emails:
                        if '@' in email and '.' in email.split('@')[1]:
                            if email not in st.session_state.employee_emails:
                                valid_emails.append(email)
                        else:
                            invalid_count += 1
                    
                    if valid_emails:
                        st.session_state.employee_emails.extend(valid_emails)
                        st.success(f"✅ Added {len(valid_emails)} emails")
                        if invalid_count > 0:
                            st.warning(f"⚠️ Skipped {invalid_count} invalid emails")
                        st.rerun()
                    elif invalid_count > 0:
                        st.error(f"❌ All {invalid_count} emails are invalid")
        
        with tab2:
            if st.session_state.employee_emails:
                gmail_count, total_count, other_count = get_email_counts(st.session_state.employee_emails)
                
                if gmail_count > 0:
                    st.success(f"📧 {gmail_count} Gmail")
                if other_count > 0:
                    st.info(f"📮 {other_count} Other providers")
                
                st.divider()
                
                if len(st.session_state.employee_emails) > 5:
                    search_term = st.text_input("🔍 Search emails", placeholder="Filter emails...")
                    filtered_emails = [email for email in st.session_state.employee_emails 
                                     if search_term.lower() in email.lower()] if search_term else st.session_state.employee_emails
                else:
                    filtered_emails = st.session_state.employee_emails
                
                for i, email in enumerate(st.session_state.employee_emails):
                    if email in filtered_emails:
                        col1, col2 = st.columns([4, 1])
                        with col1:
                            domain = email.split('@')[1].lower() if '@' in email else 'unknown'
                            if 'gmail' in domain:
                                st.text(f"📧 {email}")
                            elif 'yahoo' in domain:
                                st.text(f"📮 {email}")
                            elif 'outlook' in domain or 'hotmail' in domain:
                                st.text(f"📨 {email}")
                            else:
                                st.text(f"✉️ {email}")
                        with col2:
                            if st.button("🗑️", key=f"remove_{i}", help="Remove"):
                                st.session_state.employee_emails.pop(i)
                                st.rerun()
                
                st.divider()
                
                if st.button("🗑️ Clear All", type="secondary", use_container_width=True):
                    st.session_state.employee_emails = []
                    st.success("All cleared!")
                    st.rerun()
            else:
                st.info("📭 No recipients added yet")
    
    col1, col2 = st.columns([2.5, 1.5])
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem; color: white;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 1.4rem; font-weight: 600;">
                💬 Chat with CorpMail Agent
            </h3>
            <p style="margin: 0.3rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">
                🤖 Ask me to create professional emails, announcements, or any corporate communication
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if not st.session_state.messages:
            st.markdown("""
            <div style="background: #f8f9fa; padding: 1.2rem; border-radius: 10px; text-align: center; 
                        border: 2px dashed #dee2e6; margin: 1rem 0;">
                <h4 style="color: #6c757d; margin: 0 0 0.5rem 0; font-size: 1.2rem;">
                    👋 Start Your Conversation
                </h4>
                <p style="color: #6c757d; margin: 0 0 1rem 0; font-size: 0.95rem;">
                    Try one of these example prompts:
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📅 Create Meeting Announcement", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Create a meeting announcement for tomorrow"})
                    st.rerun()
                if st.button("🎉 Holiday Greeting", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Send a holiday greeting to all employees"})
                    st.rerun()
            with col_b:
                if st.button("📢 Company Update", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Create a company update announcement"})
                    st.rerun()
                if st.button("🏆 Team Achievement", use_container_width=True):
                    st.session_state.messages.append({"role": "user", "content": "Announce a team achievement"})
                    st.rerun()
        else:
            with st.container():
                for message in st.session_state.messages:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])
        
        if prompt := st.chat_input("💭 Ask me to generate and send emails... (e.g., 'Create a team meeting announcement')"):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            try:
                response = requests.post(
                    f"{API_BASE_URL}/chat/message",
                    json={
                        "message": prompt,
                        "employee_emails": st.session_state.employee_emails
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get("response", "Sorry, I couldn't process that request.")
                    
                    st.session_state.messages.append({"role": "assistant", "content": ai_response})
                    
                    if result.get("email_draft"):
                        st.session_state.email_draft = result["email_draft"]
                        st.session_state.pending_send = result.get("pending_send", False)
                        
                    if result.get("email_sent"):
                        send_result = result.get("send_result", {})
                        if send_result.get("success"):
                            success_msg = f"✅ Email sent successfully to {send_result.get('sent_count', 0)} recipients!"
                            st.session_state.messages.append({"role": "assistant", "content": success_msg})
                        else:
                            error_msg = "❌ Failed to send email"
                            st.session_state.messages.append({"role": "assistant", "content": error_msg})
                        st.session_state.email_draft = ""
                        st.session_state.pending_send = False
                else:
                    error_msg = "Failed to get response from AI assistant"
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    
            except requests.exceptions.RequestException as e:
                error_msg = f"Connection error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            except Exception as e:
                error_msg = f"Error: {str(e)}"
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
            
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #00b894 0%, #00a085 100%); 
                    padding: 1rem; border-radius: 10px; margin-bottom: 1rem; color: white;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h3 style="margin: 0; font-size: 1.4rem; font-weight: 600;">
                📧 Email Management
            </h3>
            <p style="margin: 0.3rem 0 0 0; opacity: 0.9; font-size: 0.85rem;">
                📝 Review and send your generated emails
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.email_draft:
            st.markdown("""
            <div style="background: #fff3cd; border: 1px solid #ffeaa7; border-radius: 8px; 
                        padding: 0.8rem; margin-bottom: 0.8rem;">
                <h5 style="margin: 0 0 0.3rem 0; color: #856404; font-size: 1.1rem;">
                    📝 Email Draft Ready
                </h5>
                <p style="margin: 0; color: #856404; font-size: 0.85rem;">
                    Review your email below and send when ready
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            try:
                if isinstance(st.session_state.email_draft, str):
                    email_data = json.loads(st.session_state.email_draft)
                else:
                    email_data = st.session_state.email_draft
                
                st.text_input("📧 Subject:", value=email_data.get("subject", ""), key="email_subject")
                st.text_area("📝 Email Body:", value=email_data.get("body", ""), height=200, key="email_body")
                
                if st.session_state.employee_emails:
                    gmail_count, total_count, other_count = get_email_counts(st.session_state.employee_emails)
                    
                    st.markdown(f"""
                    <div style="background: #e3f2fd; border-radius: 8px; padding: 1rem; margin: 1rem 0;">
                        <h5 style="margin: 0 0 0.5rem 0; color: #1565c0;">📊 Recipients Summary</h5>
                        <div style="display: flex; justify-content: space-between; color: #1976d2;">
                            <span>📧 Gmail: <strong>{gmail_count}</strong></span>
                            <span>📮 Others: <strong>{other_count}</strong></span>
                            <span>📊 Total: <strong>{total_count}</strong></span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("🚀 Send Email to All Recipients", type="primary", use_container_width=True):
                        try:
                            send_response = requests.post(
                                f"{API_BASE_URL}/email/send",
                                json={
                                    "subject": st.session_state.email_subject,
                                    "body": st.session_state.email_body,
                                    "employee_emails": st.session_state.employee_emails
                                },
                                timeout=30
                            )
                            
                            if send_response.status_code == 200:
                                result = send_response.json()
                                if result.get("success"):
                                    st.success(result.get("message", "Email sent successfully!"))
                                    st.session_state.email_draft = ""
                                    st.session_state.pending_send = False
                                else:
                                    st.error(f"Failed to send email: {result.get('message', 'Unknown error')}")
                            else:
                                st.error("Failed to send email")
                                
                        except requests.exceptions.RequestException as e:
                            st.error(f"Connection error: {str(e)}")
                        except Exception as e:
                            st.error(f"Error: {str(e)}")
                else:
                    st.warning("⚠️ Add recipients in the sidebar first")
                    
            except json.JSONDecodeError:
                st.error("❌ Invalid email draft format")
        else:
            st.markdown("""
            <div style="background: #f8f9fa; border: 2px dashed #dee2e6; border-radius: 12px; 
                        padding: 2rem; text-align: center; margin: 1rem 0;">
                <h4 style="color: #6c757d; margin: 0 0 1rem 0;">
                    📝 No Email Draft Yet
                </h4>
                <p style="color: #6c757d; margin: 0; font-size: 0.95rem;">
                    Start a conversation with the AI agent to generate your first email draft
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fd79a8 0%, #e84393 100%); 
                    padding: 1rem; border-radius: 10px; margin: 1.5rem 0 1rem 0; color: white;">
            <h4 style="margin: 0; font-size: 1.3rem; font-weight: 600;">
                📋 Recent Emails
            </h4>
            <p style="margin: 0.3rem 0 0 0; opacity: 0.9; font-size: 0.85rem;">
                📊 Your email sending history
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            recent_response = requests.get(f"{API_BASE_URL}/email/recent?limit=5", timeout=10)
            if recent_response.status_code == 200:
                recent_emails = recent_response.json()
                if recent_emails:
                    for idx, email in enumerate(recent_emails):
                        success_rate = f"{email['success_count']}/{email['total_count']}"
                        with st.expander(f"📧 {email['subject']} • {success_rate} sent", expanded=False):
                            col_a, col_b = st.columns(2)
                            with col_a:
                                st.caption("📅 Sent At")
                                st.text(email['sent_at'])
                            with col_b:
                                st.caption("👥 Recipients")
                                st.text(f"{len(email['recipients'])} total")
                            st.caption("📝 Email Content")
                            unique_key = f"recent_{idx}_{email.get('sent_at', '').replace(' ', '_').replace(':', '_')}"
                            st.text_area(
                                "Email Body",
                                value=email['body'],
                                height=80,
                                disabled=True,
                                key=unique_key,
                                label_visibility="collapsed"
                            )
                else:
                    st.info("📭 No recent emails found")
            else:
                st.warning("⚠️ Could not load recent emails")
        except requests.exceptions.RequestException:
            st.info("📡 Recent emails will appear here when the backend is running")
    
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 2rem 0; background: linear-gradient(135deg, #636e72 0%, #2d3436 100%); 
                border-radius: 12px; margin-top: 2rem; color: white;">
        <h4 style="margin: 0 0 0.5rem 0; font-weight: 600;">
            🚀 CorpMail AI - Professional Email Assistant
        </h4>
        <p style="margin: 0; opacity: 0.8; font-size: 0.9rem;">
            💼 Streamline your corporate communications with AI-powered email generation
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
