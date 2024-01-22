import firebase_admin
import firebase.secret_key as secret_key
import json
import csv
from firebase_admin import credentials, firestore
from colorama import Fore, Style

# Initialize firestore
cred = credentials.Certificate(secret_key.firebaseKey)
firebase_admin.initialize_app(cred)

db = firestore.client()

# Get a single record by ID
def getRecord(dataset, recordID):
    data = db.collection(dataset).document(recordID).get()
    return (data)

# Get all records from database collection
def getRecords(dataset):
    data = db.collection(dataset).stream()
    return (data)

# Get a single sub-record by ID
def getSubRecord(dataset, record, datasetB, recordID):
    data = db.collection(dataset).document(record).collection(datasetB).document(recordID).get()
    return (data)

# Get all sub-record records from database collection
def getSubRecords(dataset, record, datasetB, order):
    data = db.collection(dataset).document(record).collection(datasetB).order_by(order).stream()
    return (data)

# Add a record
def addRecord(dataset, data):
    data = db.collection(dataset).add(data)
    recordID = data[1].__dict__['_path'][1]
    return (recordID)

# Add a sub-record
def addSubRecord(dataset, record, datasetB, data):
    data = db.collection(dataset).document(record).collection(datasetB).add(data)
    recordID = data[1].__dict__['_path'][1]
    return (recordID)

# Update a record by ID
def updateRecord(dataset, recordID, data):
    data = db.collection(dataset).document(recordID).update(data)
    return (data)

# Update a sub-record by ID
def updateSubRecord(dataset, recordID, data, datasetB, record):
    data = db.collection(dataset).document(record).collection(datasetB).document(recordID).update(data)
    return (data)
