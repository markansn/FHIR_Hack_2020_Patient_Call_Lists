from fhir_parser import FHIR
from tqdm import tqdm

fhir = FHIR()
patients = fhir.get_all_patients()
observations = []

patients = patients[:50]

# for patient in tqdm(patients):
#     observations.extend(fhir.get_patient_observations(patient.uuid))
#
#
# for observation in observations:
#     print("**** " + observation.uuid + "**** ")
#     for component in observation.components:
#         print(component.display)
#         print(component.quantity())
#         print("--------------------------")
#

for patient in patients:
    pass