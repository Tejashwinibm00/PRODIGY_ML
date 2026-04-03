import streamlit as st
import sqlite3
from PyPDF2 import PdfReader

st.set_page_config(page_title="AI Study Assistant", layout="centered")
st.title("📚 AI Study Assistant – Final Version (Week 8)")

# -------------------------------
# INITIALIZE QUIZ (IMPORTANT FIX)
# -------------------------------
quiz = []

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
# SIDEBAR DASHBOARD
# -------------------------------
st.sidebar.title("📊 Study Dashboard")

c.execute("SELECT COUNT(*) FROM progress")
total_quizzes = c.fetchone()[0]
st.sidebar.metric("Total Quizzes", total_quizzes)

c.execute("SELECT subject, COUNT(*) FROM progress GROUP BY subject")
rows = c.fetchall()
for r in rows:
    st.sidebar.write(f"📘 {r[0]}: {r[1]}")

# -------------------------------
# FILE INPUT
# -------------------------------
st.header("📄 Upload or Paste Study Material")

uploaded_file = st.file_uploader(
    "Upload PDF or TXT file",
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

text = st.text_area("Paste study text here", value=text, height=180)

# -------------------------------
# STUDY OPTIONS
# -------------------------------
st.header("⚙️ Study Options")

subject = st.selectbox(
    "Choose Subject",
    ["Python", "DBMS", "Operating System", "Data Structures", "General"]
)

difficulty = st.radio(
    "Choose Difficulty",
    ["Easy", "Medium", "Hard"]
)

# -------------------------------
# QUIZ GENERATOR FUNCTION
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
# GENERATE QUIZ BUTTON
# -------------------------------
if st.button("📝 Generate Quiz"):
    if text.strip() == "":
        st.error("Please upload or paste study content!")
    else:
        quiz = generate_quiz(text, difficulty)

        st.success("Quiz generated successfully!")

        st.subheader("🧠 Quiz Questions")
        for i, q in enumerate(quiz, 1):
            st.write(f"{i}. {q}")

        # SAVE TO DATABASE
        c.execute(
            "INSERT INTO progress (subject, difficulty, questions) VALUES (?, ?, ?)",
            (subject, difficulty, len(quiz))
        )
        conn.commit()

        # -------------------------------
        # FLASHCARDS
        # -------------------------------
        st.subheader("🃏 Flashcards")
        for q in quiz:
            with st.expander("Show Flashcard"):
                st.write(q)

        # -------------------------------
        # EXPORT QUIZ
        # -------------------------------
        quiz_text = ""
        for i, q in enumerate(quiz, 1):
            quiz_text += f"{i}. {q}\n"

        st.download_button(
            label="📥 Download Quiz",
            data=quiz_text,
            file_name="quiz.txt",
            mime="text/plain"
        )

# -------------------------------
# STUDY RECOMMENDATION
# -------------------------------
st.header("📅 Study Recommendation")

if total_quizzes < 3:
    st.info("Study 30 minutes daily to build consistency.")
elif total_quizzes < 6:
    st.info("Study 45 minutes daily and revise weekly.")
else:
    st.success("Excellent progress! Study 1 hour daily with mixed difficulty.")