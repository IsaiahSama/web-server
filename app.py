try:
    from flask import Flask, request, send_from_directory, render_template, flash, redirect, url_for, jsonify, session
    from werkzeug.utils import secure_filename
    from os.path import exists
    from os import mkdir
    import sys
except ImportError as err:
    print("You are missing some required packages. Run `pip install -r requirements.txt` in this current directory to install them.", err )
    input("Press enter to close")
    raise SystemExit

v = sys.version_info
if not (v.major == 3 and v.minor >= 10):
    print("This program requires Python version 3.10 or higher to function. Please update your version of python and try again.")
    input("Press enter to exit")
    raise SystemExit

UPLOAD_FOLDER = "uploads"
UPLOAD_FOLDER += '/'

if not exists(UPLOAD_FOLDER):
    mkdir(UPLOAD_FOLDER)
# ALLOWED_EXTENSIONS = ['sqlite3', 'txt', 'py']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "default_secret_key"

# Main

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/ping/", methods=["POST"])
def ping():
    return_dict = {
        "SERVER": "Something goes here",
        "TITLE": "Something else goes here",
        "RESPONSE": "PING PING!!!"
    }
    return jsonify(return_dict)

@app.route("/sayhello/", methods=["POST"])
def sayhello():
    data = request.json
    try:
        text = data["TEXT"]
    except KeyError:
        return {"RESPONSE": "NO"}
    return {"RESPONSE": text}

@app.route("/setname/", methods=["POST", "GET"])
def setname():
    if request.method == 'GET':
        return """
        <h1> Who are you? </h1>
        <p> Well, since you insist... My name is Isaiah. Tell me yours! </p>

        <form method='post'>
            <p><input type=text name=newname></p>
            <p><input type=submit value=Yes></p>
        </form>
        """
    
    if not request.form or 'newname' not in request.form:
        flash("Your seem to have not wanted to tell me your name. That's all right.", "warning")
        return redirect(url_for("index"))

    session['name'] = request.form['newname']
    flash(f"Nice to meet you {session['name']}", "success")
    return redirect(url_for('index'))

@app.route("/forgetme/", methods=["GET"])
def forgetme():
    if 'name' not in session:
        flash("I never knew you in the first place...", "danger")
    else:
        session.pop('name', None)
        flash("F-Fine... Who are you again?", "error")
    
    return redirect(url_for("index"))

# Using the API

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
        return {"ERROR": "Invalid file provided. Filenames must not contain spaces", "URL": "/upload/"}

@app.route("/api/download/<name>", methods=['POST'])
def download(name:str):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], name)
    except Exception as err: 
        return {"ERROR": str(err), "URL": "/download/"+name}

# Extra
def allowed_file(filename:str):
    """Determines whether an uploaded file is allowed or not
    
    Args:
        filename (str): The name of the file to check
        
    Returns:
        bool"""

    # return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS
    return ' ' not in filename


# Error Handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404page.html")
