import numpy as np
from flask import Flask, request, jsonify, render_template
from joblib import load
app = Flask(__name__)
model = load('vi.save')
trans = load('vivtransform')
trans2 = load('vivtransform2')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/ml')
def indexp():
    return render_template('ml.html')


@app.route('/y_predict', methods=['POST'])
def y_predict():
    '''
    For rendering results on HTML GUI
    '''
    x_test = [[x for x in request.form.values()]]
    print(x_test)
    test = trans.transform(x_test)
    test = test[:, 1:]
    test = trans2.transform(test)
    test = test[:, 1:]
    print(test)
    prediction = model.predict(test)
    print(prediction)
    if prediction == 0:
        output = "Certified"
    else:
        output = "denied"
    return render_template('ml.html', prediction_text='   {}'.format(output))


if __name__ == "__main__":
    app.run(debug=True)
