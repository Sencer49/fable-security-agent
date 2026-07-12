# 🛡️ Fable 5 Autonomous Code Security Agent

An AI-powered autonomous DevSecOps agent built with Python and Claude (Fable 5 / Sonnet) that scans codebases for critical security flaws (OWASP Top 10), provides detailed vulnerability reports, and automatically generates secure patches.

## ✨ Features
- **Semantic & Static Code Analysis:** Scans Python, JavaScript, Go, and Java files for security vulnerabilities.
- **Autonomous Patching:** Automatically generates non-breaking, secure code fixes (`app_patched.py`).
- **Structured JSON Output:** Clean evaluation responses designed for easy CI/CD and pipeline integration.
- **Fail-safe Mock Mode:** Built-in testing layer for local development without API calls.

## 🚀 Quick Start

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Sencer49/fable-security-agent.git](https://github.com/Sencer49/fable-security-agent.git)
   cd fable-security-agent
   
python -m venv venv
# On Windows:
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

ANTHROPIC_API_KEY=your_actual_api_key_here

cd src
python main.py
