import flask
from flask import request, render_template
from flask_cors import CORS
import joblib
import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "dbmlwXit_00dVgPiTfK0wIFqoa5WntN5P62VAiloe-81"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
    API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app= flask.Flask(__name__,
    static_url_path='',
    static_folder='static',
    template_folder='templates'
    )
CORS(app)

@app.route('/',methods=['GET', 'POST'])
def getHomePage():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    # X = df[["GRE Score","TOEFL Score","University Rating","SOP","LOR ","CGPA"
    GRE_score=float(request.form['gre'])
    TOEFL_score=float(request.form['toefl_score'])
    University_rating=float(request.form['university'])
    sop =float(request.form['sop'])
    lor =float(request.form['lor'])
    cgpa =float(request.form['cgpa'])
    X=[[GRE_score,TOEFL_score,University_rating,sop,cgpa]]
    print(X)
    # model=joblib.load('university.pkl')
    # result=model.predict(X)[0]
    payload_scoring = {"input_data": [{"fields": [  "GRE Score",
                                "TOEFL Score",
                                "University Rating",
                                "SOP",
                                "LOR ",
                                "CGPA"
                            ], 
                    "values": [
                        [
                            GRE_score,
                            TOEFL_score,
                            University_rating,
                            sop,
                            lor,
                            cgpa
                        ]
                    ]
                    }]
                }
    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/bccfd93c-32ce-4045-b3db-eb65586ecfe0/predictions?version=2022-11-08', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    result=response_scoring.json()
    print(result['predictions'][0]['values'][0][0])
    result=result['predictions'][0]['values'][0][0]
    result=int(result*100)
    print(result)
    if result>50:
        return render_template('chance.html',result=result)
    else:
        return render_template('nochance.html',result=result)
if __name__ == '__main__':
    app.run(debug=True)