import consoleFunctions
import firebase
import heroFunctions
import battleFunctions
import playerFunctions
import json
from colorama import Fore, Style

# Sample Data
dataset = 'baseData' # heroes, baseData
datasetB = 'roleData' # roleData, raceData, classData
csvFile = 'csv/heroRole.csv' # heroes.csv, heroRace.csv, heroClass.csv, heroRole.csv 
jsonFile = 'json/heroRole,json' # heroes,json, heroRace,json, heroClass,json, heroRole,json 
recordID = 'heroBaseData' # heroBaseData 
heroID = ''

# Create a JSON file from CSV data
# data = firebase.createJsonFromCsv(csvFile, jsonFile)
# print(f"{Fore.YELLOW}Success: {Fore.GREEN}{jsonFile}{Style.RESET_ALL} has been created.")

# Create a JSON file from CSV data and upload to firebase
# data = firebase.createJsonFromCsv(csvFile, jsonFile)
# print(f"{Fore.YELLOW}Success: {Fore.GREEN}{jsonFile}{Style.RESET_ALL} has been created.")
# results = firebase.jsonToFirebase(data, dataset)
# print(results)

# Create a JSON file from CSV data and upload to firebase sub-collection
def uploadSubCollectionFromFile():
    data = firebase.createJsonFromCsv(csvFile, jsonFile)
    results = firebase.jsonToFirebaseSub (data, dataset, recordID, datasetB)
    print(f"{results}\n{Fore.YELLOW}Success: {Fore.GREEN}{datasetB}{Style.RESET_ALL} has been added to Firebase.")

# uploadSubCollectionFromFile()
    
# Test Functions
testFunctions = [
    'createNewHeroesFromFile',
    'createNewHeroesFromInput',
    'viewHero',
    'selectHeroes',
    'startBattle',
    'uploadSubCollectionFromFile',
    'addPlayerXP',
    'createPlayer'
]
validFileType = [
    'CSV',
    'JSON'
]

print(f"\n{Fore.YELLOW}Select a function to run{Style.RESET_ALL}")
selectFunction = consoleFunctions.selectListValue(testFunctions)

print(f"Start function: {Fore.GREEN}{selectFunction}{Style.RESET_ALL}")

if selectFunction == 'createNewHeroesFromFile':
    
    selectFileType = input("Select File Type (CSV or JSON): ")
    while selectFileType not in validFileType:
        print(f'{Fore.RED}Error:{Style.RESET_ALL} Select a valid file type.')
        selectFileType = input("Select File Type (CSV or JSON): ")
    if selectFileType == 'CSV':
        print(f'{Fore.RED}Warning:{Style.RESET_ALL} This function will overwrite the saved JSON file \n Do you want to continue? (Type NO to cancel)')
        warningCheck = input("Continue: ")
        if warningCheck != 'NO':
            print(f"Function {Fore.GREEN}{selectFunction}{Style.RESET_ALL} cancelled")
            exit()

    heroFunctions.createNewHeroesFromFile(selectFileType)
        
if selectFunction == 'createNewHeroesFromInput':
    heroFunctions.createNewHeroesFromInput()

if selectFunction == 'viewHero':
    heroFunctions.viewHero()

if selectFunction == 'selectHeroes':
    battleFunctions.selectHeroes()

if selectFunction == 'startBattle':
    battleFunctions.startBattle()

if selectFunction == 'uploadSubCollectionFromFile':
    uploadSubCollectionFromFile()

if selectFunction == 'createPlayer':
    results = playerFunctions.createPlayer()

if selectFunction == 'addPlayerXP':
    # TEST DATA
    playerData = {
        'Name': 'Name',
        'Experience': {
            'Level': 1,
            "Rank": 1,
            'Level XP': 0,
            'Total XP': 0
        }
    }
    add_xp = 15
    playerFunctions.addPlayerXP(add_xp, playerData)

print(results)
print(f"{Fore.YELLOW}Success: {Fore.GREEN}{selectFunction}{Style.RESET_ALL} function complete.")

# DEV FUNCTIONS
# test = firebase.getRecord(dataset, recordID)
# print(f"{test.id} => {test.to_dict()}")

# tests = firebase.getRecords(dataset)
# for test in tests:
#    print(f"{test.id} => {test.to_dict()}")
  
# firebase.addRecord(dataset, data)

# firebase.updateRecord(dataset, recordID, data)



# heroFunctions.createNewHero('Balrock', 'Orc', 'Tank', 'Brawler')
# results = heroFunctions.setHeroStats(heroID)

# print(results)