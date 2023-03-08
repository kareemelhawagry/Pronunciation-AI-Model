from flask import Flask,render_template, request, jsonify
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/pronunciation', methods=['POST'])
def check_pronunciation():
    # Get the recorded audio data from the HTML page
    audio_data = request.files['audio'].read()

    # Save the audio data to a file
    with open('audio.wav', 'wb') as f:
        f.write(audio_data)

    # Use the Python code we wrote earlier to analyze the audio data
    output = subprocess.check_output(['python', 'pronunciation_model.py', 'audio.wav'])

    # Convert the output to a JSON object
    result = {'message': output.decode('utf-8').strip()}

    # Return the result as a JSON response
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
