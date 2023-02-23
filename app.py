import boto3
import botocore
import requests
from flask import Flask, request, Response

app = Flask(__name__)

session = boto3.Session(
    aws_access_key_id="ASIAQAVUNXM4OMXVUARM",
    aws_secret_access_key="YoV/o1TqMKA73Pjn4kaHXrQsN2dVAEdE+ebRSH7n",
    aws_session_token="FwoGZXIvYXdzEGwaDL+Q9fsPOPxwiwbbMiK/AYIBGtmSmxaGTUHs+EduhzNoZVR61IXN1zWxnUeFohsECL4hmaaZC2i7Tp6GWhc3xo7JlJkiqbZPn37fraXRx910VYrtej5+KARwf8YWYz4gG9Q9/YvmcaxiVjj6MRaUg46TMNY4i6HBfhZ0zcl0bKtzkI/WtPM/fb3W2FDs1kDsfqQnruiuziqPpCrtm3X1o9Qk32Ir/2Y0y0HTOyk6Umy9wPrQeL9zoSRPs/UmF8vrebq34OH+fZx9sqVo5vupKPvd3p8GMi5ezI34NkGEAxYJQRxIiiBplkGxDyAFDGVg3K81eecktJ/HMo1P+fdSr3cmO21G",
    region_name='us-east-1'
)
s3 = session.resource('s3')

@app.route("/")
def start():
    try:
        result = requests.post('http://52.91.127.198:8080/start', json={"banner": "B00899528", "ip": "100.26.162.234"})
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
        
if __name__ == '__main__':
  app.run(host='0.0.0.0')

