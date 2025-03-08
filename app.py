from flask import Flask, render_template, request, send_from_directory, jsonify
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import os
import uuid
import wave
import json
from modules import ocr, pron

app = Flask(__name__)

@app.route('/')
def index():
    return """
    <html>
        <head>
            <style>
                body {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    margin: 0;
                    background-color: #f4f7f6;
                }

                h1 {
                    font-size: 36px;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <h1>轟はじめ世界第一可愛</h1>
        </body>
    </html>
    """

@app.route('/exam')
def exam():
    return render_template('home.html')

@app.route('/module/examA/')
def examA():
    return render_template('examA.html')

@app.route('/module/examB/')
def examB():
    return render_template('examB.html')

@app.route('/module/examA/process', methods=['POST'])
def pronunciationEval():
    file = request.files['audio']
    word = request.form.get('sentence')
    unique_filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    inputFileName = unique_filename
    file.save(inputFileName)
    audio = AudioSegment.from_wav(inputFileName)
    audio = audio.set_frame_rate(16000)
    audio.export(inputFileName, format="wav")

    print (f"Saved file to {inputFileName}")
    result = pron.get_pronunciation(inputFileName, word)
    result_dict = json.loads(result)
    #result = "Got Result of Pron!"
    response = jsonify(result_dict)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

@app.route('/module/examB/process', methods=['POST'])
def photoEval():
    result = "Got Result of Photo!"
    return jsonify({"message": result})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)