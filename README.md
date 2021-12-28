# pcsg-web-server

Here lies my private repository.

## Purpose
The purpose of this server is to provide a location where the 2 PCSG Mod Bots, can access the same database without losing / duplicating data when switching between the two.

## About the Server End
Everything is for the sole purpose of storing data in an sqlite database. 

# API Documentation

## About
This is the documentation for the API which will allow the bots to interact with the server which in turn will manipulate the database.
All Requests and Responses will contain JSON with which will be used to communicate.

## Errors
If any errors occur when interacting with the server, the following response will be returned.

```json
{
    "ERROR": "The Error that Occurred",
    "URL": "The URL that was hit, that resulted in the error"
}
```
## Uploading a file
