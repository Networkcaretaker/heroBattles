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
    "Class_Name": 'className',
    "Class_Skill":'heroSkill',
    "Role":'heroRole',
    "Description": '',
    "Experience": {
        "Level":1,
        "Rank":1,
        "Level XP":0,
        "Total XP'":0
    },
    "Stats":{
        "Primary":{},
        "Secondary":{},
        "Energy":{},
        "Battle":{}
    }
}
PrimaryStats = {
    "Strength":0,
    "Intelligence":0,
    "Agility":0,
    "Sorcery":0
}
SecondaryStats = {
    "Healing":0,
    "Dodge":0,
    "Counter":0,
    "Block":0,
    "Critical_Hit":0
}
EnergyStats = {
    "Health":0,
    "Stamina":0,
    "Magicka":0,
    "Health_Recovery":0,
    "Stamina_Recovery":0,
    "Magicka_Recovery":0
}
BattleStats = {
    "Physical_Attack":0,
    "Magic_Attack":0,
    "Physical_Defence":0,
    "Magic_Defence":0,
    "Armor":0,
    "Resistance":0,
    "Weapon_Damage": 0,
    "Magic_Damage": 0
}
Stats = {
    "Primary": PrimaryStats,
    "Secondary": SecondaryStats,
    "Energy": EnergyStats,
    "Battle": BattleStats
}

dataset = 'Heroes'

# Create a new hero and add to firebase
def createNewHero(Name, Race, Class, Role, Class_Name, Class_Skill, Title, Description):
    # dataset = 'heroes'
    keys = ['Name', 'Race', 'Class', 'Role', 'Class_Name', 'Class_Skill', 'Stats', 'Title', 'Description']
    values = [Name, Race, Class, Role, Class_Name, Class_Skill, Stats, Title, Description]
    heroData.update({key: value for key, value in zip(keys, values)})
    
    # Add hero to database
    heroID = firebase.addRecord(dataset, heroData)
    return(heroID)

