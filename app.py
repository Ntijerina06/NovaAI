from flask import Flask, render_template, request, jsonify
import json

from main import NovaAi

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/nova')
def nova():
    return render_template('nova.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/process_voice', methods=['POST'])
def process_voice():
    nova = NovaAi()
    user_text = request.json.get("user_text")
    response = nova.process_voice(user_text)
    return jsonify({"response": response})


if __name__ == '__main__':
    app.run(debug=True)
