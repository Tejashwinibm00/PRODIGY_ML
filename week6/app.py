import streamlit as st
import sqlite3
from PyPDF2 import PdfReader

st.title("AI Study Assistant – Week 6")

# -------------------------------
# DATABASE
# -------------------------------
conn = sqlite3.connect("study.db")
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS progress (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    difficulty TEXT,
    questions INTEGER
)
""")
conn.commit()

# -------------------------------
# FILE INPUT
# -------------------------------
uploaded_file = st.file_uploader(
    "Upload study file (PDF or TXT)",
    type=["pdf", "txt"]
)

text = ""

def extract_pdf_text(file):
    reader = PdfReader(file)
    content = ""
    for page in reader.pages:
        content += page.extract_text()
    return content

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_pdf_text(uploaded_file)
    else:
        text = uploaded_file.read().decode("utf-8")

text = st.text_area("Or paste study text here", value=text, height=180)

# -------------------------------
# SUBJECT & DIFFICULTY
# -------------------------------
subject = st.selectbox(
    "Choose Subject",
    ["Python", "DBMS", "Operating System", "Data Structures", "General"]
)

difficulty = st.selectbox(
    "Choose Difficulty",
    ["Easy", "Medium", "Hard"]
)

# -------------------------------
# QUIZ GENERATION
# -------------------------------
def generate_quiz(content, level):
    questions = []
    sentences = content.split(".")

    for s in sentences:
        s = s.strip()
        if len(s) < 20:
            continue

        if level == "Easy":
            q = f"True or False: {s}"
        elif level == "Medium":
            q = f"Explain: {s}"
        else:
            words = s.split()
            if len(words) > 4:
                words[2] = "______"
            q = "Fill in the blank: " + " ".join(words)

        questions.append(q)
        if len(questions) == 5:
            break

    return questions

# -------------------------------
# GENERATE BUTTON
# -------------------------------
if st.button("Generate Quiz"):
    if text.strip() == "":
        st.warning("Please upload or paste study text")
    else:
        quiz = generate_quiz(text, difficulty)

        st.subheader("Quiz Questions")
        for i, q in enumerate(quiz, 1):
            st.write(f"{i}. {q}")

        # SAVE DATA
        c.execute(
            "INSERT INTO progress (subject, difficulty, questions) VALUES (?, ?, ?)",
            (subject, difficulty, len(quiz))
        )
        conn.commit()

        st.success("Quiz attempt saved!")

# -------------------------------
# PERFORMANCE ANALYTICS
# -------------------------------
st.subheader("Performance Analytics")

c.execute("SELECT subject, COUNT(*) FROM progress GROUP BY subject")
subject_data = c.fetchall()

if subject_data:
    for s in subject_data:
        st.write(f"📘 {s[0]}: {s[1]} quizzes attempted")
else:
    st.write("No data available")

# -------------------------------
# STUDY SCHEDULE RECOMMENDATION
# -------------------------------
st.subheader("Study Schedule Recommendation")

c.execute("SELECT COUNT(*) FROM progress")
total_attempts = c.fetchone()[0]

if total_attempts < 3:
    st.info("Study at least 30 minutes daily to build consistency.")
elif total_attempts < 6:
    st.info("You are doing well. Study 45 minutes daily and revise weekly.")
else:
    st.success("Great consistency! Try 1 hour daily with mixed difficulty levels.")