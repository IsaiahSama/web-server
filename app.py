try:
    from flask import Flask, request, send_from_directory, render_template
    from werkzeug.utils import secure_filename
except ImportError as err:
    print("You are missing some required packages. Run `pip install -r requirements.txt` in this current directory to install them.", err )
    input("Press enter to close")

UPLOAD_FOLDER = 'uploads/'
# ALLOWED_EXTENSIONS = ['sqlite3', 'txt', 'py']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def hello_world():
    return render_template('index.html')

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

    # return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS
    return True

@app.route("/api/upload/", methods=["POST"])
def upload():
    if 'file' not in request.files:
        return {"ERROR": "No file was received"}
    
    file = request.files['file']
    if file.filename == '':
        return {"ERROR": "No given file"}

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        try:
            with open(f"{app.config['UPLOAD_FOLDER']}{filename}", "wb") as fp:
                file.save(fp)
        except Exception as err:
            return {"ERROR": str(err)}

        return {"RESPONSE": "File was successfully uploaded"}
    else:
        return {"ERROR": "Invalid file provided", "URL": "/upload/"}

@app.route("/api/download/<name>", methods=['POST'])
def download(name:str):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], name)
    except Exception as err: 
        return {"ERROR": str(err), "URL": "/download/"+name}
