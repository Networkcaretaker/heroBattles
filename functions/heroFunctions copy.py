import utilities.consoleFunctions as consoleFunctions
import utilities.jsonFunctions as jsonFunctions
import json
import firebase.firebase as firebase
import click
from colorama import Fore, Style

heroData = {
    "Name":'heroName',
    "Title":'heroTitle',
    "Race":'heroRace',
    "Class":'heroClass',
    "Role":'heroRole',
    "Experience": {
        "Level":1,
        "Rank":1,
        "Level XP":0,
        "Total XP'":0
    },
    "PrimaryStats":{},
    "SecondaryStats":{},
    "BattleStats":{}
}
PrimaryStats = {
    "Strength":0,
    "Intelligence":0,
    "Agility":0,
    "Sorcery":0
}
SecondaryStats = {
    "Health":0,
    "Stamina":0,
    "Magicka":0,
    "HealthRecovery":0,
    "StaminaRecovery":0,
    "MagickaRecovery":0
}
BattleStats = {
    "PhysicalAttack":0,
    "MagicAttack":0,
    "PhysicalDefence":0,
    "MagicDefence":0,
    "Healing":0,
    "Armor":0,
    "Resistance":0,
    "Dodge":0,
    "Counter":0,
    "Block":0,
    "CriticalHit":0
}

dataset = 'heroes'

# Create a new hero and add to firebase
def createNewHero(Name, Race, Class, Role):
    # dataset = 'heroes'
    keys = ['Name', 'Race', 'Class', 'Role', 'PrimaryStats', 'SecondaryStats', 'BattleStats']
    values = [Name, Race, Class, Role, PrimaryStats, SecondaryStats, BattleStats]
    heroData.update({key: value for key, value in zip(keys, values)})
    
    # Add hero to database
    heroID = firebase.addRecord(dataset, heroData)

    # Convert the list to a JSON-formatted string
    # json_heroData = json.dumps(heroData, indent=2)
    # print(f"Success: New hero \033[91m{heroData['Name']}\033[0m created.\n heroID: \033[32m{heroID}\033[0m \n heroData: {json_heroData}")

    return(heroID)

# Get stat data for Hero Basic Stats from Firebase
def getHeroStatData():
    raceData = firebase.getSubRecords('gameData', 'heroStatData', 'raceData', 'raceName')
    classData = firebase.getSubRecords('gameData', 'heroStatData', 'classData', 'className')
    roleData = firebase.getSubRecords('gameData', 'heroStatData', 'roleData', 'roleName')
    return(raceData, classData, roleData)

