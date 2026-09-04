from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "<h1 style='background:black;color:white;padding:50px;text-align:center'>YA JALO - Foto a Texto</h1>"

@app.route('/api')
def api_test():
    return "API OK"
