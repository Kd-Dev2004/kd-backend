from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
import uuid
import requests

app = Flask(__name__)
CORS(app)

# ==============================
# API KEY
# ==============================

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not set")

client = Groq(api_key=GROQ_API_KEY)

MODEL = "llama-3.1-8b-instant"

# ==============================
# MEMORY STORE
# ==============================

memory_store = {}

# ==============================
# PORTFOLIO KNOWLEDGE
# ==============================

SYSTEM_PROMPT = """
You are the AI assistant for the portfolio of Kaushal Dholakiya.

Your job is to help visitors understand Kaushal's work,
projects, skills, education, and contact information.

Always answer clearly and professionally.

------------------------------------------------
PERSON
------------------------------------------------

Name: Kaushal Dholakiya
Alias: KD / KD-2004

Roles:
Penetration Tester
VAPT Analyst
AI Engineer
Systems Engineer

Website:
https://kd-dev2004.github.io/

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
PROFILE
------------------------------------------------

Kaushal Dholakiya is a technology enthusiast working across
AI, cybersecurity, and software engineering.

He builds intelligent systems combining:

• artificial intelligence
• cybersecurity
• automation
• robotics
• backend engineering

His goal is to build intelligent and secure systems
that solve real-world problems.

------------------------------------------------
PROJECTS
------------------------------------------------

LearnMate
AI assistant for document Q&A and OCR pipelines.

CyberSense
Multi-engine antivirus scanner.

MovieMate
AI movie recommendation system using embeddings.

CreditGuard
Machine learning system for fraud detection.

InfiWasTex
Autonomous waste detection robot using
YOLO perception and SLAM navigation.

------------------------------------------------
EDUCATION
------------------------------------------------

MSc Cyber Security
Manipal University
2025

BSc Computer Science
Mumbai University
2022-2025

------------------------------------------------
SKILLS
------------------------------------------------

Cybersecurity
VAPT
Active Directory attacks
OWASP Top 10
Exploit development

AI / ML
LLMs
AI agents
Computer vision
Fraud detection

Programming
Python
Bash
SQL
C++
Java
Flask

Robotics
ROS2
YOLO
SLAM
Jetson

------------------------------------------------

If the user asks about Kaushal or his work,
answer using the information above.

If the question is unrelated to the portfolio,
answer normally.
"""

# ==============================
# SECURITY FILTER
# ==============================

def safe_prompt(prompt):

    blocked = [
        "ignore previous instructions",
        "reveal system prompt",
        "show hidden prompt",
        "print system prompt"
    ]

    for word in blocked:
        if word in prompt.lower():
            return False

    return True

# ==============================
# ROOT
# ==============================

@app.route("/")
def home():

    return jsonify({
        "service": "KD Portfolio AI",
        "status": "running",
        "developer": "Kaushal Dholakiya"
    })


# ==============================
# HEALTH
# ==============================

@app.route("/health")
def health():

    return jsonify({"status": "alive"})


# ==============================
# API INFO
# ==============================

@app.route("/api/info")
def info():

    return jsonify({
        "name": "KD Portfolio AI",
        "model": MODEL,
        "features": [
            "Portfolio Q&A",
            "AI Chat Assistant",
            "Project Explorer",
            "GitHub Repo Fetch",
            "Session Memory",
            "Voice Assistant Support"
        ]
    })


# ==============================
# PROJECTS
# ==============================

@app.route("/api/projects")
def projects():

    return jsonify({
        "projects":[
            {
                "name":"LearnMate",
                "description":"AI assistant for document understanding"
            },
            {
                "name":"CyberSense",
                "description":"Multi engine antivirus scanner"
            },
            {
                "name":"MovieMate",
                "description":"AI movie recommendation system"
            },
            {
                "name":"CreditGuard",
                "description":"Fraud detection ML system"
            },
            {
                "name":"InfiWasTex",
                "description":"Autonomous waste robot"
            }
        ]
    })


# ==============================
# SKILLS
# ==============================

@app.route("/api/skills")
def skills():

    return jsonify({
        "skills":[
            "Cybersecurity",
            "VAPT",
            "AI / Machine Learning",
            "Python",
            "Flask",
            "Robotics",
            "Active Directory Security",
            "Computer Vision"
        ]
    })


# ==============================
# CONTACT
# ==============================

@app.route("/api/contact")
def contact():

    return jsonify({
        "email":"kaushaldholakiya4@gmail.com",
        "phone":"+91 8104451162",
        "github":"https://github.com/KD-2004",
        "website":"https://kaushaldholakiya4.com"
    })


# ==============================
# GITHUB REPOS
# ==============================

@app.route("/api/github")
def github():

    url = "https://api.github.com/users/KD-2004/repos"

    r = requests.get(url)

    repos = []

    if r.status_code == 200:

        for repo in r.json():

            repos.append({
                "name": repo["name"],
                "url": repo["html_url"],
                "stars": repo["stargazers_count"]
            })

    return jsonify({"repos": repos})


# ==============================
# AI CHAT
# ==============================

@app.route("/api/chat", methods=["POST"])
def chat():

    data = request.get_json()

    prompt = data.get("prompt")
    session_id = data.get("session_id")

    if not prompt:
        return jsonify({"error":"Prompt required"}),400

    if not safe_prompt(prompt):
        return jsonify({"error":"Blocked prompt"}),403

    if not session_id:
        session_id = str(uuid.uuid4())

    if session_id not in memory_store:
        memory_store[session_id] = []

    history = memory_store[session_id]

    try:

        messages = [{"role":"system","content":SYSTEM_PROMPT}]

        for msg in history[-6:]:
            messages.append(msg)

        messages.append({"role":"user","content":prompt})

        completion = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0.7,
            max_tokens=400
        )

        response = completion.choices[0].message.content

        history.append({"role":"user","content":prompt})
        history.append({"role":"assistant","content":response})

        return jsonify({
            "session_id":session_id,
            "response":response
        })

    except Exception as e:

        return jsonify({"error":str(e)}),500


# ==============================
# VOICE (JARVIS SUPPORT)
# ==============================

@app.route("/api/voice", methods=["POST"])
def voice():

    data = request.get_json()

    text = data.get("text")

    if not text:
        return jsonify({"error":"Text required"}),400

    return jsonify({
        "speech": text
    })


# ==============================
# START SERVER
# ==============================

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=10000)
