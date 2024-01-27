import utilities.consoleFunctions as consoleFunctions
import functions.battleFunctions as battleFunctions
import functions.heroFunctions as heroFunctions
import functions.backendFunctions as backendFunctions
from colorama import Fore, Style

def Main_Menu():
    mainMenu = [
        'Start Battle',
        'View Heroes',
        'Create Hero',
        'Player Info',
        'System Options',
        'Exit Game'
    ]
    systemOptions = [
        'Update Race Data',
        'Update Class Data',
        'Update Role Data',
        'Update Character Data',
        'Go Back'
    ]

    print(f"\n{Fore.YELLOW}WELCOME TO HERO BATTLES{Style.RESET_ALL}\n")
    selectFunction = consoleFunctions.selectListValue(mainMenu)

    while selectFunction != '':

        if selectFunction == 'Start Battle':
            battleFunctions.startBattle()

        if selectFunction == 'View Heroes':
            print(f'\n{Fore.YELLOW}View Heroes{Style.RESET_ALL}\n')

        if selectFunction == 'Create Hero':
            heroFunctions.createNewHeroesFromInput()

        if selectFunction == 'Player Info':
            print(f'\n{Fore.YELLOW}Player Info{Style.RESET_ALL}\n')

        if selectFunction == 'System Options':
            print(f'\n{Fore.YELLOW}System Options{Style.RESET_ALL}\n')
            selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Update Race Data':
                print(f'\n{Fore.YELLOW}Update Race Data{Style.RESET_ALL}\n')
                backendFunctions.uploadHeroRaceFromCsvToFirebase()
                selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Update Class Data':
                print(f'\n{Fore.YELLOW}Update Class Data{Style.RESET_ALL}\n')
                backendFunctions.uploadHeroClassFromCsvToFirebase()
                selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Update Role Data':
                print(f'\n{Fore.YELLOW}Update Role Data{Style.RESET_ALL}\n')
                backendFunctions.uploadHeroRoleFromCsvToFirebase()
                selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Update Character Data':
                print(f'\n{Fore.YELLOW}Update Character Data{Style.RESET_ALL}\n')
                # backendFunctions.uploadHeroesFromCsvToFirebase()
                selectFunction = consoleFunctions.selectListValue(systemOptions)

            if selectFunction == 'Go Back':
                print(f'\n{Fore.YELLOW}Main Menu{Style.RESET_ALL}\n')
                selectFunction = consoleFunctions.selectListValue(mainMenu)

        if selectFunction == 'Exit Game':
            print(f'\n{Fore.YELLOW}Exit Game{Style.RESET_ALL}\n')
            exit()




