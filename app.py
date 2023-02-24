import boto3
import botocore
import requests
from flask import Flask, request, Response

app = Flask(__name__)

session = boto3.Session(
    aws_access_key_id="ASIAQAVUNXM4HO4LGIPF",
    aws_secret_access_key="LSsiBvStP6yamuVk3yck9gb7Fh5DoFwoCQ1ZCd1u",
    aws_session_token="FwoGZXIvYXdzEHMaDDLmXhud65IlLK4wXSK/ASWOJ5eLy5a6Kvk/ca9HgFE1ZhLAIx1Nc8jIbdbtlrIfHcZM+Cm/Vamc1uFfZ7PA7J3TnmT+Nt30XB32aFk+yQBSbNx+KKZ1Q/TN5iEBDtQqJiInvH3kGFEk3cTHCxXtNOaatTOrecit/4gzOKzQaVMfTHEVNamfaKAGDUW73nlS2Buho6YtLwOFlz5ugeMjC6WZAKZHFZL1TPnOVQcgSKFDRrulIWqyqf6SNJS175n2DgeIA1noxEs/TKDaZ17lKN6u4J8GMi6r8i5mPKo7DQJ4b0T/gZ3qIJJ2wk71V3gXiAAJ3S0RSv7EuhW4pIC5yfmRKpFv",
    region_name='us-east-1'
)
s3 = session.resource('s3')

@app.route("/")
def start():
    try:
        result = requests.post('http://52.91.127.198:8080/start', json={"banner": "B00899528", "ip": "100.25.26.205"})
        return "<pre>%s</pre>" % result.text
    except Exception as e:
        print("Exception")
        print(str(e))
        return Response(status=400)


@app.route("/storedata", methods=["POST"])
def writeToS3():
    try:
        result = request.json
        obj = s3.Object("computestorage", "file.txt")
        obj.put(Body=result["data"])
        print("Data written to S3 file")
        output = {"s3uri": "https://computestorage.s3.amazonaws.com/file.txt"}
        return output
    except Exception as e:
        print("Exception")
        print(str(e))
        return Response(status=400)


@app.route("/appenddata", methods=["POST"])
def append():
    try:
        result = request.json
        obj = s3.Object("computestorage", "file.txt")
        body = obj.get()['Body'].read()
        content = body.decode('utf-8') + result["data"]
        obj.put(Body=content)
        print("Data Appended to S3 file")
        return Response(status=200)
    except Exception as e:
        print("Exception")
        print(str(e))
        return Response(status=400)


@app.route("/deletefile", methods=["POST"])
def deleteS3File():
    try:
        s3.Object("computestorage", "file.txt").load()    
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            print("Object Doesn't exists")
            return Response(status=404)
        else:
            print("Error occurred while fetching a file from S3. Try Again.")
    else:
        print("Object Exists")
        obj = s3.Object("computestorage", "file.txt")
        obj.delete()
        return Response(status=200)  

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)        

