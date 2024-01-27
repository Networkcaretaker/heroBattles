import utilities.jsonFunctions as jsonFunctions
from colorama import Fore, Style

# Game Data

# Upload Race Data to Firebase
def uploadHeroRaceFromCsvToFirebase():
    csvFile = 'files/csv/HERO_Races.csv'
    jsonFile = 'files/json/HERO_Races.json'
    dataset = 'RaceData'
    data = jsonFunctions.createJsonFromCsv(csvFile, jsonFile)

    heroRaces = []
    for d in data:
        heroRaceData = {
            "ID": d['Race Title'],
            "DATA": {
                "Race Name": d['Race Name'],
                "Race Type": d['Race Type'],
                "Race Moto": d['Race Moto'],
                "Race Home": d['Race Home'],
                "Race Description": d['Race Description'],
                "Statistics": {
                    "Primary": 
                        {
                            "Stength": d['Strength'],
                            "Intelligence": d['Intelligence'],
                            "Agility": d['Agility'],
                            "Sorcery": d['Sorcery']
                        },
                    "Secondary": 
                        {
                            "Critical Hit": d['Critical Hit'],
                            "Dodge": d['Dodge'],
                            "Counter": d['Counter'],
                            "Block": d['Block'],
                            "Healing": d['Healing']
                    }
                }     
            }
        }
        heroRaces.append(heroRaceData)

    results = jsonFunctions.jsonToFirebaseSubWithID ('GameData', 'HeroStatData', dataset, heroRaces)
    print(f"{results}\n{Fore.YELLOW}Success: {Fore.GREEN}Race Data{Style.RESET_ALL} has been added to Firebase.")

# Upload Class Data to Firebase
def uploadHeroClassFromCsvToFirebase():
    csvFile = 'files/csv/HERO_Classes.csv'
    jsonFile = 'files/json/HERO_Classes.json'
    dataset = 'ClassData'
    data = jsonFunctions.createJsonFromCsv(csvFile, jsonFile)

    heroClasses = []
    for d in data:
        heroClassData = {
            "ID": d['Class Title'],
            "DATA": {
                "Class Name": d['Class Name'],
                "Class Skill": d['Class Skill'],
                "Statistics": {
                    "Primary": 
                        {
                            "Stength": d['Strength'],
                            "Intelligence": d['Intelligence'],
                            "Agility": d['Agility'],
                            "Sorcery": d['Sorcery']
                    }
                } 
            }    
        }
        heroClasses.append(heroClassData)

    results = jsonFunctions.jsonToFirebaseSubWithID ('GameData', 'HeroStatData', dataset, heroClasses)
    print(f"{results}\n{Fore.YELLOW}Success: {Fore.GREEN}Class Data{Style.RESET_ALL} has been added to Firebase.")

# Upload Role Data to Firebase
def uploadHeroRoleFromCsvToFirebase():
    csvFile = 'files/csv/HERO_Roles.csv'
    jsonFile = 'files/json/HERO_Roles.json'
    dataset = 'RoleData'
    data = jsonFunctions.createJsonFromCsv(csvFile, jsonFile)

    heroRoles = []
    for d in data:
        heroRoleData = {
            "ID": d['Role Name'],
            "DATA": {
                "Role Name": d['Role Name'],
                "Statistics": {
                    "Secondary": 
                        {
                            "Critical Hit": d['Critical Hit'],
                            "Dodge": d['Dodge'],
                            "Counter": d['Counter'],
                            "Block": d['Block'],
                            "Healing": d['Healing']
                    }
                } 
            }    
        }
        heroRoles.append(heroRoleData)

    results = jsonFunctions.jsonToFirebaseSubWithID ('GameData', 'HeroStatData', dataset, heroRoles)
    print(f"{results}\n{Fore.YELLOW}Success: {Fore.GREEN}Role Data{Style.RESET_ALL} has been added to Firebase.")
