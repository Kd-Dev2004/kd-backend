from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os

app = Flask(__name__)
CORS(app)

# -----------------------------
# Load API key
# -----------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set")

client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.1-8b-instant"


# -----------------------------
# Portfolio Knowledge Base
# -----------------------------
SYSTEM_PROMPT = """
You are the AI assistant for the portfolio website of Kaushal Dholakiya.

Your job is to help visitors understand Kaushal's work, projects, skills, and background.

Always answer clearly and professionally.

------------------------------------------------

PERSON

Name: Kaushal Dholakiya
Alias: KD / KD-2004

Roles:
• Penetration Tester
• VAPT Analyst
• AI Engineer
• Systems Engineer

Website:
https://kaushaldholakiya4.com

GitHub:
https://github.com/KD-2004

TryHackMe:
kaushaldholakiya4

HackTheBox:
KD-2004

Email:
kaushaldholakiya4@gmail.com

Phone:
+91 8104451162

------------------------------------------------

PROFILE SUMMARY

Kaushal Dholakiya is a technology enthusiast and systems builder working across artificial intelligence, cybersecurity, and software engineering.

His work focuses on designing intelligent systems, building practical tools, and solving real-world problems using modern technologies.

He frequently combines:

• AI & machine learning
• system engineering
• cybersecurity

to build scalable and secure solutions.

His interests include:

• AI systems
• offensive security
• autonomous robotics
• computer vision
• intelligent automation

------------------------------------------------

SKILLS

Cybersecurity & VAPT

• Vulnerability Assessment & Penetration Testing
• Web Application Pentesting (OWASP Top 10)
• Network & System Pentesting
• Vulnerability scanning & exploitation
• CVE analysis & CVSS scoring
• Proof-of-concept exploit development
• Security reporting & remediation

Active Directory Security

• Active Directory enumeration
• Privilege escalation
• Kerberos attacks
• Pass-the-hash
• Pass-the-ticket
• BloodHound attack path analysis
• Lateral movement

AI / Machine Learning

• Local LLM pipelines (DeepSeek, Phi-3, Ollama)
• Prompt engineering
• AI agents
• Fraud detection ML models
• Computer vision (YOLO, OCR, CLIP)

Programming

• Python
• Bash
• SQL
• C++
• Java
• Linux system administration
• Flask backend APIs

Robotics & IoT

• Robotics systems
• Arduino
• Raspberry Pi
• Autonomous navigation
• Edge AI systems

Security Tools

• Burp Suite
• Nmap
• Metasploit
• SQLmap
• Nikto
• OWASP ZAP
• Gobuster
• Dirsearch
• Hydra
• Medusa
• Aircrack-ng
• John the Ripper
• Hashcat
• Netcat
• Bettercap
• BloodHound
• Wireshark
• Kali Linux

------------------------------------------------

PROJECTS

LearnMate

AI assistant platform for document understanding, OCR, and automation.

Features:
• PDF Q&A
• OCR pipelines
• Local LLM integration
• Secure authentication

Tech stack:
Flask, Ollama, Phi-3, Tesseract, FAISS


CyberSense

Multi-engine antivirus scanner.

Features:
• Aggregates multiple AV engines
• YARA rule analysis
• Threat scoring

Tech stack:
Python, YARA, Redis, Celery


MovieMate

AI-powered movie recommendation system.

Features:
• LLM embeddings
• collaborative filtering
• movie metadata scraping


CreditGuard

Credit card fraud detection system.

Features:
• anomaly detection
• machine learning models
• ROC-AUC evaluation


InfiWasTex

Autonomous waste detection robot.

Features:
• YOLO object detection
• SLAM navigation
• robotic arm control

Tech stack:
ROS2, YOLOv8, Jetson

------------------------------------------------

EDUCATION

MSc Cyber Security
Manipal University
2025

BSc Computer Science
Mumbai University
2022 - 2025

------------------------------------------------

CERTIFICATIONS

• Certified Ethical Hacker (CEH)
• Python Programming
• Linux Fundamentals
• Android Development

------------------------------------------------

RESEARCH INTERESTS

• AI-driven security automation
• vulnerability discovery using ML
• adversarial machine learning
• autonomous robotics
• intelligent agents

------------------------------------------------

If someone asks about Kaushal, answer using the information above.

If the question is unrelated to the portfolio, answer normally as an AI assistant.
"""


# -----------------------------
# Conversation memory
# -----------------------------
conversation_history = []


# -----------------------------
# Root endpoint
# -----------------------------
@app.route("/")
def home():
    return jsonify({
        "status": "running",
        "developer": "KD",
        "message": "AI Backend developed by KD"
    })


# -----------------------------
# Health check
# -----------------------------
@app.route("/health")
def health():
    return jsonify({"status": "alive"})


# -----------------------------
# AI Chat Endpoint
# -----------------------------
@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body required"}), 400

    prompt = data.get("prompt")

    if not prompt:
        return jsonify({"error": "Prompt required"}), 400

    try:

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]

        for msg in conversation_history[-6:]:
            messages.append(msg)

        messages.append({"role": "user", "content": prompt})

        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=400,
            temperature=0.7
        )

        response = completion.choices[0].message.content

        conversation_history.append({"role": "user", "content": prompt})
        conversation_history.append({"role": "assistant", "content": response})

        return jsonify({
            "response": response,
            "developer": "AI backend developed by KD"
        })

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


# -----------------------------
# Run server
# -----------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