# Set hero stats in Firebase
def setHeroBasicStats(heroID):
    hero = firebase.getRecord(dataset, heroID)
    raceData = firebase.getSubRecords('GameData', 'HeroStatData', 'RaceData', 'Race_Name')
    classData = firebase.getSubRecords('GameData', 'HeroStatData', 'ClassData', 'Class_Name')
    roleData = firebase.getSubRecords('GameData', 'HeroStatData', 'RoleData', 'Role_Name')

    heroData = hero.to_dict()

    heroRace = hero.to_dict()['Race']
    heroClass = hero.to_dict()['Class']
    heroRole = hero.to_dict()['Role']

    primaryStats = heroData['Stats']['Primary']
    secondaryStats = heroData['Stats']['Secondary']
    energyStats = heroData['Stats']['Energy']
    battleStats = heroData['Stats']['Battle']
    experience = heroData['Experience']

    # Set hero primary stats from Race data
    for raceStat in raceData:
        if raceStat.to_dict()['Race_Name'] == heroRace:
            Strength = raceStat.to_dict()['Statistics']['Primary']['Strength']
            Intelligence = raceStat.to_dict()['Statistics']['Primary']['Intelligence']
            Agility = raceStat.to_dict()['Statistics']['Primary']['Agility']
            Sorcery = raceStat.to_dict()['Statistics']['Primary']['Sorcery']
            primaryStats['Strength'] = int(primaryStats['Strength']) + int(Strength)
            primaryStats['Intelligence'] = int(primaryStats['Intelligence']) + int(Intelligence)
            primaryStats['Agility'] = int(primaryStats['Agility']) + int(Agility)
            primaryStats['Sorcery'] = int(primaryStats['Sorcery']) + int(Sorcery)

    # Set hero primary stats from Class data
    for classStat in classData:
        if classStat.id == heroClass:
            Strength = classStat.to_dict()['Statistics']['Primary']['Strength']
            Intelligence = classStat.to_dict()['Statistics']['Primary']['Intelligence']
            Agility = classStat.to_dict()['Statistics']['Primary']['Agility']
            Sorcery = classStat.to_dict()['Statistics']['Primary']['Sorcery']
            primaryStats['Strength'] = int(primaryStats['Strength']) + int(Strength)
            primaryStats['Intelligence'] = int(primaryStats['Intelligence']) + int(Intelligence)
            primaryStats['Agility'] = int(primaryStats['Agility']) + int(Agility)
            primaryStats['Sorcery'] = int(primaryStats['Sorcery']) + int(Sorcery)
    
    # Set hero secondary stats from Role data
    for roleStat in roleData:
        if roleStat.id == heroRole:
            Block = roleStat.to_dict()['Statistics']['Secondary']['Block']
            Counter = roleStat.to_dict()['Statistics']['Secondary']['Counter']
            Dodge = roleStat.to_dict()['Statistics']['Secondary']['Dodge']
            Critical_Hit = roleStat.to_dict()['Statistics']['Secondary']['Critical_Hit']
            Healing = roleStat.to_dict()['Statistics']['Secondary']['Healing']
            secondaryStats['Block'] = int(secondaryStats['Block']) + int(Block)
            secondaryStats['Counter'] = int(secondaryStats['Counter']) + int(Counter)
            secondaryStats['Dodge'] = int(secondaryStats['Dodge']) + int(Dodge)
            secondaryStats['Critical_Hit'] = int(secondaryStats['Critical_Hit']) + int(Critical_Hit)
            secondaryStats['Healing'] = int(secondaryStats['Healing']) + int(Healing)

    # Calculate Primary Stats from Experience
    primaryStats['Strength'] = int(primaryStats['Strength'] + experience['Level']) * experience['Rank']
    primaryStats['Intelligence'] = int(primaryStats['Intelligence'] + experience['Level']) * experience['Rank']
    primaryStats['Agility'] = int(primaryStats['Agility'] + experience['Level']) * experience['Rank']
    primaryStats['Sorcery'] = int(primaryStats['Sorcery'] + experience['Level']) * experience['Rank']

    # Calculate Energy Stats
    energyStats['Health'] = (500 * experience['Level']) + (primaryStats['Strength'] * (experience['Rank'] * 50))
    energyStats['Stamina'] = (primaryStats['Agility'] * 10) * experience['Rank']
    energyStats['Magicka'] = (primaryStats['Sorcery'] * 10) * experience['Rank']
    energyStats['Health_Recovery'] = (experience['Level']*10) + ((energyStats['Health']*0.2)*(experience['Rank']*0.5) + (primaryStats['Intelligence'] + primaryStats['Sorcery']))
    energyStats['Stamina_Recovery'] = (experience['Level']*10) + ((energyStats['Stamina']*0.3)*(experience['Rank']*0.5))
    energyStats['Magicka_Recovery'] = (experience['Level']*10) + ((energyStats['Magicka']*0.3)*(experience['Rank']*0.5))

    # Calculate Battle Stats
    battleStats['Physical_Attack'] = primaryStats['Strength'] + (primaryStats['Agility'] * 2) * 10
    battleStats['Magic_Attack'] = primaryStats['Strength'] + (primaryStats['Sorcery'] * 2) * 10
    battleStats['Physical_Defence'] = primaryStats['Intelligence'] + (primaryStats['Strength'] * 2) * 8
    battleStats['Magic_Defence'] = primaryStats['Strength'] + (primaryStats['Intelligence'] * 2) * 8
    battleStats['Armor'] = 0
    battleStats['Resistance'] = 0
    battleStats['Weapon_Damage'] = 0
    battleStats['Magic_Damage'] = 0

    # Add stat data to hero
    heroData['Stats']['Primary'] = primaryStats
    heroData['Stats']['Secondary'] = secondaryStats
    heroData['Stats']['Battle'] = battleStats
    heroData['Stats']['Energy'] = energyStats

    # Update hero data in Firebase
    firebase.updateRecord(dataset, heroID, heroData)
    return(heroData)

