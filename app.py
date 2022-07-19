from surveys import Question, Survey, satisfaction_survey, personality_quiz, surveys
from flask import Flask, request, render_template, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route("/")
def home():
    """Home Directory where we will begin the survey"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("home.html", instructions=instructions, title=title)


@app.route("/begin", methods=["POST"])
def start_survey():
    """Clear the session of responses."""

    session["responses"] = []
    session['_flashes'] = []

    return redirect("/question/0")


@app.route("/question/<idx>")
def display_questions(idx):
    """Question Handle function, we will check if the question is being accessed correctly
    If accessed incorrectly, the user will be redirected to the correct route
    Otherwise, the question to be answered will be shown on screen"""
    idx = int(idx)
    responses = session.get("responses")
    if responses is None:
        return redirect("/")
    elif (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    elif(len(responses) != idx):
        flash(
            f"Invalid question, you must first answer the questions in order")
        return redirect(f"/question/{len(responses)}")

    question = satisfaction_survey.questions[idx].question
    choices = satisfaction_survey.questions[idx].choices
    return render_template("question.html", question=question, choices=choices)


@app.route("/answer", methods=["POST"])
def handle_answers():
    """The answer will be added to the session so we can store the data
    If all questions have been answered, the user will be moved to the  complete page"""
    answer = request.form['answer']
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses
    if (len(responses) == len(satisfaction_survey.questions)):
        return redirect("/complete")
    else:
        return redirect(f"/question/{len(responses)}")


@app.route("/complete")
def display_complete():
    """Display Thank you message to the user for answering the survey"""
    return render_template("complete.html")
