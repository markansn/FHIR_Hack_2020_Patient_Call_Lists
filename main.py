from view import View
from model import Model
view = View()

model = Model()


query = {
    'age':[50,'greater']
}

for p in model.get_patient_details_from_query(query):
    print(p.age())


print(model.save_patient_list(["patient1","patient2","patient3"], "list1"))
print(model.save_patient_list(["patient4","patient5","patient6"], "list2"))

# print(model.fetch_patient_list("test2222"))
# print(model.delete_patient_list("test23"))