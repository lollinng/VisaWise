import numpy as np
import pandas as pd
import pickle
from flask import Flask, request, jsonify, render_template


app = Flask(__name__)
model = pickle.load(open('nueral_netwoks.pkl', 'rb'))

df = pd.read_csv('Top_10_companies_ratio_and_jobsname.csv')
Employer_acceptance = df['Name'][:50]
job_acceptance = df['Name'][50:100]
soc_acceptance = df['Name'][100:150]

job = df['JOBS'][:12]
States = df['STATES'][:14]

content = [Employer_acceptance, job_acceptance, soc_acceptance, job, States]


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/predict')
def indexp():
    return render_template('predict.html', content=content)


@app.route('/y_predict', methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''

    # getting the inputs
    Ft = [int(request.form['FULL_TIME_POSITION'])]
    Employer = request.form['Employer Name']
    Job_ratio = request.form['Job Name']
    code = request.form['Code Name']
    Year = int(request.form['YEAR'])
    wage = int(request.form['PREVAILING_WAGE'])
    job_domain = request.form['Job Type']
    state = request.form['state']

    # managing the inputed data

    print("ft -", Ft)
    print("Employer -", Employer)
    print("Job_ratio -", Job_ratio)
    print("Year -", Year)
    print("wage -", wage)
    print("job_domain -", job_domain)
    print("state -", state)

    year = [0, 0, 0, 0, 0]
    if Year == 2012:
        year[0] = 1
    elif Year == 2013:
        year[1] = 1
    elif Year == 2014:
        year[2] = 1
    elif Year == 2015:
        year[3] = 1
    elif Year == 2016:
        year[4] = 1
    print("year - ", year)

    # Wage
    # 'WAGE_CATEGORY_LOW',
    # 'WAGE_CATEGORY_MEDIUM', 'WAGE_CATEGORY_VERY HIGH',
    # 'WAGE_CATEGORY_VERY LOW'
    if wage <= 50000:
        Wage = [0, 0, 0, 1]
    elif wage > 50000 and wage <= 70000:
        Wage = [1, 0, 0, 0]
    elif wage > 70000 and wage <= 90000:
        Wage = [0, 1, 0, 0]
    elif wage > 90000 and wage <= 150000:
        Wage = [0, 0, 0, 0]
    elif wage >= 150000:
        Wage = [0, 0, 1, 0]
    print("\n Wage - ", Wage)

    def binaryConverter(acceptance, ans, no):
        print(ans)
        if no == 5:
            list = [0, 0, 0, 0, 0]
            j = 0
            for i in acceptance:
                print(i)  # i is string
                if(i == ans):
                    if(j < 10):
                        list[0] = 1
                    elif(j < 20):
                        list[1] = 1
                    elif(j < 30):
                        list[2] = 1
                    elif(j < 40):
                        list[3] = 1
                    elif(j < 50):
                        list[4] = 1
                    break
                j += 1
            print(list)
            return list

        elif no == 12:
            list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        else:
            print("al")
            list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        j = 0
        for i in acceptance:
            print(i)
            if(i == ans):
                print(j)
                list[j] = 1
                break
            j += 1
        print(list)
        return list

    ratio = binaryConverter(Employer_acceptance, Employer, 5) + binaryConverter(
        job_acceptance, Job_ratio, 5) + binaryConverter(soc_acceptance, code, 5)
    job_array = binaryConverter(job, job_domain, 12)
    state_array = binaryConverter(States, state, 15)

    # # Predicting using the model
    # prediction = model.predict([[Present_Price, Kms_Driven2, Owner, Year, Fuel_Type_Diesel,
    #                              Fuel_Type_Petrol, Seller_Type_Individual, Transmission_Mannual]])
    # output = round(prediction[0], 2)            # rounded to 2 decimal pts

    x = [Ft+ratio+year+Wage+job_array+state_array]
    print(x, len(x))
    prediction = model.predict(x)
    print(prediction)
    if prediction == 1:
        output = "Certified"
    else:
        output = "denied"
    return render_template('predict.html', prediction_text='   {}'.format(output), content=content)


if __name__ == "__main__":
    app.run(debug=True)
