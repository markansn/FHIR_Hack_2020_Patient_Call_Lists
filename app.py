from flask import Flask, render_template, request, Markup
import requests
from bs4 import BeautifulSoup
import model

app = Flask(__name__, template_folder='web_files')

model = model.Model()

def assemble_call_info_display(name):
	patients = model.fetch_patient_list(name)

	patient_display = []
	for patient in patients:
		dob = str(patient[0].birth_date.day) + "/" + str(patient[0].birth_date.month) + "/" + str(patient[0].birth_date.year)
		address = patient[0].addresses[0].lines[0] + ', ' + patient[0].addresses[0].city + ', ' + patient[0].addresses[0].state + ', ' + patient[0].addresses[0].country + ', ' + patient[0].addresses[0].postal_code
		if patient[1]:
			patient_display.append(Markup(
				"<button style=\"text-decoration: line-through\">" + patient[0].full_name() + "</button>") + " | " + Markup(
				"<a href=\"skype:" + patient[0].telecoms[0].number + "?call\">Call " +patient[0].telecoms[0].number +"</a>") + " | " + Markup(
				"<a class=\"called\" href=\"#\"  id=\"" + patient[0].uuid + "__and__" + name + "\">Uncomplete</a>"))
		else:
			patient_display.append(Markup("<ee data-toggle=\"tooltip\" data-placement=\"top\" title=\"" + "DOB: " + dob + " | " + address + "\" >" + patient[0].full_name() + "</ee>") + " | " + Markup(
				"<a href=\"skype:" + patient[0].telecoms[0].number + "?call\">Call " +patient[0].telecoms[0].number +"</a>") + " | " + Markup(
				"<a href=\"#\" class=\"called\" id=\"" + patient[0].uuid + "__and__" + name + "\">Complete</a>"))

	return patient_display

@app.route('/')
def index():
	return render_template('index.html')



@app.route('/add_new_list')
def create_list():
	return render_template('add_new_list.html')

@app.route('/update_call_list')
def update_call_list():
	text = request.args.get('jsdata')

	call_list = model.get_all_patient_lists()

	return render_template("call_list.html", data=call_list)

@app.route('/get_call_info')
def get_call_info():

	name = request.args.get('jsdata')
	name = name.replace(" ", "_")
	patient_display = assemble_call_info_display(name)
	return render_template("call_info.html", data=patient_display)




@app.route('/set_call_complete')
def set_call_complete():
	text = request.args.get('jsdata')

	data = text.split("__and__")
	model.update_complete(data[1], data[0])
	patient_display = assemble_call_info_display(data[1])
	return render_template("call_info.html", data=patient_display)

@app.route('/generate_new_list', methods=["POST"])
def generate_new_list():
	elements = ["first_name", "last_name", "gender", "house", "city", "state", "postal_code", "country", "birth_day", "birth_month", "birth_year", "age"]
	query = {}
	for item in elements:
		if request.form[item].lower() != "":
			if item == "gender":
				query[item] = [request.form[item].lower(), "exact"]
			else:
				query[item] = [request.form[item], request.form["select_" + item].split(" ")[0].lower()]

	print(query)

	model.save_patient_list(model.get_patient_details_from_query(query), request.form["list_name"].replace(" ", "_").lower())


	return render_template("index.html")


if __name__ == '__main__':
	app.run(debug=True, port=25565)