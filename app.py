from flask import Flask, render_template, request, jsonify
from xai_sdk import Client
import PyPDF2
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# ✅ Initialize client using GROQ API key
client = Client(api_key=os.getenv("GROQ_API_KEY"))


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        name = request.form.get("name")
        degree = request.form.get("degree")
        skills = request.form.get("skills")
        interests = request.form.get("interests")
        goal = request.form.get("goal")

        resume_text = ""
        resume_file = request.files.get("resume")

        # Extract PDF text
        if resume_file:
            reader = PyPDF2.PdfReader(resume_file)
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    resume_text += text

        prompt = f"""
You are VidyaGuide — an advanced AI career mentor.

Student:
Name: {name}
Degree: {degree}
Skills: {skills}
Interests: {interests}
Goal: {goal}

Resume:
{resume_text}

Provide:

⭐ Top 3 Career Paths with Match %
⭐ Skill Gaps
⭐ 3-Month Roadmap
⭐ Resume Strength Score /100
⭐ Resume Improvements

Be specific. Avoid generic advice.
"""

        # ✅ Create chat (uses GROK/GROQ model)
        chat = client.chat.create(model="grok-4")

        chat.append(
            role="user",
            content=prompt
        )

        response = chat.sample()

        result = response.content

        return jsonify({"result": result})

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "result": "⚠️ AI is currently busy. Please try again."
        })


if __name__ == "__main__":
    app.run(debug=True)