# Set hero stats in Firebase
def setHeroBasicStats(heroID):
    hero = firebase.getRecord(dataset, heroID)
    raceData = firebase.getSubRecords('gameData', 'heroStatData', 'raceData', 'raceName')
    classData = firebase.getSubRecords('gameData', 'heroStatData', 'classData', 'className')
    roleData = firebase.getSubRecords('gameData', 'heroStatData', 'roleData', 'roleName')

    heroData = hero.to_dict()

    heroRace = hero.to_dict()['Race']
    heroClass = hero.to_dict()['Class']
    heroRole = hero.to_dict()['Role']

    primaryStats = heroData['PrimaryStats']
    secondaryStats = heroData['SecondaryStats']
    battleStats = heroData['BattleStats']
    experience = heroData['Experience']

    # Set hero primary stats from Race data
    for raceStat in raceData:
        if raceStat.to_dict()['raceName'] == heroRace:
            Strength = raceStat.to_dict()['Strength']
            Intelligence = raceStat.to_dict()['Intelligence']
            Agility = raceStat.to_dict()['Agility']
            Sorcery = raceStat.to_dict()['Sorcery']
            primaryStats['Strength'] = int(primaryStats['Strength']) + int(Strength)
            primaryStats['Intelligence'] = int(primaryStats['Intelligence']) + int(Intelligence)
            primaryStats['Agility'] = int(primaryStats['Agility']) + int(Agility)
            primaryStats['Sorcery'] = int(primaryStats['Sorcery']) + int(Sorcery)

    # Set hero primary stats from Class data
    for classStat in classData:
        if classStat.to_dict()['className'] == heroClass:
            Strength = classStat.to_dict()['Strength']
            Intelligence = classStat.to_dict()['Intelligence']
            Agility = classStat.to_dict()['Agility']
            Sorcery = classStat.to_dict()['Sorcery']
            primaryStats['Strength'] = int(primaryStats['Strength']) + int(Strength)
            primaryStats['Intelligence'] = int(primaryStats['Intelligence']) + int(Intelligence)
            primaryStats['Agility'] = int(primaryStats['Agility']) + int(Agility)
            primaryStats['Sorcery'] = int(primaryStats['Sorcery']) + int(Sorcery)
    
    # Set hero battle stats from Role data
    for roleStat in roleData:
        if roleStat.to_dict()['roleName'] == heroRole:
            Block = roleStat.to_dict()['Block']
            Counter = roleStat.to_dict()['Counter']
            Dodge = roleStat.to_dict()['Dodge']
            CriticalHit = roleStat.to_dict()['CriticalHit']
            battleStats['Block'] = int(battleStats['Block']) + int(Block)
            battleStats['Counter'] = int(battleStats['Counter']) + int(Counter)
            battleStats['Dodge'] = int(battleStats['Dodge']) + int(Dodge)
            battleStats['CriticalHit'] = int(battleStats['CriticalHit']) + int(CriticalHit)

    # Calculate Primary Stats from Experience
    primaryStats['Strength'] = int(primaryStats['Strength'] + experience['Level']) * experience['Rank']
    primaryStats['Intelligence'] = int(primaryStats['Intelligence'] + experience['Level']) * experience['Rank']
    primaryStats['Agility'] = int(primaryStats['Agility'] + experience['Level']) * experience['Rank']
    primaryStats['Sorcery'] = int(primaryStats['Sorcery'] + experience['Level']) * experience['Rank']

    # Calculate Secondary Stats
    secondaryStats['Health'] = (500 * experience['Level']) + (primaryStats['Strength'] * (experience['Rank'] * 50))
    secondaryStats['Stamina'] = (primaryStats['Agility'] * 10) * experience['Rank']
    secondaryStats['Magicka'] = (primaryStats['Sorcery'] * 10) * experience['Rank']
    secondaryStats['HealthRecovery'] = (experience['Level']*10) + ((secondaryStats['Health']*0.2)*(experience['Rank']*0.5) + (primaryStats['Intelligence'] + primaryStats['Sorcery']))
    secondaryStats['StaminaRecovery'] = (experience['Level']*10) + ((secondaryStats['Stamina']*0.3)*(experience['Rank']*0.5))
    secondaryStats['MagickaRecovery'] = (experience['Level']*10) + ((secondaryStats['Magicka']*0.3)*(experience['Rank']*0.5))

    # Calculate Battle Stats
    battleStats['PhysicalAttack'] = primaryStats['Strength'] + (primaryStats['Agility'] * 2) * 10
    battleStats['MagicAttack'] = primaryStats['Strength'] + (primaryStats['Sorcery'] * 2) * 10
    battleStats['PhysicalDefence'] = primaryStats['Intelligence'] + (primaryStats['Strength'] * 2) * 8
    battleStats['MagicDefence'] = primaryStats['Strength'] + (primaryStats['Intelligence'] * 2) * 8
    battleStats['Healing'] = primaryStats['Intelligence'] + primaryStats['Sorcery']

    battleStats['Armor'] = 100
    battleStats['Resistance'] = 100

    # Update Class and Skills
    splitClass = heroClass.split()
    heroData['Skill'] = splitClass[0]
    heroData['Class'] = splitClass[1]
    if len(splitClass) > 2:
        heroData['Class'] = splitClass[1] + ' ' + splitClass[0-1]

    # Add stat data to hero
    heroData['PrimaryStats'] = primaryStats
    heroData['SecondaryStats'] = secondaryStats
    heroData['BattleStats'] = battleStats

    # Update hero data in Firebase
    firebase.updateRecord(dataset, heroID, heroData)
    return(heroData)

# Select a value from list by number
def selectListValue(data):
    for i, value in enumerate(data, start=1):
        click.echo(f"{i}. {value}")
    
    selection = click.prompt("Enter the number of your selection", type=int)

    if 1 <= selection <= len(data):
            selected_value = data[selection - 1]
    else:
        click.echo("Invalid selection. Please try again.")
    
    return(selected_value)

