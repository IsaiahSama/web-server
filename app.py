import sys
v = sys.version_info
if not (v.major == 3 and v.minor >= 10):
    print("This program requires Python version 3.10 or higher to function. Please update your version of python and try again.")
    input("Press enter to exit")
    raise SystemExit

try:
    import db
    from flask import Flask, request, send_from_directory, render_template, flash, redirect, url_for, jsonify, session
    from werkzeug.utils import secure_filename
    from os.path import exists, join
    from os import mkdir, remove
    from constants import UPLOAD_FOLDER
except ImportError as err:
    print("You are missing some required packages. Run `pip install -r requirements.txt` in this current directory to install them.", err )
    input("Press enter to close")
    raise SystemExit


UPLOAD_FOLDER += '/'

if not exists(UPLOAD_FOLDER):
    mkdir(UPLOAD_FOLDER)
# ALLOWED_EXTENSIONS = ['sqlite3', 'txt', 'py']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "default_secret_key"

mydb = db.Database()

# Main

@app.route("/")
def index():
    mydb.check_entries()
    files = mydb.get_entries()
    return render_template('index.html', files=files)

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
        flash("F-Fine... Who are you again?", "danger")
    
    return redirect(url_for("index"))

# The actual relevant part

@app.route('/upload/', methods=['GET', "POST"])
@app.route('/upload/<overwrite>/', methods=["POST"])
def upload_file(overwrite=False):
    if request.method == 'GET':
        return render_template("upload.html", overwrite=overwrite)
    
    if 'file' not in request.files:
        flash("No file was detected.", "warning")
        return redirect(url_for("upload_file"))
    
    file = request.files['file']

    if not file.filename:
        flash("No file was selected", "danger")
        return redirect(url_for("upload_file"))

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # Here we make sure the file passes all other checks
        try:
            verify_file(filename)
        except FileExistsError:
            if not overwrite:
                flash("The file already exists. If you would like to overwrite it, press the button below", "danger")
                return render_template("upload.html", overwrite=True)
            else:
                flash("Overwriting existing file.", "warning")
                remove(join(app.config["UPLOAD_FOLDER"], filename))
        file.save(join(app.config['UPLOAD_FOLDER'], filename))
        mydb.add_entry(filename)
        flash("Uploaded successfully.", "success")
        return redirect(url_for("upload_file"))
    else:
        flash("Filename must not be larger than 254 characters. Apologies.", "danger")
        return redirect(url_for("upload_file"))

@app.route('/view/<filename>')
def view_file(filename):
    if not exists(join(app.config['UPLOAD_FOLDER'], filename)):
        flash("No such file exists on the server.", "danger")
        return redirect(url_for("index"))
    if not mydb.get_entry(filename):
        mydb.add_entry(filename)
    mydb.update_entry(filename, False)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/download/<filename>")
def download_file(filename):
    if not exists(join(app.config['UPLOAD_FOLDER'], filename)):
        flash("No such file exists on the server.", "danger")
        return redirect(url_for("index"))
    if not mydb.get_entry(filename):
        mydb.add_entry(filename)
    mydb.update_entry(filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route("/delete/<filename>")
def delete_file(filename):
    filepath = join(app.config["UPLOAD_FOLDER"], filename)
    if exists(filepath):
        remove(filepath)
        flash("File removed successfully", "success")
    else:
        flash("No such file exists.", "warning")
    if mydb.get_entry(filename):
        mydb.update_entry(filename, False)
        # flash("Removed entry from database.", "success")
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
        return {"ERROR": "Invalid file provided. Filenames must not be longer than 254 characters", "URL": "/upload/"}

@app.route("/api/download/<name>", methods=['POST'])
def download(name:str):
    try:
        return send_from_directory(app.config['UPLOAD_FOLDER'], name)
    except Exception as err: 
        return {"ERROR": str(err), "URL": "/download/"+name}

# Extra
def allowed_file(filename:str):
    """Determines whether an uploaded file has a valid name.
    
    Args:
        filename (str): The name of the file to check
        
    Returns:
        bool"""

    # return '.' in filename and filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS
    return len(filename) < 255

def verify_file(filename:str):
    """Determines whether a file is valid or not
    
    Args:
        filename (str): The name of the file to check.
        
    Raises:
        FileExistsError"""

    full_path = join(app.config["UPLOAD_FOLDER"], filename)
    if exists(full_path):
        raise FileExistsError
    


# Error Handlers
@app.errorhandler(404)
def page_not_found(error):
    return render_template("404page.html")

@app.errorhandler(500)
def application_error(error):
    return render_template("500page.html", error=error)
