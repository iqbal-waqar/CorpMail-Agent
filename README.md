
# 📧 CorpMail - AI-Powered Email Assistant

**Automate and streamline your corporate email communications with AI.**

---

## 🚀 Overview

CorpMail is an intelligent email automation system for companies and teams. It enables managers and executives to generate, format, and send professional emails instantly using AI, saving time and ensuring consistency.

---

## ✨ Key Features

- **AI-Powered Email Generation:** Uses advanced LLMs (Groq, LangChain) to create professional emails from simple prompts.
- **Branded HTML Templates:** Automatically formats emails with company branding and responsive design.
- **Bulk Sending:** Send announcements and updates to multiple recipients at once.
- **Interactive Chat UI:** Streamlit dashboard for real-time interaction and email preview.
- **Reliable Delivery:** Integrates with SendGrid for enterprise-grade email delivery.

---

## �️ Technology Stack

- **Backend:** FastAPI, LangChain, LangGraph, Groq LLM, SendGrid
- **Frontend:** Streamlit
- **Other:** dotenv for environment management, JSON for templates

---

## 🏗️ Project Structure

```
CorpMail/
├── backend/
│   ├── interactors/     # Business logic (email processing)
│   ├── routes/          # API endpoints (chat, email)
│   ├── schemas/         # Data models
│   ├── services/        # LLM, SendGrid, workflow tools
│   └── utils/           # Helper functions
├── frontend/
│   └── frontend.py      # Streamlit dashboard
├── email_scenarios.json # Predefined email scenarios/templates
├── main.py              # FastAPI app entry point
├── pyproject.toml       # Project dependencies
├── uv.lock              # Dependency lock file
└── README.md            # This file
```

---

## ⚡ Quick Start

### Prerequisites

- Python 3.10+
- SendGrid API key
- Groq API key

### Installation

1. **Clone the repository**
    ```bash
    git clone <your-repo-url>
    cd CorpMail
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    # or
    uv sync
    ```

3. **Environment Setup**
    Create a `.env` file in the root directory:
    ```
    SENDGRID_API_KEY=your_sendgrid_api_key
    SENDGRID_FROM_EMAIL=noreply@yourcompany.com
    GROQ_API_KEY=your_groq_api_key
    ```

4. **Run the Application**
    - Start backend: `python main.py`
    - Start frontend: `streamlit run frontend/frontend.py`

5. **Access**
    - Frontend: http://localhost:8501
    - Backend API: http://localhost:8000
    - API Docs: http://localhost:8000/docs

---

## � Usage Examples

- **Generate a meeting email:**  
  User: "Make an email for team meeting tomorrow at 2:00 PM in conference room A"  
  AI: Generates a formatted meeting announcement.

- **Send an announcement:**  
  User: "Announce that our sales team exceeded quarterly targets by 150%"  
  AI: Creates and sends a celebratory announcement.

- **Bulk notification:**  
  User: "Send system maintenance notification to all users for this weekend"  
  AI: Notifies all recipients with details.

---

## 🔧 Configuration

- **Email Templates:**  
  Customize scenarios in `email_scenarios.json`.

- **Environment Variables:**  
  - `SENDGRID_API_KEY`: SendGrid API key  
  - `SENDGRID_FROM_EMAIL`: Sender address  
  - `GROQ_API_KEY`: Groq API key

---

## 🎯 Use Cases

- **Executives/Managers:** Announcements, updates, team communications, recognition
- **HR:** Welcomes, policy updates, training, events
- **IT:** Maintenance, security, technical updates, support

---

## 🔒 Security

- Secure API keys via environment variables
- Email validation and error handling
- No storage of sensitive email content

---

## 🤝 Contributing

Contributions are welcome! Please open issues or pull requests.

---

## 📄 License

MIT License

---

## 🆘 Support

- Email: waqar302iqbal@gmail.com

---

**CorpMail** - Transforming your corporate communications with AI. 🚀