# Create a new hero from input, add to json file and upload to Firebase
def createNewHeroesFromInput():
    print(f"{Fore.YELLOW}Create a new Hero{Style.RESET_ALL}")
    Name = input("Enter hero name: ")

    # Select a Race
    click.echo(f"{Fore.YELLOW}Choose a Race{Style.RESET_ALL}")
    races = []
    raceData = firebase.getSubRecords('gameData', 'heroStatData', 'raceData', 'raceName')
    for raceStat in raceData:
        races.append(raceStat.to_dict()['raceName'])
    Race = consoleFunctions.selectListValue(races)

    # Select a Class
    print(f"{Fore.YELLOW}Choose a Class{Style.RESET_ALL}")
    classes = []
    classData = firebase.getSubRecords('gameData', 'heroStatData', 'classData', 'className')
    for classStat in classData:
        classes.append(classStat.to_dict()['className'])
    Class = consoleFunctions.selectListValue(classes)

    # Select a Role
    print(f"{Fore.YELLOW}Choose a Role{Style.RESET_ALL}")
    roles = []
    roleData = firebase.getSubRecords('gameData','heroStatData', 'roleData', 'roleName')
    for roleStat in roleData:
        roles.append(roleStat.to_dict()['roleName'])
    Role = consoleFunctions.selectListValue(roles)

    heroID = createNewHero(Name, Race, Class, Role)
    print(f"{Fore.YELLOW}Success:{Style.RESET_ALL} A new hero has been created. \n ID: {Fore.GREEN}{heroID}{Style.RESET_ALL}\n {Fore.BLUE}{Name, Race, Class, Role}{Style.RESET_ALL}")

    results = setHeroBasicStats(heroID)
    json_heroData = json.dumps(results, indent=2)
    print(f"{Fore.YELLOW}Success:{Style.RESET_ALL} Hero stats have been updated \n {json_heroData}")

    addJSON = input("Do you want to add new hero to JSON? ")
    if addJSON == 'yes' or addJSON == 'y'or addJSON == 'Yes' or addJSON == 'Y' or addJSON == 'YES':
        newHero = {
        "Name": Name,
        "Race": Race,
        "Class": Class,
        "Role": Role
        }
        jsonFunctions.updateJsonFile('files/json/heroes,json', newHero)

# Create New Heroes from JSON file
def createNewHeroesFromFile(fileType):
    if fileType == 'CSV':
        heroes = jsonFunctions.createJsonFromCsv('files/csv/heroes.csv', 'files/json/heroes,json')
    if fileType == 'JSON':
        with open('files/json/heroes,json', 'r') as file:
            # Load the existing JSON content
            heroes = json.load(file)
            print(f"{Fore.YELLOW}Success: {Fore.GREEN}{'files/json/heroes,json'}{Style.RESET_ALL} has been loaded.")
    
    heroCount = len(heroes)
    print(f"{heroCount} heroes in file.")

    for hero in heroes:
        Name = hero['Name']
        Race = hero['Race']
        Class = hero['Class']
        Role = hero['Role']
        print(f"{Fore.YELLOW}Success:{Style.RESET_ALL} New hero created {Fore.GREEN}{Name, Race, Class, Role}{Style.RESET_ALL}") 
        heroID = createNewHero(Name, Race, Class, Role)
        print(f"{Fore.YELLOW}Success:{Style.RESET_ALL} New hero added to Firebase. ID: {Fore.GREEN}{heroID}{Style.RESET_ALL}") 
        results = setHeroBasicStats(heroID)
        json_heroData = json.dumps(results, indent=2)
        print(f"{Fore.YELLOW}Success:{Style.RESET_ALL} Hero stats have been updated \n{json_heroData}")

def getHero():
    allHeroes = firebase.getRecords(dataset)
    heroes = []
    heroIDs = []

    for hero in allHeroes:
        heroName = hero.to_dict()['Name']
        heroID = hero.id
        heroes.append(heroName)
        heroIDs.append({'Name':heroName, 'ID':heroID})
    
    print(f"\n{Fore.YELLOW}Choose a Hero{Style.RESET_ALL}\n")
    selectedHero = consoleFunctions.selectListValue(heroes)
    print(f"\n{Fore.YELLOW}{selectedHero}{Style.RESET_ALL}\n")

    for heroID in heroIDs:
        if heroID['Name'] == selectedHero:
            hero_id = heroID['ID']

    hero = firebase.getRecord('heroes', hero_id)

    return(hero)

