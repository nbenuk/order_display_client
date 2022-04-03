from flask import Flask, redirect, render_template, url_for, flash
import time
import requests
import json

from forms import OrderForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '123'

@app.route("/")
def home():
    url = "http://127.0.0.1:8000/vieworders"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    
    data = json.loads(response.text)
    pend = []
    prep = []
    ready =[]
    for i in range(len(data)):
        if data[i]['status'] == 'Pending':
            pend.append({"order_ref": data[i]['order_ref'], "status":data[i]['status']})
        elif data[i]['status'] == 'Preparing':
            prep.append({"order_ref": data[i]['order_ref'], "status":data[i]['status']})
        elif data[i]['status'] == 'Ready':
            ready.append({"order_ref": data[i]['order_ref'], "status":data[i]['status']})
    return render_template('vieworders.html', pend=pend, prep=prep, ready=ready)

@app.route("/station")
def station():
    return render_template('station.html')

@app.route("/preprep", methods=['GET','POST'])
def preprep():
    form = OrderForm()
    if form.validate_on_submit():
        url = "http://127.0.0.1:8000/neworder"

        payload={'order_ref': form.order_ref.data}
        files=[

        ]
        headers = {}

        requests.request("POST", url, headers=headers, data=payload, files=files)

        flash(f'Order {form.order_ref.data} added', 'success')
    return render_template('preprep.html', form=form)

@app.route("/prep")
def prep():
    url = "http://127.0.0.1:8000/vieworders"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    
    data = json.loads(response.text)
    pend = []
    prep = []
    ready =[]
    for i in range(len(data)):
        if data[i]['status'] == 'Pending':
            pend.append({"order_ref": data[i]['order_ref'], "status":data[i]['status']})
        elif data[i]['status'] == 'Preparing':
            prep.append({"order_ref": data[i]['order_ref'], "status":data[i]['status']})
        elif data[i]['status'] == 'Ready':
            ready.append({"order_ref": data[i]['order_ref'], "status":data[i]['status']})
    return render_template('prep.html',pend=pend)

@app.route("/ready")
def ready():
    url = "http://127.0.0.1:8000/vieworders"
    payload={}
    headers = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    
    data = json.loads(response.text)
    pend = []
    prep = []
    ready =[]
    for i in range(len(data)):
        if data[i]['status'] == 'Pending':
            pend.append({"order_ref": data[i]['order_ref'], "status":data[i]['status']})
        elif data[i]['status'] == 'Preparing':
            prep.append({"order_ref": data[i]['order_ref'], "status":data[i]['status']})
        elif data[i]['status'] == 'Ready':
            ready.append({"order_ref": data[i]['order_ref'], "status":data[i]['status']})
    return render_template('ready.html', prep=prep, ready=ready)

@app.route("/update<order_ref>-<status>-<return_to>")
def update_status(order_ref, status, return_to):
    url = "http://127.0.0.1:8000/updatestatus"

    payload={'order_ref': order_ref,
    'status': status}
    files=[

    ]
    headers = {}

    response = requests.request("PUT", url, headers=headers, data=payload, files=files)

    print(response.text)
    return redirect( url_for(return_to))

@app.route("/update<order_ref>-<return_to>")
def delete_order(order_ref, return_to):
    url = "http://127.0.0.1:8000/deleteorder"

    payload={'order_ref': order_ref}
    files=[

    ]
    headers = {}

    response = requests.request("DELETE", url, headers=headers, data=payload, files=files)

    print(response.text)
    return redirect( url_for(return_to))


if __name__ == '__main__':
    app.run(debug=True)
    