#Azure Imports
import urllib.request
import json
import os
import ssl
#-----
from flask import Flask, render_template,request
app = Flask(__name__)

pregnancies = 0
glucose = 0
bloodPressure = 0
skinThickness = 0
insulin = 0
bmi = 0
diabetesPedigreeFunction = 0
age = 0


@app.route('/')
def hello_world():
    return render_template('home.html')

@app.route('/calculate', methods=['GET', 'POST'])
def calculate():
    if(request.method == 'POST'):
        pregnancies = request.form['Pregnancies']
        glucose = request.form['Glucose']
        bloodPressure = request.form['BloodPressure']
        skinThickness = request.form['SkinThickness']
        insulin = request.form['Insulin']
        bmi = request.form['BMI']
        diabetesPedigreeFunction = request.form['DiabetesPedigreeFunction']
        age = request.form['Age']

        def allowSelfSignedHttps(allowed):
            # bypass the server certificate verification on client side
            if allowed and not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None):
                ssl._create_default_https_context = ssl._create_unverified_context

        allowSelfSignedHttps(True)  # this line is needed if you use self-signed certificate in your scoring service.

        # Request data goes here
        # The example below assumes JSON formatting which may be updated
        # depending on the format your endpoint expects.
        # More information can be found here:
        # https://docs.microsoft.com/azure/machine-learning/how-to-deploy-advanced-entry-script
        data = {
            "Inputs": {
                "input1": [
                    {
                        "Pregnancies": pregnancies,
                        "Glucose": glucose,
                        "BloodPressure": bloodPressure,
                        "SkinThickness": skinThickness,
                        "Insulin": insulin,
                        "BMI": bmi,
                        "DiabetesPedigreeFunction": diabetesPedigreeFunction,
                        "Age": age
                    }
                ]
            },
            "GlobalParameters": {}
        }

        body = str.encode(json.dumps(data))

        url = 'http://e835bc4c-b0ba-4efc-b971-b39395680f65.eastus.azurecontainer.io/score'
        # Replace this with the primary/secondary key or AMLToken for the endpoint
        api_key = 'vBU1im4v0Vp5haE8WpoTryr8qFrSYicX'
        if not api_key:
            raise Exception("A key should be provided to invoke the endpoint")

        headers = {'Content-Type': 'application/json', 'Authorization': ('Bearer ' + api_key)}

        req = urllib.request.Request(url, body, headers)

        try:
            response = urllib.request.urlopen(req)

            result = response.read()
            #print(result)
            return result
        except urllib.error.HTTPError as error:
            print("The request failed with status code: " + str(error.code))

            # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
            print(error.info())
            print(error.read().decode("utf8", 'ignore'))
    else:
        return 'ERROR'


if __name__ == '__main__':
    app.run()