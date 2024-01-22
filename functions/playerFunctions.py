import firebase.firebase as firebase

playerData = {
    'UID': 'UID', # use to connect player accounts to a registered user.
    'Name': 'Name',
    'Experience': {
        'Level': 1,
        "Rank": 1,
        'Level XP': 0,
        'Total XP': 0
    }
}

dataset = 'playerAccounts'



# XP TO LEVEL
def addPlayerXP(add_xp, playerData):

    print('add_xp:', add_xp)

    xpToNextLevel = (playerData['Experience']['Level'] * (playerData['Experience']['Level'] + 10)) + (playerData['Experience']['Level'] + 10)
    xpRequired = xpToNextLevel - playerData['Experience']['Level_xp']

    print('level:', playerData['Experience']['Level'], 'total_xp:', playerData['Experience']['Total XP'], 'current_xp:', playerData['Experience']['Level_xp'])
    print('xpToNextLevel:', xpToNextLevel)
    print('xpRequired:', xpRequired)

    playerData['Experience']['Level_xp'] = playerData['Experience']['Level_xp'] + add_xp
    playerData['Experience']['Total XP'] = playerData['Experience']['Total XP'] + add_xp

    while playerData['Experience']['Level_xp'] >= xpToNextLevel:
        print('LEVEL UP!')
        playerData['Experience']['Level'] = playerData['Experience']['Level'] + 1
        playerData['Experience']['Level_xp'] = playerData['Experience']['Level_xp'] - xpToNextLevel
        xpToNextLevel = (playerData['Experience']['Level'] * (playerData['Experience']['Level'] + 10)) + (playerData['Experience']['Level'] + 10)
        xpRequired = xpToNextLevel - playerData['Experience']['Level_xp']

          
        print('level:', playerData['Experience']['Level'], 'total_xp:', playerData['Experience']['Total XP'], 'current_xp:', playerData['Experience']['Level_xp'])

    print('')     
    print('xpToNextLevel:', xpToNextLevel)
    print('xpRequired:', xpRequired)
    print(playerData)

def getPlayers():
    allPayers = firebase.getRecords(dataset)
    players = []
    playerIDs = []

    for player in allPayers:
        playerName = player.to_dict()['Name']
        playerID = player.id
        players.append(playerName)
        playerIDs.append({'Name':playerName, 'ID':playerID})
    
    # print('playerIDs', playerIDs)

    return(playerIDs)

def createPlayer():

    playerName = input("Enter Username: ")
    # check for duplicates
    playerIDs = getPlayers()
    
    for playerID in playerIDs:
        if playerName == playerID['Name']:
            print('Name already used. Please use another name.')
            playerName = input("Enter Username: ")

    playerData['Name'] = playerName
    playerID = firebase.addRecord(dataset, playerData)
    
    # ADD HERO TO NEW PLAYER
    TEMPdata = {'hero': 'NONE'}
    firebase.addSubRecord(dataset, playerID, 'heroes', TEMPdata,)

    print(f'New Player Created. ID: {playerID}\n{playerData}')
    return (playerID, playerData)