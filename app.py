from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import Question, Survey, satisfaction_survey, personality_quiz

app = Flask(__name__)

app.config['SECRET_KEY'] = "MissMillieIsGood"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# not sure how to stop the user from visiting a question out of order
# I think I need to see how session works more

# USER_RESPONSES = "responses"
responses = []

@app.route('/old-home-page')
def old_home_page():
    flash("That page has moved!")
    return redirect('/')

@app.route('/')
def home_page():
    survey_title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template("begin.html", survey_title=survey_title, instructions=instructions)

#i want to handle the id numbers by how many questions there are.
#1-4
# use length of questions
# len(satisfaction_survey.questions)

@app.route('/questions/<int:id>')
# why do I have to write it out like int:id?
def question(id):
    curr_id = id - 1
    if id > len(satisfaction_survey.questions):
        return redirect('/not-found')
    else:
        return render_template('questions.html', survey_q1=satisfaction_survey.questions[(curr_id)].question, choices=satisfaction_survey.questions[(curr_id)].choices)

@app.route('/questions/0', methods=["POST"])
def initialize():
    # session[USER_RESPONSES] = []
    return redirect('/questions/1')

@app.route('/answer', methods=["POST"])
def submit_answer():
    choice = request.form['answer']
    # responses = session[USER_RESPONSES]
    responses.append(choice)
    # session[USER_RESPONSES] = responses
    if len(responses) == len(satisfaction_survey.questions):
        return redirect('/thank-you')
    else:
        return redirect(f'/questions/{len(responses) + 1}')

@app.route('/thank-you')
def thank_you():
    return render_template('completion.html')

@app.route('/not-found')
def not_found():
    return "Question Not Found"