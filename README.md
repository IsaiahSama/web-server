# WebServer

This is the repository for my personal webserver that I localhost on my laptop.
Due to it being local hosted, it's also available for anyone to download and run it themselves.

Given that, please do not try to host this on any hosting platforms such as Heroku, as the code is designed to only work locally.

## Purpose
I often find myself in the situation where I need to upload some files quickly to my secondary laptop, but would always run into some issue, whether it be my inability to find my flashdrive, or file being too large for bluetooth, or even the file being on my phone.

So I decided to make my own server to (hopefully) simplify the issue. 

# Usage
When you run the `wsgi.py` file, once you have all of the required libraries installed, you will see a bit of information displayed to you, including the URL which the server is hosted on. Output may look like:

```
Server Flask app 'app' (lazy loading)
Environment: production
Warning: This is a development server. Do not use it in a production deployment.
---
Running on http://ipaddress:port/ (Press CTRL+C to quit)
```

The URL that the server is hosted on, is the one link that says: http:// etc. Visiting that link on any device connected to the same internet as the server, will allow you to interact with the server, allowing you to Upload, Download and view files as you desire.


# API Documentation

## About
This is the documentation for the API which some of my bots use to interact with the server to backup their databases.

If you wish to interact with the server via a script instead of visiting the website, then there's an API for you 😎.

The URL will be the same one shown when you run the `wsgi.py` file.

All Responses from the server will have JSON.

## Errors
If any errors occur when interacting with the server, the following response will be returned.

```json
{
    "ERROR": "The Error that Occurred",
    "URL": "The URL that was hit, that resulted in the error"
}
```
## Uploading a file
The database can be uploaded using the following URL: `/upload/`

Expected to be in the request must be a files kwarg, defined in the following way

```json
{
    "file1": "File buffer",
    "file2": "Second File Buffer"
}
```

Example of uploading a file to the server using Python.

```py
import requests
files = {}
fp = open("somefile.txt", "rb")
fp2 = open("somefile.sqlite3", "rb")
files['file1'] = fp
files['file2'] = fp2

response = requests.post(URL, files=files)
try:
    response.raise_for_status()
except Exception as err:
    print(err)
    input()
    raise SystemExit

data = response.json()

if 'ERROR' in data:
    print(data['ERROR'])
elif 'RESPONSE' in data:
    print(data['RESPONSE'])
else:
    print("Unknown error has ocurred with the server. Error:", response)

exit()
```

## Downloading a file
The database can be downloaded by using the following URL: `/download/filename.extension`

Where `filename` is the name of the file to be accessed.

Will return text, which will contain the contents of the file

Example of downloading a file using Python.

```py
import requests

response = post(URL + name_of_file_you_want)

data = response.json()

if 'ERROR' in data:
    print(data["ERROR"])

with open("name_you_want_to_call_the_file_when_you_download_it", "wb") as fp:
    fp.write(response.content)
    print("Completed")
```

Downloaded file will be written to the specified filepath.

## Successful Response

A file being successfully uploaded will return the following response.

```json
{
    "RESPONSE": "Success Message"
}

```