def viewHero():
    hero = getHero()
    hero = hero.to_dict()

    splitClassSkill = hero['Class'].split()
    heroClass = splitClassSkill[0-1]
    heroSkill = splitClassSkill[0]

    print(f"Name: {Fore.GREEN}{hero['Name']}{Style.RESET_ALL}")
    print(f"Race: {Fore.LIGHTBLACK_EX}{hero['Race']}{Style.RESET_ALL}")
    print(f"Class: {Fore.LIGHTBLACK_EX}{heroClass}{Style.RESET_ALL}")
    print(f"Role: {Fore.LIGHTBLACK_EX}{hero['Role']}{Style.RESET_ALL}")
    print(f"Skill: {Fore.LIGHTBLACK_EX}{heroSkill}{Style.RESET_ALL}")
    print('')
    print(f'{Fore.BLUE}Experience{Style.RESET_ALL}')
    print(f"Level XP: {Fore.YELLOW}{hero['Experience']['Level XP']}{Style.RESET_ALL}")
    print(f"Total XP: {Fore.YELLOW}{hero['Experience']['Total XP']}{Style.RESET_ALL}")
    print(f"Level: {Fore.YELLOW}{hero['Experience']['Level']}{Style.RESET_ALL}")
    print(f"Rank: {Fore.YELLOW}{hero['Experience']['Rank']}{Style.RESET_ALL}")
    print('')
    print(f'{Fore.BLUE}Primary Stats{Style.RESET_ALL}')
    print(f"Strength: {Fore.YELLOW}{hero['PrimaryStats']['Strength']}{Style.RESET_ALL}")
    print(f"Intelligence: {Fore.YELLOW}{hero['PrimaryStats']['Intelligence']}{Style.RESET_ALL}")
    print(f"Agility: {Fore.YELLOW}{hero['PrimaryStats']['Agility']}{Style.RESET_ALL}")
    print(f"Sorcery: {Fore.YELLOW}{hero['PrimaryStats']['Sorcery']}{Style.RESET_ALL}")
    print('')
    print(f'{Fore.BLUE}Secondary Stats{Style.RESET_ALL}')
    print(f"Health: {Fore.YELLOW}{hero['SecondaryStats']['Health']}{Style.RESET_ALL}")
    print(f"Stamina: {Fore.YELLOW}{hero['SecondaryStats']['Stamina']}{Style.RESET_ALL}")
    print(f"Magicka: {Fore.YELLOW}{hero['SecondaryStats']['Magicka']}{Style.RESET_ALL}")
    print(f"Health Recovery: {Fore.YELLOW}{hero['SecondaryStats']['HealthRecovery']}{Style.RESET_ALL}")
    print(f"Stamina Recovery: {Fore.YELLOW}{hero['SecondaryStats']['StaminaRecovery']}{Style.RESET_ALL}")
    print(f"Magicka Recovery: {Fore.YELLOW}{hero['SecondaryStats']['MagickaRecovery']}{Style.RESET_ALL}")
    print('')
    print(f'{Fore.BLUE}Battle Stats{Style.RESET_ALL}')
    print(f"Physical Attack: {Fore.RED}{hero['BattleStats']['PhysicalAttack']}{Style.RESET_ALL}")
    print(f"Physical Defence: {Fore.RED}{hero['BattleStats']['PhysicalDefence']}{Style.RESET_ALL}")
    print(f"Magic Attack: {Fore.MAGENTA}{hero['BattleStats']['MagicAttack']}{Style.RESET_ALL}")
    print(f"Magic Defence: {Fore.MAGENTA}{hero['BattleStats']['MagicDefence']}{Style.RESET_ALL}")
    print(f"Healing: {Fore.YELLOW}{hero['BattleStats']['Healing']}{Style.RESET_ALL}")
    print(f"Dodge: {Fore.YELLOW}{hero['BattleStats']['Dodge']}{Style.RESET_ALL}")
    print(f"Counter: {Fore.YELLOW}{hero['BattleStats']['Counter']}{Style.RESET_ALL}")
    print(f"Block: {Fore.YELLOW}{hero['BattleStats']['Block']}{Style.RESET_ALL}")
    print(f"Critical Hit: {Fore.YELLOW}{hero['BattleStats']['CriticalHit']}{Style.RESET_ALL}")
    print(f"Armor: {Fore.YELLOW}{hero['BattleStats']['Armor']}{Style.RESET_ALL}")
    print(f"Resistance: {Fore.YELLOW}{hero['BattleStats']['Armor']}{Style.RESET_ALL}")
    print('\n')

    return(hero)



    