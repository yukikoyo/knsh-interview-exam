from flask import Flask, render_template, request, send_from_directory, jsonify, url_for
from werkzeug.utils import secure_filename
from pydub import AudioSegment
import os
import uuid
import json
from modules import ocr, pron

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

OUTPUT_FOLDER = "outputs"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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
    inputFileName = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(inputFileName)
    
    audio = AudioSegment.from_wav(inputFileName)
    audio = audio.set_frame_rate(16000)
    audio.export(inputFileName, format="wav")

    print(f"Saved file to {inputFileName}")
    result = pron.get_pronunciation(inputFileName, word)
    result_dict = json.loads(result)
    response = jsonify(result_dict)
    response.headers["Content-Type"] = "application/json; charset=utf-8"
    return response

@app.route('/module/examB/process', methods=['POST'])
def photoEval():
    file = request.files['file']
    unique_filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
    inputFileName = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(inputFileName)

    results = ocr.ocr_analysis(inputFileName)
    if results is None:
        return jsonify({"error": "No text detected."})
    url_results_pair = {}
    url_results_pair["imgUrl"] = url_for('getImg', filename=results[1])
    url_results_pair["results"] = results[0]
    return jsonify(url_results_pair)

@app.route('/outputs/<filename>')
def getImg(filename):
    return send_from_directory(OUTPUT_FOLDER, filename, as_attachment=False)
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)