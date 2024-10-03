import os
import openai
from flask import Flask, request, render_template, session, redirect, url_for
from flask_session import Session
from werkzeug.utils import secure_filename
from resume_parser import resumeparse
from elevenlabs.client import ElevenLabs
from flask_socketio import SocketIO, emit
import eventlet
import requests
import base64
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

eventlet.monkey_patch()


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key


app.config['SESSION_TYPE'] = 'filesystem'
Session(app)


socketio = SocketIO(app, manage_session=False)


UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

openai.api_key = os.getenv('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')  # Use environment variables for security
ELEVENLABS_API_KEY = os.getenv('sk_05ec65e9acce6cb054e88ac96031d4664a91965b28032e4b')


client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

# Allowed extensions for resume upload
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'doc'}

nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        return "No file part"
    file = request.files['resume']
    if file.filename == '':
        return "No selected file"
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        data = resumeparse.read_file(filepath)
        session['candidate_data'] = data
        os.remove(filepath)  # Clean up after parsing
        return redirect(url_for('interview'))
    else:
        return "Invalid file type"


@app.route('/interview')
def interview():
    data = session.get('candidate_data', None)
    if not data:
        return redirect(url_for('index'))
    questions = generate_questions(data)
    session['questions'] = questions
    session['current_question_index'] = 0
    session['responses'] = []
    session['evaluations'] = []
    session['sentiments'] = []
    return render_template('interview.html')


def generate_questions(data):
    name = data.get('name', 'Candidate')
    skills = ', '.join(data.get('skills', []))
    experience = data.get('total_experience', 0)

    prompts = []

    intro_prompt = f"Create a friendly introductory question for an interview with {name}."
    prompts.append(intro_prompt)

    tech_prompt = f"Based on these technical skills: {skills}, generate a technical interview question."
    prompts.append(tech_prompt)

    exp_prompt = f"The candidate has {experience} years of experience. Generate a question that explores their past roles."
    prompts.append(exp_prompt)

    eq_prompt = "Generate an emotional intelligence question suitable for a job interview."
    prompts.append(eq_prompt)

    situational_prompt = "Generate a situational question to assess problem-solving abilities in a professional setting."
    prompts.append(situational_prompt)

    questions = []
    for prompt in prompts:
        response = openai.ChatCompletion.create(
            model='gpt-4',
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates interview questions."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100,
            n=1,
            stop=None,
            temperature=0.7,
        )
        question = response.choices[0].message['content'].strip()
        questions.append(question)

    return questions


@socketio.on('get_audio')
def handle_get_audio(data):
    question_index = session.get('current_question_index', 0)
    questions = session.get('questions', [])
    if question_index < len(questions):
        text = questions[question_index]
        audio_base64 = text_to_speech(text)
        emit('play_audio', {'audio': audio_base64})
    else:
        emit('interview_complete')

def text_to_speech(text):
    audio = client.generate(
        text=text,
        voice="Rachel",  
        model="eleven_monolingual_v1"
    )
    audio_bytes = audio  # 'audio' is already in bytes
    audio_base64 = base64.b64encode(audio_bytes).decode('utf-8')
    return audio_base64


@socketio.on('audio_data')
def handle_audio_data(data):
    audio_base64 = data.get('audio')
    audio_data = base64.b64decode(audio_base64)

    # Transcribe audio data
    transcription = transcribe_audio(audio_data)
    session['responses'].append(transcription)

    # Evaluate the response
    question_index = session.get('current_question_index', 0)
    questions = session.get('questions', [])
    if question_index < len(questions):
        question = questions[question_index]
        evaluation, sentiment = evaluate_response(question, transcription)
        session['evaluations'].append(evaluation)
        session['sentiments'].append(sentiment)
        session['current_question_index'] = question_index + 1
        emit('evaluation_complete')
    else:
        emit('interview_complete')

def transcribe_audio(audio_data):
    # Placeholder transcription function
    transcription = "Transcribed text of the candidate's response."
    return transcription


def evaluate_response(question, response):
    criteria = [
        'Communication skills',
        'Technical relevance',
        'Situational awareness',
        'Experience relevance'
    ]

    # Analyze sentiment using NLTK's VADER
    sentiment_scores = sia.polarity_scores(response)
    # Store sentiment scores on the backend
    sentiment = sentiment_scores  # This will be stored in session

    # Prepare the evaluation prompt
    prompt = f"""
    Evaluate the following response based on {', '.join(criteria)}:

    Question: {question}
    Response: {response}

    Provide a score out of 10 for each criterion and a brief justification.
    """

    response = openai.ChatCompletion.create(
        model='gpt-4o-mini-2024-07-18',
        messages=[
            {"role": "system", "content": "You are an expert interviewer evaluating candidate responses."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=350,
        n=1,
        stop=None,
        temperature=0.7,
    )
    evaluation = response.choices[0].message['content'].strip()
    return evaluation, sentiment

# Route to display results (for recruiters)
@app.route('/results')
def results():
    evaluations = session.get('evaluations', [])
    sentiments = session.get('sentiments', [])
    responses = session.get('responses', [])
    questions = session.get('questions', [])
    result_data = zip(questions, responses, evaluations, sentiments)
    return render_template('results.html', result_data=result_data)

if __name__ == '__main__':
    socketio.run(app, debug=True)
