import pickle
import glob
from fhir_parser import FHIR
from tqdm import tqdm
import datetime
import os
class Model:
    fhir = FHIR()
    patients = fhir.get_all_patients()
    patient_lists = []
    def __init__(self):
       self.patient_lists = self.get_all_patient_lists()



    def get_all_patient_lists(self):
        files = glob.glob("saved_lists/*")
        l = []
        for file in files:
            file = file.replace("saved_lists/", "")
            file = file.replace(".pickle", "")
            l.append(file)
        return l

    def get_patient_details_from_name(self, firstname, surname):
        patients_with_name = []
        self.patients = self.fhir.get_all_patients()
        for patient in self.patients:
            if patient.name.given.lower() == firstname.lower() and patient.name.given.lower() == surname.lower():
                patients_with_name.append(patient)

        return patients_with_name





    def save_patient_list(self, list, filename):
        files = glob.glob("saved_lists/*")
        for file in files:
            if os.path.join("saved_lists", filename + "." + "pickle") == file:

                return False


        with open("saved_lists/"+filename+".pickle", 'wb') as handle:
            pickle.dump(list, handle, protocol=pickle.HIGHEST_PROTOCOL)

        return True


    def fetch_patient_list(self, filename):

            path = os.path.join("saved_lists", filename + "." + "pickle")
            return self.get_pickle(path)


    def get_pickle(self, path):
        try:
            with open(path, 'rb') as handle:
                p = pickle.load(handle)

            return p
        except FileNotFoundError:
            return []


    def delete_patient_list(self,filename):
        try:
            os.remove(os.path.join("saved_lists", filename + "." + "pickle"))
        except FileNotFoundError:
            return False

        return True

    def get_patient_details_from_query(self, query):
        patients = []

        for patient in self.patients:
            patient_dict = self.generate_patient_dict(patient)
            passed = True
            for key in query:
                info = query[key][0]
                contains_or_exact = query[key][1]
                try:
                    if contains_or_exact == "contains":
                        if info not in patient_dict[key]:
                            passed = False
                            break
                    if contains_or_exact == "exact":
                        if not patient_dict[key] == info:
                            passed = False
                            break
                    if contains_or_exact == "less":
                        if not patient_dict[key] < info:
                            passed = False
                            break
                    if contains_or_exact == "greater":
                        if not patient_dict[key] > info:
                            passed = False
                            break
                except TypeError:
                    passed = False
                    break

            if passed:
                patients.append(patient)

        return patients





    def generate_patient_dict(self, p):
        today = datetime.date.today()

        return {
            'uuid': p.uuid,
            'first_name': ''.join([i for i in p.name.given if not i.isdigit()]),
            'last_name': ''.join([i for i in p.name.family if not i.isdigit()]),
            'gender':p.gender,
            'birth_year':p.birth_date.year,
            'birth_month':p.birth_date.month,
            'birth_day':p.birth_date.day,
            'age':today.year - p.birth_date.year - ((today.month, today.day) < (p.birth_date.month, p.birth_date.day)),
            'house': p.addresses[0].lines,
            'city': p.addresses[0].city,
            'state':p.addresses[0].state,
            'postal_code':p.addresses[0].postal_code,
            'country':p.addresses[0].country,
            'marital_status':p.marital_status.marital_status,
            'language':p.communications.languages[0]
        }

