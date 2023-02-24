import boto3
import botocore
import requests
from flask import Flask, request, Response

app = Flask(__name__)

session = boto3.Session(
    aws_access_key_id="ASIAQAVUNXM4HALIXVFV",
    aws_secret_access_key="XBJCTu7WQPeTS217hAKU2SS74YBYZAQof5L2Dpo5",
    aws_session_token="FwoGZXIvYXdzEHAaDJr89kDxFwhofJq/xSK/AUiHVYoqHcwFKm9nA/qVKIiXUJfuFy4CGPWYbmcejRB5pl4fAUeKqIct1Lv07b0NfYRSz8hfLtIG3qC/mwfENOddAlEyOv2k4E3k1moff5CJxRiJkxkrKGSPagEtHYlvN4vWmk0jqfGUa4Vq4mzcV+5O4eqR7HmcWP+t75wSRe4cxzn/yNs4fBztJtNc79VY350FksYweJ5FKMBaihMgauAN4Ix04AkSDEhfJ2YNh0LG9WyKrkJFtZmiW8LUPuNAKJDN358GMi7WfRko/WJIGBR/bGiSM9ivfVt9ouPbYeTnz9oCz2xegp2ygZgd7jdqKyhJM/Na",
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
      

