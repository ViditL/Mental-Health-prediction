# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 03:21:17 2020

@author: Adi
"""
from flask import Flask,request, url_for, redirect, render_template
import pickle
import numpy as np

app = Flask(__name__)

model=pickle.load(open('model.pkl','rb'))
@app.route('/')
def hello_world():
    return render_template("login.html")
database={'aadesh':'123','vidit':'abc','admin':'admin'}

@app.route('/form_login',methods=['POST','GET'])
def login():
    name1=request.form['username']
    pwd=request.form['password']
    if name1 not in database:
	    return render_template('login.html',info='Invalid User')
    else:
        if database[name1]!=pwd:
            return render_template('login.html',info='Invalid Password')
        else:
	         return render_template('mental.html',name=name1)


@app.route('/predict',methods=['POST','GET'])
def predict():
	int_features=[int(x) for x in request.form.values()]
	final=[np.array(int_features)]
	prediction=model.predict_proba(final)
	output='{0:.{1}f}'.format(prediction[0][1], 2)

	if output>str(0.62):
		return render_template('result.html',pred='You need to see psychiatrist.\nProbability is {}'.format(output),inf='1. If you feel that your work is affecting your mental health, talk to your superiors for steps to alter your work-life',inf1='2. Alternatively, you can engage in activities such as yoga, jogging, listening to music')
	elif output>str(0.35):
		return render_template('result.html',pred='You do not suffer from mental illness currently, but it is advised to take precautions for the future .\n Probability is {}'.format(output),inf='1. You should consider exercises such as jogging, cycling, swimming, meditating, whenever you feel stressed.',inf1='2. You can also consult a mental health professional for understanding whether you need to take extra care about your mental well-being',inf2='3. You may talk to your managers at work if you feel that your job is making you feel stressed or depressed')
	else:
		return render_template('result.html',pred='You do not suffer from mental illness.\n Probability is {}'.format(output),inf='Consider exercising for at least 30 minutes a per day to ensure mental and physical freshness eg. walk, cycle, swim etc.')


if __name__ == '__main__':
    app.run(debug=True)
