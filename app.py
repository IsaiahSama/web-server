from flask import Flask, request
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'db/'
ALLOWED_EXTENSIONS = ['sqlite3', 'txt']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello_world():
    return "<p>Hello, world</p>"

@app.route("/ping/", methods=["POST"])
def ping():
    return_dict = {
        "SERVER": "Something goes here",
        "TITLE": "Something else goes here",
        "RESPONSE": "PING PING!!!"
    }
    return return_dict

@app.route("/sayhello/", methods=["POST"])
def sayhello():
    data = request.json
    try:
        text = data["TEXT"]
    except KeyError:
        return {"RESPONSE": "NO"}
    return {"RESPONSE": text}

def allowed_file(filename:str):
    """Determines whether an uploaded file is allowed or not
    
    Args:
        filename (str): The name of the file to check
        
    Returns:
        bool"""

    return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS


@app.route("/takefile/", methods=["POST"])
def takefile():
    if 'file' not in request.files:
        return {"ERROR": "No file was received"}
    
    file = request.files['file']
    if file.filename == '':
        return {"ERROR": "No given file"}

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        with open(f"{app.config['UPLOAD_FOLDER']}{filename}", "wb") as fp:
            file.save(fp)

        return {"RESPONSE": "File was successfully uploaded"}
    else:
        return {"ERROR": "Invalid file provided"}