import json
import csv
from colorama import Fore, Style

# Create a JSON file from CSV
def createJsonFromCsv(csvFile, jsonFile):
    with open(csvFile, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        # Convert CSV data to a list of dictionaries
        data = [row for row in csv_reader]

        # Create JSON object
        json_data = json.dumps(data, indent=2)

        # Write JSON object to a file
        with open(jsonFile, 'w') as json_file:
            json_file.write(json_data)

        print(f"{Fore.YELLOW}Success: {Fore.GREEN}{jsonFile}{Style.RESET_ALL} has been created.")

        return(data)

# Function to open a JSON file, add a new item, and save the updated content
def updateJsonFile(file_path, new_item):
    # Open the JSON file for reading
    with open(file_path, 'r') as file:
        # Load the existing JSON content
        data = json.load(file)
    data.append(new_item)

    # Open the same JSON file for writing
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

    print(f"{Fore.YELLOW}Success:{Style.RESET_ALL} JSON file has been updated")

# Upload data from JSON to Firebase
def jsonToFirebase(records, dataset):
    results = []
    for record in records:
        recordID = addRecord(dataset, record)
        results.append([recordID, record])
    return(results)

# Upload data from JSON to Firebase Sub-collection
def jsonToFirebaseSub(records, dataset, recordID, datasetB):
    results = []
    for record in records:
        subrecordID = addSubRecord(dataset, record, datasetB, recordID)
        results.append([subrecordID, record])
    return(results)