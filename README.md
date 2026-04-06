---
title: AI Email Security System
emoji: 📧
colorFrom: blue
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

🚀 AI Email Security System

An intelligent, real-world AI-powered email threat analysis system designed for the Meta OpenEnv Hackathon.

This system simulates how modern security tools detect spam, phishing, and suspicious emails using multi-signal reasoning and explainable AI.

---

🔥 Live Demo

👉 Hugging Face Space  
https://huggingface.co/spaces/Spandan-Satapute/ai-email-security-system-v2

👉 Interactive API (Swagger UI)  
https://spandan-satapute-ai-email-security-system-v2.hf.space/docs

---

🧠 Problem Statement

Email-based attacks are rapidly increasing in sophistication.

Traditional systems:

- ❌ Only detect spam  
- ❌ Provide no explanation  
- ❌ Lack risk awareness  
- ❌ Fail on phishing detection  

---

💡 Solution

This system provides a complete AI email security pipeline:

- ✅ Spam detection  
- ✅ Phishing detection  
- ✅ Suspicious email identification  
- ✅ Risk level classification (Low / High)  
- ✅ Confidence scoring  
- ✅ Explainable AI (WHY classification happened)  

---

🎯 OpenEnv Compliance

This project fully implements the OpenEnv specification.

---

🔹 Action Space

Input → Email text

- Type: string  
- Min Length: 1  
- Max Length: 10000  

---

🔹 Observation Space

```json
{
  "intent": "spam | safe | phishing | suspicious",
  "confidence": 0.0,
  "risk_level": "low | high",
  "risk_score": 0.0,
  "explanation": "string",
  "reward": 0.0,
  "step_count": 1
}
🔹 Reward Function
+0.4 → Correct intent
+0.3 → Confidence > 0.7
+0.2 → Correct risk level
+0.1 → Explanation quality
👉 Final Reward ∈ [0.0, 1.0]
🔹 Task Levels
🟢 Easy Task
Detect spam vs safe
🟡 Medium Task
Intent + confidence
🔴 Hard Task
Full reasoning (intent + risk + explanation)
🔹 Episode Design
Each request = new environment
Stateless execution
Done = True after classification
⚙️ Features
📧 Spam & Phishing Detection
🔍 Multi-Signal Analysis
📊 Risk Level Classification
🎯 Confidence Scoring
🧠 Explainable AI Output
🔄 OpenEnv Environment
⚡ FastAPI Backend
🐳 Docker Deployment
🌐 Hugging Face Hosting
🏗️ System Architecture
Component
Technology
Model
TF-IDF + Naive Bayes
Backend
FastAPI
Environment
OpenEnv
UI
Gradio
Deployment
Docker + HF Spaces
🔌 API Endpoints
Method
Endpoint
Description
POST
/classify
Classify email
POST
/grade
Grade output
POST
/reset
Reset environment
GET
/state
Get environment state
GET
/health
Health check
🧪 Example
Input
JSON
{
  "text": "URGENT! Click this link to claim your prize"
}
Output
JSON
{
  "intent": "phishing",
  "confidence": 0.87,
  "risk_level": "high",
  "risk_score": 0.9,
  "explanation": "Urgency + suspicious link detected",
  "reward": 0.95,
  "step_count": 1
}

⚙️ Local Setup
Bash
git clone https://github.com/Spandan-Satapute/ai-email-security-system.git
cd ai-email-security-system

python -m venv venv
pip install -r requirements.txt

uvicorn email_env.server.app:app --reload
👉 Open: http://127.0.0.1:8000/docs⁠�

🐳 Docker Setup
Bash
docker build -t ai-email-security .
docker run -p 7860:7860 ai-email-security

📦 Tech Stack
Python
FastAPI
Scikit-learn
Gradio
Docker
Hugging Face Spaces

🏆 Evaluation Strengths
Real-world cybersecurity system
Multi-level task evaluation
Deterministic reward system
Explainable AI outputs
Fully OpenEnv compliant

👨‍💻 Author
Spandan Satapute
CSE Student | AI Developer 🚀