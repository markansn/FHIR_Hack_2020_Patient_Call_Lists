from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import model

app = Flask(__name__, template_folder='web_files')

model = model.Model()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/create_list')
def create_list():
    return render_template('create_list.html')

@app.route('/update_call_list')
def update_call_list():
    text = request.args.get('jsdata')

    call_list = model.patient_lists

    return render_template("call_list.html", data=call_list)

@app.route('/get_call_info')
def get_call_info():

    name = request.args.get('jsdata')
    name.replace(" ", "_")
    patients = model.fetch_patient_list(name)

    return render_template("call_info.html", data=patients)


if __name__ == '__main__':
    app.run(debug=True, port=25565)