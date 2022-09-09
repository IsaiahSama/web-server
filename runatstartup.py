"""File which can be run to startup the server automatically.

On Windows:
    This file should be added to the windows application Task Scheduler, with the Trigger set to On Log on, and the action being this file.
    This will allow the server to be started whenever you log on to your device.
On other Operating Systems:
    I am unsure as to how other operating systems may handle task management"""
import os

def main():
    base_path = os.path.dirname(os.path.abspath(__file__)) + '/'

    os.chdir(base_path)
    # The location of the interpreter. Change to suit your needs
    interpreter_location = base_path + ".venv/Scripts/python.exe"

    if not os.path.exists(interpreter_location):
        print("Specified interpreter location could not be found. Using default Interpreter")
        interpreter_location = "py"
    
    os.system(interpreter_location + " " + base_path + "wsgi.py")

try:
    main()
except Exception as err:
    print("An error has occurred.", err)
    input("Press Enter to close")