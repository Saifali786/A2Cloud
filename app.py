import boto3
import botocore
import requests
from flask import Flask, request, Response

app = Flask(__name__)

session = boto3.Session(
    aws_access_key_id="ASIAQAVUNXM4POQMLJZX",
    aws_secret_access_key="seki7sGWoqSS0tw3/LIdVoHP+DrXJBRqsIhUYGmf",
    aws_session_token="FwoGZXIvYXdzEFkaDHECv3/Pc4wE0Ht+8CK/AQzzyzCu9Pye7N3xQINBzRx7QOb6rHUNlsJGiX1A31QuL4cHZj0mtZ58aDdVkHwbDzQIFc+Yk+X2LcHa2ZPY5d94RSd5f5w4F89ldRJjbcsPRTLffXjCWdPYnkYddH4aEolVMdyISD61jeOzmSsQATDCwv0iAwpQ+AQclQzt5VXj9Qys1EMdUNHAlkKIBwGyn258OxsvAnVIETznZ+RnQPSCeeZPuaolmAT2S5yXzcPUwR0KFOqJEShgzU6pvzbfKJfD2p8GMi4djUEHPy+HTjSVORzbTZFWhJvtIj+tdsEZlJIyPRKi0LG9kYMQdZrQB2R7b3LT",
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

    if __name__ == "__main__":
        app.run(host="0.0.0.0",port=5000)   