# Create a new hero from input, add to json file and upload to Firebase
def createNewHeroesFromInput():
    print(f"\n{Fore.YELLOW}Create a new Hero{Style.RESET_ALL}\n")
    Name = input("Enter hero name: ")
    Title = input("Enter hero title: ")
    Description = input("Enter hero description: ")

    # Select a Race
    click.echo(f"\n{Fore.YELLOW}Choose a Race{Style.RESET_ALL}\n")
    raceTypes = [
        'Demon',
        'Human',
        'Mystical Entity',
        'AI Machine',
        'Orc',
        'Dwarf',
        'Elf'
    ]
    raceType = consoleFunctions.selectListValue(raceTypes)

    click.echo(f"\n{Fore.YELLOW}{raceType}{Style.RESET_ALL}\n")

    races = []
    raceData = firebase.getSubRecords('GameData', 'HeroStatData', 'RaceData', 'Race_Name')

    for raceStat in raceData:
        if raceStat.to_dict()['Race_Type'] == raceType:
            races.append(raceStat.to_dict()['Race_Name'])
    Race = consoleFunctions.selectListValue(races)

    # Select a Class
    print(f"\n{Fore.YELLOW}Choose a Class{Style.RESET_ALL}\n")
    classes = []
    classData = firebase.getSubRecords('GameData', 'HeroStatData', 'ClassData', 'Class_Skill')
    for classStat in classData:
        classes.append(classStat.id)
    Class = consoleFunctions.selectListValue(classes)

    xClass = firebase.getSubRecord('GameData', 'HeroStatData', 'ClassData', Class)
    Class_Name = xClass.to_dict()['Class_Name']
    Class_Skill = xClass.to_dict()['Class_Skill']

    # Select a Role
    print(f"\n{Fore.YELLOW}Choose a Role{Style.RESET_ALL}\n")
    roles = []
    roleData = firebase.getSubRecords('GameData', 'HeroStatData', 'RoleData', 'Role_Name')
    for roleStat in roleData:
        roles.append(roleStat.id)
    Role = consoleFunctions.selectListValue(roles)

    print(f"\n{Fore.YELLOW}Add New Hero{Style.RESET_ALL}\n")
    print(f"Name: {Fore.BLUE}{Name}{Style.RESET_ALL}  Title: {Fore.BLUE}{Title}{Style.RESET_ALL}")
    print(f"Race: {Fore.BLUE}{Race}{Style.RESET_ALL}  Role: {Fore.BLUE}{Role}{Style.RESET_ALL}")
    print(f"Class: {Fore.BLUE}{Class_Name}{Style.RESET_ALL}  Skill: {Fore.BLUE}{Class_Skill}{Style.RESET_ALL}")
    print(f"Description: {Fore.BLUE}{Description}{Style.RESET_ALL}\n")
    confirm = consoleFunctions.selectListValue(['Confirm', 'Decline'])
    
    if confirm == 'Decline':
        createNewHeroesFromInput()

    heroID = createNewHero(Name, Race, Class, Role, Class_Name, Class_Skill, Title, Description)
    print(f"\n{Fore.YELLOW}Success:{Style.RESET_ALL} A new hero has been created. \n \nID: {Fore.GREEN}{heroID}{Style.RESET_ALL}")
    print(f"\nName: {Fore.BLUE}{Name}{Style.RESET_ALL} Race: {Fore.BLUE}{Race}{Style.RESET_ALL} Class: {Fore.BLUE}{Class}{Style.RESET_ALL} Role: {Fore.BLUE}{Role}{Style.RESET_ALL}")
    print(f"\n{Fore.YELLOW}Setting Hero Stats{Style.RESET_ALL}\n")
    
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
        jsonFunctions.updateJsonFile('files/json/HERO_heroes.json', newHero)

# Create New Heroes from JSON file
def createNewHeroesFromFile(fileType):
    if fileType == 'CSV':
        heroes = jsonFunctions.createJsonFromCsv('files/csv/HERO_heroes.csv', 'files/json/HERO_heroes.json')
    if fileType == 'JSON':
        with open('files/json/HERO_heroes.json', 'r') as file:
            # Load the existing JSON content
            heroes = json.load(file)
            print(f"{Fore.YELLOW}Success: {Fore.GREEN}files/json/HERO_heroes.json{Style.RESET_ALL} has been loaded.")
    
    heroCount = len(heroes)
    print(f"\n{heroCount} heroes in file.\n")

    for hero in heroes:
        Name = hero['Name']
        Race = hero['Race']
        Class = hero['Class']
        Role = hero['Role']
        Title = hero['Title']
        Description = hero['Description']

        splitClass = Class.split()
        Class_Name = splitClass[1]
        Class_Skill = splitClass[0]
        if len(splitClass) > 2:
            Class_Name = splitClass[1] + ' ' + splitClass[0-1]

        print(f"{Fore.YELLOW}Success:{Style.RESET_ALL} New hero created {Fore.GREEN}{Name, Race, Class, Role}{Style.RESET_ALL}") 
        heroID = createNewHero(Name, Race, Class, Role, Class_Name, Class_Skill, Title, Description)

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



    