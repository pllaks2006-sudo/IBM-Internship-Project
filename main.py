from flask import Flask, render_template, request, redirect, url_for, session

# ==========================================
# AI LEARNING AND STUDY ASSISTANT
# ==========================================

app = Flask(__name__)

# Session Secret Key
app.secret_key = "ai_learning_secret_key_2026"


# ==========================================
# STUDENT DATABASE
# Temporary Storage
# ==========================================

students = {}


# ==========================================
# LOGIN REQUIRED FUNCTION
# ==========================================

def user_logged_in():

    return "username" in session


# ==========================================
# HOME PAGE
# ==========================================

@app.route("/")
def home():

    if not user_logged_in():

        return redirect(url_for("login"))

    return render_template(
        "index.html",
        username=session["username"]
    )


# ==========================================
# REGISTER
# ==========================================

@app.route("/register", methods=["GET", "POST"])
def register():

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username == "" or password == "":

            message = "Please enter username and password."

        elif username in students:

            message = "Username already exists!"

        else:

            students[username] = password

            return redirect(url_for("login"))

    return render_template(
        "register.html",
        message=message
    )


# ==========================================
# LOGIN
# ==========================================

@app.route("/login", methods=["GET", "POST"])
def login():

    message = ""

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        if username in students and students[username] == password:

            session["username"] = username

            return redirect(url_for("home"))

        else:

            message = "Invalid username or password!"

    return render_template(
        "login.html",
        message=message
    )


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ==========================================
# STUDY PLAN GENERATOR
# ==========================================

@app.route("/study-plan", methods=["POST"])
def study_plan():

    if not user_logged_in():

        return redirect(url_for("login"))

    subject = request.form.get("subject", "").strip()
    days = request.form.get("days", "").strip()

    try:

        days = int(days)

        if days <= 0:

            return "Please enter a number greater than 0."

    except ValueError:

        return "Please enter a valid number."

    topics = [

        "Introduction and Basics",
        "Important Concepts",
        "Practical Examples",
        "Advanced Topics",
        "Revision and Practice"

    ]

    plan = []

    for day in range(1, days + 1):

        topic = topics[(day - 1) % len(topics)]

        plan.append({

            "day": day,
            "topic": topic

        })

    return render_template(

        "study_plan.html",
        username=session["username"],
        subject=subject,
        days=days,
        plan=plan

    )


# ==========================================
# QUIZ QUESTIONS
# ==========================================

questions = [

    {

        "question": "Why is learning regularly important?",

        "options": [

            "A. To improve knowledge",
            "B. To avoid studying",
            "C. To waste time",
            "D. Nothing"

        ],

        "answer": "A"

    },

    {

        "question": "What helps improve your knowledge?",

        "options": [

            "A. Avoiding practice",
            "B. Regular practice",
            "C. Sleeping all the time",
            "D. Ignoring lessons"

        ],

        "answer": "B"

    },

    {

        "question": "Which is important for effective learning?",

        "options": [

            "A. Practice",
            "B. Revision",
            "C. Understanding",
            "D. All of the Above"

        ],

        "answer": "D"

    }

]


# ==========================================
# QUIZ PAGE
# ==========================================

@app.route("/quiz")
def quiz():

    if not user_logged_in():

        return redirect(url_for("login"))

    return render_template(

        "quiz.html",
        username=session["username"],
        questions=questions

    )


# ==========================================
# SUBMIT QUIZ
# ==========================================

@app.route("/submit-quiz", methods=["POST"])
def submit_quiz():

    if not user_logged_in():

        return redirect(url_for("login"))

    score = 0

    for i, question in enumerate(questions):

        user_answer = request.form.get(f"question{i}")

        if user_answer == question["answer"]:

            score += 1

    return render_template(

        "result.html",
        username=session["username"],
        score=score,
        total=len(questions)

    )


# ==========================================
# COURSE MATERIAL
# ==========================================

course_material = {

    "python":
        "Python is a high-level programming language. It is easy to learn and widely used in Artificial Intelligence, Data Science and Web Development.",

    "java":
        "Java is an object-oriented programming language used for developing software and web applications.",

    "artificial intelligence":
        "Artificial Intelligence enables computers and machines to perform tasks that normally require human intelligence.",

    "machine learning":
        "Machine Learning is a branch of Artificial Intelligence where computers learn patterns from data.",

    "data science":
        "Data Science involves collecting, analyzing and interpreting data to find useful information."

}


# ==========================================
# COURSE Q&A
# ==========================================

@app.route("/ask-question", methods=["POST"])
def ask_question():

    if not user_logged_in():

        return redirect(url_for("login"))

    question = request.form.get(
        "question",
        ""
    ).lower().strip()

    answer = "Sorry! Information for this topic is not available."

    for topic, topic_answer in course_material.items():

        if topic in question:

            answer = topic_answer
            break

    return render_template(

        "answer.html",
        username=session["username"],
        question=question,
        answer=answer

    )


# ==========================================
# LEARNING ASSISTANT
# ==========================================

@app.route("/learning-assistant", methods=["POST"])
def learning_assistant():

    if not user_logged_in():

        return redirect(url_for("login"))

    topic = request.form.get("topic", "").strip()

    tips = [

        "Start with the basic concepts of the topic.",
        "Create short and simple notes while studying.",
        "Practice regularly with examples.",
        "Revise the topic every day.",
        "Test your knowledge by answering questions."

    ]

    return render_template(

        "learning.html",
        username=session["username"],
        topic=topic,
        tips=tips

    )


# ==========================================
# RUN APPLICATION
# ==========================================

if __name__ == "__main__":

    app.run(debug=True)