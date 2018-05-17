from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import pyrebase

config = {
    #config details removed as they contain access details.
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

db = firebase.database()

def display(request):

    data = ""
    record = 1

    patientMRN = request.POST.get("Patient_MRN")

    mrn = db.child("PROCESSED_PATIENT_DATA").shallow().get().val()

    if patientMRN in mrn:
        AllData = db.child("PROCESSED_PATIENT_DATA").child(patientMRN).shallow().get().val()
        patient = "MRN: " + patientMRN + "\n"
        for i in AllData:
            dataDict = dict(db.child("PROCESSED_PATIENT_DATA").child(patientMRN).child(i).get().val())
            error = dataDict["ERROR"]
            time = dataDict["Time"]
            averageHR = dataDict["minHR"]
            maxHR = dataDict["maxHR"]
            minHR = dataDict["minHR"]
            numberOfEpisodes = dataDict["numberOfEpisodes"]
            result = dataDict["result"]
            data = data + "RECORD NUMBER: " + str(record) + "\n" + "Time: " + time + "\n" + "ERROR: " + error + "\n" + "Average HR: " + str(averageHR) + ", max HR: " + str(maxHR) + ", min HR: " + str(minHR) + "\n" + "RESULT: " + result + ", number of episodes: " + str(numberOfEpisodes) + "\n" + "\n"
            record = record + 1

    else:
        patient = "MRN: " + patientMRN + "\n"
        data = "This MRN is not available please search again."

    return render(request, 'display.html', {"PATIENT": patient, "DATA": data})